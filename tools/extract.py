# -*- coding: utf-8 -*-
"""Extract text from the vault PDFs into episode-structured books.json."""
import fitz, json, re, os, sys
from collections import Counter

ROOT = r"C:\Users\sands\OneDrive\Desktop\forbidden"
OUT = os.path.join(ROOT, "vault", "tools", "books.json")

BOOKS = [
    dict(id="laws48",    file="The+48+Laws+Of+Power.pdf",
         title="The 48 Laws of Power", author="Robert Greene",
         wing="shadow", glyph="♛", accent="#d4af37"),
    dict(id="seduction", file="the-art-of-seduction-robert-greene.pdf",
         title="The Art of Seduction", author="Robert Greene",
         wing="shadow", glyph="\U0001f339", accent="#c0392b"),
    dict(id="dark3in1",  file="toaz.info-dark-psychology-3-books-in-1-manipulation-and-dark-psychology-persuasion-and-da-pr_3dcd544069c7dadb05496c45e076e642.pdf",
         title="Dark Psychology: 3 Books in 1", author="Various",
         wing="shadow", glyph="\U0001f9e0", accent="#8e44ad"),
    dict(id="covert30",  file="30 Covert Emotional Manipulation Tactics_ How Manipulators Take Control In Personal Relationships - PDF Room.pdf",
         title="30 Covert Emotional Manipulation Tactics", author="Adelyn Birch",
         wing="shadow", glyph="\U0001f3ad", accent="#e67e22"),
    dict(id="deception", file="Kevin_Mitnick_-_The_Art_of_Deception.pdf",
         title="The Art of Deception", author="Kevin Mitnick",
         wing="shadow", glyph="\U0001f576", accent="#2c3e50"),
    dict(id="manip",     file="Manipulation Dark Psychology to Manipulate and Control People by Arthur Horn [Horn, Arthur] (z-lib.org) (1).pdf",
         title="Manipulation: Dark Psychology", author="Arthur Horn",
         wing="shadow", glyph="\U0001f9f2", accent="#7f8c8d"),
    dict(id="persuasion", file="The Psychology of Persuasion.pdf",
         title="Influence: The Psychology of Persuasion", author="Robert Cialdini",
         wing="shadow", glyph="\U0001f3af", accent="#c0a062"),
    dict(id="quietinf",  file="16-05-2021-050120The-Art-of-Quiet-Influence.pdf",
         title="The Art of Quiet Influence", author="Jocelyn Davis",
         wing="light", glyph="\U0001f343", accent="#27ae60"),
    dict(id="bliss",     file="Ajahn_Brahm-Mindfulness_Bliss_and_Beyond-Chapters1-4_copy.pdf",
         title="Mindfulness, Bliss and Beyond", author="Ajahn Brahm",
         wing="light", glyph="\U0001fab7", accent="#16a085"),
    dict(id="insight",   file="bp520s_Goldstein_Experience-of-Insight.pdf",
         title="The Experience of Insight", author="Joseph Goldstein",
         wing="light", glyph="\U0001f441", accent="#2980b9"),
    dict(id="beautiful", file="How To Have A Beautiful Mind.pdf",
         title="How to Have a Beautiful Mind", author="Edward de Bono",
         wing="light", glyph="\U0001f48e", accent="#9b59b6"),
    dict(id="tmi",       file="The Mind Illuminated - A Complete Meditation Guide Integrating Buddhist Wisdom and Brain Science ( PDFDrive.com ) (1).pdf",
         title="The Mind Illuminated", author="Culadasa (John Yates)",
         wing="light", glyph="\U0001f319", accent="#34495e"),
]

HEAD_RE = re.compile(
    r"^(law|chapter|part|tactic|rule|key|stage|section|book|step|principle|weapon|interlude|appendix)"
    r"[\s:#]*([0-9ivxlcIVXLC]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)?\b",
    re.IGNORECASE)


def clean(t):
    t = t.replace("­", "")
    t = re.sub(r"-\n(?=[a-z])", "", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip()


def is_heading(p):
    if len(p) > 72 or len(p) < 3:
        return False
    if p.endswith((".", ",", ";", "?", "!")) and not HEAD_RE.match(p):
        return False
    if HEAD_RE.match(p) and len(p.split()) <= 12:
        return True
    letters = [c for c in p if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.82 and len(letters) >= 4:
        return True
    return False


def extract(meta):
    path = os.path.join(ROOT, meta["file"])
    doc = fitz.open(path)
    npages = len(doc)
    blocks = []
    for page in doc:
        for b in page.get_text("blocks"):
            if b[6] != 0:
                continue
            t = b[4].strip()
            if t:
                blocks.append(t)
    doc.close()

    # strip repeated headers/footers
    norm = lambda s: re.sub(r"\d+", "#", s.strip().lower())[:48]
    freq = Counter(norm(t) for t in blocks if len(t) < 90)
    thresh = max(4, npages // 5)
    blocks = [t for t in blocks if not (len(t) < 90 and freq[norm(t)] >= thresh)]
    # strip bare page numbers / roman numerals
    blocks = [t for t in blocks if not re.fullmatch(r"[\divxlc\s.\-–•|]+", t.strip().lower())]
    # strip front-matter boilerplate
    junk = re.compile(r"copyright|isbn|library of congress|all rights reserved|penguin\s|viking penguin"
                      r"|z-lib|pdf room|pdfdrive|www\.|http|printed in the|first published|publishing division",
                      re.IGNORECASE)
    blocks = [t for t in blocks if not (len(t) < 400 and junk.search(t))]

    paras = [p for p in (clean(t) for t in blocks) if p]

    # some PDFs emit one block per printed line; merge fragments into real paragraphs
    avg = sum(len(p.split()) for p in paras) / max(1, len(paras))
    if avg < 25:
        joined = []
        for p in paras:
            if (joined and not is_heading(p) and not is_heading(joined[-1])
                    and len(joined[-1]) < 900
                    and joined[-1][-1] not in '.!?:;"”’'):
                joined[-1] += " " + p
            else:
                joined.append(p)
        paras = joined

    episodes = []
    cur_title, cur_paras, words = None, [], 0

    def flush():
        nonlocal cur_title, cur_paras, words
        if cur_paras:
            title = cur_title or f"Episode {len(episodes) + 1}"
            if title.isupper():
                title = title.title()
            episodes.append({"t": title, "p": cur_paras})
        cur_title, cur_paras, words = None, [], 0

    for p in paras:
        if is_heading(p):
            if words > 150:
                flush()
                cur_title = p
            elif cur_title is None and not cur_paras:
                cur_title = p
            else:
                cur_paras.append(p)
        else:
            cur_paras.append(p)
            words += len(p.split())
            if words > 1400:
                flush()
    flush()

    # merge tiny trailing episodes
    merged = []
    for ep in episodes:
        w = sum(len(p.split()) for p in ep["p"])
        if merged and w < 120:
            merged[-1]["p"].extend(ep["p"])
        else:
            merged.append(ep)

    total_words = sum(len(p.split()) for ep in merged for p in ep["p"])
    book = {k: meta[k] for k in ("id", "title", "author", "wing", "glyph", "accent")}
    book["episodes"] = merged
    return book, npages, len(paras), total_words


def main():
    out, report = [], []
    for meta in BOOKS:
        try:
            book, npages, nparas, words = extract(meta)
            neps = len(book["episodes"])
            ok = words > 3000
            if ok:
                out.append(book)
            report.append(f"{'OK ' if ok else 'BAD'} {meta['id']:<11} pages={npages:<4} paras={nparas:<5} words={words:<7} episodes={neps}")
        except Exception as e:
            report.append(f"ERR {meta['id']:<11} {e}")
    data = {"v": 1, "books": out}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("\n".join(report))
    print(f"\nwrote {OUT} ({os.path.getsize(OUT)/1e6:.2f} MB, {len(out)} books)")


if __name__ == "__main__":
    main()
