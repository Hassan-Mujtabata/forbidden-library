# -*- coding: utf-8 -*-
"""
The Vault — self-regulating Gemini content pipeline.

Turns an extracted book into dependency-locked Path lessons in the EXACT schema of the
hand-authored nodes, with hard safeguards so generated output can never corrupt the graph:

  * Gemini writes ONLY content (title, bridge, sources, quiz, apply, whyreq).
    All STRUCTURE (id, track, tier, prereq) is assigned deterministically here, so
    output cannot create a cycle, dangling prereq, or malformed wiring.
  * Every node is schema-validated + sanitized; invalid output is retried, then skipped.
  * Near-duplicate titles are dropped (dedupe).
  * The merge is trial-validated on a COPY with the same rules build.py enforces;
    graph.json is only written if the whole graph still passes. A .bak is kept.
  * Quota-aware: rotates through all keys on 429; a per-day budget stops work and the
    daily GitHub Action resumes tomorrow. Progress is checkpointed so nothing repeats.

Keys come from env (GEMINI_API_KEY, GEMINI_API_KEY_2..5) in CI, or tools/.gemini_keys locally.
"""
import json, os, re, sys, time, urllib.request, urllib.error, unicodedata, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
STATUS = os.path.join(HERE, "..", "status.json")     # non-secret progress, safe to commit
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DAILY_BUDGET = int(os.environ.get("GEMINI_DAILY_NODES", "40"))   # nodes/day across all keys

def load_keys():
    env = [os.environ.get("GEMINI_API_KEY")] + [os.environ.get(f"GEMINI_API_KEY_{i}") for i in range(2, 8)]
    env = [k for k in env if k]
    if env:
        return env
    p = os.path.join(HERE, ".gemini_keys")
    return [k.strip() for k in open(p)] if os.path.exists(p) else []

KEYS = load_keys()

# ---------------------------------------------------------------- prompt
PROMPT = """You are a curriculum author for "The Vault", a serious offline self-study app. \
You are given a passage from "{title}" by {author}. Distill ONE distinct, self-contained idea \
into a lesson. Avoid ideas already covered: {avoid}.

Return ONLY one JSON object (no markdown fences, no text outside JSON) with EXACTLY:
{{
 "title": "<concept as a 2-6 word noun phrase, Title Case>",
 "glyph": "<one relevant emoji>",
 "bridge": ["<p1>","<p2>","<p3>"],
 "sources": [{{"book":"{title}","ref":"<2-5 word topical locator, NOT the author name>","quote":["<faithful excerpt/close paraphrase from the passage, 12-40 words>"]}}],
 "quiz": [{{"q":"<question>","c":["<o0>","<o1>","<o2>","<o3>"],"a":<int 0-3>,"why":"<one sentence>"}}],
 "apply": {{"prompt":"<a concrete first-person practice/reflection task grounded in the reader's real life>","min":50}},
 "whyreq": "<one sentence: why this idea builds on more basic understanding>"
}}

HARD RULES:
- bridge: EXACTLY 3 paragraphs, 45-110 words each, second person, calm and precise. NO markdown, NO asterisks/underscores for emphasis, NO headings. Do NOT quote the book verbatim in the bridge.
- quiz: EXACTLY 3 items, each EXACTLY 4 options, integer answer index in range, plausible distractors.
- Ground everything in the passage; invent no facts. Plain text only.

PASSAGE:
{chunk}
"""

# ---------------------------------------------------------------- gemini call w/ key rotation
class Quota(Exception): pass

def call(prompt, temp=0.7):
    last = None
    for ki, key in enumerate(KEYS):
        if key in call.dead:
            continue
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
        body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                           "generationConfig": {"temperature": temp, "responseMimeType": "application/json"}}).encode()
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.load(r)
            return d["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 403):          # quota/rate → retire this key for today
                call.dead.add(key); continue
            if e.code >= 500:
                time.sleep(2); continue
            raise
        except Exception as e:
            last = e; time.sleep(2); continue
    raise Quota(f"all keys exhausted/failed ({last})")
call.dead = set()

# ---------------------------------------------------------------- sanitize + validate content
def clean_text(t):
    t = unicodedata.normalize("NFC", str(t))
    t = re.sub(r"[*_`#]+", "", t)                       # strip markdown emphasis/headers
    t = re.sub(r"\s+", " ", t).strip()
    return t

def sanitize(n):
    n["title"] = clean_text(n["title"])[:60]
    n["glyph"] = (str(n.get("glyph", "•")).strip() or "•")[:4]
    n["bridge"] = [clean_text(p) for p in n["bridge"]][:3]
    for s in n["sources"]:
        s["book"] = clean_text(s["book"]); s["ref"] = clean_text(s["ref"])[:60]
        s["quote"] = [clean_text(q)[:400] for q in s["quote"]][:2]
    for q in n["quiz"]:
        q["q"] = clean_text(q["q"]); q["why"] = clean_text(q["why"])
        q["c"] = [clean_text(c) for c in q["c"]]
    n["apply"]["prompt"] = clean_text(n["apply"]["prompt"])
    n["apply"]["min"] = int(n["apply"].get("min", 50)) or 50
    n["whyreq"] = clean_text(n.get("whyreq", ""))
    return n

def content_errors(n):
    e = []
    try:
        if not (2 <= len(n["title"].split()) <= 8): e.append("title")
        if not (len(n["bridge"]) == 3 and all(25 <= len(p.split()) <= 140 for p in n["bridge"])): e.append("bridge")
        if not (1 <= len(n["sources"]) <= 3): e.append("sources#")
        for s in n["sources"]:
            if not (s["book"] and s["ref"] and s["quote"] and all(5 <= len(q) for q in s["quote"])): e.append("source")
        if len(n["quiz"]) != 3: e.append("quiz#")
        for q in n["quiz"]:
            if not (q["q"] and len(q["c"]) == 4 and len(set(q["c"])) == 4 and isinstance(q["a"], int) and 0 <= q["a"] < 4 and q["why"]): e.append("quiz")
        if not (n["apply"]["prompt"] and isinstance(n["apply"]["min"], int)): e.append("apply")
        if not n["whyreq"]: e.append("whyreq")
    except Exception as ex:
        e.append(f"exc:{ex}")
    return e

def generate_node(book, chunk, avoid, retries=3):
    prompt = PROMPT.format(title=book["title"], author=book["author"],
                           avoid="; ".join(avoid[-12:]) or "(none yet)", chunk=chunk[:6500])
    for attempt in range(retries):
        try:
            raw = call(prompt, temp=0.7 - attempt * 0.2)
        except Quota:
            raise
        except Exception:
            continue
        try:
            n = sanitize(json.loads(raw))
        except Exception:
            continue
        if not content_errors(n):
            return n
    return None

# ---------------------------------------------------------------- structure assignment + safe merge
def slug(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())[:14]

def next_track_id(graph):
    used = {t["id"] for t in graph["tracks"]}
    for c in "GHIJKLMNOPQRSTUVWXYZ":
        if c not in used:
            return c
    raise RuntimeError("out of track ids")

def merge_nodes(graph, track_meta, contents):
    """Assign structure to a list of generated CONTENTS and add a new chained track. Returns a NEW graph."""
    import copy
    g = copy.deepcopy(graph)
    tid = track_meta["id"]
    g["tracks"].append(track_meta)
    existing_ids = {n["id"] for n in g["nodes"]}
    prev = None
    for i, c in enumerate(contents):
        nid = f"{tid.lower()}{i+1}"
        while nid in existing_ids:
            nid += "x"
        existing_ids.add(nid)
        node = {
            "id": nid, "track": tid, "tier": i,
            "prereq": [prev] if prev else [],
            "glyph": c["glyph"], "title": c["title"],
            "bridge": c["bridge"], "sources": c["sources"],
            "quiz": c["quiz"], "apply": c["apply"],
        }
        if prev:                       # concrete, honest dependency reason referencing the actual prior lesson
            node["whyreq"] = clean_text(f"Builds directly on “{contents[i-1]['title']}” — grasp that idea first, then this one follows.")
        g["nodes"].append(node)
        prev = nid
    return g

def graph_ok(graph, books):
    """Full structural re-validation — identical rules to build.validate. True = safe to write."""
    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
        return True, "ok"
    except SystemExit:
        return False, "validate() rejected"
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------------- driver
def chunk_book(book, target):
    paras = [p for ep in book["episodes"] for p in ep["p"]]
    words, cur, out, budget = 0, [], [], max(1, sum(len(p.split()) for p in paras)//target)
    for p in paras:
        cur.append(p); words += len(p.split())
        if words >= budget:
            out.append(" ".join(cur)); cur, words = [], 0
    if cur: out.append(" ".join(cur))
    return out

def too_similar(title, seen):
    t = title.lower()
    return any(difflib.SequenceMatcher(None, t, s.lower()).ratio() > 0.8 for s in seen)

def write_status(**kw):
    st = {}
    if os.path.exists(STATUS):
        try: st = json.load(open(STATUS))
        except Exception: st = {}
    st.update(kw); st["updated"] = int(time.time())
    json.dump(st, open(STATUS, "w"), indent=1)

def run(book_id, track_name, track_glyph, track_accent, target_nodes, max_this_run, dry=False):
    books = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
    graph = json.load(open(GRAPH, encoding="utf-8"))
    book = next(b for b in books["books"] if b["id"] == book_id)
    seen = [n["title"] for n in graph["nodes"]]
    chunks = chunk_book(book, target_nodes)
    print(f"book={book_id} chunks={len(chunks)} budget/run={max_this_run} model={MODEL} keys={len(KEYS)}")
    contents, avoid = [], []
    for i, ch in enumerate(chunks):
        if len(contents) >= max_this_run:
            print(f"  reached run budget ({max_this_run})"); break
        try:
            n = generate_node(book, ch, avoid)
        except Quota:
            print("  QUOTA: all keys exhausted — will resume next run"); break
        if not n:
            print(f"  chunk {i}: invalid after retries — skipped"); continue
        if too_similar(n["title"], seen + avoid):
            print(f"  chunk {i}: duplicate '{n['title']}' — skipped"); continue
        contents.append(n); avoid.append(n["title"])
        print(f"  chunk {i}: OK  {n['glyph']} {n['title']}")
    if not contents:
        print("no new nodes produced this run."); return
    tid = next_track_id(graph)
    tmeta = {"id": tid, "name": track_name, "glyph": track_glyph, "accent": track_accent,
             "blurb": clean_text(f"AI-authored from {book['title']} — {len(contents)} ideas, dependency-locked.")}
    merged = merge_nodes(graph, tmeta, contents)
    ok, msg = graph_ok(merged, books)
    print(f"trial-merge validation: {'PASS' if ok else 'FAIL — ' + msg}")
    if not ok:
        print("ABORT: not writing graph.json (safeguard held)."); return
    if dry:
        print(f"DRY RUN ok: would add track {tid} with {len(contents)} nodes."); 
        json.dump(merged, open(os.path.join(HERE, "graph_preview.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return
    import shutil
    shutil.copy(GRAPH, GRAPH + ".bak")
    json.dump(merged, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    write_status(last_book=book_id, last_track=tid, added=len(contents),
                 total_nodes=len(merged["nodes"]), state="added")
    print(f"WROTE graph.json (+track {tid}, +{len(contents)} nodes). Backup at graph.json.bak")

if __name__ == "__main__":
    import argparse
    if "--queue" in sys.argv:
        run_queue(); raise SystemExit
    ap = argparse.ArgumentParser()
    ap.add_argument("book"); ap.add_argument("--name", required=True)
    ap.add_argument("--glyph", default="🤖"); ap.add_argument("--accent", default="#5dade2")
    ap.add_argument("--target", type=int, default=8); ap.add_argument("--max", type=int, default=DAILY_BUDGET)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    run(a.book, a.name, a.glyph, a.accent, a.target, a.max, a.dry)

# ================================================================ CLOUD (GitHub Actions) mode
import gzip, base64 as _b64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
CONTENT = os.path.join(HERE, "..", "content.enc")
QUEUE = os.path.join(HERE, "queue")

def vault_key():
    k = os.environ.get("VAULT_KEY") or open(os.path.join(HERE, "key.txt")).read().strip()
    return _b64.urlsafe_b64decode(k + "==")

def dec_enc(path):
    raw = open(path, "rb").read()
    pt = AESGCM(vault_key()).decrypt(raw[:12], raw[12:], None)
    return json.loads(gzip.decompress(pt))

def enc_obj(obj, path):
    data = gzip.compress(json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode(), 9)
    iv = os.urandom(12)
    open(path, "wb").write(iv + AESGCM(vault_key()).encrypt(iv, data, None))

def append_to_track(graph, tmeta, contents):
    import copy
    g = copy.deepcopy(graph)
    tid = tmeta["id"]
    if not any(t["id"] == tid for t in g["tracks"]):
        g["tracks"].append(tmeta)
    tnodes = [n for n in g["nodes"] if n["track"] == tid]
    prev = max(tnodes, key=lambda n: n["tier"])["id"] if tnodes else None
    base_tier = (max(n["tier"] for n in tnodes) + 1) if tnodes else 0
    ids = {n["id"] for n in g["nodes"]}
    for i, c in enumerate(contents):
        nid = f"{tid.lower()}{base_tier + i + 1}"
        while nid in ids: nid += "x"
        ids.add(nid)
        node = {"id": nid, "track": tid, "tier": base_tier + i,
                "prereq": [prev] if prev else [], "glyph": c["glyph"], "title": c["title"],
                "bridge": c["bridge"], "sources": c["sources"], "quiz": c["quiz"], "apply": c["apply"]}
        if prev:
            node["whyreq"] = clean_text(f"Builds directly on “{(contents[i-1]['title'] if i>0 else next(n['title'] for n in g['nodes'] if n['id']==prev))}” — grasp that first.")
        g["nodes"].append(node); prev = nid
    return g

def graph_ok_books(graph, books):
    sys.path.insert(0, HERE); import build
    try:
        build.validate({"books": books}, graph); return True, "ok"
    except SystemExit: return False, "rejected"
    except Exception as e: return False, str(e)

def run_queue():
    """Cloud entry: process one pending encrypted job, chaining across daily runs. Idempotent + resumable."""
    if not os.path.isdir(QUEUE):
        print("no queue dir; nothing to do"); return
    jobs = sorted(f for f in os.listdir(QUEUE) if f.endswith(".job.enc"))
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = dec_enc(CONTENT)["books"]                      # library text, from the encrypted payload only
    seen = [n["title"] for n in graph["nodes"]]
    processed = 0
    for jf in jobs:
        jp = os.path.join(QUEUE, jf)
        job = dec_enc(jp)
        if job.get("done", 0) >= len(job["chunks"]):
            continue                                       # already finished
        tmeta = {"id": job["track_id"], "name": job["name"], "glyph": job["glyph"],
                 "accent": job["accent"], "blurb": job["blurb"]}
        contents, avoid, i = [], [], job.get("done", 0)
        while i < len(job["chunks"]) and processed < DAILY_BUDGET:
            try:
                n = generate_node({"title": job["title"], "author": job["author"]}, job["chunks"][i], avoid)
            except Quota:
                print("quota exhausted; resume next run"); break
            i += 1; processed += 1
            if n and not too_similar(n["title"], seen + avoid):
                contents.append(n); avoid.append(n["title"]); print(f"  {job['id']} #{i}: {n['glyph']} {n['title']}")
            else:
                print(f"  {job['id']} #{i}: skipped (invalid/dup)")
        if contents:
            merged = append_to_track(graph, tmeta, contents)
            ok, msg = graph_ok_books(merged, books)
            if not ok:
                print(f"  ABORT merge for {job['id']}: {msg}"); continue
            graph = merged
            json.dump(graph, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            enc_obj({"v": 2, "books": books, "tracks": graph["tracks"], "nodes": graph["nodes"]}, CONTENT)
        job["done"] = i
        enc_obj(job, jp)
        pct = round(100 * job["done"] / len(job["chunks"]))
        write_status(job=job["id"], title=job["title"], track=job["track_id"],
                     done=job["done"], total=len(job["chunks"]), percent=pct,
                     state="complete" if job["done"] >= len(job["chunks"]) else "in-progress")
        print(f"  {job['id']}: {job['done']}/{len(job['chunks'])} ({pct}%)")
        break                                              # one job per run keeps quota predictable
    else:
        write_status(state="idle"); print("queue idle — all jobs complete")
