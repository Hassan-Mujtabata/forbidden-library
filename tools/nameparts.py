# -*- coding: utf-8 -*-
"""#167 JOB 2 — give every numbered slice a name taken from its own text.

A chapter longer than the word budget is cut into slices, and every slice after the first
inherits the chapter name with a number: "Step Three: Strategies Toward Bringing Out the
Rational (12)". Twelve identical names is still one undifferentiated block, which is the thing
the library was supposed to fix. extract.py already recovers every heading the PDF actually
contains; what is left over are long stretches the author never subdivided, so there is no
heading to find and a name has to come from the slice's own content.

THE RULE, same as the one governing the quotes: derived, never invented. The label is lifted
from the slice's opening sentence, not written about it -- so it cannot claim the slice contains
something it does not. Where the opening is a pure continuation ("It was the same for him"),
there is nothing honest to lift and the numbered form is KEPT rather than replaced with a guess.
A missing name is a smaller failure than a wrong one.

    python tools/nameparts.py --preview     # show what it would do, write nothing
    python tools/nameparts.py               # apply to books.json
"""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "books.json")

PART = re.compile(r"^(.*) \((\d+)\)$")

# Openers that carry no information about the slice. Stripped before the label is taken, because
# "Second, the Laws will make you a master interpreter" says something and "Second" does not.
LEAD = re.compile(
    r"^(second|third|fourth|fifth|first|finally|lastly|next|then|now|so|but|and|yet|however|"
    r"moreover|furthermore|therefore|thus|hence|meanwhile|instead|besides|still|again|"
    r"in fact|in short|in other words|of course|for example|for instance|that is|after all|"
    r"on the other hand|at the same time|in this way|in the end|as a result|indeed|likewise)"
    r"\b[,:;]?\s*", re.IGNORECASE)

# A label starting with one of these refers to something in the PREVIOUS slice, so it cannot
# stand alone as a name.
DANGLING = re.compile(r"^(it|he|she|they|them|this|that|these|those|his|her|their|its|such|"
                      r"there|here|we|you|i|him|one|another|both|each|either|neither)\b",
                      re.IGNORECASE)

STOP = set("""a an the and or but of in on at to for from by with as is are was were be been
being it its that this these those he she they them his her their our your my we you i not no
so if then than there here what which who whom whose when where why how all any some most more
much many few own same such only just very can will would could should may might must do does
did done have has had having if into over under out up down off about against between through
during before after above below again further once because while until also them then""".split())


def sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", p) if s.strip()]


def label_from(text, seen):
    """Lift a short label from the opening of `text`, or return None if nothing honest is there."""
    s = sentences(text)
    if not s:
        return None
    first = s[0]
    first = LEAD.sub("", first, count=1)
    if not first or DANGLING.match(first):
        return None
    # cut at the first natural boundary so the label is a phrase, not half a sentence
    cut = re.split(r"[,;:—–]| — | that | which | because | when | while | but | and ",
                   first, maxsplit=1)[0]
    w = cut.split()
    if len(w) > 8:
        w = w[:8]
    while w and w[-1].lower() in STOP:
        w.pop()
    if len(w) < 3:
        return None
    lab = " ".join(w).strip(" .,;:—–\"'“”’")
    if len(lab) < 12 or len(lab) > 64:
        return None
    if not any(c.isalpha() for c in lab):
        return None
    # must carry at least two content words, else it says nothing
    content = [x for x in lab.lower().split() if x not in STOP and len(x) > 2]
    if len(content) < 2:
        return None
    key = " ".join(content)
    if key in seen:
        return None
    seen.add(key)
    return lab[0].upper() + lab[1:]


def main():
    preview = "--preview" in sys.argv
    only = [a.split("=",1)[1] for a in sys.argv if a.startswith("--book=")]
    books = json.load(open(BOOKS, encoding="utf-8"))
    named = kept = 0
    samples = []

    for b in books["books"]:
        if only and b["id"] not in only:
            continue
        seen = set()
        for ep in b["episodes"]:
            m = PART.match(ep["t"])
            if not m:
                continue
            base, num = m.group(1), m.group(2)
            lab = None
            for p in ep["p"][:2]:               # opening paragraph, then the one after it
                lab = label_from(p, seen)
                if lab:
                    break
            if not lab:
                kept += 1
                continue
            title = f"{base} — {lab}"
            if len(title) > 96:                 # keep the tail, it is the informative half
                title = f"…{base[-28:]} — {lab}"
            if len(samples) < 24:
                samples.append((b["title"], ep["t"], title))
            ep["t"] = title
            named += 1

    print("%-22s %-46s %s" % ("BOOK", "WAS", "NOW"))
    for bk, was, now in samples:
        print("%-22s %-46s %s" % (bk[:22], was[:46], now[:70]))
    print()
    print("named from content: %d" % named)
    print("left numbered (no honest label available): %d" % kept)

    if preview:
        print("\n--preview: books.json NOT written")
        return
    json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False,
              separators=(",", ":"))
    print("\nbooks.json updated -> next: python tools/build.py")


if __name__ == "__main__":
    main()
