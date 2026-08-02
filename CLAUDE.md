# The Vault

Single-file encrypted reading PWA. Hassan's books become gamified ~1,200-word lessons
(XP, streaks, spaced review, achievements, AI tutor) on a dependency-locked idea graph.

- Live: https://hassan-mujtabata.github.io/forbidden-library/ (needs `#k=<key>` fragment)
- Repo: `Hassan-Mujtabata/forbidden-library` — public, holds **ciphertext + app shell only**
- Key: `tools/key.txt` (gitignored)

## Layout

| Path | What |
|---|---|
| `index.html` | The whole app — ~3000 lines, inline CSS + JS. Almost every change lands here. |
| `sw.js` | Service worker. `CACHE` const must bump with every `index.html` change. |
| `content.enc` | AES-256-GCM(gzip(books + graph)). The only place lesson text exists publicly. |
| `tools/ship.py` | **Release command.** Checks, bumps, commits, pushes. Use this, not manual steps. |
| `tools/verify.js` | **Start here.** `VV.all({stage:1})` — harness, selftest, overflow, contrast x3, one verdict. |
| `tools/audit.js` | Browser-side contrast audit (`VA.run`) + layout-overflow check (`VA.fits`). |
| `tools/selftest.js` | Browser-side logic suite — `VT.run()`. Merge/tombstone/fold/sane invariants. |
| `tools/bump.py` | Bumps `APP_VER` + `CACHE` together. `ship.py` calls it; rarely run directly. |
| `tools/build.py` | Validates the graph (acyclic, prereqs resolve) → rebuilds `content.enc`. |
| `tools/cleantext.py` | Repairs PDF-extraction damage in `books.json`. Run `--fix` then `build.py`. |
| `tools/extract.py`, `add_book.py` | PDF → text → queued job. |
| `tools/gemini_pipeline.py` | Cloud cron that turns queued books into lessons. |

## Hard rules

1. **`access.json` is Hassan's config. Never modify it, never touch it, never comment on its
   contents.** Upstream commits titled "access: update library visibility" are his own admin
   saves — rebase onto them, never revert or amend them.
2. **Never commit** `key.txt`, `tools/books.json`, `tools/graph.json`, `.gemini_keys`, or any PDF.
   The plaintext graph in a public repo would defeat the encryption. `ship.py` blocks these.
3. **Gemini only adds book content** — lessons in the existing node format, nothing else. It never
   touches `index.html`/`sw.js`/app code. Features are authored by Claude only. Enforced in CI by a
   commit whitelist, not `git add -A`.
4. **Fidelity rule:** never blend the books' methods. Where traditions differ (Goldstein noting-first
   vs Brasington jhāna-first vs Culadasa unified), the lesson says so explicitly.
5. **Never type a control or private-use character into source. Write `\u0000`, not the byte.**
   A literal one is invisible in every editor, survives `node --check`, and — for the private-use
   range — renders as a *different glyph in every font*, so it reads as a font bug rather than
   bad data. `ship.py` blocks these now (`check_glyphs`).
   Related trap: **the Bash heredoc eats one level of backslashes.** Writing `"\\ue053"` through
   it lands a real PUA character in the file. Use `r"..."` raw strings, then re-read the file and
   verify — and always `flush()`/`fsync()`, because an unclosed write here does not reach disk
   before the next read (this produced two "the fix didn't apply" false alarms).

## Releasing

```bash
python tools/ship.py "3.41 Name Of Release"
```

Runs in order: secret scan → `node --check` on the extracted script → `PATCHES` entry present →
`bump.py` → commit → fetch → rebase if behind → push. Any failure stops before the commit.
`--dry` checks without committing.

Before shipping, add the `PATCHES` entry in `index.html` yourself (newest first):

```js
{v:"3.41",n:"Name Of Release",d:"27 Jul 2026",items:[["new","What you added."],["fix","What you fixed."]]}
```

Tags are `new` / `fix` / `polish` / `content`. Every release needs one — returning users get an
auto-popup and the 📜 button glows.

## Gotchas that have each cost real time

**Stale cache is the #1 false bug.** A "X is broken" report is usually a service worker serving an
old `index.html`. Always bump `CACHE` (ship.py does). To verify a deploy actually shipped, grep the
live `index.html` or decrypt live `content.enc` — never trust the Pages build-status endpoint, it lags.

**`?cachebust` does not work.** The SW cache-matches with `{ignoreSearch:true}`, and the in-app
browser pane keeps its own HTTP disk cache and runs no SW. To see fresh code: unregister the SW,
clear caches, reload — or serve on a fresh port (which is a new origin the pane must approve;
`preview_start {url}` reopens the pane after a reset).

**A green check you cannot make go red is worth nothing.** Both browser tools have now reported a
clean pass while measuring nothing at all — the audit once swept 0 elements and said "0 failures",
and a stale service-worker copy of `audit.js` later passed a placeholder bug it could not see. So
after touching either tool, break the thing on purpose and confirm the tool says so. Writing the
assertion is the easy half. `tools/selftest.js` was mutation-tested this way, and it caught a test
of mine that pinned nothing: it set `_syncOn=false` when the real bug was `_syncOn=true` with no
token, so the broken predicate passed it.

**Contrast audits lie in three specific ways.** Use `tools/audit.js`, which handles all three:
transitions must be killed before measuring (mid-transition reads produced ~300 phantom failures),
gradient-backed text can't be composited and must be skipped, and closed overlays plus inactive
state branches are invisible to a naive sweep — that's where real bugs hide.

**Gemini quota is per key, so fan out.** `geminiParallel(jobs)` runs one lane per key at once;
`geminiCall(...,{startAt:i})` pins the first key tried and `{only:true}` disables fallback (needed
for a per-key health check, or a dead key passes on someone else's quota). Calls round-robin from
`GEM_CURSOR` — before that the loop always began at `keys[0]`, so five extra keys did nothing but
sit there as failover. Anything expensive and fan-out-shaped belongs on this path, not in a loop.

**Bulk jobs must not cascade.** By default `geminiCall` retries a failed request across every key
*and* every model — fine for one call, ruinous for 22, where a single throttled book spends all five
keys' quota and the run finishes half the shelf. Bulk callers pass `{maxKeys:2,maxModels:2}` plus a
`gap`, keep prompts small (~4KB, not 10KB), and treat a partial result as normal: mining is
incremental, so re-running only fetches what's missing.

**Never let a model produce a quote.** It will invent them, and a fabricated quote attributed to a
book Hassan owns is the one unrecoverable failure here. Sources in a forged lesson are the verbatim
passages retrieval found, with the real book and chapter attached — the model writes the *prose*
around them, never the evidence itself.

**Retrieval matches whole words** (`hasWord`), not substrings. `includes` had a lesson about holding
your TEMPER quoting "barometric TEMPERature", and `hold` matching inside `household`. Up to two
trailing letters are allowed so `temper` still finds `tempers`.

**Streaming:** `geminiAsk(prompt, onChunk, …)` streams via SSE and falls back to `geminiCall` on any
failure. Paint chunks by writing into the existing bubble — re-rendering the whole thread per token
rebuilds the input and steals focus mid-sentence.
**`onChunk(cumulative, delta)` — the first argument is EVERYTHING SO FAR, not the new piece.**
Assign it (`acc = partial`), never append. Appending grows the answer quadratically: the first live
run of ask-the-library printed the same paragraph four times, each copy longer than the last.

**Generate on a schedule, not once.** A feature that calls Gemini once and caches the result forever
is a static feature with an API bill — Hassan's actual complaint, twice. `autoRefreshHooks()` rotates
six books a day from `landing()` and on `visibilitychange`, claiming the day in `_meta.day` *before*
the run so a reload can't double-fire. Crucially the sampler is **seeded by the date**: deterministic
sampling would re-send identical passages and get identical output back, spending quota to look busy.
Verified end-to-end — the same book on two days returned five hooks each with zero overlap.

**Derived AI content goes in its own localStorage key, never in `S`.** `vault_hooks` is ~20KB of
regenerable text; `S` is real progress and is pushed to the sync gist on every save. What the user
*did* with that content (`S.hookSeen`) is progress and does belong in `S`.

**Never feed the model `ep.t` blindly.** Most episode titles are `"Episode 133"` — this app's own
chunk numbering — and a model handed one cites it back at the reader as a source. Pass chapter
titles only when they are real. Strip markdown on render too (`demd`); asking for plain prose in the
prompt does not stop it, and the answer is rendered as `textContent`, so asterisks show up literally.

**Colours baked at render time don't follow the theme.** A CSS variable can't fix a colour already
written into an inline style. If you write `style="color:${...}"` during render, the root view must
re-render on theme change — that's what `refreshRoot()` is for.

**New state fields must be added to `mergeState`,** or they won't survive cross-device sync.
Deletions need tombstones (`S.hlDel`) or sync resurrects them; an undo must lift the tombstone too.
This rule was documented here and still got broken five times in one session — `forged`, `gauntlet`,
`council`, `hookSeen`, `dispatchSeen` were all silently dropped on the first sync from another
device. `selftest.js` now has a class guard ("no field from the other device is silently dropped");
**add the new field to that fixture** when you add it to `S`, or the guard cannot see it either.

**Removing a form field?** Grep the render function for leftover `$("id")` refs — a null throw
before `classList.add("on")` silently breaks the whole overlay.

**Text damage hides in valid Unicode.** The 3.43 pass fixed control bytes and private-use
ligatures, so every later check reported the corpus clean — while a second subset font had parked
its ligatures on *real letters*: "first" stored as "ɹrst" (IPA turned-r), every jhāna in Bliss
Beyond as "jh›na". Nothing is invalid, nothing renders as a box, and search silently misses the one
book that is entirely about jhānas. When looking for damage, sweep for *implausible* characters —
IPA in an English book, Cyrillic homoglyphs, a lone `›` — not just invalid ones. Each damaged code
point turned out to be confined to exactly one book, which is the signature of a per-PDF font quirk
and is itself the evidence the mapping is real.

**Repair with the corpus as the dictionary, never with a guess.** `cleantext.py` builds a set of
every word the library already spells correctly (seen 2+ times in 13.3M chars) and only applies an
ambiguous fix when the result is in it — U+0283 is "ff" in "suʃered" but "ffi" in "suʃcient", and
the dictionary decides which. Same rule rejoins line-break hyphens: 306 joined, **248 declined**
because "Christa/pher" and "Gilga/mesh" would have become words that do not exist. Declining is the
feature.

**Before stripping a character wholesale, print its real context.** `~` looked like pure OCR noise
(636 of them) — it is also the attribution dash in Covert 30 ("~ Caesar"), the separator in Quiet
Influence ("Confucius ~ Rumi"), and part of a **real URL** in Thinking Fast and Slow
(`princeton.edu/~kahneman/docs/`). A blanket strip corrupts all three. Only a guillemet or tilde
with a letter on *both* sides is treated as a hyphen; the rest is reported, not touched.

**A repair that deletes real information is worse than the damage.** The first title cleaner
rewrote 405 titles when 47 were damaged — it "fixed" the genuine "Chapter 2 (Pages 17-56)" down to
"Chapter 2" and ate the page ranges from all 40 Right Concentration chapters because `|` is a real
separator there. Gate a repair on evidence of damage, then dump every before/after and read them
before writing. Titles fall back to `"Episode N"`, never `""` — `esc(ep.t)` has no fallback of its
own, so a blank title renders as a blank CONTINUE card.

**Never repair text with `str.replace(token, ...)`.** It rewrites every occurrence of that
substring, and damaged tokens overlap: a paragraph held both `oʃcially` and a stray `oʃ`, and
because `oʃ` is a prefix of the longer word, expanding it first turned `oʃcially` into `offcially`
— then that word's own pass had nothing left to match. It shipped in 3.55 and put a word in
Hassan's book that appears **zero** times in the original scan. Substitute match-by-match with
`re.sub(pattern, fn, s)` so every occurrence is resolved independently. `cleantext.py --selftest`
pins this exact collision; restoring the old code makes it fail with `offcially`.
Corollary: **re-repair from the pristine original, never patch on top of a bad repair** — the
damaged character is already gone, so the second pass cannot see what went wrong. `--fix` moves the
input to `books.json.bak`, which is what made the redo possible; copy it somewhere safe first.

**Felt figures (#155) are staged diagrams, not decoration.** The 43 keyword-matched `FIGURES` in
the reader are decoration; a `fig` on a Path node is authored for that lesson and answers what
prose is bad at — where attention goes, what it should feel like, in what order (the reference is
Hassan's account of finding a heartbeat internally: fingertips, then soles, then everywhere).
- **Specs are DATA, components are CODE.** The spec ships in `content.enc`; `FIGC` + `renderFig`
  live in `index.html`. Same split as the rest of the app. ~0.5KB a figure.
- **A figure must show the MECHANISM, not the sensation's location.** First heartbeat figure drew
  expanding rings where the pulse is felt, on a stick figure. Hassan's correction was the design:
  the body is a balloon under building pressure and the beat *travels* from the heart to the ends.
  `flow` draws the route, runs a segment along it (`pathLength="100"` normalises every route so
  near and far stay in step) and swells the destination as it lands, staggered so distant points
  arrive later. Reach for "what is actually happening" over "where you notice it".
- **Stick figures cannot be under pressure.** Bodies are filled silhouettes so they can swell.
- **Components publish anchors; layers attach to them.** `hand` exposes `fingertips`, `feet`
  exposes `soles`; `pressure` reads whatever the body before it published. Order matters —
  `pressure` alone falls back to centre. That indirection is what makes the figure teachable
  rather than hard-coded, and `figTests` pins it (10 rings on 5 pads, 4 on 2 soles).
- **`FIG_COMPONENTS` in `build.py` mirrors `FIGC`.** Extend both together or a spec validates and
  then draws nothing. The gate refuses unknown components, missing `alt`, empty scenes, markup in
  captions and an out-of-range `place` — all five mutation-tested.
- Captions are real text so `VA` can measure them; stage controls are real `<button>`s. Staging one
  in the audit needs `#node` shown first — `scan()` skips anything with no `offsetParent`, so the
  first attempt measured nothing and honestly said `unmeasured: feltfig`.
- Only the figure on screen animates (`figPulse`, scroll + `visibilitychange` — **not**
  IntersectionObserver, which is unreliable in the pane). Reduced motion keeps the stages, drops
  the movement.
- The content fingerprint hashes **book prose only**, so adding figures does not bin derived
  caches — checked deliberately: nothing derived quotes figures, and a figure edit should not throw
  away 20KB of good hooks. Revisit if a future feature starts quoting them.

**Added books must pass the Weave, or they sit beside the graph rather than in it.**
`gemini_pipeline.merge_nodes` sets `"prereq":[prev]` — every generated track is a chain with zero
edges out of it (measured: hand-built tracks share 19 cross-track prereqs, pipeline tracks 0), and
its cross-references live only in bridge prose. `tools/integrate.py` fixes that:
`--orphans` surveys, `--track X` judges, `--track X --apply` writes. Five rules it enforces:
- Edges point **new → old only**, so a cycle is structurally impossible (build.py still checks).
- A prereq edge is auto-applied **only when the target is already read** (`--done`), because a
  wrong prereq locks a reader out of a lesson. Everything else demotes to `rel` and is listed.
- **`tier` is AUTHORED, not derived.** Recomputing depth graph-wide from prereqs rewrote 62 nodes
  across every other track and pushed each track's opening lesson off tier 0. Only a node that
  gained a prereq in this run may move, only deeper. Nothing outside the track is ever touched.
- The judge is a **forced choice over ids**, not a yes/no per pair: asked "are these related?" one
  pair at a time it answered KINSHIP to *every* pair including deliberately unrelated ones. Given
  a numbered list it miscounted and named a candidate that did not exist. Ids, and "choose at most
  one, or none", is what finally discriminated. Verify that on unrelated nodes before trusting it.
- `rel` is optional, undirected kinship. It gates nothing; `relOf()` in the client only surfaces
  partners the reader has already finished.

**`extract.py` rewrites the WHOLE of `books.json` from the PDFs.** It applies only the
per-paragraph repairs (`cleantext.clean`); everything corpus-wide — resolving ambiguous ligatures,
rejoining line-break hyphens, letter-level OCR correction, the junk-title gate — needs a vocabulary
built from the whole library and cannot run per paragraph. So a re-extract used to silently discard
every repair 3.55 and 3.57 made and regress the books to "the ɹrst law". It now shells out to
`cleantext.py --fix` itself and fails loudly if that step does not succeed. **Never hand-roll a
second copy of the repair logic** — the one in `cleantext.py` is the one with the pinned regression.
`cleantext.py` also scores every book for scan-damage (rare tokens unique to it, per 1000 words) and
names any that look scanned but are missing from `SCANNED`, which is otherwise a hardcoded pair that
goes quietly wrong the moment a scanned book is added.

**Nothing in the library is a page scan any more** (1 Aug 2026 — Hassan replaced 48 Laws and
Meditations with text editions, and swapped the Bliss Beyond ch.1–4 excerpt and the Right
Concentration *summary* for the real books). `SCANNED` is now empty and no book gets letter-level
correction. The detector still scores every book on every run: laws48 20 and meditations 13 per
1000 look scan-like but are **false positives** — sampled and they are Greene's historical proper
nouns and an archaic translation's classical names (`aesculapius`, `agrigentum`, `abideth`).
Sample before believing that number. The section below is kept because the reasoning is what
matters if a scan is ever added again.

**A text edition can drop the line-break hyphen entirely**, leaving "accumu lation" and "knowl
edge" split across a plain space — no stray character for the guillemet rejoin to anchor on.
`rejoin_splits()` walks TOKENS, not `re.sub`: a substitution consumes both words, so in "for knowl
edge" it matches "for knowl", declines it and has already eaten the fragment. Repeating does not
help — a declined match leaves the string identical, so every pass aligns the same way.
Two safety rules, both needed: the first half must not be a word (that is what stops
*the rapist* → *therapist*), **or** must be rarer than the joined word — because a fragment split
seven times appears seven times and otherwise vouches for itself as real. `build_vocab` returns
counts, not a set, for exactly that comparison.

**Only two books were scans, and only they got letter-level repair.** Measured, not assumed:
rare tokens unique to a book, per 1000 words — `laws48` 34.6, `meditations` 17.1, every other book
2.0–9.5. Those two are page images with the scanner's own bad reading baked into the text layer
(the 48 Laws PDF is 476 image pages), so `vvith`/`frorn`/`pcople` are damage. **In a typed book a
rare word is a rare word**: `clown`, `clone`, `eases`, `wafer` and `farce` all live in clean books,
and a corpus-frequency dictionary will "fix" them into down/done/cases/water/force. Re-extraction
cannot help these two — the garbage *is* the text layer — and there is no OCR tool installed.

**A corpus dictionary cannot recognise real words the corpus never uses.** The automatic gate
(rare + scan-only + unique candidate + common target) still proposed `trajan`→`trojan` (Trajan is
an emperor Greene discusses), `aught`→`ought` (archaic English, in an archaic translation),
`carnage`→`carriage`, `defecting`→`detecting` and `filing`→`filling`. `DENY` in `cleantext.py`
holds the 21 reviewed exceptions; it is a judgement, written out in the open so it can be argued
with, not derived. **Generate the list, read all of it, then apply** — `--list` prints it.
Where a scan contradicts itself the PDF settles it rather than inference: the 48 Laws scan prints
each law twice, and page 9's "Iyrrhir" is page 91's "Pyrrhic". `javiac` looked like damage and is
a real place name in the same PDF. The books live in `Desktop\forbidden\*.pdf` — read them.

**Derived AI content must be invalidated when the source text changes.** Repairing the books left
every mined hook still quoting the old damaged text, cached per book, and the daily refresh only
rotates six books at a time — so `jh›na` would have kept surfacing for days. `build.py` hashes the
prose into `payload["gen"]`, and `pruneStaleHooks()` (called from `landing()`, since `HOOKS` is
built at parse time before `DATA` exists) bins `vault_hooks` when the stamp differs. It is ~20KB of
regenerable text, so throwing it away costs nothing.
**This started as a hand-bumped `const CONTENT_GEN` and lasted exactly one release** — 3.57 rewrote
159 words and left it at 2. If a rule says "remember to bump X", the rule is the bug: derive it.

**`S.read` says THAT, never WHEN.** It is `{bookId:[episodeIndex,…]}` — flat, unioned across
devices, tombstoned against. Anything needing "what did I read yesterday" uses `S.readLog`
(`{"YYYY-MM-DD":[[bookId,ep],…]}`, seven days, written by `logRead` inside `markRead` — the single
choke point every read passes through) and `readOn(day)`. Do **not** add timestamps to `S.read`
itself: `mergeState` unions it and `S.readDel` tombstones against it, and neither survives a shape
change. The merge unions per day so two devices reading on the same date both count.

**`restoreVault` is a deliberate REPLACE, and that is correct** — checked, not assumed. It confirms
with the backup's date, overwrites `vault_state` wholesale, offers to make the backup authoritative
in the cloud too (otherwise the next sync merges the old state straight back — #29), then reloads,
which is also why no achievement-toast storm is possible. Do not "fix" it into a merge.

**NaN is the worst possible failure value here.** A review record merged from another device without
its `k` interval index made `Math.min(undefined,1)` → NaN → `RV_DAYS[NaN]` → `undefined` → a `due`
of NaN. Nothing throws, and `NaN <= now` is false forever, so the idea left Sharpen **permanently
and silently**. Anything that computes a date or a score from stored state must clamp on the way in
(`rvClamp`) — a thrown error gets reported, a NaN never does.

**A dot on a button the phone hides is a notification nobody gets.** 3.54 moved ten icons into ☰
and silently took the 📜 patch and 📰 Dispatch unread markers with them. Anything that toggles
`hasnew` must call `syncMenuBadge()`, which mirrors the marker onto ☰ — but only while
`matchMedia("(max-width:820px)")` matches, or desktop shows the dot twice.

**The top bar is not a shelf, and nothing was measuring it.** Adding one icon per release took the
row from 8 buttons to 14; at the 44px tap-target minimum that needs 668px and a phone has 353. Five
buttons sat off-screen, and because the row is `overflow:visible` the *document* went 583px wide, so
every view panned sideways — the bug read as "the whole page is broken", not "the bar is too long".
The fix is default-hidden: under 820px an `.iconbtn` is `display:none` unless it opts in with
`.keep`, and the ☰ menu builds its rows from the same `.iconrow`, so a button added later is
listed automatically and *cannot* re-break the layout. Two rules follow from this:
- The menu tests availability with `b.style.display`, **not** `getComputedStyle` — on a phone the
  CSS hides the whole row, so a computed check reports an empty menu, correctly and uselessly.
- Every `.iconbtn` title reads `Name — what it does`; the menu splits on that em dash. `selftest.js`
  fails the build if one is missing, along with the width sum and any icon reachable from neither.

**Phone widths must be tested in an iframe.** The in-app browser pane refuses to go below ~583px —
`resize_window({preset:"mobile"})` cheerfully returns "Viewport set to 375x812" and leaves
`innerWidth` at 583, i.e. above the 560 breakpoint, so the phone CSS never even applies. An iframe
gets its own viewport for media queries, so this actually tests a phone:
`f.style.width="375px"; f.src="/index.html#k="+key`, then probe `f.contentDocument`. Reach app
internals with `f.contentWindow.eval(src)` (indirect eval sees the lexical `const`s; the parent
frame cannot). `VA.fits()` is the reusable form of the probe.

**`cache:"reload"` on a fetch is not enough once the SW is gone.** Re-fetching `selftest.js` that
way returned the pane's stale disk copy, so a mutation test re-installed the *old* assertion and
reported that breaking the layout on purpose changed nothing. A `?x=`+timestamp query works here —
the `{ignoreSearch:true}` warning above only applies while a service worker is registered.
The first version of that same width guard also counted the wrong buttons (it excluded `btn-menu`,
which occupies exactly as much room as any other) and passed a five-button bar. **Mutate every new
assertion in both directions before believing it.**

## Conventions

**Theme vars** live in `:root`, overridden by `:root[data-theme="light"]` and `[data-theme="sepia"]`:
`--bg --bg2 --card --card2 --tx --tx2 --gold --goldbtn --jade --line --read --lh --rw --read-font
--overlay --sticky --err --ok --ai`.

`--gold` is a *text* accent and darkens on light themes. `--goldbtn` is fixed bright, for filled gold
buttons with black text. They pull in opposite directions — don't collapse them back into one.

**Overlays** are `.overlay > .panel > h2 > button.x[data-close]`. Toggle with `.classList.add("on")`.
Check the existing markup before inventing class names.

**Verify with one call, not forty-five lines.** Paste `tools/verify.js` and run `VV.all({stage:1})`:
it unregisters the service worker, clears caches, builds a 375px iframe (the pane cannot resize
below ~583px and will report a phone while testing a tablet), stages the states where bugs actually
live — a half-finished track, an overdue idea, a pre-repair highlight — then runs the selftest, the
overflow check and all three themes, and prints one `VERDICT` line. Retyping that setup inline on
every pass was the largest avoidable cost in a working session; `{w:1200}` for the desktop chrome.

**Verify in the browser with DOM probes,** not screenshots — screenshots, IntersectionObserver and
rAF don't fire reliably in the in-app pane. Clear `vault_state` on the github.io origin after testing
so Hassan's real progress isn't polluted.

## Working style

Ship in verified batches: syntax-check → browser-test → `ship.py`. When Hassan says "continue" it
means work autonomously — if the task list is done, generate the next batch and start, without
asking. Every pass, re-audit recently-touched UI for theme/contrast regressions in your own prior
work; that's where the recurring bugs have been.
