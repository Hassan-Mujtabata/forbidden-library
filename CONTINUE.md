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
- **FIRST REAL FEEDBACK ON A FINISHED LESSON (Meditations / "Sorting What Is Actually Yours",
  ~830w with the lever figure): "looks okayish to me... just increase its overall size a bit...
  conceptually i cant say anything cause i dont understand the concept" yet.** Two things follow.
  (1) Nudge lesson length UP — target ~1,000-1,200w where the idea supports it, not 830.
  (2) He cannot validate accuracy before learning the material, so DO NOT wait on him for that.
  Correctness has to come from the book's own text, which is why every path_*.py records the
  exact episodes it was written against. Grounding is the check, not his review.
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
- Path: **109 nodes, 18 tracks, 30 with figures** (shadow 11/33, light 19/76). All five new tracks have at least one. **ALL 24 BOOKS ARE COVERED** —
  verified: zero books have no lesson citing them. Track O fully deepened (3.112);
  track P = Meditations (3.113), covered but at ~600 words/lesson — NEEDS DEEPENING to the
  track-O standard, it carries the four elements but compactly. Track N = first mini-path (Laws of
  Human Nature). Track O = Reading the Body (Navarro), 4 lessons, one `pattern` figure. Backup at `tools/backup/graph.pre-rebuild.json`.
- App: **3.109 live and pushed.** The token at `C:\Users\sands\.secrets\github_token.txt` is
  still missing, so ship.py's push is intermittent — when it fails, Hassan runs
  `python -c "import sys; sys.path.insert(0,'tools'); import ship; ship.push()"` himself.
- `/reset.html` clears a wedged service worker without touching progress or the key (#171).
- `VV.all({stage:1})` passed 98/98 as of 3.102.
- **507 book figures live and ALL 507 placed** (was 505 — two were silently dropped by an
  over-strict placement rule; #179 attaches to the nearest chapter at any distance instead).
  Encrypted per book under `img/<id>.enc`; 24 bundles.

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

### [x] JOB 6 — Reset controls + book-to-path map  — DONE, shipped 3.114
- **Reset a stage**: ⟲ in the lesson header. **Reset a path**: ⟲ on the track header.
- Both delete the WHOLE `S.node[id]` entry, not just `doneAt` — leaving `rv` behind would keep a
  reset lesson in the spaced-review rotation as though it had been seen.
- Resetting a mini-path parent clears its STEPS, because the parent stores nothing of its own.
- `S.nodePos` / `S.lastTrack` pointing into cleared state are dropped, or the CONTINUE card
  offers a lesson whose progress no longer exists.
- A book's page now names the tracks that draw on it (`tracksForBook()`, built from
  `sources[].book`) above the individual idea chips.
- `tools/reset_test.py` — 13 assertions against the real functions, wired into ship.py.

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

**COVERAGE IS COMPLETE (3.116).** Every one of the 24 books now has at least one lesson.
Verify with: for each book title, is it in any node's `sources[].book`? Answer is currently 24/24.
Tracks added this session: O Navarro (3.110) · P Meditations (3.113) · Q Carnegie (3.115) ·
R van der Kolk (3.116), plus N Laws of Human Nature (3.109).

**WHAT REMAINS IN JOB 5 — depth, then figures.** Coverage is not the same as done:
- **Deepened so far:** track O (`deepen.py` o1 -> 1,519w, `deepen2.py` o2-o4 -> ~850w) and
  track Q (`deepen3.py`, 4 lessons ~500 -> ~870w).
- **Deepened:** track N (`deepen4.py` + `deepen5.py`) — 185-276w -> 563-682w/lesson. Now carries
  failure+tell, mechanism worked down, a second case, and the edge on every step.
- **ALL FIVE TRACKS ARE NOW AT DEPTH** (`deepen6.py` finished P and R). Every lesson across
  N/O/P/Q/R carries: the mechanism worked down to why it must be so, a concrete case, the
  failure the reader will actually produce, the tell for it, and the edge where it stops.
  Word counts: O 850-1519 · R 854-961 · Q 822-909 · P 706-832 · N 563-682.
  **Revised target after Hassan's feedback is ~1,000-1,200w.** Done: R (`deepen7.py`, adds a
  SECOND worked case per lesson — one mechanism plus one example transfers to that example
  only; two in different settings is what makes the real one recognisable).
  **Next, in order: N (563-682, thinnest, 7 nodes) then P (706-832) then Q (822-909).**
  Note `deepen7.py` pops the closing clinical edge off track R's lessons and re-appends it last —
  any future pass on R must preserve that, it is the last thing read for a reason.
- **WHAT REMAINS IN JOB 5: figures.** 25 nodes have one; the five new tracks have two between
  them (o4 `pattern`, n1s2 `tape`). See the figure section below — authorised, owed, and the
  thing Hassan has repeatedly said makes the difference.
- **What deepening should ADD** (deepen3.py is the model — it appends rather than rewrites):
  the second case that goes WRONG, the failure the reader will actually produce, and the tell
  that they are producing it. Agreeing with a mechanism is easy; the gap is always execution.
- Figures: only track O has one. See the figure section below — they are authorised and owed.

**Track Q is the model for a list-shaped book.** Carnegie's 30 numbered principles were NOT
mirrored as 30 steps — they reduce to 4 mechanisms, and the track teaches those with the
principles as worked instances inside them. 30 rules is 30 things to remember and generates no
31st; 4 mechanisms generate all 30. Apply the same reduction to 48 Laws and 30 Covert Tactics.
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
- **DONE SO FAR:** `pattern` -> o4 (Navarro baseline, Bond & DePaulo 2006). `tape` -> n1s2
  (Conviction Bias, Langer copier 60/94/93). `trade` -> q2 (ego threat, Amabile 1983 "Brilliant
  but Cruel"). `lever` -> p2 (the Stoic sort; its own research note says the world lever must
  NOT be drawn as useless, which is exactly that lesson's edge). All three are reuses of components whose research was already done — the correct
  pattern, and the only one that does not require fresh research before drawing.
- **HOW TO FIND THE NEXT ONE:** list components already used in the graph (they carry research);
  read the component's own comment block in index.html for its claim and its stage names; then
  find a lesson whose claim is THE SAME, not merely adjacent. Components never used anywhere are
  suspects, not a menu — `drift`, `pacer` and `curve` were each audited and each encoded the
  wrong claim.
- **REJECTED, and why:** `crowd` for n1s4 (The Group Bias). It draws social proof as DENSITY,
  and that lesson's claim is positions correlating across unrelated issues. Not the same claim,
  so not shipped. Record rejections here — the log is what stops the next session re-deriving it.
- **[DONE 3.125] Track R now has its figure** — the specced `routes` component was built and
  registered in build.py's FIG_COMPONENTS at the same time (the mirror rule). Kept below for the
  reasoning, which still applies to every future figure:
- **NO EXISTING COMPONENT FITTED TRACK R. Checked, not assumed.** Every
  researched component was read against r1-r4's claims and each encodes something else:
  `frames` = "a wobbly mind sees the story, a steady mind sees the frames" (meditation insight —
  and note the VALENCE IS INVERTED: there, discreteness is the truth being revealed; in r2 it is
  a processing failure, so reusing it would teach that fragmentation is insight);
  `closure` = WYSIATI coherence; `episode` = peak-end / the cold-hand study; `threshold` = a
  visible break at an unmarked line; `suffuse` = jhāna saturation; `nearer` = hotel-towel social
  proof. Adjacent is not the same claim. Do not force one of these.

- **BUILD THIS INSTEAD — a new component for r3, and the research is already done because it is
  the book's own finding.** Van der Kolk's scans show Broca's area going offline during a
  flashback while the alarm pathway stays lit. Two routes from one event: the fast low road to
  the amygdala, and the high road to the frontal lobes/speech. Stage 1 — ordinary event, both
  routes carry, the verbal one produces a description. Stage 2 — overwhelming event, the alarm
  route lights harder AND the verbal route goes dark. Stage 3 — the practical consequence: a
  question addressed to the dark route gets nothing, which is not refusal. No numbers on it; the
  paper's effect sizes are not in hand, and inventing ticks is the failure `trade` avoided.
  Remember: add the name to FIG_COMPONENTS in build.py at the same time (the mirror rule), or a
  spec using it validates and then draws nothing.
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

## THE CONCEPT SPINE + SITUATION INDEX  (design — build this, it reshapes everything else)

**The diagnosis.** Hassan has said for weeks that he understands the concepts and still cannot
apply them, and that reading takes years to become usable. That is not a lesson-quality problem
and writing better prose will not fix it. It is two structural faults:

1. **24 books are 24 silos.** Greene's confirmation bias, Kahneman's WYSIATI, Cialdini's
   consistency principle and Navarro's baseline discipline are THE SAME MECHANISM described by
   four authors who never read each other. Presented separately they are four unrelated facts,
   so learning is additive — every book makes the pile bigger. Named as one mechanism they are
   one idea with four instances, so learning COMPOUNDS: book five makes books one to four
   clearer instead of heavier. ~20 mechanisms generating a thousand observations is far easier
   to hold than a thousand observations.
2. **Everything is indexed by SOURCE, and life does not arrive by source.** When someone goes
   quiet in a meeting, nothing in the library is reachable — you would have to already know it
   is a Navarro problem, recall the track, find the lesson. That is not a comprehension failure,
   it is a RETRIEVAL-PATH failure, and it is the actual reason knowledge sits inert for years.

**THE FIX — three parts, in order.**

**(a) Tag every lesson with the mechanism(s) it instances.** Add `mech: ["motivated-reasoning"]`
to nodes (array — a lesson may instance more than one). Register the ids in build.py exactly the
way FIG_COMPONENTS works, and validate against it: that mirror rule already exists and has caught
real bugs. Unknown id = build fails.

**(b) A Mechanisms view.** One screen per mechanism: the mechanism stated once, then every lesson
across every book that instances it. This is where compounding becomes visible — four books
agreeing is far more convincing, and far more memorable, than any one of them asserting it.

**(c) A situation index — the piece that makes it apply in real life.** Tag lessons with
`trigger` phrases in the reader's own language, and give the app an entry point that asks "what
is happening right now?" rather than "which book?". Triggers to start from:
"they went quiet" · "they agreed too fast" · "I'm about to decide something I already want" ·
"I'm explaining and losing them" · "I can't stop thinking about it" · "they keep bringing it up"
· "I said yes and regret it" · "I know what to do and I'm not doing it" · "this keeps happening
to me" · "I feel worse after talking to them".
Also: **spaced review currently resurfaces LESSONS; it should resurface SITUATIONS** ("you are in
this position — what is running?"). Retrieval practice only builds the path you actually
practise, and right now the practised path is "recall lesson", never "recognise moment".

**THE MECHANISM LIST — started, not finished. Refine against the text; do not invent to fill.**

| id | mechanism | books that instance it |
|---|---|---|
| `motivated-reasoning` | You believe what is pleasant to believe, then recruit the evidence | Greene, Kahneman, Cialdini, Navarro |
| `appraisal-gap` | Event → judgement → response; the judgement is the only lever | Aurelius, Frankl, TMI, van der Kolk, Kahneman |
| `automaticity` | Repetition turns behaviour into reflex that runs without you | Clear, TMI, Aurelius, Greene |
| `ego-threat-stops-processing` | A threatened self-image ends learning and persuasion outright | Carnegie, Greene, Dark Psych, Davis |
| `importance-deficit` | People are starved for significance; supplying it opens them | Carnegie, Schafer, Greene, Seduction |
| `body-precedes-narrative` | Physiological response fires before, and independent of, the story | Navarro, van der Kolk, TMI |
| `attention-is-the-control-surface` | Where attention goes decides what is learned and what is felt | TMI, Brasington, Goldstein, de Bono, Clear |
| `baseline-and-deviation` | Signal exists only relative to that person's own normal | Navarro, Kahneman, Levine & Heller |
| `conformity-without-pressure` | The group sets belief while no pressure is ever felt | Cialdini, Greene, Dark Psych |
| `reciprocity-debt` | A gift creates obligation that operates below awareness | Cialdini, Greene, Schafer, Seduction |
| `loss-looms-larger` | Losses and scarcity outweigh equivalent gains | Kahneman, Cialdini |
| `commitment-consistency` | A small yes binds the next; self-image defends past choices | Cialdini, Clear, Greene |
| `attachment-template` | Early relational patterns replay in adult relationships | Levine & Heller, van der Kolk, Greene |
| `meaning-bears-load` | What can be endured is set by what it is for | Frankl, Aurelius, Buddhaghosa |
| `impermanence-non-identification` | Experience is a stream of arisings, not a solid self | TMI, Goldstein, Brahm, Buddhaghosa, Aurelius |
| `frame-controls-answer` | How a choice is presented determines the choice | Kahneman, Cialdini, Greene, Dark Psych |
| `front-and-halo` | People present managed fronts; one quality implies the rest | Greene, Navarro, Seduction, 48 Laws |
| `state-contagion` | States transfer between people below awareness | Schafer, van der Kolk, Davis, Seduction |
| `edge-of-capacity` | Capacity grows only at the edge, and only with feedback | TMI, Clear, Brasington |
| `suppression-rebounds` | Fighting a state feeds it; allowing it releases it | TMI, Goldstein, van der Kolk, Aurelius |

**WHY THIS BEFORE MORE BOOKS.** It changes how the remaining books get written. *The Body Keeps
the Score* written against mechanisms that already exist is a smaller job producing a better
result than the same book written with a fresh vocabulary nobody else shares. Every book added
after the spine exists is cheaper AND makes the existing ones clearer. Every book added before it
is another silo to reconcile later.

---

## THE FIGURE RESEARCH PROTOCOL  (Fable 5's workorder-6 rules — the workorder file is gone, these are the rules)

`tools/figs_research/` is GITIGNORED and ship-blocked, so the rules live here or they are lost.
`LOG.md` in that folder is the audit trail and shows the protocol being executed; read it before
starting a cycle. These rules are not ceremony — every one of them exists because a figure was
shipped or nearly shipped that was wrong.

**1. RESEARCH IS MANDATORY, AND IT MUST SPAN FOUR SOURCE CLASSES.** Hassan: "please make sure it
does research properly... this book is just basic concept... it needs to even do online
research", and later: research "on forums and research papers and other sources like that". A
cycle that only used one class is not finished. The four:
  a. **The library books** — the concept, and the fidelity check. A figure must not contradict
     any book in the library, not just the one it belongs to. (The breathing pacer passed its own
     lesson and contradicted all three meditation books.)
  b. **Peer-reviewed papers, read in full** — the numbers, the method, the controls, and whether
     it replicated. Never a summary. See rules 3 and 4.
  c. **FORUMS AND FIRST-PERSON ACCOUNTS** — r/streamentry, Dharma Overground, StackExchange,
     Hacker News, long-form comment threads, Goodreads review threads. This class supplies what
     papers structurally cannot: what the thing actually FEELS like from inside, the words people
     reach for, and the error they really make rather than the error the author assumed. A figure
     built without it is accurate and inert — it will not be recognised in the moment, which is
     the entire job.
  d. **Practitioner / teacher prose** — the bridge between (b) and (c).

**1a. THE CORROBORATION RULE BITES HARDEST ON CLASS (c).** Hassan: "someone can just put random
stuff for trolling so 1 isnt really enough." A single forum post is worth nothing — it may be a
troll, an outlier, or someone repeating the book back. Require **at least three independent
people describing the same experience in their own words**, ideally across different communities.
Independence is the test: three replies in one thread agreeing with each other is one source.
And check the account is not just paraphrasing the book you are already citing — that is
circular, and it is the same trap as leighb.com being Brasington's own site.

**1b. RECORD WHAT THE CRAWLER CANNOT REACH.** reddit.com returns HTTP 400 to the crawler, so
cycle 1's evidence base has no raw beginner voice and SAYS SO. If class (c) is unreachable for a
topic, that is a stated limitation on the figure, not something to paper over — and it is a
reason to weaken what the figure claims, not to claim it anyway.

**2. NO CLAIM EVER RESTS ON A SINGLE SOURCE. THIS IS GLOBAL — IT IS NOT A FORUM RULE.**
Hassan has said this twice, and the second time because the write-up had drifted into sounding
like it only governed forum posts. It governs EVERY class and EVERY claim a figure makes:
  * **One paper is not enough.** A single study is a result, not a finding — it needs
    replication or an independent line reaching the same place. This is not pedantry: the decoy
    effect had a famous paper and died at 11 successes in 91 attempts.
  * **One book is not enough.** Cross-check against the other 23. A figure that satisfies its own
    lesson can still contradict the library — the breathing pacer did exactly that, and was
    contradicted by all three meditation books.
  * **One forum post is worth nothing** — troll, outlier, or someone repeating the book back.
    Three independent people, own words, ideally different communities. Three replies in one
    thread is ONE source.
  * **One author across two places is still one source.** leighb.com was used to corroborate
    Brasington and IS Brasington's own site. Discarded and replaced with Ajahn Brahm — a
    different lineage, which is what independence actually means.

**Independence test, apply it every time:** different author, different method, and ideally a
different tradition or field. If the second source could have got its claim FROM the first, it is
not a second source. Write both into LOG.md with the link, so the independence can be checked by
someone who does not trust you — that is what the log is for.

**3. READ THE PRIMARY SOURCE IN FULL, NOT A SUMMARY.** Cycle 2 read Draganski et al. Nature 2004
as the PDF and got the third scan, the "transient" wording and the non-juggler control — none of
which survives in a summary. A vivid simile widely attributed to TMI was checked against
books.json, found NOT to be in the actual text, and dropped.

**4. CHECK IT REPLICATED BEFORE YOU DRAW IT.** The decoy effect was killed before a single line
was drawn: Yang & Lynn 2014 attempted it 91 times and it worked 11. The figure was replaced with
one built on defaults (Johnson & Goldstein, 42% -> 82%), which holds.

**5. RECORD WHAT YOU REJECTED AND WHY.** Half the value of LOG.md is the rejections. A figure
that was considered and dropped will otherwise be re-derived by the next session — this session
alone rejected `crowd` for n1s4 and `frames` for r2, and both took real work to rule out.

**6. STATE WHAT YOU COULD NOT GET.** Cycle 1 records that reddit blocks the crawler, so there is
no raw beginner voice in that evidence base. A gap that is stated is a limitation; a gap that is
hidden is a claim you cannot support.

**7. NO INVENTED PRECISION.** If the effect sizes are not in hand, the figure carries direction
only and no tick values — `trade` and `routes` both do this deliberately. Putting numbers on an
axis you did not get from the paper is fabrication that looks like rigour.

**8. THE FIGURE MUST TEACH AWAY A SPECIFIC ERROR.** Every LOG entry names the "error taught
away" first. A figure that merely restates the paragraph beside it adds load and subtracts
nothing. If you cannot name the wrong belief it removes, do not build it.

**9. AUDIT AFTER DRAWING.** `VV.figs()` in the browser checks no-shrink, cause-before-effect,
rest, label-fit, motion-safe and no cut-offs. A reduced-motion bug hid in b2 from 3.74 because
`fg-leave`/`fg-hop` restored transform but not opacity — invisible to everyone using
prefers-reduced-motion, for weeks.

**10. UNUSED COMPONENTS ARE SUSPECTS, NOT A MENU.** Every unused one audited so far (`drift`,
`pacer`, `curve`) encoded the wrong claim. Prefer reusing a component whose research is done and
whose claim is THE SAME — not adjacent. Otherwise build a new one and register it in
FIG_COMPONENTS in build.py at the same time.

### HOW MANY FIGURES — ~65 of 109 is the FLOOR, not the ceiling

**Hassan, 5 Aug: "im guessing those figures are critically needed. once finished with them then
start making more to support where u think could help and research."** So the ~38 below are the
committed set — treat them as required work, not a proposal. AFTER they are done, keep going:
add figures wherever your own judgement says one would help, each still research-backed and each
still logged. He is explicitly delegating the choice of the later ones, which means the
selection rule becomes yours to apply and the protocol below is what keeps that honest.

The one thing that does NOT relax: a figure still has to do something prose physically cannot.
"More figures" is not the goal — understanding is. A decorative figure fails his first rule
("anything makes it harder dont even bring it close") no matter how many are wanted.


Counted 5 Aug 2026. Hassan asked for this split explicitly; his guess that ~84 was the light wing
alone was close but that number was both wings together.

| wing | lessons | have one | missing | sensible target | to build |
|---|---|---|---|---|---|
| **dark (shadow)** | 36 | 8 | 28 | ~24 | **16** |
| **light** | 73 | 19 | 54 | ~41 | **22** |
| total | 109 | 27 | 82 | ~65 | **~38** |

**Why not 82.** A figure earns its place ONLY when it does something prose physically cannot —
motion, staged reveal, two things changing at once, before/after. One that restates the
paragraph beside it ADDS load: another thing to parse for no new information. Sort the lessons:
- *mechanism* lessons (a process with moving parts — the gate that reads a reason's shape, two
  roads out of one event, the lever that is not connected) → these want a figure, ~60% of the
  library;
- *distinction* lessons (this vs the thing it is confused with) → better as a contrasting case
  in prose;
- *practice* lessons (a drill you do) → a figure adds nothing.

**DARK WING FIRST.** Hassan asked for it, and independently it is the right order: social
mechanisms are the most figurable material here — two parties, a threshold, a trade, something
that runs before thought. All four figures built on 5 Aug came from that wing for that reason.
Light wing is harder because inner states resist diagramming, though `groove`, `suffuse` and
`distil` show it is possible.

**RATE.** One cycle = one figure = one LOG.md entry with sources, independent corroboration,
rejections and gaps. ~38 figures at that rate is a long run of sessions, not one. Do not batch
them to go faster — the figures produced faster than this are the ones that were wrong (the
breathing pacer contradicting all three meditation books; the decoy effect that does not
replicate).

### THE SIX CYCLES ARE DONE — AND THE RESULT CHANGES THE PRIORITY

Counted after cycle 12: **109 lessons, 30 with figures** (shadow 11/33, light 19/76).

**THE TALLY THAT MATTERS.** Six research cycles produced **3 figures and 6 lesson corrections**.
Every single lesson audited needed correcting, and three planned figures were killed because they
would have drawn an overclaim. What was wrong, in order:
1. `n1s1` — the famous source's memorable half (polarization) does not replicate; nearly drew it.
2. `n1s6` — stated a mechanism as settled; it is disputed. Then over-corrected, then fixed again.
3. `o2` — right order, wrong cause: the driver is threat imminence, not escalating cost.
4. `q1` — the lesson's PREMISE (attention is scarce) is unverified; rebuilt on the measured chain.
5. `q4` — durability claim withdrawn; found a MODERATOR that inverts the advice.
6. `n1s4` — asserted universal cross-issue correlation; the canonical measurement found the
   opposite for the mass public.

**WHAT THIS IMPLIES, AND IT IS UNCOMFORTABLE.** Those six were written the same day, the same way,
by the same process as the other ~100 lessons. There is no reason to think the unaudited ones are
cleaner — the sample says roughly every lesson carries at least one claim that is overstated,
mis-caused, or contradicted by its own best source. A confident, well-written lesson is exactly
what a wrong claim looks like from inside.

**SO THE PRIORITY CHANGES: CLAIM-AUDIT BEFORE NEW FIGURES.** A wrong claim in prose is read as
true; a missing figure is merely absent. Auditing an existing lesson is also cheaper than a figure
cycle — it needs rules 2–4 (corroborate, primary source, replication) but no component, no
drawing and no class (c). Roughly: one audit per lesson, batched by track, correcting in place.
Figures resume afterwards, built on corrected lessons rather than on the originals — which is
also why building more figures first would have been wasted work.

**AUDIT PROGRESS: o1 (3.136) and o3 (3.137) done. o3 was the first audit that MOSTLY CONFIRMED
a lesson - record that, because six corrections in a row could bias a session into assuming
everything is wrong. Its core upgraded from assertion to measurement (cortisol RCT n=159; facial
self-touch a more reliable stress indicator than facial expression); only my neck/vagus mechanism
was unverified. Track O fully audited. Track R started: r1 done (3.138) - I had conflated autonomic reactivity
(supported) with hormonal tone (contested; resting cortisol is meta-analytically LOWER in PTSD,
the HPA paradox). Lesson now separates them and carries a genre warning about tidy single
mechanisms. r2 (3.139) and r4 (3.140) done - r4 was the largest correction yet: Maier & Seligman (2016)
RETRACTED their own mechanism, passivity is the unlearned DEFAULT and what is learned is CONTROL.
Track R fully audited. Track Q: q2 done (3.141) - first MAGNITUDE error rather than a
mechanism error; direction right, but stated as a switch when the measured effects are small.
q3 done (3.142) - TRACK Q FULLY AUDITED. q3 was the most consequential audit yet: it
invalidated the ACTION, not just the mechanism. The lesson instructed perspective-TAKING, which 25
experiments show does not improve accuracy and can raise confidence without it; rewritten around
perspective-GETTING (asking). Track P started: p1 done (3.143) - the "always a judgement step" claim is the strong Lazarus
side of an unresolved debate; bounded to a SCOPE claim, with the practical payoff that it tells
the reader when the tool does NOT apply. p2 done (3.144) - CONFIRMED, and the audit supplied the missing mechanism (worry is reinforced
because feared things mostly do not happen; and verbal worry is less vivid than imagery, so it
functions as avoidance). Retro-justifies p3. p3 done (3.145) - TRACK P COMPLETE. Action confirmed and sharpened into if-then form
(implementation intentions, d=.65). Track N: n1 done (3.146) - Greene's "one mechanism behind all bias" bounded to the HOT family;
the COLD family (anchoring, availability) needs PROCEDURAL fixes, not honesty. Next: n1s3, n1s5,
then the eleven never-audited tracks A-M.
**THIRD CROSS-LIBRARY JOIN FOUND BY AUDITING** (q1<->q3, p1<->r2, now N<->K as hot vs cold
families). The audit keeps producing concept-spine links as a by-product - finish the audit before
building the spine formally.
**NEW GENERAL RULE FOUND IN AUDIT 10: when a lesson prescribes a technique whose evidence comes
from FACILITATED delivery, the reader is getting the weaker arm** (document g=0.277 vs interactive
g=0.465). Say so rather than implying the full effect transfers. Applies to every 'do this
exercise' instruction in the library.
**Audit tally so far: 7 corrections, 2 confirmations** - the base rate of error is high but not
total, which matters: do not go in assuming every lesson is wrong.
**NOTE: auditing keeps JOINING lessons** (q1<->q3, now p1<->r2). It is doing concept-spine work
informally, which is an argument for finishing the audit before building the spine formally.
**METHOD NOW HAS THREE CHECKS: mechanism, magnitude, and ACTION.** A lesson can have a correct
mechanism and still tell the reader to do the one thing the evidence says fails.
**ADD TO THE AUDIT METHOD: check MAGNITUDE as well as direction.** A claim can be correctly aimed
and still wrong by being absolute. Hunt the words "entirely", "stops", "cannot", "never" - that is
where overstatement hides once the direction is right.
**Note across all five audits: the ACTION in each lesson survived even where the MECHANISM did
not** - which is why auditing mechanism sentences is safe to do quickly. Earlier: r2 (3.139) - the low-road/high-road speed story is contested (Pessoa & Adolphs); the
observation survives, the wiring does not. Next: r4.
**THE AUDIT PATTERN IS NOW FOUR FOR FOUR AND SHOULD BE USED AS A METHOD: go straight at the
MECHANISM sentence.** Every mechanism-level claim audited has been overstated (neck/vagus,
hormones-stay-high, introspection-weighting, low-road speed) and every OBSERVATION has survived.
That makes auditing much faster than a research cycle - find the sentence that explains WHY, and
check only that. Earlier note: o1 (3.136) - bounded against the deception literature; the honesty
framing and any lie-detection promise are withdrawn, mechanism intact. Notably the audit made the
track MORE internally consistent: o3/o4 were already built on comfort/discomfort, so o1 was the
outlier. Next: o3, then track R.**

**AUDIT ORDER** — by how load-bearing and how confidently asserted: O (4) → R (4) → Q (2 left)
→ P (3) → N (1 left), then the eleven older tracks A–M, which have never been audited at all and
are the largest unknown in the library.

### THE PLAN — first six cycles, dark wing, in this order

Written before starting so the work is not re-derived each session. One cycle per session is the
expected rate. Each entry states the ERROR TAUGHT AWAY first, because rule 8 says a figure with
no named wrong belief to remove should not be built. "Candidate research" is where to START, not
a citation — it still has to be read in full and independently corroborated (rules 2 and 3), and
if it fails replication it gets killed before drawing (rule 4), exactly as the decoy effect did.

**Cycle 1 — `n1s1` Confirmation Bias. [x] DONE, shipped 3.127** as the new `sieve` component.
CLASS (c) WAS NOT OBTAINED — reddit blocks the crawler and no three independent first-person
accounts surfaced, so the `feel` lines carry MEASURED results instead of an invented lived
voice, and the claim was weakened to what the papers support. That is rule 1b applied, and it
is the model for what to do when a source class is unreachable. Original notes: Full notes in
`figs_research/LOG.md` cycle 7. **Key finding, do not lose it: Lord, Ross & Lepper (1979) reports
TWO results and only one survives.** BIASED ASSIMILATION (each side rated the study agreeing with
them as better conducted) is the half this figure needs. ATTITUDE POLARIZATION (mixed evidence
makes people more extreme) FAILED TO REPLICATE — Miller et al. 1993, Kuhn & Lao 1996, Munro &
Ditto 1997 all lost it once they measured actual pre/post opinions instead of the original's
self-reported change; later work calls polarization "the exception, not the rule".
**So the figure shows the two gates ONLY and must NOT show the sides moving apart afterwards** —
that is the dead half, and drawing it would repeat the decoy-effect error exactly. **CORROBORATION DONE:** Taber & Lodge (2006) AJPS, "Motivated Skepticism" — different lab, method
(thought-listing measures counterarguing directly) and domain; finds participants "counterargued
the contrary arguments and uncritically accepted supporting arguments", i.e. the scrutiny
asymmetry measured rather than inferred. Replicated in Political Behavior (2008).
**Conflict recorded, not resolved:** Taber & Lodge DO find polarization while Miller/Kuhn/Munro do
not, so that consequence is genuinely contested — which is exactly why the figure draws the gates
only. Do not quietly settle it in either direction.
**Still owed before drawing: class (c) only** — three independent first-person accounts of the
felt asymmetry ("I read the one I disagreed with three times looking for the flaw"). Papers give
the mechanism; forums give the words he will recognise it by.
Highest value in the library: it is the mechanism most of the others sit on.
- Error taught away: "I checked, and the evidence supports me." The reader believes the failure
  is not looking at the other side. It is not — they DO look.
- Claim to draw: asymmetric SCRUTINY, not asymmetric selection. Opposing evidence is examined
  hard and a flaw is found (everything has one); supporting evidence is waved through on a
  glance. Two gates at different heights, same evidence arriving at both.
- Candidate research: Lord, Ross & Lepper (1979) biased assimilation — same two studies shown to
  both sides, each rating the study agreeing with them as better conducted. Corroborate with an
  independent replication, NOT a summary of Lord.
- Component: new. Nothing existing encodes two different thresholds.

**Cycle 2 — `n1s6` Superiority Bias. [x] DONE, shipped 3.130** as the new `selfrank`
component, drawing the PHENOMENON only — the recorded fallback, taken because the mechanism is
contested. Original notes: — see LOG.md cycle 8.
Rule 4 passes strongly: Svenson (1981) has a preregistered N=1,203 direct replication (91% safer,
93% more skilled than average), and Alicke (1985) gives an independent second line with its own
2021 replication. **But those establish the PHENOMENON, not the MECHANISM the lesson teaches**
("you see your own process and only other people's output"). Before drawing, verify the
mechanism line — bias blind spot (Pronin, Lin & Ross 2002) and the introspection-illusion account
(Pronin & Kugler 2007) — read, not cited from memory, replication checked. **MECHANISM IS CONTESTED — 3.128 OVERSTATED IT, CORRECTED IN 3.129.** The PHENOMENON is rock
solid (Scopelliti 2015 validated scale; 2024 preregistered replication d = -1.72). The
introspection EXPLANATION was tested directly by JDM "Hypothesized drivers of the bias blind
spot" and questioned: no crossover, r = .11, non-significant once cognitive sophistication is in
the model. **Protocol lesson: run rule 4 on the MECHANISM claim separately from the phenomenon —
they replicate independently, and a figure drawn on the mechanism would have encoded something
its own field disputes.** Earlier note: Pronin & Kugler (2007) JESP —
the blind spot PERSISTED even when observers were handed the other person's introspections, so it
is a WEIGHTING asymmetry, not an information one. n1s6 rewritten (682 -> 906w). Figure still NOT
drawn: needs the full text (this used abstract-level reporting), replication status, and class (c).
Design implied by the finding: stage 3 shows their introspection handed over and still discounted
— a better figure than the one planned, and it exists only because the research contradicted the plan. Pairs with cycle 1 and explains why the whole track is
read as being about other people.
- Error taught away: "I'm more rational than most" — held by nearly everyone, so it cannot be
  true of nearly everyone.
- Claim to draw: you see your own PROCESS and only other people's OUTPUT. Two panels of the same
  decision — one showing deliberation, one showing only the result.
- Candidate research: better-than-average effect. Svenson (1981), drivers rating themselves above
  median. Check the replication literature before drawing; parts of this area have not held.
- Component: new (inside view vs outside view).

**Cycle 3 — `o2` Freeze, Flight, Fight. [x] DONE — lesson corrected 3.131, figure shipped
3.132** as the new `imminence` component on the distance axis. Order
corroborated (defence cascade / Fanselow). But the selector is THREAT IMMINENCE, not cost — so
the planned rising-cost drawing is on the wrong axis and `ladder` does not fit. Redesign around
distance, with a separate branch for inescapable (which links to r4). See LOG.md cycle 9. The order is the whole lesson and the order is what
everyone gets wrong.
- Error taught away: "fight or flight" — two responses, wrong order, and it hides the one you
  will actually see, which looks like composure.
- Claim to draw: escalation by COST. Freeze is nearly free and reversible; flight spends energy;
  fight risks injury. A system trying the cheap move first is why freeze comes first.
- Candidate research: Navarro's own text is the floor; corroborate the freeze-first ordering with
  the defence-cascade literature (tonic immobility) from a source independent of him.
- Component: new (three steps with rising cost), or possibly `ladder` — audit it first, it is
  unused and therefore a suspect.

**Cycle 4 — `q1` The Importance Deficit. LESSON CORRECTED 3.133, FIGURE NOT DRAWN.** The
SCARCITY premise is UNVERIFIED and is now labelled as Carnegie's assertion. The measured chain
(listening -> anxiety down -> defensiveness down -> attitude extremity down, 9 experiments) is in
the lesson instead and links q1 to q2. `spotlight` reuse is DEAD - it would have drawn the
scarcity gap. See LOG.md cycle 10. Carnegie's engine; a third of his rules reduce to it.
- Error taught away: "appreciation is flattery, and people see through it."
- Claim to draw: attention is SCARCE, so supplying it is disproportionate — most listening is
  waiting to reply, and the difference is detectable.
- Candidate research: START with Itzchakov & Kluger on high-quality listening (their work
  measures what changes in a speaker when listening quality is manipulated — attitude
  extremity, self-awareness, defensiveness), and with the literature on perspective-taking vs
  actual perspective-GETTING (Eyal, Steffel & Epley) — which reports that people are markedly
  worse at reading others than they believe, i.e. the deficit is real and unnoticed on both
  sides. Corroborate independently; do not build on one lab.
- Component: likely new — a gap between "attention delivered" and "attention believed
  delivered", which is the same shape as `spotlight` (felt vs actual visibility). AUDIT
  `spotlight` first: if its claim generalises, that is a reuse rather than a new component.
- Only skip if BOTH lines fail replication. "Hard to source" was not a good enough reason —
  that judgement was made before looking.

**Cycle 5 — `q4`. LESSON CORRECTED + BOUNDED 3.134, FIGURE NOT DRAWN.** Self-generated
persuasion verified; the DURABILITY claim withdrawn (unevidenced). Found a MODERATOR that inverts
the advice: the advantage holds only while generating feels EASY - when it is a struggle the
difficulty is read as evidence against the idea. Figure design changed to the moderated version
(two runs, easy vs hard, opposite endings). See LOG.md cycle 11. The most useful thing in Carnegie and the least
intuitive.
- Error taught away: "if they agreed, it is settled."
- Claim to draw: compliance decays, ownership does not — an instruction sits outside the
  self-image and can be dropped for free; a conclusion is defended because dropping it means
  admitting error.
- Candidate research: effort justification / IKEA effect, and the durability difference between
  induced and self-generated conclusions. Corroborate across two independent lines.
- Component: new (two identical positions, different anchoring, one decaying over time).

**Cycle 6 — `n1s4`. OVERCLAIM FOUND AND CORRECTED 3.135, FIGURE DEAD.** The lesson claimed
universal cross-issue correlation; Converse (1964) measured exactly that and found the opposite
for the mass public (ideological innocence), with constraint concentrated among the engaged.
Corrected to conditional, plus the corollary that tight alignment tracks being INFORMED rather
than sheep-like. The planned correlated-axes figure is dead - it would have drawn the overclaim.
Any future figure here should be relief-versus-pressure. See LOG.md cycle 12. Deliberately LAST of the six, and it may not be buildable.
- Error taught away: "my ideas are my own."
- Claim to draw: positions arriving as a SET — correlation across unrelated issues.
- **The risk is real but it is NOT unbuildable — that was too quick a call.** Asch and Sherif
  are the obvious sources and both measure PRESSURE, while this lesson claims the opposite: no
  pressure is felt, only relief. Drawing Asch would teach a different mechanism.
- The claim that DOES match is attitude CONSTRAINT — positions correlating across logically
  unrelated issues. Start with Converse, "The Nature of Belief Systems in Mass Publics" (1964),
  which is precisely about issue positions travelling as a bundle rather than being reasoned
  separately, and with the later work on ideological sorting that re-measures it on modern data.
  That is the correlated-positions claim, measured, and it is a different literature from
  conformity-under-pressure.
- Component: new — several unrelated axes whose positions line up once one is known. `crowd` was
  correctly rejected (it draws social-proof density, a different claim).
- Only abandon if constraint fails to replicate on the modern data. Check that before drawing.

After these six, re-count coverage and continue down the dark wing (M, D, E, F), then light.

### THE FULL BACKLOG, RANKED — and how each is built

Hassan asked for the numbers and the method, 5 Aug. Ranked by gain, not by appetite.

| # | work | count | needs research? |
|---|---|---|---|
| 1 | figures, committed floor (dark wing first) | **38** | yes, one cycle each |
| 2 | concept spine + situation index | ~20 mechanism pages + tag 109 lessons + ~15 triggers | no |
| 3 | contrasting cases, one per lesson | ~109 | no |
| 4 | faded worked examples, on mechanism lessons | ~65 | no |
| 5 | second figures on lessons carrying two mechanisms | ~7 | yes |
| 6 | — | — | stop here |

**Why it stops at ~72 figures total.** Past that you are figuring lessons whose core is a
distinction or a drill, where a figure is one more thing to parse for no new information. That
breaks his first rule in the direction hardest to notice, because adding looks like generosity.

**2. Concept spine — how.** Design is already written above. Tag each node `mech:[...]`, register
ids in build.py the way FIG_COMPONENTS is registered, build a Mechanisms view (one screen per
mechanism listing every lesson across every book that instances it), then the situation index
keyed by trigger phrases in his own words. No research — the mechanisms are already identified,
the work is tagging and two views. **This is the largest single comprehension win available and
it is cheaper than ten figures.**

**3. Contrasting cases — how.** One paragraph appended per lesson: the near-miss beside the real
thing, and what distinguishes them. A freeze looks like thinking; a pacifier looks like an itch;
conviction looks like expertise. Cheapest gain per unit of work in the whole library — no
research, no components, and it converts a definition into a discrimination, which is the skill.
Do these in track-sized batches with a `deepen*`-style appending tool.

**4. Faded worked examples — how.** After the fully worked case, add a SECOND case that stops
halfway and hands the reader the finish: "their hand goes to their neck right after you say the
date — what do you now know, and what do you not know?" Completing a partly-worked case builds
transfer that reading a finished one does not. This is the difference between a library that
explains and one that trains, and there are currently none.

**5. Second figures.** Only where one lesson genuinely carries two mechanisms — `o1` is the clear
case (limbic-vs-neocortex, and honesty-tracks-attention are two separate things sharing a page).
Same protocol, no shortcuts.

### WHICH LESSONS HAVE NO FIGURE (worst-covered first)

Dark wing: N 1/7 (n1, n1s1, n1s3-n1s6) · M 1/6 (m2-m6) · D 2/6 (d2, d4, d5, d6) ·
E 1/5 (e1, e3, e4, e5) · F 1/4 (f2, f3, f4) · O 1/4 (o1, o2, o3) · Q 1/4 (q1, q3, q4).

Light wing: J 2/12 (j1, j4-j11) · I 1/8 (i2-i8) · K 3/10 (k2, k4-k7, k9, k10) ·
B 4/9 (b1, b3, b4, b8, b9) · C 1/6 (c2-c6) · G 1/6 (g2-g6) · H 1/6 (h1, h3-h6) ·
A 3/5 (a4, a5) · L 1/4 (l2, l3, l4) · R 1/4 (r1, r2, r4) · P 1/3 (p1, p3).

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
