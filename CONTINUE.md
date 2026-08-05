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
- **THE ONE RULE ABOVE ALL THE OTHERS, in his words:** "UNDERSTANDING IS THE MAIN POINT.
  ANYTHING THAT MAKES UNDERSTANDING EASIER U CAN ADD IT. ANYTHING MAKES IT HARDER DONT EVEN
  BRING IT CLOSE — like u cut the text before, or remove images, and sumerized idea and what
  not." Every drift this session was a breach of this wearing a different disguise: cutting
  text, summarising the idea, treating his reading capacity as a quota to fill, then trimming
  because volume was misread as the complaint. Before adding anything, ask only: does this make
  it easier to understand? If yes it goes in at any length or size. If no it does not get built.
- **LENGTH FOLLOWS THE IDEA. IT IS A CEILING, NOT A QUOTA.** He can sit 10-30 minutes with a
  single stage if the idea warrants it — "u can put 1 lesson in there if needed, not squeeze
  there 2 of them to fill time, its all about understanding." So: ONE idea per lesson, carried
  to whatever length that idea actually needs. Never pad to reach the ceiling and never weld two
  ideas together to use up the room. A six-minute lesson that finishes its idea is correct; a
  thirty-minute lesson containing two ideas is not.
- **LONG IS NOT THE PROBLEM. LEAVING HIM TO WORK IT OUT IS.** Hassan, verbatim: "if text is
  broken by lessons and is easier to understand more then even the book id rather have that —
  read for 5 hrs then read 2 hrs and spend a day figuring it out on my own how concept works
  after understanding it." He will happily read MORE than the book if the reading does the work.
  A lesson that is shorter than the book but leaves him reconstructing the mechanism has cost
  him a day and saved him three hours. That is the trade he is refusing.
  This has now been got wrong in BOTH directions: first by writing summaries, then by assuming
  the complaint was volume and trimming. It is neither. Work the mechanism all the way through,
  at whatever length that takes, and leave nothing for him to reverse-engineer.
- **UNDERSTANDING IS NOT THE GOAL. APPLYING IT IS.** Hassan's words: "if I read books I should
  not just understand concept I should be easily apply it in real life — I been understanding it
  for years, that's why the figures are there for." He does not need a chapter explained. He
  needs to be able to CATCH the thing happening and DO something. A lesson that recounts what the
  author said is a summary no matter how well written, and it has now been written twice by
  mistake. Build each lesson around: the TELL (what it feels like from the inside, in the live
  moment), WHERE it will actually happen to him, and the MOVE (one thing small enough to
  actually do). The author's claim is the floor, not the lesson.
- **Figures are FOR the applying.** They exist to show the mechanism in motion so it can be
  recognised in real life — that is why he asked for them. They are not illustrations glued onto
  an explanation.
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
- Path: **101 nodes, 16 tracks, 23 with figures**. Track O fully deepened (3.112);
  track P = Meditations (3.113), covered but at ~600 words/lesson — NEEDS DEEPENING to the
  track-O standard, it carries the four elements but compactly. Track N = first mini-path (Laws of
  Human Nature). Track O = Reading the Body (Navarro), 4 lessons, one `pattern` figure. Backup at `tools/backup/graph.pre-rebuild.json`.
- App: **3.109 live and pushed.** The token at `C:\Users\sands\.secrets\github_token.txt` is
  still missing, so ship.py's push is intermittent — when it fails, Hassan runs
  `python -c "import sys; sys.path.insert(0,'tools'); import ship; ship.push()"` himself.
- `/reset.html` clears a wedged service worker without touching progress or the key (#171).
- `VV.all({stage:1})` passed 98/98 as of 3.102.
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

### [x] JOB 3 — Relabel the quotes  — DONE, shipped 3.104
The quotation marks are gone and every authored passage is labelled "in the book's sense, not its
words". The content was always honest; the framing was not.

**The app had been labelling only SOME of them, and its rule was wrong.** `aiTrack` assumed tracks
A–F carried real quotes and only marked G+ as paraphrase. Tested instead of trusted: all **143**
source passages searched against the full text of the 24 books, **zero appear verbatim, A–F
included**. The matcher was positive-controlled first (24 real book sentences, 24/24 found) and
negative-controlled, because an always-fails matcher would have produced exactly the same 0/143.

**Forged lessons keep their quotation marks** — `forgeLesson()` builds sources from
`passages[0].text`, lifted straight out of the book, so those really are verbatim. A blanket
relabel would have been a new lie in the other direction.

Not done, and deliberately: no hunt for real verbatim passages. That reverses a deliberate
copyright decision and is Hassan's to make. `tools/quotefix.py` still generates the review file
if he ever chooses it.

### [x] JOB 4 — The mini-path data model  — DONE, shipped 3.105
**The model only. No lesson was split into steps — that is JOB 5.** It ships inert: with no
`parent` in the data the rendering is byte-identical to 3.104, so nothing moved on screen.

**THE SPEC — build content against this, do not redesign it.**

A node carrying `parent: "<nodeId>"` is a STEP of that node, which makes that node a mini-path.

```jsonc
{"id":"e4",    "track":"E", "tier":3, "prereq":["e3"], "title":"...", ...}      // the mini-path
{"id":"e4s1",  "track":"E", "tier":1, "prereq":[],      "parent":"e4", ...}     // step 1
{"id":"e4s2",  "track":"E", "tier":2, "prereq":["e4s1"],"parent":"e4", ...}     // step 2
{"id":"e5",    "track":"E", "tier":4, "prereq":["e4"],  ...}                    // waits on the whole mini-path
```

- **The link lives on the CHILD**, like `track` does. There is no `steps:[]` on the parent, so a
  step list can never disagree with the steps.
- **`tier` is the step order** within the parent. Ties are rejected — a tie means the reader gets
  an arbitrary sequence.
- **One level deep. Enforced.** A step may not own steps. A tree is a worse version of the problem
  mini-paths solve: "open this, to find this, to find the actual lesson."
- **The parent is the main-path node that introduces the idea; the steps are the small ones.**
  The parent keeps its own `bridge`/`quiz`/`apply` — opening it opens that intro.
- **Parent completion is DERIVED, never stored:** done when every step is done. So a step must
  NOT list its parent in `prereq` — the parent cannot finish until the step does, and that
  deadlock is silent. build.py rejects it.
- **A step's availability follows its parent's AVAILABILITY, not its completion.**
- **Progress counts leaves.** A container is not counted alongside its own steps.
- **Steps are always visible, never behind a toggle.** Seeing that eight short steps cover the
  whole thing is the entire point; hiding them rebuilds the wall.

`tools/minipath_test.py` runs the REAL functions lifted out of index.html against a synthetic
graph — 15 assertions, wired into `ship.py` as a gate, and mutation-tested three ways (breaking
derivation, breaking parent-gating, counting containers — all three caught). build.py rejects
seven malformed shapes; that was tested both directions too.

### [ ] JOB 5 — Build the mini-paths, then the figures
**Step 1 (pick) done. First mini-path SHIPPED in 3.109. Four uncovered books remain.**

**READ THE TWO NEW LINES IN THE POINT BEFORE WRITING ANY LESSON.** The first draft of the
Irrationality mini-path was a summary of Greene's chapter and was thrown away unshipped. Hassan
has now corrected this twice. He does not need concepts explained — he has understood them for
years. Each lesson is three things and nothing else:
  * **THE TELL** — the sentence he actually hears in his own head when it runs, first person.
  * **WHERE** — the specific place it will catch *him*, not a generic example.
  * **THE MOVE** — one action small enough to do in under a minute.
The author's claim is the floor and lives in `sources`. Quizzes test RECOGNITION IN A SITUATION,
never recall of what the author wrote — naming the bias is the thing he already has.

**DONE — track N, The Laws of Human Nature** (`tools/path_irrationality.py`, hand-authored):
`n1 The Law of Irrationality` on the main path with six steps beneath it (`n1s1`..`n1s6`) —
confirmation, conviction, appearance, group, blame, superiority. Note there are SIX biases, not
five: the extractor folded "The Blame Bias" into the Group Bias chapter, so working from chapter
titles alone loses one. Read the episode TEXT, never just the titles.

**PHASE ORDER — Hassan, verbatim: "once u finish library this part then u can start adding
small notes here and there for making understanding easier and figures animated or whatever
anything u can think of that would make understanding easier."**
So: COVER EVERY BOOK FIRST. Notes, animated figures and any other comprehension aid come after
coverage is complete — they are not a reason to leave a book uncovered, and coverage is not a
reason to ship a lesson that does not do its working.

**DEPTH STANDARD — set by `tools/deepen.py` (o1) and `tools/deepen2.py` (o2-o4).** Every lesson
must carry: the mechanism down to WHY it must be so; one concrete case run start to finish; the
obvious objection raised and answered; and the edge where the idea stops holding. A lesson
missing any of those is leaving homework. Length follows the idea — o1 needed 1,519 words,
o2-o4 needed ~850 each. Do not pad to a budget and do not merge two ideas to fill one.

**STILL UNCOVERED (no lesson, no track, no mention):**
The Body Keeps the Score (172,208w) · How to Win Friends (79,675w).
(What Everybody Is Saying -> track O in 3.110. Meditations -> track P in 3.113.)

**COVERED BUT STILL AT SUMMARY DEPTH — needs the same treatment as track O:**
Track N (Laws of Human Nature), all 7 nodes, still ~200-400 words each.
Then the thin ratios: Seduction (240,398w / 3 lessons), Deception, Dark Psychology, Purification,
48 Laws.

**FIGURES + SMALL NOTES ARE AUTHORISED AND OWED — Hassan, 5 Aug: "u can add figures ... for
dark wing and small notes (AKA MAKING UNDERSTANDING EASIER)."** Phase order still stands
(coverage first), but figures and notes are explicitly wanted and are not decoration — they are
the comprehension aid he has asked for repeatedly: "that's why the figures are there for."

- **DARK WING first** — the `wing:"shadow"` books: 48 Laws, The Art of Seduction, Dark
  Psychology 3-in-1, 30 Covert Tactics, The Art of Deception, Manipulation, Influence, The Laws
  of Human Nature, What Everybody Is Saying, How to Win Friends, The Like Switch.
- **Build figures via `tools/figs_research/` — read `LOG.md` FIRST.** It records which figures
  were built and then killed for encoding the wrong claim. Do NOT write specs from intuition.
- **Reuse an existing component whose research is already done where one fits.** Track O's
  `pattern` figure is the model: it came with Bond & DePaulo (2006) — 206 studies, 24,483
  observers, 54% accuracy on one encounter and 47% on lies — behind it, and Navarro's baseline
  rule is the same finding from another direction. That is a correct reuse. Picking a component
  because it looks nice is the failure this rule exists to stop.
- **`c` is the component key — a label passed as `c` overwrites the component name. Use `c3`.**
- Caption cap 220 chars, `feel` line cap 200, max 5 stages, `place` must index into `bridge`.
  build.py enforces all of these; the 200-char `feel` cap already caught one overrun.
- **Small notes**: short clarifying asides inside a lesson. Same test as everything else — only
  if they make it easier. A note that adds a caveat nobody asked about makes it harder.

`tools/gemini_pipeline.py:merge_minipaths()` lays a generated track out as mini-paths
automatically (tested against build.validate in four shapes) — but Hassan asked for lessons to be
**written directly, not generated**: "use gemini for help do the task urself for best quality."

---|---|---|---|---|
| The Laws of Human Nature | 270,396 | 232 | **0** | — |
| The Body Keeps the Score | 172,208 | 220 | **0** | — |
| How to Win Friends and Influence People | 79,675 | 70 | **0** | — |
| Meditations | 72,513 | 56 | **0** | — |
| What Everybody Is Saying | 69,836 | 156 | **0** | — |
| The Art of Seduction | 240,398 | 312 | 3 | 80,132 |
| The Art of Deception | 118,049 | 97 | 2 | 59,024 |
| Dark Psychology: 3 Books in 1 | 86,782 | 87 | 2 | 43,391 |
| The Path of Purification | 421,300 | 416 | 12 | 35,108 |
| The 48 Laws of Power | 237,215 | 270 | 9 | 26,357 |

**FIVE BOOKS ARE NOT ON THE PATH AT ALL** — no track, no lesson, not even a mention in any
lesson's text. Verified before believing it: all 19 citation strings in graph.json match a
library title exactly, so this is a real absence and not a title-matching artefact. Note the old
CURRENT STATE line "every lesson citation resolves to a real book" is true but says nothing about
the reverse, which is where the hole was.

**ORDER OF WORK**
1. The five uncovered books first — a book with no lessons is the worst version of "the library
   makes it harder", because the Path gives no way in at all.
2. Then the worst ratios: Seduction (80k words per lesson), Deception, Dark Psychology,
   Purification, 48 Laws.
3. Each large book becomes mini-paths per the JOB 4 spec: a main-path node introducing the idea,
   with the small steps beneath it. Each step is ONE thing. Small because it is one idea, NEVER
   because content was cut — re-read THE POINT first.
4. Only then figures on the steps, via `tools/figs_research/` — read `LOG.md` first, it records
   what has already been rejected and why.

Generation runs through the Gemini pipeline. **Gemini may add book content only, never app code.**

---

## DECISIONS ONLY HASSAN CAN MAKE

1. **Where images are stored** — inside `content.enc`, or separate encrypted files fetched per
   book. Separate is probably right (thousands of images; the app should not load all of them to
   read one book) but it changes how the reader works.
2. **Quotes** — RESOLVED by doing the recommended half (relabelled, 3.104). Still open only if he
   wants the other route: replacing the paraphrases with real short verbatim passages plus
   attribution. That is his copyright risk to accept, not ours to assume. Do not start it unasked.

---

## HOW TO ACTUALLY MAKE IT EASIER — my recommendations, not Hassan's

He asked for these rather than only implementing his ideas. These are the levers that reliably
move comprehension, ordered by how much they would improve THIS library specifically. Build them
into every lesson; none is decoration.

1. **CONTRASTING CASE — the single highest-value addition, and the library has almost none.**
   You do not understand a concept until you know what it is NOT. A freeze looks like thinking.
   A pacifier looks like an itch. Conviction looks like expertise. Every lesson should show the
   near-miss beside the real thing and say what distinguishes them, because the near-miss is what
   he will actually meet. Discrimination is the skill; a definition alone does not build it.

2. **PRE-EMPT THE WRONG MODEL, EARLY.** Most readers arrive with a wrong version already
   installed ("fight or flight", "crossed arms mean defensive", "Stoicism means not caring").
   Naming and killing it in the first paragraphs is worth more than adding correct material,
   because the wrong model actively intercepts everything that follows. Track O lesson 2 does
   this and it is why that lesson works.

3. **FADED WORKED EXAMPLE.** Run one case fully (already the standard). Then give a second case
   and stop halfway — "their hand goes to their neck right after you say the date; what do you
   now know, and what do you NOT know?" Completing a partly-worked case builds transfer that
   reading a finished one does not. This is the biggest gap between the current lessons and
   something that actually trains a skill.

4. **GENERATION BEFORE RECOGNITION.** The quizzes are all multiple choice, which tests
   recognition — the weakest form. Add ONE free-recall prompt before the options appear ("what
   is the tell that this is running?"). Retrieving beats recognising by a wide margin, and the
   app already has the spaced-review machinery to schedule it.

5. **CONCRETE FIRST, ABSTRACT SECOND — always.** Open with the specific situation, then name the
   principle. Abstract-first forces him to hold an empty container until an example arrives.
   Several existing lessons still open with the principle; invert them.

6. **FIGURES: SHOW THE MECHANISM, NOT THE SUMMARY.** A figure earns its place only when it does
   something prose physically cannot — motion, staged reveal, two things changing at once,
   before/after. A figure restating the paragraph beside it adds load and subtracts nothing.
   Put the label ON the thing it labels (split attention is a real cost), and cut anything
   decorative: interesting-but-irrelevant detail measurably reduces what gets understood.

7. **CROSS-LINK IDEAS THAT ARE THE SAME IDEA.** `rel` already exists and is barely used. Greene's
   confirmation bias, Navarro's baseline discipline and Kahneman's WYSIATI are one mechanism seen
   three times. Saying so converts three isolated facts into one structure, which is both easier
   to hold and harder to forget.

8. **STATE THE EDGE.** Already in the depth standard, and worth keeping for a reason beyond
   honesty: an unbounded rule gets misapplied, fails, and is then discarded wholesale. Marking
   where it stops is what stops him throwing the whole idea away the first time it does not work.


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
- **`respondWith()` must ALWAYS resolve to a Response.** #170: the service worker ended in
  `const net = fetch(req).catch(() => hit); return hit || net;` — with nothing cached and a
  failing fetch that resolves to `undefined`, which does NOT fall back to the network. It cancels
  the navigation, so the whole app paints as a blank white page with no error, and every reload
  repeats it. A version bump is the way in: each release fills a new cache and deletes the old
  one, and filling deliberately tolerates failures, so one flaky moment leaves the new cache
  without index.html after the working copy was already deleted. `tools/sw_test.py` pins both and
  is a ship gate; it reports 3 failures against the pre-fix file, which is why its passing means
  something.
- **A blank page is not evidence that the deployment is broken.** Check the server side first:
  every asset returned 200, live index.html was byte-identical to the commit across five fetches,
  and live content.enc decrypted to 24 books / 87 nodes. The fault was entirely client-side.
- **Never tell Hassan to "clear site data" to fix a stuck app.** That wipes localStorage, which
  holds his Path progress AND his stored key. Unregistering the service worker is enough.
- **A test that copies the logic instead of loading it will pass forever after the code changes.**
  `minipath_test.py` lifts the real functions out of index.html by name and would fail loudly if
  they were renamed. Mutation-test any new gate before trusting it — all three deliberate breaks
  were caught, which is the only reason the green run means anything.
- **Control the matcher before believing the match rate.** "0 of 143 quotes are verbatim" is the
  same output a broken matcher gives. It was only trustworthy after 24 real book sentences were
  fed through it and all 24 were found. Any search that returns a clean 0% or 100% is suspect
  until it has been run against a case whose answer is already known.
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
