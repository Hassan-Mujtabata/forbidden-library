# CONTINUE — read this first, before anything else

This is the running handoff for The Vault. It survives session resets and context compaction.
**If you are a new session: read this file top to bottom, then start at the first unfinished job
in the queue. Do not re-plan. Do not re-investigate what is already recorded here.**

When you finish a job: tick it, add what you learned to "Hard rules", and commit this file.

---

## THE POINT (Hassan's words, do not drift from these)

- **Size does not matter. At all.** The library can be 500MB. He has said this from the start.
  Never propose compression, word budgets, reading-time targets, or "keep it short". If a
  previous session's note reasons about size, that note is wrong.
- **The Path is stairs, not a summary.** A 500-page book is intimidating because it is one block.
  Three lessons make that worse — you can see three lessons cannot cover 500 pages. Forty small
  steps that visibly DO cover it make it climbable. Small steps because each is ONE thing, never
  because content was cut.
- **Never trade understanding for brevity.** Longer is fine if it is clearer. The enemy is
  confusion, not length.
- **The Path's job:** make a huge book not feel like a huge deal, and tell you where to start.
  It must not duplicate the book. The book is the depth.
- **Figures add what a book physically cannot do** — motion, staged reveal, mechanism. That is
  why they exist. They are not decoration on a summary.
- **Library first, figures later.** Everything from every book, A to Z, organised — that is the
  critical path. Figures come after.

---

## CURRENT STATE (verified, 5 Aug 2026)

- **24 books**, 2,859,295 words, 3,522 chapters. The forbidden folder contains exactly those 24
  PDFs and nothing else.
- Text extraction: **93–99% of every book**. Not a problem. Do not "fix" it.
- Chapter names: **39 unnamed, 36 duplicated, 296 still numbered parts** (was 994 unnamed,
  631 duplicated, 893 numbered). The remainder are genuinely unheaded in the PDFs.
- Every lesson citation resolves to a real book (Attached and The Path of Purification were
  ingested 4 Aug; before that 21 citations pointed at nothing).
- Path: **87 nodes, 13 tracks, 22 with figures**. Backup at `tools/backup/graph.pre-rebuild.json`.
- App: 3.103 live.  `VV.all({stage:1})` passed 98/98 as of 3.102.
- **507 book figures live**, encrypted per book under `img/<id>.enc`.

---

## JOB QUEUE — do these in order

### [x] JOB 1 — Extract every image from all 24 books  — DONE, shipped 3.102
**507 figures extracted, 505 placed in their correct chapter, 2 orphans.** Tools:
`tools/bookimages.py` (extract + filter), `tools/packimages.py` (place + encrypt).
- Raw files land in `tools/bookimg/` — gitignored AND ship-blocked (publishers' images, plaintext).
- Shipped as one AES-GCM bundle per book at `img/<id>.enc`, fetched when that book is opened.
  NOT inside content.enc — not for size (size never matters here) but for LOAD ORDER: 34MB of
  photographs in the main payload means a spinner before the first word of text.
- Reader: `injectBookFigures()` in index.html decrypts, caches per session, and spreads the
  figures through the chapter.
- Chapters now carry `pg` (their printed page range) so a figure from page N lands in the chapter
  that discusses page N. Word-proportional estimation was REJECTED: pages holding a big figure
  carry little text, so a word-based guess drifts most exactly where the figures are.

### [x] JOB 2 — Give long chapters real names  — DONE, shipped 3.103
**Identical chapter names across the library: 631 → 36. Longest run: 171 → 3. Numbered parts:
893 → 296. Named chapters: 3,489 → 3,522.** Prose loss across the whole re-extract: 62
word-occurrences of 2,859,612 (0.002%), all publisher boilerplate.

Root cause was NOT the splitting. `is_heading()` only recognised ALL-CAPS and numbered headings,
so ordinary Title Case section titles were invisible — Laws of Human Nature has 190 chapters and
four were detected. `_titlecase_heading()` now catches them (58 real headings, 0 false positives
when tested on that book). Everything else was junk being adopted as a name, now refused:
- **the author's own byline** — "Viktor E. Frankl" named 19 consecutive chapters. Matched as a
  token SUBSET, because the metadata says "Viktor Frankl" and the title page says "Viktor E.
  Frankl" and a substring test misses that.
- **front matter** — "Also by Daniel Kahneman" named 14.
- **scanner noise** — "1. Rgrrr 2. Grgrrr 3. Grrrrr" named 16. Detected by internal case flips
  (`TIlE`, `MASQlJE`), letter-digit mashes (`BORC1IAS`) and 5+ consonant runs. NOT by vowel
  ratio — ordinary words are vowel-poor ("Stock" .20, "Self" .25) and a ratio gate deletes them.
- **margin epigraph attributions** — "Baltasar Gracian, 1601-1658". Comma plus a digit.
- **repeated lines** — a short line occurring verbatim 4+ times in a book is not the unique name
  of anything. This one rule took duplicates from 521 to 36.

`tools/nameparts.py` names what is left from the slice's own opening line, and KEEPS the numbered
form when the opening is a pure continuation with nothing honest to lift. Same rule as the quotes:
derived, never invented. A missing name is a smaller failure than a wrong one.

### [ ] JOB 3 — Relabel the quotes (small, do it any time)
`sources[].quote` is rendered as a quotation but the generator was **explicitly instructed** to
write "a faithful close paraphrase, NEVER a verbatim copyrighted sentence"
(`tools/gemini_pipeline.py` line ~74). So they are paraphrases wearing quote marks — the content
is honest, the framing is not.
- Simplest honest fix: stop presenting them as quotation. Do not go find real verbatim passages
  unless Hassan says so — that reverses a deliberate copyright decision.
- `tools/quotefix.py` exists and generates a review file if the other route is ever chosen.

### [ ] JOB 4 — The mini-path data model
Only after 1 and 2. Parent nodes owning child steps; the graph is flat tiers today. A long
chapter becomes a mini-path of real steps rather than "(1)…(12)". **Build the model before
generating any content**, or everything gets regenerated twice.

### [ ] JOB 5 — Figures on the steps
Last. Use the research protocol in `tools/figs_research/` — read `LOG.md` first, it records what
has already been rejected and why.

---

## DECISIONS ONLY HASSAN CAN MAKE

1. **Where images are stored** — inside `content.enc`, or separate encrypted files fetched per
   book. Separate is probably right (thousands of images; the app should not load all of them to
   read one book) but it changes how the reader works.
2. **Quotes** — relabel (recommended, free, honest immediately) or actually quote short passages
   with attribution (his copyright risk to accept, not ours to assume).

---

## HARD RULES (learned the expensive way — do not rediscover these)

- **Never propose reducing size.** See THE POINT. This has been re-litigated four times.
- **Verify before claiming.** Multiple "findings" this week were wrong on first measurement:
  a contrast check that ignored alpha and compared against white; a quote matcher whose absolute
  threshold could never be met by short quotes; an image count that mistook a page footer for 956
  figures. Always sanity-check a result that looks dramatic.
- **Check what references a file before deleting it.** Deleting the duplicate TMI PDF silently
  removed the whole book from the library, because `extract.py` pointed at the copy that was
  deleted. Caught only because a word count did not add up.
- **A re-extract must be diffed against the previous library before shipping.** Compare total
  words AND book count — a book vanishing shows as zero per-book drift if you only compare books
  present in both files.
- **A bare `except: continue` will hide a catastrophe.** The first image extractor reported THREE
  images for a 269-page book of photographs because fitz.Pixmap() throws on ordinary encodings
  (JPX, JBIG2, masked images) and the bare except swallowed every failure. Count failures, print
  them, never discard silently. Prefer doc.extract_image() and keep Pixmap as the fallback.
- **Images in a Separation colourspace are stored as INK, not brightness — they come out inverted.**
  Every photograph in What Every Body Is Saying extracted as a colour negative. THE TRAP: comparing
  extract_image() against fitz.Pixmap() shows NO difference, because both skip the conversion the
  page-draw applies. Only rendering the actual page reveals it. Invert when cs-name contains
  "Separation".
- **Unused figure components are suspects, not a menu.** Every one checked against its source
  encoded the wrong claim (`drift`, `pacer`, `curve`). 24 remain unaudited.
- **`c` is the scene item's component key.** A label passed as `c` overwrites the component name.
  Use `c3`. build.py catches it; it has happened twice.
- **ship.py owns the version bump.** Do not edit `APP_VER` by hand. Version goes 3.99 → 3.100.
  Patch note date must be today or it refuses.
- **`tools/figs_research/`, `tools/backup/`, `books.json`, `graph.json`, `key.txt` are
  ship-blocked.** Do not force-add them.
- **access.json is Hassan's config. Never touch it, never modify it.**
- **`extract.py` REBUILDS books.json from the PDFs, so it wipes `ep["img"]`.** Re-run
  `tools/packimages.py` after every re-extract or the library silently loses all 505 figures.
  Order is: `extract.py` → `nameparts.py` → `packimages.py` → `build.py`.
- **A rule that is good enough to distrust a line is not good enough to delete it.** The
  running-header rule first DROPPED matching blocks and cost 1,716 words of real prose. Rewritten
  to bar those lines from becoming names while leaving the text in the body: loss went to 62.
  Mark, don't delete.
- **A word-count drop is not proof of loss — diff the actual tokens.** #167 looked like it lost
  2,119 words. The missing tokens turned out to be 170 repetitions of one boilerplate title, the
  `(3)`/`(4)` part markers, and OCR garbage. Real prose loss was 20 occurrences of publisher
  boilerplate. Compare old body against new body+titles as a case-insensitive multiset and READ
  what is missing; the count alone will lie to you in both directions.
- **Safety copies must go in `tools/backup/`.** `books.json.pre*` in `tools/` is NOT gitignored;
  ship.py caught three of them staged for commit.

---

## HOW TO VERIFY ANYTHING

```
cd vault
python tools/build.py            # validates the graph, rebuilds content.enc
python tools/ship.py             # all gates, then commits and pushes
```
Browser: start the `vault` preview, then
`fetch("/tools/verify.js").then(r=>r.text()).then(s=>{eval(s);return VV.all({stage:1})})`
Copy verify.js to a fresh filename first — the pane serves stale tool files from cache.
