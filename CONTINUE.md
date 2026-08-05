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

- **24 books**, 2,859,612 words, 3,489 chapters. The forbidden folder contains exactly those 24
  PDFs and nothing else.
- Text extraction: **93–99% of every book**. Not a problem. Do not "fix" it.
- Chapter names: **99 unnamed, down from 994**. The rest are genuinely unheaded in the PDFs.
- Every lesson citation resolves to a real book (Attached and The Path of Purification were
  ingested 4 Aug; before that 21 citations pointed at nothing).
- Path: **87 nodes, 13 tracks, 22 with figures**. Backup at `tools/backup/graph.pre-rebuild.json`.
- App: 3.102 live. `VV.all({stage:1})` passes 98/98.
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

### [ ] JOB 2 — Give long chapters real names
A chapter over ~1400 words is split into slices. Slices currently inherit the chapter name with a
number: `Step Three: Strategies Toward Bringing Out the Rational (12)`. Twelve identical names is
still one undifferentiated block — Hassan called this "a mess" and he is right.
- Each slice needs its own name, derived from its own content.
- Do NOT invent a name that overstates what the slice contains. Same rule as the quotes.
- Done when: no book has runs of identically-named parts.

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
