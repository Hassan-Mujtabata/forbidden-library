# -*- coding: utf-8 -*-
"""Validate the idea-graph, merge it with the library, gzip + AES-256-GCM encrypt -> ../content.enc."""
import os, json, gzip, base64, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "books.json")
GRAPH = os.path.join(HERE, "graph.json")
DST = os.path.join(HERE, "..", "content.enc")
KEYFILE = os.path.join(HERE, "key.txt")


def die(msg):
    print("FAIL:", msg)
    sys.exit(1)


# Mirrors FIGC in index.html. If you add a component there, add it here — otherwise a spec using
# it validates fine and then draws nothing, which is the failure mode this list exists to prevent.
FIG_COMPONENTS = {
    # bodies + sensation
    "hand", "feet", "body", "sit", "pressure", "flow", "wash", "dot", "halo", "pacer",
    # structure over time
    "loop", "stages", "label", "curve", "ripple", "fork",
    # relationships and forces (#158) — what psychology actually needs
    "scale", "lanes", "gauge", "tether", "crowd", "spot", "gap", "grip", "stack", "magnet",
    # concept-shaped, added because specific lessons needed them (#161)
    "drift", "two", "ladder",
}


def validate(books, graph):
    tracks = {t["id"] for t in graph["tracks"]}
    nodes = graph["nodes"]
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        die("duplicate node ids")
    idset = set(ids)
    booktitles = {b["title"] for b in books["books"]}

    problems, warns = [], []
    for n in nodes:
        if n["track"] not in tracks:
            problems.append(f"{n['id']}: unknown track {n['track']}")
        for p in n.get("prereq", []):
            if p not in idset:
                problems.append(f"{n['id']}: prereq '{p}' does not exist")
        # #155: felt figures. The spec is DATA and the components are CODE, so a spec naming a
        # component the runtime does not have would render an empty box with a caption promising
        # something that is not there. Caught here, where it is loud, not at view time where it
        # is silent. FIG_COMPONENTS mirrors FIGC in index.html — extend both together.
        for fi, f in enumerate(n.get("fig", []) or []):
            where = f"{n['id']}: fig[{fi}]"
            if not isinstance(f, dict):
                problems.append(f"{where}: not an object"); continue
            if not f.get("alt"):
                problems.append(f"{where}: no alt text (it is the screen-reader description)")
            stages = f.get("stages") or ([{"cap": f.get("cap", ""), "scene": f.get("scene", [])}]
                                         if f.get("scene") else [])
            if not stages:
                problems.append(f"{where}: no stages and no scene")
            if len(stages) > 5:
                problems.append(f"{where}: {len(stages)} stages — more than five is a slideshow")
            place = f.get("place")
            if place is not None and not (0 <= place < max(1, len(n.get("bridge") or []))):
                problems.append(f"{where}: place {place} is outside the lesson's paragraphs")
            for si, st in enumerate(stages):
                cap = (st.get("cap") or f.get("cap") or "")
                if len(cap) > 220:
                    problems.append(f"{where} stage {si}: caption is {len(cap)} chars, cap is 220")
                if "<" in cap or "&#" in cap:
                    problems.append(f"{where} stage {si}: caption contains markup")
                if not (st.get("scene") or []):
                    problems.append(f"{where} stage {si}: empty scene")
                for it in (st.get("scene") or []):
                    c = (it or {}).get("c")
                    if c not in FIG_COMPONENTS:
                        problems.append(f"{where} stage {si}: unknown component '{c}'")
        # #149: `rel` is undirected kinship added by integrate.py. It gates nothing, so it is not
        # part of cycle detection — but a dangling one would render as a dead cross-link, and a
        # self-link would have a lesson pointing at itself in "Connect my ideas".
        for r in n.get("rel", []):
            if r not in idset:
                problems.append(f"{n['id']}: rel '{r}' does not exist")
            elif r == n["id"]:
                problems.append(f"{n['id']}: rel points at itself")
        if not n.get("stub"):
            for key in ("bridge", "sources", "quiz", "apply"):
                if not n.get(key):
                    problems.append(f"{n['id']}: authored node missing '{key}'")
            for q in n.get("quiz", []):
                if not (0 <= q["a"] < len(q["c"])):
                    problems.append(f"{n['id']}: quiz answer index out of range")
            for s in n.get("sources", []):
                if s["book"] not in booktitles:
                    warns.append(f"{n['id']}: source '{s['book']}' not a library book (quarried/external — no cross-link)")

    # cycle detection (DFS)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    pre = {n["id"]: n.get("prereq", []) for n in nodes}

    def dfs(u, stack):
        color[u] = GRAY
        for v in pre[u]:
            if color[v] == GRAY:
                die(f"cycle detected: {' -> '.join(stack + [u, v])}")
            if color[v] == WHITE:
                dfs(v, stack + [u])
        color[u] = BLACK

    for i in ids:
        if color[i] == WHITE:
            dfs(i, [])

    # reachability: every node's prereq chain bottoms out at a root (prereq == [])
    roots = [n["id"] for n in nodes if not n.get("prereq")]
    if not roots:
        die("no root nodes (every node has a prereq -> nothing is ever available)")

    if problems:
        for p in problems:
            print("  PROBLEM:", p)
        die(f"{len(problems)} structural problem(s)")

    return warns, roots


def load_graph():
    """#49: prefer local plaintext graph.json; if it's absent (it is no longer committed to the repo),
    derive the graph from the encrypted content.enc so a fresh clone with the key can still rebuild."""
    if os.path.exists(GRAPH):
        return json.load(open(GRAPH, encoding="utf-8"))
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    raw = open(DST, "rb").read()
    pt = AESGCM(key).decrypt(raw[:12], raw[12:], None)
    payload = json.loads(gzip.decompress(pt))
    return {"tracks": payload["tracks"], "nodes": payload["nodes"]}


def main():
    check_only = "--check" in sys.argv                     # #56: validate the graph without needing the key / writing output
    books = json.load(open(BOOKS, encoding="utf-8"))
    graph = load_graph()
    warns, roots = validate(books, graph)

    authored = [n for n in graph["nodes"] if not n.get("stub")]
    stubs = [n for n in graph["nodes"] if n.get("stub")]
    print(f"tracks={len(graph['tracks'])}  nodes={len(graph['nodes'])} "
          f"(authored={len(authored)}, stub={len(stubs)})  roots={roots}")
    print("integrity: acyclic OK, all prereqs resolve OK, roots present OK")
    for w in warns:
        print("  note:", w)

    if check_only:
        print("check-only: graph is valid; not writing content.enc")
        return

    payload = {"v": 2, "books": books["books"], "tracks": graph["tracks"], "nodes": graph["nodes"]}
    # #131: stamp a fingerprint of the BOOK TEXT into the payload so anything derived from it
    # (mined hooks, forged sources) can tell it is stale without a human remembering to bump a
    # constant. The constant version of this lasted exactly one release before I forgot it: 3.57
    # rewrote 159 words and left CONTENT_GEN at 2. Hash only the prose, so a graph or blurb edit
    # does not needlessly bin 20KB of perfectly good hooks.
    import hashlib
    h = hashlib.sha256()
    for b in payload["books"]:
        h.update(b["id"].encode("utf-8"))
        for e in b["episodes"]:
            h.update((e.get("t") or "").encode("utf-8"))
            for p in e["p"]:
                h.update(p.encode("utf-8"))
    payload["gen"] = h.hexdigest()[:12]
    print("  text fingerprint: %s" % payload["gen"])
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    data = gzip.compress(raw, 9)

    if not os.path.exists(KEYFILE):
        die("key.txt missing — run the original encrypt.py once or restore the key")
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, data, None)
    open(DST, "wb").write(iv + ct)

    print(f"payload {len(raw)/1e6:.2f} MB -> gzip {len(data)/1e6:.2f} MB -> content.enc {os.path.getsize(DST)/1e6:.2f} MB")


if __name__ == "__main__":
    main()
