# -*- coding: utf-8 -*-
"""Repair text damage that PDF extraction bakes into books.json.

    python tools/cleantext.py            # scan only: report what is damaged, change nothing
    python tools/cleantext.py --fix      # repair books.json in place (writes books.json.bak first)

Three distinct kinds of damage were found in the corpus, and each needs a DIFFERENT repair.
Stripping the bad bytes is not enough -- for two of the three it silently deletes real letters:

 1. UTF-16BE READ AS LATIN-1  (Right Concentration, 40722 chars, 454/725 paragraphs)
    The extractor decoded part of the PDF byte-for-byte, so every character arrived as its
    two UTF-16 bytes: "bliss" -> "\\x00b\\x00l\\x00i\\x00s\\x00s".
    Deleting the NULs looks like it works on ASCII, but the non-ASCII letters are encoded in
    BOTH bytes -- "jhana" is really "jh\\x01\\x01na", and stripping controls turns the a-macron
    into NOTHING: "jhna". Only a real UTF-16BE decode restores it as "jhana" with the macron.
    Runs are interleaved with correctly-decoded text inside the same paragraph, so we repair
    run-by-run rather than per paragraph.

 2. PRIVATE-USE LIGATURES  (The Like Switch, 854 chars, 524/1395 paragraphs)
    The PDF embedded a subset font whose "Th" ligature sits at U+E053/U+E04E/U+E002 -- code
    points with no Unicode meaning, so the glyph shown is whatever the CURRENT font happens to
    have in its private range. That is the bug Hassan reported: the symbol CHANGES when you
    switch the reading typeface, because each font invents its own picture for it.
    Worse, the "Th" is genuinely missing from the text: "Then" reads as "en".
    The mapping is proven, not guessed: all 26 distinct following fragments form real words
    when "Th" is prepended (e/is/ey/ese/at/ere/eir/en/us/ink/ird/ank/ereafter/roughout/...),
    and every occurrence is word-initial. See PUA below.

 3. LEFTOVER CONTROL CHARACTERS
    Whatever survives 1 and 2 has no glyph at all, so the browser draws each one with the
    font's .notdef box -- which again differs per font. Strip them last, after the repairs
    above have had their chance to interpret them as data.

Anything in the Private Use Area that is NOT in the proven map is reported by name and
dropped, never guessed at -- a wrong guess would put invented words into the books.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "books.json")

# Proven by context, not assumed -- see the module docstring. All three are the same "Th"
# ligature; a subset font is free to place the same glyph at several private code points.
PUA = {"\ue002": "Th", "\ue04e": "Th", "\ue053": "Th"}

# Presentation-form ligatures. Unlike everything else here these LOOK correct on screen, so
# they hide in plain sight -- but "first" is stored as a single code point U+FB01 + "rst", and
# the journal/library search compares plain text, so typing "first" never finds it. Expanding
# them is the standard NFKC decomposition: lossless, and it makes 1415 words searchable again.
LIGATURES = {"\ufb00": "ff", "\ufb01": "fi", "\ufb02": "fl",
             "\ufb03": "ffi", "\ufb04": "ffl", "\ufb05": "st", "\ufb06": "st"}

# Control characters that never carry meaning in book prose. Tab and newline are kept.
CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")
# Characters that only ever appear as the high byte of a mis-decoded UTF-16 pair.
TRIGGER = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
ANY_PUA = re.compile(r"[\ue000-\uf8ff]")
# Ad copy the Bookey summary app injects into its own PDF exports.
ADS = re.compile(r"install bookey app to unlock full text( and audio)?\.?", re.I)


def plausible(cp):
    """Is this code point a letter we would expect a UTF-16BE pair to decode to?

    Accepting too much is the danger: a run must END where the mis-decoded region ends and
    correctly-decoded text resumes, and the only signal for that is the pair stopping to look
    like Latin text. Latin-1 + Latin Extended-A/B + IPA + Latin Extended Additional covers
    every script in this corpus (jhana, Vinnana, Nanamoli) and nothing else.
    """
    return 0x20 <= cp <= 0x2FF or 0x1E00 <= cp <= 0x1EFF


# A genuine mis-decode runs for whole sentences (the shortest in this corpus is dozens of
# characters). Two ADJACENT stray control bytes would also pair into a "plausible" code point --
# \x01\x02 decodes to "A-breve" -- which would invent a letter that was never in the book. Require
# a real run so isolated damage falls through to being stripped instead of reinterpreted.
MIN_RUN = 4


def repair_utf16(s):
    """Decode mis-decoded UTF-16BE runs in place, leaving correctly-decoded text alone."""
    if not TRIGGER.search(s):
        return s
    out, i, n = [], 0, len(s)
    while i < n:
        if TRIGGER.match(s[i]) and i + 1 < n:
            j, buf = i, []
            while j + 1 < n:
                cp = (ord(s[j]) << 8) | ord(s[j + 1])
                if not plausible(cp):
                    break
                buf.append(chr(cp))
                j += 2
            if len(buf) >= MIN_RUN:       # consumed a real run
                out.append("".join(buf))
                i = j
                continue
        out.append(s[i])
        i += 1
    return "".join(out)


def clean(s, unknown=None):
    s = repair_utf16(s)
    for k, v in PUA.items():
        s = s.replace(k, v)
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    if unknown is not None:
        for ch in ANY_PUA.findall(s):
            unknown[ch] = unknown.get(ch, 0) + 1
    s = ANY_PUA.sub("", s)                # unmapped PUA: reported above, never guessed
    s = ADS.sub("", s)
    s = CTRL.sub("", s)
    s = s.replace("\u00a0", " ")     # non-breaking space: invisible, but breaks word search
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def main():
    fix = "--fix" in sys.argv
    data = json.load(open(BOOKS, encoding="utf-8"))
    unknown, total, empties = {}, 0, 0

    print("%-12s %8s %8s %8s" % ("book", "paras", "damaged", "chars"))
    for b in data["books"]:
        dmg = chars = paras = 0
        for e in b["episodes"]:
            new = []
            for p in e["p"]:
                paras += 1
                c = clean(p, unknown)
                if c != p:
                    dmg += 1
                    chars += (len(CTRL.findall(p)) + len(ANY_PUA.findall(p)) +
                              sum(p.count(k) for k in LIGATURES))
                if c:
                    new.append(c)
                else:
                    empties += 1          # paragraph was nothing but ad copy / control bytes
            e["p"] = new
        total += chars
        if dmg:
            print("%-12s %8d %8d %8d" % (b["id"], paras, dmg, chars))

    if unknown:
        print("\nUNMAPPED private-use code points (dropped, not guessed):")
        for ch, n in sorted(unknown.items(), key=lambda kv: -kv[1]):
            print("   U+%04X  x%d" % (ord(ch), n))

    print("\n%d damaged characters across the library." % total)
    if empties:
        print("%d paragraph(s) removed (nothing left but injected ad copy)." % empties)

    if not fix:
        print("Scan only. Re-run with --fix to write the repairs.")
        return
    os.replace(BOOKS, BOOKS + ".bak")
    with open(BOOKS, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("books.json repaired (previous copy at books.json.bak).")
    print("Now run: python tools/build.py    to rebuild content.enc")


if __name__ == "__main__":
    main()
