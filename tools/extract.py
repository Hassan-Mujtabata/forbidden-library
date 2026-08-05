# -*- coding: utf-8 -*-
"""Extract text from the vault PDFs into episode-structured books.json."""
import fitz, json, re, os, sys, subprocess, unicodedata
from collections import Counter
from cleantext import clean as repair_text

HERE = os.path.dirname(os.path.abspath(__file__))

ROOT = r"C:\Users\sands\OneDrive\Desktop\forbidden"
OUT = os.path.join(ROOT, "vault", "tools", "books.json")

BOOKS = [
    dict(id="laws48",    file="the+48+laws+of+power_2.pdf",
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
    dict(id="bliss",     file="Mindfulness, Bliss and Beyond.pdf",
         title="Mindfulness, Bliss and Beyond", author="Ajahn Brahm",
         wing="light", glyph="\U0001fab7", accent="#16a085"),
    dict(id="insight",   file="bp520s_Goldstein_Experience-of-Insight.pdf",
         title="The Experience of Insight", author="Joseph Goldstein",
         wing="light", glyph="\U0001f441", accent="#2980b9"),
    dict(id="beautiful", file="How To Have A Beautiful Mind.pdf",
         title="How to Have a Beautiful Mind", author="Edward de Bono",
         wing="light", glyph="\U0001f48e", accent="#9b59b6"),
    dict(id="tmi",       file="The Mind Illuminated - A Complete Meditation Guide Integrating Buddhist Wisdom and Brain Science ( PDFDrive.com ).pdf",
         title="The Mind Illuminated", author="Culadasa (John Yates)",
         wing="light", glyph="\U0001f319", accent="#34495e"),
    dict(id="rightconc", file="right concentration a practical guide to the jhanas by leigh brasington.pdf",
         title="Right Concentration", author="Leigh Brasington",
         wing="light", glyph="\U0001f506", accent="#f39c12"),
    dict(id="kahneman", file="Daniel Kahneman-Thinking, Fast and Slow  .pdf",
         title="Thinking, Fast and Slow", author="Daniel Kahneman",
         wing="light", glyph="✏️", accent="#c9a227"),
    dict(id="atomic", file="Atomic habits ( PDFDrive ).pdf",
         title="Atomic Habits", author="James Clear",
         wing="light", glyph="⚛️", accent="#e08a3c"),
    dict(id="bodyscore", file="The-Body-Keeps-the-Score-PDF.pdf",
         title="The Body Keeps the Score", author="Bessel van der Kolk",
         wing="light", glyph="\U0001fac0", accent="#b0413e"),
    dict(id="meditations", file="Marcus-Aurelius-Meditations.pdf",
         title="Meditations", author="Marcus Aurelius",
         wing="light", glyph="\U0001f3db️", accent="#8a94a6"),
    dict(id="humannature", file="The Laws of Human Nature.pdf",
         title="The Laws of Human Nature", author="Robert Greene",
         wing="shadow", glyph="\U0001f989", accent="#8e6f47"),
    dict(id="navarro", file="what-everybody-is-saying.pdf",
         title="What Everybody Is Saying", author="Joe Navarro",
         wing="shadow", glyph="\U0001f440", accent="#5d6d7e"),
    dict(id="winfriends", file="31-10-2020-083612How to Win Friends and Influence People - Dale Carnegie.pdf",
         title="How to Win Friends and Influence People", author="Dale Carnegie",
         wing="shadow", glyph="\U0001f91d", accent="#4a90b8"),
    dict(id="likeswitch", file="The Like Switch_ An Ex-FBI Agen - Schafer_ Jack_ Karlins_ Marvin.pdf",
         title="The Like Switch", author="Jack Schafer",
         wing="shadow", glyph="\U0001f60a", accent="#e6844d"),
    dict(id="meaning", file="632ecf70b27a5-man-s-search-for-meaning.pdf",
         title="Man's Search for Meaning", author="Viktor Frankl",
         wing="light", glyph="\U0001f54a️", accent="#7f8fa6"),
    # #164: both were cited by authored lessons but were never in the library, so those
    # citations could not cross-link and their quotes could not be checked against anything.
    dict(id="attached",  file='Amir_Levine,_Rachel_Heller-Attached__The_New_Science_of_Adult_Attachment_and_How_It_Can_Help_You_Find_–_and_Keep_–_Love__-Penguin_Group_USA_(2010)[1].pdf',
         title="Attached", author="Amir Levine & Rachel Heller",
         wing="light", glyph="💞", accent="#e08a3c"),
    dict(id="purific",   file='PathofPurification2011.pdf',
         title="The Path of Purification", author="Bhadantacariya Buddhaghosa",
         wing="light", glyph="👁", accent="#2980b9"),
]

# repair common Pali terms that lose their diacritics in extraction
PALI = [
    (r"\bjh[aā]?\s?nas\b", "jhānas"), (r"\bjh[aā]?\s?na\b", "jhāna"),
    (r"\bsam[aā]dhi\b", "samādhi"), (r"\bnibb[aā]na\b", "nibbāna"),
    (r"\bvipassan[aā]\b", "vipassanā"), (r"\b[aā]n[aā]p[aā]na\b", "ānāpāna"),
    (r"\bmett[aā]\b", "mettā"), (r"\bsati\b", "sati"), (r"\bsukha\b", "sukha"),
]

HEAD_RE = re.compile(
    r"^(law|chapter|part|tactic|rule|key|stage|section|book|step|principle|weapon|interlude|appendix)"
    r"[\s:#]*([0-9ivxlcIVXLC]+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)?\b",
    re.IGNORECASE)


def clean(t):
    # Repair extraction damage FIRST, while the raw shape is still intact: mis-decoded UTF-16
    # runs, private-use ligatures that eat the "Th" off a word, control bytes, and ﬁ/ﬂ ligatures
    # that silently defeat search. 43,000 of these reached the shipped library before anyone
    # noticed, because they are invisible in a diff and look like a font problem on screen.
    # repair_text keeps \n and \t, so the line-joining below still works.
    t = repair_text(t)
    t = t.replace("­", "")
    t = re.sub(r"-\n(?=[a-z])", "", t)
    t = re.sub(r"\s*\n\s*", " ", t)
    t = re.sub(r"\s{2,}", " ", t)
    for pat, rep in PALI:
        t = re.sub(pat, rep, t, flags=re.IGNORECASE)
    return t.strip()


_SMALL = {"a", "an", "the", "and", "or", "of", "in", "on", "at", "to", "for", "from", "by",
          "with", "as", "is", "it", "its", "that", "this"}


# #167: the author's own name, set per book by extract(). A Title Case rule accepts a byline as
# readily as a section title, and a byline that becomes a chapter name does not stay local: it is
# carried across every following split, so ONE stray match renames a whole book. "Viktor E.
# Frankl" titled 19 consecutive parts of Man's Search for Meaning and "Also by Daniel Kahneman"
# titled 14 of Thinking, Fast and Slow. Matching against the known author is exact where a
# general "looks like a person's name" heuristic would eat real headings.
_CUR_AUTHOR = ""
_AUTHOR_VARIANTS = []
# normalised running-header lines for the book being extracted; barred as chapter names
_RUNNING_HEADERS = set()
_NORM = lambda s: re.sub(r"\d+", "#", s.strip().lower())[:48]
_FRONTMATTER = re.compile(
    r"^(also by|by the same author|about the author|other books|praise for|contents|"
    r"acknowledgment|acknowledgement|dedication|translated by|copyright)\b", re.IGNORECASE)


def _norm_toks(s):
    return [t for t in re.sub(r"[^a-z ]", " ", s.lower()).split() if len(t) >= 3]


def _author_variants(author):
    """Token sets to match a byline against, one per credited person.

    Substring matching is not enough: the metadata says "Viktor Frankl" and the title page says
    "Viktor E. Frankl", so the middle initial breaks the match and 19 chapters kept the byline.
    Matching the author's tokens as a SUBSET tolerates initials, honorifics and reordering.
    "Various" is a placeholder in this corpus, not a name, so it is never matched on.
    """
    out = []
    for part in re.split(r"&|\band\b", author or ""):
        toks = [t for t in _norm_toks(part) if t != "various"]
        if toks:
            out.append(toks)
    return out


def _is_byline(p):
    if _FRONTMATTER.match(p.strip()):
        return True
    line = _norm_toks(p)
    if not line:
        return False
    seen = set(line)
    for toks in _AUTHOR_VARIANTS:
        # subset match, and the line must be little more than the name itself -- otherwise a real
        # heading that happens to mention the author would be thrown away
        if all(t in seen for t in toks) and len(line) <= len(toks) + 3:
            return True
    return False


def _titlecase_heading(p):
    """#167: Title Case section headings.

    is_heading only ever recognised ALL-CAPS lines and numbered patterns, so ordinary Title Case
    headings were invisible to it. The Laws of Human Nature has 190 chapters and only FOUR were
    detected — "Confirmation Bias", "The Blame Bias", "Rising Pressure" and every other section
    title fell through, collapsing the book into one 171-part block of identical names.
    Tested on that book before adoption: 58 real headings caught, 0 false positives across 1,072
    body paragraphs. The comma test is what excludes epigraph attributions
    ("—Fyodor Dostoyevsky, A Raw Youth"), and the initial-capital test excludes quotes and dashes.
    """
    if len(p) > 72 or len(p) < 6:
        return False
    if not p[0].isupper():
        return False
    if p.rstrip()[-1] in ".,;:?!":
        return False
    if "," in p:
        return False
    w = p.split()
    if not (2 <= len(w) <= 8):
        return False
    big = [x for x in w if len(x) >= 4 and x.lower() not in _SMALL]
    if not big:
        return False
    return sum(1 for x in big if x[0].isupper()) / len(big) >= 0.75


def _is_vowel(c):
    # accent-aware: "jhāna" and "samādhi" are words, not noise
    return unicodedata.normalize("NFD", c)[0].lower() in "aeiouy"


def _letterdigit(t):
    """A word with a digit wedged inside it -- "BORC1IAS", "i89". Never a real heading word."""
    t = t.strip(".,;:!?()[]\"'“”’—–")
    return bool(re.search(r"[A-Za-z]\d|\d[A-Za-z]", t))


def _garbled_token(t):
    # hyphenated compounds are judged part by part, or "Stock-Picking" reads as one long
    # vowel-poor run and a real heading gets thrown away
    return any(_garbled_part(x) for x in re.split(r"[-–—]", t) if x)


def _garbled_part(t):
    t = t.strip(".,;:!?()[]\"'“”’—–")
    letters = [c for c in t if c.isalpha()]
    if len(letters) < 3:
        return False                                   # too short to judge; roman numerals etc.
    if any(c.isdigit() for c in t):
        return True
    # A case flip inside one word is the scanner confusing I/l/J. Checked per hyphen-part, so
    # "Stock-Picking" is two ordinary words and not a flip. Only flagged when the part is mostly
    # capitals -- an initial capital followed by lowercase is just a normal word.
    ups = "".join("U" if c.isupper() else "l" for c in letters)
    if ups.count("U") >= 2 and "l" in ups[1:]:
        return True                                    # "TIlE", "MASQlJE", "COLOREIl"
    if not any(_is_vowel(c) for c in letters):
        return True                                    # "Rgrrr", "Grgrrr"
    # 5+ consonants in a row. Deliberately NOT a vowel-ratio test: ordinary English words are
    # vowel-poor ("Stock" .20, "Self" .25, "Strength" .12) and a ratio gate throws them away.
    run = best = 0
    for c in letters:
        run = 0 if _is_vowel(c) else run + 1
        best = max(best, run)
    return best >= 5                                   # "Xuzonlcjm"


def _looks_garbled(p):
    """True when a heading candidate is mostly scan noise rather than words.

    #167: Thinking, Fast and Slow renders its part-title pages in a decorative font that OCRs to
    "1. Rgrrr 2. Grgrrr 3. Grrrrr" and "Xuzonlcjm Tapcerhob"; 48 Laws produces "TIIE BORC1IAS,
    IVAN CUHJLAS". cleantext has a junk-title gate, but it runs AFTER extraction and only sees
    the finished title -- by then the garbage has already been adopted as a chapter name and, via
    head_level qualification, stamped onto every section beneath it. Rejecting the candidate here
    means it never becomes a name in the first place; the text itself stays in the body either
    way, so nothing is lost by refusing to use it as a label.
    """
    toks = [t for t in p.split() if any(c.isalpha() for c in t)]
    if not toks:
        return False
    if any(_letterdigit(t) for t in p.split()):
        return True
    # An epigraph attribution from the margin: "IDRIES SHAH, 1968", "Baltasar Gracian, 1601-1658".
    # 48 Laws sets these in caps, so they reach the ALL-CAPS branch and become chapter names for
    # the fable beside them. A real chapter heading does not pair a comma with a date.
    if "," in p and re.search(r"\d", p):
        return True
    bad = sum(_garbled_token(t) for t in toks)
    if bad / len(toks) >= 0.33:   # one bad word in three is already scan noise
        return True
    # a page-header artefact like "Law 2 4 187": a keyword and a scatter of numbers
    nums = sum(1 for t in p.split() if t.strip(".,:").isdigit())
    return nums >= 3


def head_level(p):
    """2 = chapter-level heading, 1 = section-level heading.

    #167: some books reuse the SAME section name in every chapter -- The Laws of Human Nature has
    a "Keys to Human Nature" section in all eighteen -- so a section name alone is not a usable
    chapter title, however correctly it was detected. Section headings get qualified by the
    chapter they sit under; chapter headings stand alone.
    """
    # HEAD_RE's keyword list includes "key", so "Keys to Power" -- a section that recurs in every
    # one of the 48 laws -- matched as chapter-level and became its own qualifier, leaving 25
    # chapters with that identical name. Chapter level requires the NUMBER too ("Law 24",
    # "CHAPTER XIV"); a bare keyword is a section, and gets qualified by the law it sits under.
    m = HEAD_RE.match(p)
    if m and m.group(2) and len(p.split()) <= 12:
        return 2
    # Caps alone DO count as chapter-level. Requiring a keyword as well was tried and reverted:
    # it pushed duplicate names up (552 -> 589) because it demoted real caps-set chapter titles.
    letters = [c for c in p if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.82 and len(letters) >= 4:
        return 2
    return 1


def is_heading(p):
    if len(p) > 72 or len(p) < 3:
        return False
    if _is_byline(p):                      # guards the ALL-CAPS branch too ("VIKTOR E. FRANKL")
        return False
    if _NORM(p) in _RUNNING_HEADERS:
        return False
    if _looks_garbled(p):
        return False
    if p.endswith((".", ",", ";", "?", "!")) and not HEAD_RE.match(p):
        return False
    if HEAD_RE.match(p) and len(p.split()) <= 12:
        return True
    letters = [c for c in p if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.82 and len(letters) >= 4:
        return True
    return _titlecase_heading(p)


def extract(meta):
    global _CUR_AUTHOR, _AUTHOR_VARIANTS
    _CUR_AUTHOR = meta.get("author", "")
    _AUTHOR_VARIANTS = _author_variants(_CUR_AUTHOR)
    path = os.path.join(ROOT, meta["file"])
    doc = fitz.open(path)
    npages = len(doc)
    # #166: blocks carry their PAGE so extracted figures can be placed in the right chapter.
    # Word-proportional estimation was rejected: pages holding a big figure carry little text, so
    # a word-based guess drifts most precisely where the figures are.
    blocks = []
    for pno, page in enumerate(doc, 1):
        for b in page.get_text("blocks"):
            if b[6] != 0:
                continue
            t = b[4].strip()
            if t:
                blocks.append((pno, t))
    doc.close()

    # strip repeated headers/footers
    norm = lambda s: re.sub(r"\d+", "#", s.strip().lower())[:48]
    freq = Counter(norm(t) for _, t in blocks if len(t) < 90)
    thresh = max(4, npages // 5)
    blocks = [(pg, t) for pg, t in blocks if not (len(t) < 90 and freq[norm(t)] >= thresh)]

    # strip bare page numbers / roman numerals
    blocks = [(pg, t) for pg, t in blocks if not re.fullmatch(r"[\divxlc\s.\-–•|]+", t.strip().lower())]
    # strip front-matter boilerplate
    junk = re.compile(r"copyright|isbn|library of congress|all rights reserved|penguin\s|viking penguin"
                      r"|z-lib|pdf room|pdfdrive|www\.|http|printed in the|first published|publishing division",
                      re.IGNORECASE)
    blocks = [(pg, t) for pg, t in blocks if not (len(t) < 400 and junk.search(t))]


    paras = [(pg, c) for pg, c in ((pg, clean(t)) for pg, t in blocks) if c]

    # some PDFs emit one block per printed line; merge fragments into real paragraphs
    avg = sum(len(p.split()) for _, p in paras) / max(1, len(paras))
    if avg < 25:
        joined = []
        for pg, p in paras:
            if (joined and not is_heading(p) and not is_heading(joined[-1][1])
                    and len(joined[-1][1]) < 900
                    and joined[-1][1][-1] not in '.!?:;"”’'):
                joined[-1] = (joined[-1][0], joined[-1][1] + " " + p)
            else:
                joined.append((pg, p))
        paras = joined

    # #167: bar repeated lines from becoming chapter names.
    #
    # A book with several parts has a DIFFERENT running header per part, so each appears on only
    # its share of the pages and slips under the npages//5 threshold used above. Worse, in The
    # Path of Purification the header is not a block at all -- the line-join step above welds
    # "PATH OF PURIFICATION" to "Part 3: Understanding (Paññá)", so it exists only AFTER joining
    # and a raw-block detector cannot see it. It ended up naming 41 chapters.
    #
    # So the count is taken here, on the joined text, and the test is simply: a short line that
    # occurs verbatim four or more times is not the unique name of anything. That also catches
    # genuinely recurring section names ("KEYS TO POWER", once per law) which are equally useless
    # as chapter names.
    #
    # They are BARRED FROM BEING NAMES, never deleted. An earlier version dropped these blocks
    # outright and cost 1,716 words of real prose: the rule is good enough to distrust a line as
    # a title, nowhere near good enough to destroy text with.
    global _RUNNING_HEADERS
    rep = Counter(_NORM(t) for _, t in paras if len(t) < 90)
    _RUNNING_HEADERS = {k for k, v in rep.items() if v >= 4}

    episodes = []
    cur_title, cur_paras, words = None, [], 0
    # #165: a chapter longer than the 1400-word budget gets split, and every slice after the first
    # had no heading of its own — so it fell through to "Episode 137". That is why 994 chapters
    # across the library were unnamed and the reader was unnavigable: Laws of Human Nature was 97%
    # anonymous purely because its chapters are long. Carry the real chapter name across the split
    # and number the parts instead.
    last_head, part = None, 0
    # #167: the most recent CHAPTER-level heading, used to qualify section-level ones.
    cur_major, cur_level = None, 0

    cur_pages = []

    def flush():
        nonlocal cur_title, cur_paras, words, last_head, part, cur_pages, cur_level
        if cur_paras:
            if cur_title:
                head = cur_title.title() if cur_title.isupper() else cur_title
                if (cur_level == 1 and cur_major
                        and head.lower() not in cur_major.lower()
                        and cur_major.lower() not in head.lower()
                        and len(cur_major) + len(head) <= 88):
                    head = f"{cur_major}: {head}"
                last_head, part = head, 1
                title = head
            elif last_head:
                part += 1
                title = f"{last_head} ({part})"
            else:
                title = f"Episode {len(episodes) + 1}"
            ep = {"t": title, "p": cur_paras}
            # #166: the printed page range this chapter came from, so a figure extracted from
            # page N can be shown in the chapter that actually discusses it.
            if cur_pages:
                ep["pg"] = [min(cur_pages), max(cur_pages)]
            episodes.append(ep)
        cur_title, cur_paras, words, cur_pages, cur_level = None, [], 0, [], 0

    def take_head(p):
        nonlocal cur_title, cur_level, cur_major
        cur_title, cur_level = p, head_level(p)
        if cur_level == 2:
            cur_major = p.title() if p.isupper() else p

    for pg, p in paras:
        if is_heading(p):
            if words > 150:
                flush()
                take_head(p)
            elif cur_title is None and not cur_paras:
                take_head(p)
            else:
                cur_paras.append(p); cur_pages.append(pg)
        else:
            cur_paras.append(p); cur_pages.append(pg)
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

    # #144: THIS SCRIPT REWRITES books.json FROM THE PDFs. extract() applies only the
    # per-paragraph repairs (cleantext.clean); everything added in 3.55 and 3.57 --
    # resolving the ambiguous ligatures, rejoining line-break hyphens, letter-level OCR
    # correction, the junk-title gate -- needs a vocabulary built from the WHOLE library and so
    # cannot run per paragraph. Without this call a re-extract silently throws all of it away and
    # the books quietly regress to "the ɹrst law" and "a Iyrrhir victory".
    # Shelling out to the real entry point rather than reimplementing it, so there is exactly one
    # copy of the repair logic and it is the one with the pinned regression test.
    print("\nrunning the corpus-wide repairs (cleantext --fix)…")
    r = subprocess.run([sys.executable, os.path.join(HERE, "cleantext.py"), "--fix"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stdout.write(r.stdout or "")
    if r.returncode != 0:
        sys.stderr.write(r.stderr or "")
        raise SystemExit("cleantext failed — books.json is EXTRACTED BUT UNREPAIRED. Fix and "
                         "re-run `python tools/cleantext.py --fix` before build.py.")
    print("next: python tools/build.py")


if __name__ == "__main__":
    main()
