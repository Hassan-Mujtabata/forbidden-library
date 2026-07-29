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
| `tools/audit.js` | Browser-side contrast audit. Paste into `javascript_tool`. Returns terse JSON. |
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

**Removing a form field?** Grep the render function for leftover `$("id")` refs — a null throw
before `classList.add("on")` silently breaks the whole overlay.

## Conventions

**Theme vars** live in `:root`, overridden by `:root[data-theme="light"]` and `[data-theme="sepia"]`:
`--bg --bg2 --card --card2 --tx --tx2 --gold --goldbtn --jade --line --read --lh --rw --read-font
--overlay --sticky --err --ok --ai`.

`--gold` is a *text* accent and darkens on light themes. `--goldbtn` is fixed bright, for filled gold
buttons with black text. They pull in opposite directions — don't collapse them back into one.

**Overlays** are `.overlay > .panel > h2 > button.x[data-close]`. Toggle with `.classList.add("on")`.
Check the existing markup before inventing class names.

**Verify in the browser with DOM probes,** not screenshots — screenshots, IntersectionObserver and
rAF don't fire reliably in the in-app pane. Clear `vault_state` on the github.io origin after testing
so Hassan's real progress isn't polluted.

## Working style

Ship in verified batches: syntax-check → browser-test → `ship.py`. When Hassan says "continue" it
means work autonomously — if the task list is done, generate the next batch and start, without
asking. Every pass, re-audit recently-touched UI for theme/contrast regressions in your own prior
work; that's where the recurring bugs have been.
