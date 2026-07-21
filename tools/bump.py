# -*- coding: utf-8 -*-
"""#92: bump APP_VER (index.html) and the service-worker CACHE (sw.js) together.

Editing index.html without bumping sw.js's CACHE makes the service worker serve a stale
copy — the #1 source of "it's broken" reports. Run this before every deploy that touches
index.html or sw.js:  python tools/bump.py            (auto-increments the minor version)
                       python tools/bump.py 3.20       (sets an explicit version)
"""
import re, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.join(HERE, "..", "index.html")
SW = os.path.join(HERE, "..", "sw.js")


def read(p):
    return open(p, encoding="utf-8", newline="").read()   # newline="" preserves existing LF endings


def write(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


def main():
    idx = read(IDX)
    m = re.search(r'const APP_VER="(\d+)\.(\d+)";', idx)
    if not m:
        print("FAIL: couldn't find APP_VER in index.html"); sys.exit(1)
    new_ver = sys.argv[1] if len(sys.argv) > 1 else f"{m.group(1)}.{int(m.group(2)) + 1}"

    sw = read(SW)
    mc = re.search(r'const CACHE = "vault-v(\d+)";', sw)
    if not mc:
        print("FAIL: couldn't find CACHE in sw.js"); sys.exit(1)
    new_cache = int(mc.group(1)) + 1

    write(IDX, re.sub(r'const APP_VER="[\d.]+";', f'const APP_VER="{new_ver}";', idx, count=1))
    write(SW, re.sub(r'const CACHE = "vault-v\d+";', f'const CACHE = "vault-v{new_cache}";', sw, count=1))
    print(f"APP_VER -> {new_ver}   CACHE -> vault-v{new_cache}")
    print("Now add a PATCHES entry for", new_ver, "in index.html, then rebuild + commit.")


if __name__ == "__main__":
    main()
