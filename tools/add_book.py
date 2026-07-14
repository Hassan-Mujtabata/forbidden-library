# -*- coding: utf-8 -*-
"""
Local book-adding tool. Extracts a PDF, chunks it, and writes an ENCRYPTED job into
tools/queue/<id>.job.enc (ciphertext — safe to commit). The daily GitHub Action decrypts
it with the vault key and turns it into a dependency-locked Path track, a chunk at a time.

Usage:
  python tools/add_book.py "C:/path/Some Book.pdf" --name "Track Name" --author "Author" \
         --glyph 🤖 --accent "#5dade2" --nodes 8
Then: git add tools/queue && git commit -m "queue: add <book>" && git push
"""
import fitz, json, os, re, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gemini_pipeline as gp

def extract(path):
    doc = fitz.open(path)
    paras, junk = [], re.compile(r"copyright|isbn|all rights reserved|www\.|http", re.I)
    for page in doc:
        for b in page.get_text("blocks"):
            t = re.sub(r"\s+", " ", b[4]).strip()
            if len(t.split()) >= 8 and not junk.search(t[:120]):
                paras.append(t)
    doc.close()
    return paras

def chunk(paras, n):
    total = sum(len(p.split()) for p in paras)
    budget = max(120, total // max(1, n))
    out, cur, w = [], [], 0
    for p in paras:
        cur.append(p); w += len(p.split())
        if w >= budget:
            out.append(" ".join(cur)); cur, w = [], 0
    if cur: out.append(" ".join(cur))
    return out

def reserve_track_id():
    graph = json.load(open(gp.GRAPH, encoding="utf-8"))
    used = {t["id"] for t in graph["tracks"]}
    if os.path.isdir(gp.QUEUE):
        for f in os.listdir(gp.QUEUE):
            if f.endswith(".job.enc"):
                try: used.add(gp.dec_enc(os.path.join(gp.QUEUE, f))["track_id"])
                except Exception: pass
    for c in "GHIJKLMNOPQRSTUVWXYZ":
        if c not in used: return c
    raise SystemExit("no free track id")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf"); ap.add_argument("--name", required=True); ap.add_argument("--author", default="Unknown")
    ap.add_argument("--glyph", default="🤖"); ap.add_argument("--accent", default="#5dade2")
    ap.add_argument("--nodes", type=int, default=8)
    a = ap.parse_args()
    if not os.path.exists(a.pdf): raise SystemExit("no such pdf: " + a.pdf)
    paras = extract(a.pdf)
    chunks = chunk(paras, a.nodes)
    bid = re.sub(r"[^a-z0-9]+", "", os.path.splitext(os.path.basename(a.pdf))[0].lower())[:16] or "book"
    tid = reserve_track_id()
    job = {"id": bid, "title": a.name, "author": a.author, "track_id": tid,
           "name": a.name, "glyph": a.glyph, "accent": a.accent,
           "blurb": f"AI-authored from {a.name} — a dependency-locked track.",
           "chunks": chunks, "done": 0}
    os.makedirs(gp.QUEUE, exist_ok=True)
    out = os.path.join(gp.QUEUE, f"{bid}.job.enc")
    gp.enc_obj(job, out)
    print(f"queued {out}")
    print(f"  book='{a.name}' track={tid} chunks={len(chunks)} words={sum(len(c.split()) for c in chunks)}")
    print("  next: git add tools/queue && git commit -m 'queue: {}' && git push".format(a.name))

if __name__ == "__main__":
    main()
