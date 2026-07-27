# -*- coding: utf-8 -*-
"""One command to release The Vault: check -> bump -> commit -> rebase -> push.

    python tools/ship.py           # auto-increment the minor version
    python tools/ship.py 3.41      # ship an explicit version
    python tools/ship.py --dry     # run every check, change nothing
    python tools/ship.py --no-push # commit locally, don't push

The release name and commit message come from the PATCHES entry in index.html, so a
release physically cannot ship without patch notes. Add the entry first:

    {v:"3.41",name:"Name Of Release",items:[["new","..."],["fix","..."]]}

Checks, in order, all of which abort before anything is committed:
  1. no secret or gitignored-plaintext file is about to be committed
  2. access.json is untouched  (Hassan's config -- off limits)
  3. no API-token-shaped strings in the staged text
  4. every inline <script> in index.html passes `node --check`
  5. a PATCHES entry exists for the version being shipped

What this CANNOT check is the browser: run tools/audit.js for contrast and click through
the feature before shipping. Everything else is mechanical, so it lives here.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
IDX = os.path.join(ROOT, "index.html")
TOKEN_FILE = r"C:\Users\sands\.secrets\github_token.txt"

# Files that must never reach the public repo. Plaintext lesson content in a public repo
# would defeat the whole point of encrypting content.enc.
FORBIDDEN = [
    re.compile(r"(^|/)key\.txt$"),
    re.compile(r"(^|/)books\.json$"),
    re.compile(r"(^|/)graph\.json"),
    re.compile(r"(^|/)\.gemini_keys$"),
    re.compile(r"\.pdf$", re.I),
    re.compile(r"github_token"),
]
# Token shapes: GitHub classic / fine-grained, Google API keys.
SECRET_RE = re.compile(r"\b(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AIza[A-Za-z0-9_\-]{30,})")

FAILED = []


def run(args, check=True, quiet=False):
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0 and not quiet:
        out = ((p.stdout or "") + (p.stderr or "")).strip()
        die("command failed: %s\n%s" % (" ".join(args[:3]), out[:600]))
    return p


def die(msg):
    print("\n[FAIL] " + msg)
    sys.exit(1)


def ok(msg):
    print("  [ok] " + msg)


def read(p):
    return open(p, encoding="utf-8", newline="").read()


# ---------------------------------------------------------------- checks

def pending_files():
    """Everything that `git add -A` would stage, including untracked."""
    p = run(["git", "status", "--porcelain", "--untracked-files=all"])
    files = []
    for line in p.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:].strip().strip('"')
        if " -> " in path:                       # renames
            path = path.split(" -> ")[-1]
        files.append(path)
    return files


def check_files(files):
    bad = [f for f in files for rx in FORBIDDEN if rx.search(f)]
    if bad:
        die("refusing to commit protected file(s):\n    " + "\n    ".join(sorted(set(bad))) +
            "\n  These are gitignored for a reason. Check .gitignore wasn't bypassed with -f.")
    ok("no protected files staged")

    if any(f.endswith("access.json") for f in files):
        die("access.json is modified. That file is Hassan's config and is off limits.\n"
            "  Revert it (git checkout -- access.json) and ship again.")
    ok("access.json untouched")


def check_secrets(files):
    hits = []
    for f in files:
        full = os.path.join(ROOT, f)
        if not os.path.isfile(full) or os.path.getsize(full) > 4_000_000:
            continue
        try:
            body = open(full, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        m = SECRET_RE.search(body)
        if m:
            hits.append("%s (%s...)" % (f, m.group(0)[:10]))
    if hits:
        die("token-shaped string found in:\n    " + "\n    ".join(hits) +
            "\n  Move it to an env var or a gitignored file.")
    ok("no token-shaped strings")


def check_syntax():
    html = read(IDX)
    blocks = re.findall(r"<script([^>]*)>(.*?)</script>", html, re.S | re.I)
    checked = 0
    for attrs, body in blocks:
        if "src=" in attrs.lower():
            continue
        t = re.search(r'type\s*=\s*["\']([^"\']+)', attrs, re.I)
        if t and t.group(1).lower() not in ("text/javascript", "module", "application/javascript"):
            continue                              # JSON-LD, templates, etc.
        if not body.strip():
            continue
        tmp = os.path.join(HERE, "_syntax_check.js")
        open(tmp, "w", encoding="utf-8").write(body)
        try:
            p = subprocess.run(["node", "--check", tmp], capture_output=True, text=True,
                               encoding="utf-8", errors="replace")
            if p.returncode != 0:
                msg = (p.stderr or "").strip()
                # node reports line numbers against the extracted block, not index.html
                die("JavaScript syntax error in index.html:\n" + msg[:800] +
                    "\n  (line numbers are relative to the <script> block)")
        except FileNotFoundError:
            print("  [--] node not found, skipping syntax check")
            return
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)
        checked += 1
    ok("node --check passed (%d inline script block%s)" % (checked, "" if checked == 1 else "s"))


def patch_entry(version):
    """Find the PATCHES entry for this version and return its release name."""
    html = read(IDX)
    m = re.search(r'\{\s*v\s*:\s*"%s"\s*,\s*n\s*:\s*"([^"]+)"' % re.escape(version), html)
    if not m:
        die('no PATCHES entry for %s in index.html.\n'
            '  Add one at the TOP of PATCHES (newest first) before shipping:\n'
            '    {v:"%s",n:"Your Release Name",d:"%s",items:[["new","..."]]}'
            % (version, version, __import__("datetime").date.today().strftime("%d %b %Y")))
    ok('patch notes present: "%s"' % m.group(1))
    return m.group(1)


def next_version():
    m = re.search(r'const APP_VER="(\d+)\.(\d+)";', read(IDX))
    if not m:
        die("couldn't find APP_VER in index.html")
    return "%s.%d" % (m.group(1), int(m.group(2)) + 1)


# ---------------------------------------------------------------- ship

def push():
    """Push over HTTPS using the PAT, without ever printing it."""
    token = None
    if os.path.exists(TOKEN_FILE):
        token = open(TOKEN_FILE, encoding="utf-8").read().strip()
    if not token:
        p = run(["git", "push"], check=False)
        if p.returncode != 0:
            die("push failed and no token at %s\n%s" % (TOKEN_FILE, (p.stderr or "")[:400]))
        return
    url = "https://%s@github.com/Hassan-Mujtabata/forbidden-library.git" % token
    p = subprocess.run(["git", "push", url, "HEAD:main"], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        die("push failed:\n" + (p.stderr or "").replace(token, "<token>")[:400])
    # Pushing to an explicit URL does not move origin/main, so every check afterwards would
    # report "1 ahead" on an already-pushed commit. Refresh the tracking ref.
    run(["git", "fetch", "origin"], check=False)


def main():
    args = [a for a in sys.argv[1:]]
    dry = "--dry" in args or "--check" in args
    nopush = "--no-push" in args
    rest = [a for a in args if not a.startswith("--")]

    msg = None
    if "-m" in args:
        i = args.index("-m")
        if i + 1 >= len(args):
            die("-m needs a message")
        msg = args[i + 1]
        rest = [a for a in rest if a != msg]

    files = pending_files()
    if not files and not dry:
        die("nothing to commit.")

    # A commit that doesn't touch the app shell isn't a release: no version, no patch
    # notes, no cache bump. Tooling and docs go out as ordinary commits.
    release = any(f in ("index.html", "sw.js") for f in files)

    version = None
    if release:
        version = rest[0] if rest else next_version()
        if not re.fullmatch(r"\d+\.\d+", version):
            die("version must look like 3.41, got %r" % version)
        print("The Vault -> %s%s" % (version, "   (dry run)" if dry else ""))
    else:
        print("Tooling commit (index.html untouched)%s" % ("   (dry run)" if dry else ""))

    check_files(files)
    check_secrets(files)
    check_syntax()
    name = patch_entry(version) if release else None

    if dry:
        print("\nAll checks passed. %d file(s) ready. Nothing was changed." % len(files))
        if release:
            print("Browser check still owed: paste tools/audit.js, run VA.run() per theme.")
        return

    if release:
        run([sys.executable, os.path.join(HERE, "bump.py"), version])
        ok("bumped APP_VER + sw CACHE")

    run(["git", "add", "-A"])
    staged = run(["git", "diff", "--cached", "--name-only"]).stdout.split()
    if any(f.endswith("access.json") for f in staged):
        die("access.json ended up staged. Unstage it and ship again.")
    run(["git", "commit", "-m", "%s: %s" % (version, name) if release else (msg or "tools: update")])
    ok("committed")

    run(["git", "fetch", "origin"], check=False)
    behind = run(["git", "rev-list", "--count", "HEAD..@{u}"], check=False).stdout.strip()
    if behind.isdigit() and int(behind) > 0:
        run(["git", "rebase", "@{u}"])
        ok("rebased onto %s upstream commit(s)" % behind)

    if nopush:
        print("\nCommitted locally, not pushed (--no-push).")
        return
    push()
    ok("pushed")

    sha = run(["git", "rev-parse", "--short", "HEAD"]).stdout.strip()
    if release:
        print("\n%s \"%s\" shipped as %s. Files: %d." % (version, name, sha, len(staged)))
        print("Pages lags -- verify by grepping the live index.html, not the build status.")
    else:
        print("\nPushed %s. Files: %d. No version bump (app shell untouched)." % (sha, len(staged)))


if __name__ == "__main__":
    main()
