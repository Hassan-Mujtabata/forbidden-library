# -*- coding: utf-8 -*-
"""
#166 JOB 1 — pull every real figure out of the book PDFs.

The library has 0% of the books' own images. For several books the pictures ARE the teaching:
What Everybody Is Saying is about reading body language, TMI's diagrams carry its model of
attention. Text-only extraction threw all of it away.

WHAT COUNTS AS A REAL FIGURE. Not every image object in a PDF is a picture from the book. Page
furniture — a rule, a footer, a chapter ornament — is embedded once per page and shows up as
hundreds of "images". The 48 Laws reports 956 image objects and almost all of them are one
repeating footer; TMI reports 128 and 123 of them are genuine. So:
  - drop anything whose identical bytes appear on 4+ pages          (furniture)
  - drop anything smaller than MIN_W x MIN_H                        (bullets, rules, icons)
  - drop anything with an extreme aspect ratio                      (dividers, sidebars)
Everything surviving is kept at full quality. Size is not a constraint on this project.

  python tools/bookimages.py --inventory     # count + measure, writes nothing
  python tools/bookimages.py                 # extract to tools/bookimg/<id>/
"""
import os, sys, io, json, hashlib, argparse
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Users\sands\OneDrive\Desktop\forbidden"
OUTDIR = os.path.join(HERE, "bookimg")

MIN_W, MIN_H = 180, 140          # below this it is an icon, not a figure
MAX_ASPECT = 6.0                 # a 10:1 strip is a divider
FURNITURE_PAGES = 4              # same bytes on this many pages = page furniture


def books():
    """the id -> pdf mapping already lives in extract.py; reuse it rather than duplicate"""
    sys.path.insert(0, HERE)
    import extract
    return [(m["id"], m["title"], os.path.join(ROOT, m["file"])) for m in extract.BOOKS]


def harvest(pdf):
    """every image object with its page, deduped by content hash.

    #166: the first version used fitz.Pixmap() inside a bare `except: continue`. Pixmap throws on
    several perfectly ordinary encodings (JPX, JBIG2, some masked images) and the bare except
    swallowed every one — What Everybody Is Saying, a book of photographs, reported THREE images
    for 269 pages. doc.extract_image() returns the stored bytes without re-rasterising and handles
    those cases; Pixmap is now only the fallback. Failures are counted and returned, never hidden.
    """
    import fitz
    doc = fitz.open(pdf)
    pages = doc.page_count
    found, failed = [], Counter()
    for pno in range(pages):
        for img in doc[pno].get_images(full=True):
            xref = img[0]
            raw = w = h = None
            cs = ""
            try:                                     # preferred: the bytes as stored
                d = doc.extract_image(xref)
                raw, w, h = d["image"], d.get("width", 0), d.get("height", 0)
                cs = d.get("cs-name") or ""
            except Exception as e:
                failed["extract_image: " + type(e).__name__] += 1
            if raw is None:                          # fallback: rasterise
                try:
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha >= 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    raw, w, h = pix.tobytes("png"), pix.width, pix.height
                    pix = None
                except Exception as e:
                    failed["pixmap: " + type(e).__name__] += 1
                    continue
            if not w or not h:                       # dimensions from the bytes if absent
                try:
                    from PIL import Image
                    w, h = Image.open(io.BytesIO(raw)).size
                except Exception:
                    failed["no dimensions"] += 1
                    continue
            found.append((hashlib.md5(raw).hexdigest(), pno + 1, w, h, raw, cs))
    doc.close()
    return pages, found, failed


def classify(found):
    """split into keepers and rejects, with the reason"""
    onpages = defaultdict(set)
    for sig, pno, _, _, _, _ in found:
        onpages[sig].add(pno)
    keep, reject = {}, Counter()
    for sig, pno, w, h, raw, cs in found:
        if sig in keep:
            continue
        if len(onpages[sig]) >= FURNITURE_PAGES:
            reject["page furniture"] += 1
            continue
        if w < MIN_W or h < MIN_H:
            reject["too small"] += 1
            continue
        ar = max(w, h) / max(1, min(w, h))
        if ar > MAX_ASPECT:
            reject["divider/strip"] += 1
            continue
        keep[sig] = (pno, w, h, raw, cs)
    return keep, reject


def store_bytes(raw, cs=""):
    """Keep the ORIGINAL embedded bytes where they are already correct. Returns (bytes, ext).

    #166 INVERSION. Images in a Separation colourspace store INK COVERAGE, not luminance: 0 means
    no ink (white paper), 255 means full ink (black). Decoded as ordinary greyscale that is exactly
    backwards, and What Every Body Is Saying stores all its photographs that way — every one came
    out as a photographic negative. Caught only by rendering the real page and comparing: the page
    shows a dark suit on white, the extracted file showed a white suit on black.
    THE TRAP: comparing extract_image() against fitz.Pixmap() shows NO difference, because both
    skip the colourspace conversion that page-drawing applies. A same-source comparison cannot see
    this. Only the rendered page can.

    #166: an earlier draft re-encoded everything to WebP to save space. Two reasons that was
    wrong. First, size is explicitly not a constraint on this project — the whole library of 507
    figures is 36MB as stored, which is nothing. Second, extract_image() hands back the bytes the
    publisher embedded, usually already-compressed JPEG; re-encoding those adds generation loss to
    a photograph for no gain. The only conversion done is for formats a browser cannot display.
    """
    from PIL import Image
    if "separation" in (cs or "").lower():
        im = Image.open(io.BytesIO(raw)).convert("L")
        im = Image.eval(im, lambda v: 255 - v)          # ink coverage -> luminance
        buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
        return buf.getvalue(), "png"
    sig = raw[:4]
    if sig[:3] == b"\xff\xd8\xff":
        return raw, "jpg"
    if sig == b"\x89PNG":
        return raw, "png"
    if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        return raw, "webp"
    # anything else (JPX, TIFF, BMP) — convert once, losslessly, so the browser can show it
    im = Image.open(io.BytesIO(raw))
    if im.mode not in ("RGB", "RGBA", "L"):
        im = im.convert("RGBA" if "A" in im.mode else "RGB")
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue(), "png"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventory", action="store_true")
    ap.add_argument("--only", default=None, help="book id, for testing")
    a = ap.parse_args()

    total_keep = total_png = total_webp = 0
    rows, manifest = [], {}
    for bid, title, pdf in books():
        if a.only and bid != a.only:
            continue
        if not os.path.exists(pdf):
            print("MISSING PDF:", bid); continue
        pages, found, failed = harvest(pdf)
        keep, reject = classify(found)
        png = sum(len(v[3]) for v in keep.values())
        webp = 0
        if not a.inventory:
            d = os.path.join(OUTDIR, bid)
            os.makedirs(d, exist_ok=True)
            items = []
            for i, (sig, (pno, w, h, raw, cs)) in enumerate(sorted(keep.items(), key=lambda kv: kv[1][0])):
                data, ext = store_bytes(raw, cs)
                webp += len(data)
                fn = f"{i:03d}.{ext}"
                open(os.path.join(d, fn), "wb").write(data)
                items.append({"f": fn, "page": pno, "w": w, "h": h, "bytes": len(data)})
            manifest[bid] = {"title": title, "pages": pages, "images": items}
            json.dump(manifest[bid], open(os.path.join(d, "manifest.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
        total_keep += len(keep); total_png += png; total_webp += webp
        rows.append((title, pages, len(found), len(keep), png, webp, dict(reject), dict(failed)))

    print("%-42s %5s %7s %6s %9s %9s" % ("BOOK", "pages", "objects", "KEPT", "source", "stored"))
    anyfail = False
    for t, pg, nf, nk, png, wb, rej, fail in sorted(rows, key=lambda r: -r[3]):
        if fail: anyfail = True
        print("%-42s %5d %7d %6d %9s %9s" % (t[:42], pg, nf, nk,
              f"{png/1e6:.1f}MB", f"{wb/1e6:.1f}MB" if wb else "-"),
              ("  FAILED:" + str(fail)) if fail else "")
    print()
    print("TOTAL real figures: %d   stored %.0f MB" % (total_keep, (total_webp or total_png)/1e6))
    if not a.inventory:
        json.dump({k: {"title": v["title"], "n": len(v["images"])} for k, v in manifest.items()},
                  open(os.path.join(OUTDIR, "index.json"), "w", encoding="utf-8"), indent=1)
        print("wrote", OUTDIR)


if __name__ == "__main__":
    main()
