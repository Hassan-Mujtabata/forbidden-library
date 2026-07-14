# -*- coding: utf-8 -*-
"""Derisk test: can Gemini produce a node whose CONTENT passes the vault's validation?"""
import json, os, re, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = [k.strip() for k in open(os.path.join(HERE, ".gemini_keys")) if k.strip()]
MODEL = "gemini-2.5-flash"

# --- real source text: pull a chunk from an existing book (simulating a "new book") ---
books = json.load(open(os.path.join(HERE, "books.json"), encoding="utf-8"))
book = next(b for b in books["books"] if b["id"] == "beautiful")  # de Bono
chunk = " ".join(p for ep in book["episodes"][8:14] for p in ep["p"])[:6000]

SCHEMA_PROMPT = """You are an expert curriculum author for "The Vault", a serious self-study reading app. \
You will be given a passage from the book "{title}" by {author}. \
Distill ONE self-contained idea from it into a lesson, returning ONLY a single JSON object (no markdown, no prose outside JSON) with EXACTLY these fields:

{{
  "title": "<the concept as a short noun phrase, 2-6 words, Title Case>",
  "glyph": "<a single relevant emoji>",
  "bridge": ["<para1>", "<para2>", "<para3>"],   // exactly 3 paragraphs of your own connective explanation ("guide note"), 45-110 words each, second-person, plain and vivid, NEVER quoting the book verbatim here
  "sources": [                                     // 1 to 2 items, each an attributed excerpt
    {{"book": "{title}", "ref": "<short topical locator, 2-6 words, NOT the author's name>", "quote": ["<one faithful short excerpt or close paraphrase from the passage, 12-40 words>"]}}
  ],
  "quiz": [                                        // EXACTLY 3 multiple-choice questions
    {{"q": "<question>", "c": ["<opt0>","<opt1>","<opt2>","<opt3>"], "a": <index 0-3 of the correct option>, "why": "<one-sentence explanation of the answer>"}}
  ],
  "apply": {{"prompt": "<a concrete first-person practice or reflection task tying the idea to the reader's real life>", "min": 50}},
  "whyreq": "<one sentence: why understanding this idea depends on grasping more basic ideas first>"
}}

Rules: valid JSON only. Exactly 3 bridge paragraphs. Exactly 3 quiz questions, each with exactly 4 options and an integer answer index in range. Do not invent facts not supported by the passage. Match a calm, precise, non-cheesy tone.

PASSAGE:
{chunk}
"""

def gen(key, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"}
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    return d["candidates"][0]["content"]["parts"][0]["text"]

# --- the SAME kind of validation the build uses, applied to generated CONTENT ---
def validate_content(n):
    errs = []
    if not isinstance(n.get("title"), str) or not (2 <= len(n["title"].split()) <= 8): errs.append("title shape")
    if not isinstance(n.get("glyph"), str) or len(n["glyph"]) > 4: errs.append("glyph")
    if not (isinstance(n.get("bridge"), list) and len(n["bridge"]) == 3 and all(isinstance(x, str) and len(x.split()) >= 25 for x in n["bridge"])): errs.append("bridge (need 3 substantial paras)")
    if not (isinstance(n.get("sources"), list) and 1 <= len(n["sources"]) <= 3): errs.append("sources count")
    for s in n.get("sources", []):
        if not (isinstance(s.get("book"), str) and isinstance(s.get("ref"), str) and isinstance(s.get("quote"), list) and s["quote"]): errs.append("source shape")
    if not (isinstance(n.get("quiz"), list) and len(n["quiz"]) == 3): errs.append("quiz count")
    for q in n.get("quiz", []):
        if not (isinstance(q.get("q"), str) and isinstance(q.get("c"), list) and len(q["c"]) == 4 and isinstance(q.get("a"), int) and 0 <= q["a"] < 4 and isinstance(q.get("why"), str)): errs.append("quiz item shape")
    ap = n.get("apply", {})
    if not (isinstance(ap, dict) and isinstance(ap.get("prompt"), str) and isinstance(ap.get("min"), int)): errs.append("apply shape")
    if not isinstance(n.get("whyreq"), str): errs.append("whyreq")
    return errs

prompt = SCHEMA_PROMPT.format(title=book["title"], author=book["author"], chunk=chunk)
raw = gen(KEYS[0], prompt)
try:
    node = json.loads(raw)
except Exception as e:
    print("JSON PARSE FAIL:", e); print(raw[:800]); raise SystemExit

errs = validate_content(node)
print("=" * 70)
print("VALIDATION:", "PASS ✓" if not errs else "FAIL -> " + ", ".join(errs))
print("=" * 70)
print("title :", node.get("title"), node.get("glyph"))
print("bridge[0]:", node["bridge"][0][:220])
print("source:", node["sources"][0]["book"], "—", node["sources"][0]["ref"])
print("  quote:", node["sources"][0]["quote"][0][:160])
print("quiz[0]:", node["quiz"][0]["q"])
for i, c in enumerate(node["quiz"][0]["c"]):
    print(f"   {'*' if i==node['quiz'][0]['a'] else ' '} {c}")
print("   why:", node["quiz"][0]["why"])
print("apply :", node["apply"]["prompt"][:200], "(min", node["apply"]["min"], ")")
print("whyreq:", node.get("whyreq"))
open(os.path.join(HERE, "gemini_test_out.json"), "w", encoding="utf-8").write(json.dumps(node, ensure_ascii=False, indent=2))
