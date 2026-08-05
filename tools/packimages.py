# -*- coding: utf-8 -*-
"""
#166 JOB 1, part 2 — place the extracted figures in the right chapter and ship them encrypted.

WHY NOT INSIDE content.enc. Size is not a constraint on this project, but LOAD ORDER is: the app
cannot render anything until content.enc is fetched and decrypted, so folding 39MB of photographs
into it would mean staring at a spinner before the first word of text. The figures go into one
encrypted bundle per book, fetched only when that book is opened. Same key, same AES-GCM, same
"public repo is fine because it is encrypted" — just not on the critical path.

    python tools/packimages.py            # -> ../img/<bookid>.enc  + refs in books.json
"""
import base64, gzip, json, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(HERE, "bookimg")
BOOKS = os.path.join(HERE, "books.json")
KEYFILE = os.path.join(HERE, "key.txt")
OUT = os.path.join(HERE, "..", "img")


def main():
    books = json.load(open(BOOKS, encoding="utf-8"))
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    os.makedirs(OUT, exist_ok=True)
    placed_total = orphan_total = 0
    report = []

    for b in books["books"]:
        bid = b["id"]
        mpath = os.path.join(IMGDIR, bid, "manifest.json")
        if not os.path.exists(mpath):
            continue
        man = json.load(open(mpath, encoding="utf-8"))
        # episode page ranges, in order
        eps = [(i, e.get("pg")) for i, e in enumerate(b["episodes"])]
        ranged = [(i, pg) for i, pg in eps if pg]

        bundle, placed, orphan = {}, 0, 0
        for e in b["episodes"]:
            e.pop("img", None)                       # idempotent: never accumulate on re-run
        for item in man["images"]:
            page = item["page"]
            hit = None
            for i, (lo, hi) in ranged:
                if lo <= page <= hi:
                    hit = i
                    break
            if hit is None:                          # page fell in a gap (front matter, plates)
                nearest = min(ranged, key=lambda r: min(abs(page - r[1][0]), abs(page - r[1][1])),
                              default=None)
                if nearest and min(abs(page - nearest[1][0]), abs(page - nearest[1][1])) <= 2:
                    hit = nearest[0]
                else:
                    orphan += 1
                    continue
            data = open(os.path.join(IMGDIR, bid, item["f"]), "rb").read()
            ref = item["f"]
            bundle[ref] = base64.b64encode(data).decode("ascii")
            ep = b["episodes"][hit]
            ep.setdefault("img", []).append({"f": ref, "w": item["w"], "h": item["h"]})
            placed += 1

        if not bundle:
            continue
        raw = json.dumps(bundle, separators=(",", ":")).encode("utf-8")
        blob = gzip.compress(raw, 6)                 # base64 of JPEG barely shrinks; 6 is plenty
        iv = os.urandom(12)
        ct = AESGCM(key).encrypt(iv, blob, None)
        open(os.path.join(OUT, bid + ".enc"), "wb").write(iv + ct)
        placed_total += placed
        orphan_total += orphan
        report.append((b["title"], placed, orphan, len(iv + ct)))

    json.dump(books, open(BOOKS, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print("%-42s %7s %8s %10s" % ("BOOK", "placed", "orphans", "bundle"))
    for t, p, o, sz in sorted(report, key=lambda r: -r[1]):
        print("%-42s %7d %8d %9.1fMB" % (t[:42], p, o, sz / 1e6))
    print()
    print("placed %d figures, %d could not be located in any chapter" % (placed_total, orphan_total))
    print("bundles ->", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
