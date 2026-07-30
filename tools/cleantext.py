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

 4. IPA / PUNCTUATION STAND-INS FOR LIGATURES  (Man's Search for Meaning, Bliss Beyond)
    A second family of subset fonts mapped their ligatures onto real Unicode letters instead of
    the private-use area, so the damage is INVISIBLE to every check above -- the characters are
    perfectly valid, they are just the wrong ones. "first" is stored as "ɹrst" with an IPA
    turned-r, and every jhana in Bliss Beyond is "jh›na" with a single angle quote where the
    a-macron belongs. Each damaged code point is confined to exactly ONE book (see MAP below),
    which is what a per-PDF font quirk looks like and is itself evidence the mapping is real.
    Two of them are ambiguous -- U+0283 is "ff" in "suʃered" but "ffi" in "suʃcient" --
    so those are resolved per word against a dictionary built from THIS corpus: whatever the
    library already spells correctly somewhere in its 13.3M characters is a real word. 594 of the
    620 damaged tokens resolve that way; the rest are hyphenated compounds and rare Pali proper
    nouns whose expansion is unambiguous anyway.

 5. LINE-BREAK HYPHENS THAT BECAME GUILLEMETS  (48 Laws, ~1100 occurrences)
    The extractor turned the soft hyphen at a line break into "»", "«" or "~", leaving
    "resent» ment" and "manipu~ late" mid-sentence. Rejoining is only done when the joined
    form is a word the corpus already knows, so a real hyphen ("East~West") is never eaten and
    no new word is ever invented; anything unresolved just loses the stray character.

 6. JUNK EPISODE TITLES  (47 of them)
    Front-matter pages came through as "1(}A.‘3\\ Law 15" and "VVC)Rl(()D$TT{EZ}IEAURTS".
    These are read out in the reader header, the CONTINUE card and every search result, so they
    are the most VISIBLE damage in the library. Junk tokens are dropped and the recognisable part
    kept ("Law 15"); a title with nothing recognisable left falls back to "Episode N", which is
    what most of this corpus already uses, rather than to an empty string -- `esc(ep.t)` is
    rendered with no fallback of its own, so a blank title shows as a blank CONTINUE card.

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

# Ligatures a subset font parked on real Unicode letters (damage #4). Every one of these is
# confined to a single book, listed here so a future scan can tell "still there" from "came back".
#   U+0279 fi   U+027B fl   U+0283 ff|ffi   U+0280 ffl|ffi|ffil   U+027D ffi   [meaning]
#   U+203A a-macron   U+02DB t-underdot                                        [bliss]
# The single-valued ones are applied unconditionally; the list-valued ones go to the resolver.
MAP = {
    "ɹ": "fi",
    "ɻ": "fl",
    "›": "ā",                    # a with macron: jh›na -> jhāna
    "˛": "ṭ",                    # t with dot below: a˛˛hakathā -> aṭṭhakathā
}
AMBIG = {
    "ʃ": ["ff", "ffi"],               # suʃered -> suffered, suʃcient -> sufficient
    "ʀ": ["ffl", "ffi", "ffil"],      # aʀictions -> afflictions, aʀiated -> affiliated
    "ɽ": ["ffi"],                     # diɽcilia -> difficilia (Latin, 1 occurrence)
}
# Used when no candidate is a known word: the overwhelmingly commoner expansion. Every token
# that lands here was checked by hand and is a hyphenated or em-dashed compound (side-eʃect,
# aʃording, k›ma-cchanda) whose expansion is not in doubt, only absent from the dictionary.
AMBIG_DEFAULT = {"ʃ": "ff", "ʀ": "ffl", "ɽ": "ffi"}

# A line-break hyphen that arrived as a guillemet or tilde (damage #5). Captures the letters
# either side so the join can be dictionary-checked before it is made.
HYPH = re.compile(r"([A-Za-zÀ-ɏ]{2,})[«»~]([ \t]*)([A-Za-zà-ɏ]{2,})")
# A stray guillemet/tilde still sitting between two letters after the rejoin pass was a plain
# hyphen all along ("Chiang Kai~shek"), so it becomes one rather than being dropped.
HYPH_TIGHT = re.compile(r"([A-Za-zÀ-ɏ])[«»~]([A-Za-zÀ-ɏ])")
WORD = re.compile(r"[A-Za-zÀ-ɏḀ-ỿ']+")

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
    for k, v in MAP.items():
        s = s.replace(k, v)
    if unknown is not None:
        for ch in ANY_PUA.findall(s):
            unknown[ch] = unknown.get(ch, 0) + 1
    s = ANY_PUA.sub("", s)                # unmapped PUA: reported above, never guessed
    s = ADS.sub("", s)
    s = CTRL.sub("", s)
    s = s.replace("\u00a0", " ")     # non-breaking space: invisible, but breaks word search
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def resolve(s, vocab, stats=None):
    """Second pass: the repairs that need to know what a real word looks like.

    Kept separate from clean() because the dictionary is built FROM clean() output -- a word
    can only vouch for a spelling once its own damage has been repaired.
    """
    # #129: substituted match-by-match, NOT with s.replace(tok, ...). Replacing by token text
    # rewrites every occurrence of that substring, and a short damaged token is frequently a
    # prefix of a longer one in the same paragraph ("su<x>er" inside "su<x>ering") -- the short
    # token's expansion lands inside the long one first, leaving a word its own pass can no longer
    # find. On this corpus both expansions happened to agree so nothing was corrupted, but that is
    # luck, not correctness, and the next book's ligature will not be as kind.
    for ch, cands in AMBIG.items():
        if ch not in s:
            continue

        def fix(m, ch=ch, cands=cands):
            tok = m.group(0)
            core = tok.lower().strip(".,;:!?\u201c\u201d\u2018\u2019()[]'\u2014-")
            for c in cands:
                if core.replace(ch, c) in vocab:
                    if stats is not None:
                        stats["resolved"] += 1
                    return tok.replace(ch, c)
            if stats is not None:
                stats["fallback"].append(tok)
            return tok.replace(ch, AMBIG_DEFAULT[ch])

        s = re.sub(r"\S*" + re.escape(ch) + r"\S*", fix, s)

    def join(m):
        a, gap, b = m.group(1), m.group(2), m.group(3)
        if (a + b).lower() in vocab:                     # resent\u00bb ment -> resentment
            if stats is not None:
                stats["joined"] += 1
            return a + b
        if (a + "-" + b).lower() in vocab:               # East~West stays hyphenated
            return a + "-" + b
        if stats is not None:
            stats["unjoined"].append(a + "/" + b)
        # No space meant no line break, so this was a real hyphen and not a wrap artefact --
        # "tea~bowl" is "tea-bowl", never "tea bowl". With a space, the words stay separate:
        # joining on a guess is how "Christa pher" would have become a word that does not exist.
        return a + ("-" if gap == "" else " ") + b

    return HYPH_TIGHT.sub(r"\1-\2", HYPH.sub(join, s))


# Characters that only ever turn up in an episode title as OCR sludge. This is a GATE, not a
# filter: a title containing none of these is left byte-for-byte alone. The first version of this
# rewrote 405 titles when only 47 were damaged -- it "cleaned" the real "Chapter 2 (Pages 17-56)"
# down to "Chapter 2" and ate the bullet page numbers in Seduction's contents. Losing real
# information to a repair is worse than the damage being repaired.
# "|" is deliberately absent: Right Concentration titles chapters "Chapter 1 | Quotes From Pages
# 19-20", and treating the pipe as sludge tripped the filter on all 40 and threw the range away.
TITLE_JUNK = re.compile(r"[{}\\^~\u00ab\u00bb\ue000-\uf8ff\x00-\x1f]")
# Inside a damaged title a token is kept only if it still reads as a word, a number, a page range
# or a roman numeral -- tested against the token with its edge punctuation already stripped, and
# the STRIPPED form is what gets kept, so "Law 3}" comes out as "Law 3" and not "Law 3}".
TITLE_OK = re.compile(r"^[A-Za-z\u00c0-\u00ff][A-Za-z\u00c0-\u00ff'\u2019.-]*$"
                      r"|^[0-9]{1,4}(?:[-\u2013][0-9]{1,4})?$|^[IVXLC]+$")
TITLE_EDGE = "{}()[]|\\^~\u00ab\u00bb$.,;:\u2019'\"\u201c\u201d"


def clean_title(t, index, unknown=None, vocab=None):
    """Strip OCR sludge out of an episode title, keeping whatever is genuinely readable.

    Titles are the most visible text in the library -- the reader header, the CONTINUE card and
    every search result print them -- so "1(}A.\u20183\\ Law 15" is worse than no title at all.
    Falls back to "Episode N" (which most of this corpus already uses) rather than to "", because
    the app renders ep.t with no fallback of its own.
    """
    c = clean(t, unknown)
    if not TITLE_JUNK.search(c):
        return c, c != t                      # undamaged: only the shared clean() applies
    # A word-shaped token is only kept if the library actually uses that word somewhere. Without
    # this, "Ptiuiy" and "CLIFION" survive as titles purely because they are spelled with letters.
    toks = []
    for tok in c.split():
        t2 = tok.strip(TITLE_EDGE)
        if not t2 or not TITLE_OK.match(t2):
            continue
        word = re.match(r"^[A-Za-zÀ-ÿ]", t2)
        if word and vocab is not None and t2.lower().strip("'’.-") not in vocab:
            continue
        toks.append(t2)
    out = re.sub(r"\s{2,}", " ", " ".join(toks)).strip(" .,-|\\")
    # A lone stray letter or number is not a title -- "K" and "8" are page furniture.
    if len(out) < 3 or not re.search(r"[A-Za-z\u00c0-\u00ff]{3}", out):
        return "Episode %d" % (index + 1), True
    return out, out != t


def build_vocab(data):
    """Dictionary of words this library already spells correctly, from clean() output.

    Two sightings, because a single sighting could itself be the damaged spelling -- and a word
    that appears only once cannot vouch for anything anyway.
    """
    seen = {}
    for b in data["books"]:
        for e in b["episodes"]:
            for p in e["p"]:
                for w in WORD.findall(clean(p)):
                    w = w.lower().strip("'")
                    if len(w) > 2:
                        seen[w] = seen.get(w, 0) + 1
    return set(w for w, n in seen.items() if n >= 2)


def selftest():
    """The collision that corrupted 3.55, pinned so it cannot come back.

    A paragraph holding both "o<esh>" and "o<esh>cially" resolves to "off" and "officially".
    The old str.replace(token, ...) rewrote every occurrence of the substring, so whichever token
    the set happened to yield first won: "o<esh>" -> "off" turned "o<esh>cially" into "offcially",
    and that word's own pass then had nothing left to match. It shipped that way.
    """
    esh = "ʃ"
    para = "was o%scially announced" % esh + " and o%s it went" % esh
    vocab = {"officially", "off", "announced", "went"}
    got = resolve(para, vocab)
    bad = [w for w in ("offcially", "oﬃcially") if w in got]
    if "officially" not in got or bad:
        return "expected 'officially', got: " + got.encode("ascii", "backslashreplace").decode()
    # and the short token must still expand on its own
    if " off it went" not in got:
        return "short token mis-expanded: " + got.encode("ascii", "backslashreplace").decode()
    return True


def main():
    if "--selftest" in sys.argv:
        r = selftest()
        print("selftest: " + ("ok" if r is True else "FAIL -- " + str(r)))
        sys.exit(0 if r is True else 1)
    fix = "--fix" in sys.argv
    data = json.load(open(BOOKS, encoding="utf-8"))
    unknown, total, empties = {}, 0, 0

    vocab = build_vocab(data)
    stats = {"resolved": 0, "joined": 0, "fallback": [], "unjoined": []}
    print("dictionary: %d words the library already spells correctly\n" % len(vocab))

    print("%-12s %8s %8s %8s %8s" % ("book", "paras", "damaged", "chars", "titles"))
    for b in data["books"]:
        dmg = chars = paras = titles = 0
        for i, e in enumerate(b["episodes"]):
            new = []
            for p in e["p"]:
                paras += 1
                c = resolve(clean(p, unknown), vocab, stats)
                if c != p:
                    dmg += 1
                    chars += (len(CTRL.findall(p)) + len(ANY_PUA.findall(p)) +
                              sum(p.count(k) for k in LIGATURES) +
                              sum(p.count(k) for k in MAP) + sum(p.count(k) for k in AMBIG) +
                              len(HYPH.findall(p)))
                if c:
                    new.append(c)
                else:
                    empties += 1          # paragraph was nothing but ad copy / control bytes
            e["p"] = new
            t, changed = clean_title(e.get("t", ""), i, unknown, vocab)
            if changed:
                titles += 1
            e["t"] = t
        total += chars
        if dmg or titles:
            print("%-12s %8d %8d %8d %8d" % (b["id"], paras, dmg, chars, titles))

    print("\nligature resolver: %d tokens matched a known word, %d fell back to the default"
          % (stats["resolved"], len(stats["fallback"])))
    if stats["fallback"]:
        # the console here is cp1252 and cannot print the damaged characters themselves
        print("   fallbacks: " + ", ".join(
            sorted(set(stats["fallback"]))[:10]).encode("ascii", "backslashreplace").decode())
    print("hyphen rejoin:     %d words put back together, %d left as two words"
          % (stats["joined"], len(stats["unjoined"])))

    # Report, don't repair. What is left is «/» sitting inside front-matter that OCR destroyed
    # outright ("«:ircmrIslumte,.r."); deleting the guillemet does not make that readable, so it
    # would be churn. Counted here so a later pass can tell leftovers from a regression.
    # It is also why «/»/~ are NEVER stripped wholesale: ~ is real punctuation in three books
    # ("~ Caesar" as an attribution, "Confucius ~ Rumi" as a separator) and sits inside a real
    # URL in Thinking Fast and Slow (princeton.edu/~kahneman/docs/). A blanket strip corrupts all
    # three. Only a guillemet or tilde with a letter on BOTH sides is treated as a hyphen.
    left = sum(p.count(c) for b in data["books"] for e in b["episodes"]
               for p in e["p"] for c in "«»")
    if left:
        print("unrepairable:      %d guillemet(s) left inside OCR sludge (reported, not touched)"
              % left)

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
