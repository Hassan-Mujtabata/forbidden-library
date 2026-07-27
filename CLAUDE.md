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
| `tools/bump.py` | Bumps `APP_VER` + `CACHE` together. `ship.py` calls it; rarely run directly. |
| `tools/build.py` | Validates the graph (acyclic, prereqs resolve) → rebuilds `content.enc`. |
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

**Contrast audits lie in three specific ways.** Use `tools/audit.js`, which handles all three:
transitions must be killed before measuring (mid-transition reads produced ~300 phantom failures),
gradient-backed text can't be composited and must be skipped, and closed overlays plus inactive
state branches are invisible to a naive sweep — that's where real bugs hide.

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
