# -*- coding: utf-8 -*-
"""Weave a track into the graph instead of parking it beside one.

    python tools/integrate.py --orphans            # which tracks are islands. Reports, changes nothing.
    python tools/integrate.py --track E            # judge one track, write integrate_report.txt
    python tools/integrate.py --track E --apply    # judge AND apply the auto-safe subset
    python tools/integrate.py --selftest           # pinned parser/rule tests, no network

WHY THIS EXISTS. gemini_pipeline.merge_nodes assigns `"prereq": [prev] if prev else []` — every
generated track is a CHAIN and nothing ever points out of it. Measured on the real graph: the
hand-built tracks carry 19 cross-track prereq edges between them; every pipeline track carries 0.
The cross-references the pipeline does produce live in the bridge PROSE ("the feeling-tone you met
earlier") — words, not structure. So an added book reads like it was bolted on, because it was.

WHAT IS AND IS NOT SAFE HERE. Prereq edges gate content: a wrong one locks a reader out of a
lesson they could have read. So:
  * edges point NEW -> OLD only, which makes a cycle structurally impossible (build.py still checks)
  * a prereq edge is auto-applied ONLY when the target is already DONE for this reader — it adds
    meaning to the Path and cannot lock anything. Everything else is demoted to a kinship link
    and listed in the report for a human to promote deliberately.
  * existing nodes are never modified. The in-track chain is never removed.
  * "related topics" is not a dependency. The judge prompt defines DEPENDENCY as "a reader who has
    not internalised A will MISUNDERSTAND B", and the parser refuses any reply that is not exactly
    one of the three verdicts. Refusing is the feature; see cleantext.py for the same discipline.

`rel` is a new OPTIONAL node field: undirected kinship, used by the client to pick genuinely
related ideas for "Connect my ideas" instead of picking at random. It gates nothing.
"""
import json, os, re, sys, math, argparse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
REPORT = os.path.join(HERE, "integrate_report.txt")

MAX_PAIRS_PER_TRACK = 18      # ceiling on judged pairs, so one track cannot eat a day of quota
MAX_PREREQ_PER_TRACK = 3      # a woven track, not a re-parented one
MAX_PREREQ_PER_NODE = 1
MAX_REL_PER_NODE = 2
CAND_PER_NODE = 3

WORD = re.compile(r"[A-Za-zÀ-ɏ][A-Za-zÀ-ɏ'’-]*")
STOP = set("""the a an and or but if then than that this these those of in on at to for with from by
as is are was were be been being it its it's they them their there here what which who whom whose
you your yours we our us i me my he she his her not no nor so too very can will just do does did
about into over under again further once all any both each few more most other some such only own
same s t don now one two three when where why how because while during before after above below""".split())


def norm(s):
    return [w.lower() for w in WORD.findall(s or "") if w.lower() not in STOP and len(w) > 2]


def node_text(n):
    """Everything about a node that carries meaning, for scoring and for the judge."""
    parts = [n.get("title", "")]
    b = n.get("bridge")
    if isinstance(b, list):
        parts += [str(x) for x in b]
    elif b:
        parts.append(str(b))
    for s in (n.get("sources") or []):
        if s.get("ref"):
            parts.append(str(s["ref"]))
    return "\n".join(parts)


# ------------------------------------------------------------------ candidate selection
def candidates(graph, track_id):
    """Rank existing nodes against each new node by RARITY-weighted overlap, not raw overlap.

    Counting shared words rewards whichever pair happens to use "practice" and "attention" a lot.
    Weighting by how rare a word is across the whole graph lets the words that actually identify an
    idea decide — the same reasoning as councilSeats() in index.html.
    """
    nodes = graph["nodes"]
    mine = [n for n in nodes if n["track"] == track_id and not n.get("stub")]
    others = [n for n in nodes if n["track"] != track_id and not n.get("stub")]
    if not mine or not others:
        return []

    docs = {n["id"]: set(norm(node_text(n))) for n in nodes if not n.get("stub")}
    df = collections.Counter()
    for s in docs.values():
        df.update(s)
    N = max(1, len(docs))
    idf = {w: math.log((N + 1) / (df[w] + 1)) for w in df}

    pairs = []
    for a in mine:
        sa = docs[a["id"]]
        scored = []
        for b in others:
            shared = sa & docs[b["id"]]
            if len(shared) < 3:
                continue
            sc = sum(idf.get(w, 0) for w in shared)
            scored.append((sc, b, sorted(shared, key=lambda w: -idf.get(w, 0))[:6]))
        scored.sort(key=lambda x: -x[0])
        for sc, b, shared in scored[:CAND_PER_NODE]:
            pairs.append({"new": a, "old": b, "score": round(sc, 2), "shared": shared})
    pairs.sort(key=lambda p: -p["score"])
    return pairs[:MAX_PAIRS_PER_TRACK]


# ------------------------------------------------------------------ the judge
JUDGE_PROMPT = """A new idea has been added to a reader's learning path.

NEW IDEA:
"{btitle}"
{btext}

CANDIDATES the reader already knows:
{cands}

Choose, using the exact id strings shown in brackets and nothing else:
  dependency — AT MOST ONE id, or "" for none
  kinship    — AT MOST TWO ids, or an empty list

Return ONLY this JSON:
{{"dependency": "<id or empty string>", "kinship": ["<id>"], "why": {{"<id>": "<reason, max 18 words>"}}}}

Start from "0 and empty" and move only if the evidence forces you.

NONE is the correct answer for the great majority of pairs, including every pair that is merely
"both about the mind", "both about people", "both about improving yourself", or that shares
vocabulary. Two ideas from different books being broadly compatible is NONE.

KINSHIP requires a SPECIFIC named link: one idea explains a mechanism the other relies on, or they
give opposing answers to the SAME question. If your WHY sentence could be said about dozens of
other pairs in a self-improvement library, the answer was NONE.

DEPENDENCY requires more: a reader who has NOT internalised A will actively MISUNDERSTAND B — A is
load-bearing. Being useful earlier is not a dependency. If you hesitate at all, it is not one.

Ask yourself before answering: would a thoughtful editor be embarrassed to see this link printed
next to these two lessons? If yes, leave it out. Most new ideas connect to NOTHING on this list."""

VERDICTS = ("DEPENDENCY", "KINSHIP", "NONE")


def parse_choice(t, valid_ids):
    """Parse the forced-choice reply, keyed by node ID rather than by position.

    Positions were the first design and the model miscounted them — it answered "4" when three
    candidates were offered, which the parser rightly refused and which cost a real answer. An id
    either is in the candidate set or it is not, so a hallucinated one is simply dropped and the
    rest of the reply still stands.
    """
    if not t:
        return None
    s = t.strip()
    i, j = s.find("{"), s.rfind("}")
    if i < 0 or j <= i:
        return None
    try:
        d = json.loads(s[i:j + 1])
    except Exception:
        return None
    valid = set(valid_ids)
    dep = d.get("dependency") or ""
    dep = dep.strip() if isinstance(dep, str) else ""
    if dep and dep not in valid:
        dep = ""                                   # invented an id: drop it, keep the rest
    kin = d.get("kinship")
    if kin is None:
        kin = []
    if not isinstance(kin, list):
        return None
    out = []
    for k in kin:
        if isinstance(k, str) and k.strip() in valid and k.strip() != dep and k.strip() not in out:
            out.append(k.strip())
    why = d.get("why") or {}
    if not isinstance(why, dict):
        why = {}
    return {"dependency": dep, "kinship": out[:2],
            "why": {str(a): re.sub(r"\s+", " ", str(b)).strip()[:160] for a, b in why.items()}}


def parse_verdict(t):
    """Refuse anything that is not exactly one of the three verdicts plus a reason.

    Accepts BOTH shapes on purpose: gemini_pipeline.call sets responseMimeType=application/json
    unconditionally, so asking for `VERDICT: X` lines gets back {"VERDICT":"X","WHY":"…"} instead.
    The first live run refused every single reply for exactly that reason.
    """
    if not t:
        return None
    v = why = None
    s = t.strip()
    if s.startswith("{"):
        try:
            j = json.loads(s)
            v = str(j.get("VERDICT") or j.get("verdict") or "").strip()
            why = str(j.get("WHY") or j.get("why") or "").strip()
        except Exception:
            return None
    if not v:
        m = re.search(r"^\s*VERDICT\s*:\s*([A-Za-z]+)", t, re.M)
        w = re.search(r"^\s*WHY\s*:\s*(.+)$", t, re.M)
        if not m or not w:
            return None
        v, why = m.group(1), w.group(1)
    v = v.strip().upper()
    if v not in VERDICTS:
        return None
    why = re.sub(r"\s+", " ", why or "").strip().strip('"')
    if len(why) < 4:
        return None
    return {"verdict": v, "why": why[:160]}


def judge_node(new_node, cand_nodes, call):
    """One forced choice per NEW node over all its candidates at once.

    The first design asked "is A related to B?" once per pair and the model answered KINSHIP to
    every single pair, including deliberately unrelated ones — an isolated yes/no invites yes.
    Choosing at most one from a numbered list, with 0 explicitly allowed, is what produces
    discrimination. It is also a third of the calls.
    """
    cands = "\n".join("%d. [%s] %s\n   %s" % (i + 1, c["id"], c.get("title", ""),
                                              node_text(c)[:420].replace("\n", " "))
                      for i, c in enumerate(cand_nodes))
    p = JUDGE_PROMPT.format(btitle=new_node.get("title", ""),
                            btext=node_text(new_node)[:1500], cands=cands)
    try:
        raw = call(p, temp=0.15, schema=None)
    except Exception as e:
        return None, str(e)[:120]
    got = parse_choice(raw, [c["id"] for c in cand_nodes])
    if not got:
        return None, "unparseable: " + re.sub(r"\s+", " ", (raw or ""))[:90]
    out = []
    for cid, verdict in ([(got["dependency"], "DEPENDENCY")] if got["dependency"] else []) + \
                        [(k, "KINSHIP") for k in got["kinship"]]:
        out.append({"old_id": cid, "verdict": verdict,
                    "why": got["why"].get(cid, "").strip() or "(no reason given)"})
    return out, None


# ------------------------------------------------------------------ applying
def apply_decisions(graph, track_id, decided, done_ids):
    """Turn judged pairs into edges under the caps. Returns (graph, log)."""
    import copy
    g = copy.deepcopy(graph)
    byid = {n["id"]: n for n in g["nodes"]}
    log, used_prereq, per_node = [], 0, collections.Counter()

    # Strongest first, so the cap spends itself on the best-evidenced dependencies.
    for d in sorted(decided, key=lambda x: -x["score"]):
        nid, oid, v = d["new_id"], d["old_id"], d["verdict"]
        n = byid.get(nid)
        if not n or v in ("NONE", "ERROR", "REFUSED"):
            log.append((nid, oid, v, "not an edge", d["why"]))
            continue
        as_rel = True
        if v == "DEPENDENCY":
            if oid not in done_ids:
                log.append((nid, oid, v, "demoted to rel — target not yet read, would lock content", d["why"]))
            elif used_prereq >= MAX_PREREQ_PER_TRACK:
                log.append((nid, oid, v, "demoted to rel — track prereq cap reached", d["why"]))
            elif per_node[nid] >= MAX_PREREQ_PER_NODE:
                log.append((nid, oid, v, "demoted to rel — node prereq cap reached", d["why"]))
            else:
                pre = n.setdefault("prereq", [])
                if oid not in pre:
                    pre.append(oid)
                    used_prereq += 1
                    per_node[nid] += 1
                    n["whyreq"] = d["why"]          # the lock now names the real prior idea
                    log.append((nid, oid, v, "APPLIED as prereq", d["why"]))
                    as_rel = False
        if as_rel:
            rel = n.setdefault("rel", [])
            if oid not in rel and len(rel) < MAX_REL_PER_NODE:
                rel.append(oid)
                log.append((nid, oid, v, "APPLIED as rel", d["why"]))

    # TIER IS AUTHORED, NOT DERIVED. The first version of this recomputed depth for the whole
    # graph from prereqs, on the assumption that tier just means "one below your deepest
    # prerequisite". It is not: the hand-built tracks use tier as intended DISPLAY depth, and
    # deriving it rewrote 62 nodes across every other track — pushing each track's opening lesson
    # off tier 0 and reshaping a Path that was fine. Reverted, and now the rule is minimal:
    # only a node that GAINED a prereq in this run can move, only downwards, and only far enough
    # to sit below the thing it now depends on. Nothing outside the track is ever touched.
    for nid in per_node:
        n = byid.get(nid)
        if not n:
            continue
        pres = [byid[p].get("tier", 0) for p in n.get("prereq", []) if p in byid]
        if pres:
            deepest = max(pres) + 1
            if deepest > n.get("tier", 0):
                log.append((nid, "", "TIER", "moved %s -> %s to sit below its new prereq"
                            % (n.get("tier"), deepest), ""))
                n["tier"] = deepest
    return g, log


# ------------------------------------------------------------------ reporting
def write_report(track_id, decided, log, voice=None):
    L = []
    L.append("TRACK %s — %d pair(s) judged\n" % (track_id, len(decided)))
    counts = collections.Counter(d["verdict"] for d in decided)
    L.append("verdicts: " + ", ".join("%s=%d" % kv for kv in counts.most_common()) + "\n")
    if voice:
        L.append("\nVOICE PASS\n")
        for k, v in voice.items():
            L.append("   %-7s %s\n" % (k, v))
    L.append("\nDECISIONS (new -> old)\n")
    for nid, oid, v, what, why in log:
        L.append("   %-6s -> %-6s  %-10s %-52s %s\n" % (nid, oid, v, what, why))
    L.append("\nNothing above marked APPLIED has changed graph.json unless --apply was passed.\n")
    open(REPORT, "w", encoding="utf-8").write("".join(L))
    return REPORT


# ------------------------------------------------------------------ orphan survey
def orphans(graph):
    byid = {n["id"]: n for n in graph["nodes"]}
    cross = collections.Counter(); count = collections.Counter()
    for n in graph["nodes"]:
        count[n["track"]] += 1
        for p in n.get("prereq", []):
            if p in byid and byid[p]["track"] != n["track"]:
                cross[n["track"]] += 1
    rows = []
    for t in graph["tracks"]:
        rows.append((t["id"], t.get("name", ""), count[t["id"]], cross[t["id"]]))
    return rows


# ------------------------------------------------------------------ selftest (no network)
def selftest():
    fails = []

    def ck(name, cond):
        if cond is not True:
            fails.append("%s -- %s" % (name, cond))

    good = "VERDICT: DEPENDENCY\nWHY: Without stable attention the later technique cannot be attempted."
    p = parse_verdict(good)
    ck("parses a well-formed verdict", (p and p["verdict"] == "DEPENDENCY") or "got %r" % p)
    ck("parses the JSON shape call() actually returns",
       (parse_verdict('{"VERDICT":"KINSHIP","WHY":"A explains B."}') or {}).get("verdict") == "KINSHIP"
       or "refused the JSON shape")
    for label, bad in {
        "prose": "I think these are quite related to each other!",
        "bad verdict word": "VERDICT: MAYBE\nWHY: because",
        "no why": "VERDICT: KINSHIP",
        "empty why": "VERDICT: NONE\nWHY:   ",
        "bad json verdict": '{"VERDICT":"MAYBE","WHY":"x"}',
    }.items():
        ck("refuses " + label, (parse_verdict(bad) is None) or "accepted it")

    # The forced-choice parser is what stands between a hallucinated candidate number and an edge.
    IDS = ["a4", "b1", "j2"]
    c = parse_choice('{"dependency":"a4","kinship":["b1","j2"],"why":{"a4":"load bearing"}}', IDS)
    ck("forced choice parses", (c and c["dependency"] == "a4" and c["kinship"] == ["b1", "j2"]) or "got %r" % c)
    ck("nothing chosen is legal",
       (parse_choice('{"dependency":"","kinship":[]}', IDS) or {"dependency": "x"})["dependency"] == ""
       or "rejected an empty answer")
    ck("an invented dependency id is dropped, the rest survives",
       (lambda r: r and r["dependency"] == "" and r["kinship"] == ["b1"])
       (parse_choice('{"dependency":"zz9","kinship":["b1"]}', IDS)) or "kept an id that was never offered")
    ck("an invented kinship id is dropped",
       (parse_choice('{"dependency":"","kinship":["b1","zz9"]}', IDS) or {}).get("kinship") == ["b1"]
       or "kept a bad id")
    ck("refuses prose", parse_choice("Sure! I think the second one.", IDS) is None or "accepted prose")
    ck("a candidate cannot be both",
       (parse_choice('{"dependency":"a4","kinship":["a4","b1"]}', IDS) or {}).get("kinship") == ["b1"]
       or "let one candidate be dependency and kinship at once")

    # A DEPENDENCY on a target the reader has NOT done must never become a prereq.
    g = {"tracks": [{"id": "A"}, {"id": "Z"}],
         "nodes": [{"id": "a1", "track": "A", "tier": 0, "prereq": [], "title": "A one"},
                   {"id": "z1", "track": "Z", "tier": 0, "prereq": [], "title": "Z one"}]}
    d = [{"new_id": "z1", "old_id": "a1", "verdict": "DEPENDENCY", "why": "w", "score": 9}]
    g2, log = apply_decisions(g, "Z", d, done_ids=set())
    z = [n for n in g2["nodes"] if n["id"] == "z1"][0]
    ck("undone target is demoted, not gated", ("a1" not in z.get("prereq", []) and "a1" in z.get("rel", []))
       or "prereq=%s rel=%s" % (z.get("prereq"), z.get("rel")))

    g3, _ = apply_decisions(g, "Z", d, done_ids={"a1"})
    z3 = [n for n in g3["nodes"] if n["id"] == "z1"][0]
    ck("done target becomes a real prereq", ("a1" in z3.get("prereq", [])) or "prereq=%s" % z3.get("prereq"))
    ck("tier follows the new depth", (z3["tier"] == 1) or "tier=%s" % z3["tier"])
    ck("whyreq names the reason", (z3.get("whyreq") == "w") or "whyreq=%r" % z3.get("whyreq"))

    # The regression that cost a revert: recomputing depth globally rewrote 62 untouched nodes.
    wide = {"tracks": [{"id": "A"}, {"id": "Z"}], "nodes": [
        {"id": "a1", "track": "A", "tier": 0, "prereq": [], "title": "root"},
        {"id": "a2", "track": "A", "tier": 5, "prereq": ["a1"], "title": "authored deep"},
        {"id": "q1", "track": "Q", "tier": 0, "prereq": [], "title": "another track"},
        {"id": "z1", "track": "Z", "tier": 0, "prereq": [], "title": "the new one"}]}
    g5, _ = apply_decisions(wide, "Z", [{"new_id": "z1", "old_id": "a1", "verdict": "DEPENDENCY",
                                         "why": "w", "score": 1}], done_ids={"a1"})
    untouched = [n for n in g5["nodes"] if n["id"] in ("a1", "a2", "q1")]
    before = {"a1": 0, "a2": 5, "q1": 0}
    moved = [n["id"] for n in untouched if n["tier"] != before[n["id"]]]
    ck("nodes outside the run keep their authored tier", (not moved) or "moved: " + ",".join(moved))

    # The track cap must hold even when every verdict is a dependency.
    many = [{"new_id": "z1", "old_id": "a1", "verdict": "DEPENDENCY", "why": "w", "score": i} for i in range(6)]
    g4, _ = apply_decisions(g, "Z", many, done_ids={"a1"})
    z4 = [n for n in g4["nodes"] if n["id"] == "z1"][0]
    ck("per-node prereq cap holds", (len(z4.get("prereq", [])) <= MAX_PREREQ_PER_NODE)
       or "%d prereqs" % len(z4.get("prereq", [])))

    print("integrate selftest: " + ("ok" if not fails else "FAIL\n  " + "\n  ".join(fails)))
    return not fails


# ------------------------------------------------------------------ main
def main():
    # Track names carry macrons ("Concentration & Jhāna") and this console is cp1252, which turns
    # a survey into a crash. The report file is always written as UTF-8 regardless.
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--track"); ap.add_argument("--orphans", action="store_true")
    ap.add_argument("--apply", action="store_true"); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--done", default="", help="comma-separated node ids treated as already read")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() else 1)

    graph = json.load(open(GRAPH, encoding="utf-8"))

    if a.orphans or not a.track:
        print("%-6s %-28s %6s %6s" % ("track", "name", "nodes", "cross"))
        for tid, name, n, c in orphans(graph):
            print("%-6s %-28s %6d %6d %s" % (tid, name[:28], n, c, "  <-- ISLAND" if c == 0 else ""))
        if not a.track:
            print("\nPick one with --track <ID>. Add --apply to write the auto-safe subset.")
            return

    pairs = candidates(graph, a.track)
    if not pairs:
        print("no candidate pairs for track %s (nothing shares enough rare vocabulary)" % a.track)
        return
    print("judging %d candidate pair(s) for track %s…" % (len(pairs), a.track))

    sys.path.insert(0, HERE)
    import gemini_pipeline as gp
    if not gp.KEYS:
        print("no Gemini keys — cannot judge. Report not written."); return

    # Group the candidates per new node — one forced choice each, not one yes/no per pair.
    by_new = collections.OrderedDict()
    for p in pairs:
        by_new.setdefault(p["new"]["id"], {"node": p["new"], "cands": [], "scores": {}})
        by_new[p["new"]["id"]]["cands"].append(p["old"])
        by_new[p["new"]["id"]]["scores"][p["old"]["id"]] = p["score"]

    decided = []
    for nid, grp in by_new.items():
        picks, err = judge_node(grp["node"], grp["cands"], gp.call)
        if err:
            print("  %-6s  SKIPPED — %s" % (nid, err))
            continue
        if not picks:
            print("  %-6s  no genuine link to anything it already knows" % nid)
            continue
        for pk in picks:
            decided.append({"new_id": nid, "old_id": pk["old_id"],
                            "score": grp["scores"].get(pk["old_id"], 0),
                            "verdict": pk["verdict"], "why": pk["why"]})
            print("  %-6s -> %-6s  %-10s %s" % (nid, pk["old_id"], pk["verdict"], pk["why"][:58]))

    done = set(x for x in a.done.split(",") if x)
    g2, log = apply_decisions(graph, a.track, decided, done)
    path = write_report(a.track, decided, log)
    print("\nreport: %s" % path)

    if not a.apply:
        print("Nothing written. Re-run with --apply once the report reads right.")
        return
    json.dump(g2, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("graph.json updated. NEXT: python tools/build.py  (it revalidates and re-encrypts)")


if __name__ == "__main__":
    main()
