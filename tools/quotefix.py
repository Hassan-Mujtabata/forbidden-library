# -*- coding: utf-8 -*-
"""
#164: find, for every source quote in graph.json, the passage in the cited book that actually
says it — or report that no honest match exists.

WHY THIS EXISTS. 143 quotes sit in graph.json's `sources[].quote`, presented to the reader as
passages from named books. Only 3 are verbatim; most share almost no five-word phrases with the
book they cite. They are PARAPHRASES wearing quotation marks.
IMPORTANT CORRECTION, kept here because the first version of this file got it wrong: that does
NOT mean they are fabrications. Spot-checking showed the ideas are faithful and the real passage
usually exists — e.g. a1's "the way to deep meditation is through letting go" against Brahm's
actual "the way into stillness is through the pīti-sukha born of letting go". The defect is
presentation, not content: a paraphrase is being attributed as a quotation. The repair is to swap
in the real wording, not to delete the claim.

WHAT THIS DOES *NOT* DO. It does not edit graph.json. It writes a review file with, for each
quote, the best real candidates ranked by how much distinctive vocabulary they share. A human
picks — or rejects. A quote with no good candidate must be DROPPED, not fudged: that is the whole
lesson of this repair.

  python tools/quotefix.py            -> tools/figs_research/quotes_review.md
"""
import json, os, re, sys, math
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "books.json")
GRAPH = os.path.join(HERE, "graph.json")
OUT = os.path.join(HERE, "figs_research", "quotes_review.md")

STOP = set("""a an the and or but if then than that this these those of in on at to for from by with
without about into over under again further once here there all any both each few more most other some
such no nor not only own same so too very can will just should now is are was were be been being have
has had do does did doing i you he she it we they them his her its their our your my me him us as
what which who whom when where why how there's it's you're we're they're i'm don't can't won't""".split())


def words(s):
    return [w for w in re.findall(r"[a-z']+", s.lower()) if len(w) > 2 and w not in STOP]


def phrases(s, n=5):
    w = re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def main():
    books = json.load(open(BOOKS, encoding="utf-8"))
    graph = json.load(open(GRAPH, encoding="utf-8"))
    # paragraphs per book, plus a document-frequency table so common words don't dominate scoring
    paras, df = {}, {}
    for b in books["books"]:
        ps = [(e.get("t", ""), p) for e in b["episodes"] for p in e["p"] if len(p) > 120]
        paras[b["title"]] = ps
        d = Counter()
        for _, p in ps:
            d.update(set(words(p)))
        df[b["title"]] = (d, len(ps))

    rows, stats = [], Counter()
    for n in graph["nodes"]:
        for si, s in enumerate(n.get("sources") or []):
            bt = s["book"]
            if bt not in paras:
                stats["book missing"] += 1
                continue
            d, N = df[bt]
            for qi, q in enumerate(s.get("quote") or []):
                qw = set(words(q))
                if not qw:
                    continue
                qp = phrases(q)
                # idf-weighted overlap: reward rare shared vocabulary, ignore filler
                scored = []
                for t, p in paras[bt]:
                    pw = set(words(p))
                    common = qw & pw
                    if len(common) < 3:
                        continue
                    sc = sum(math.log(N / (1 + d[w])) for w in common)
                    # a shared 5-word phrase is much stronger evidence than shared vocabulary
                    ph = len(qp & phrases(p))
                    scored.append((sc + ph * 25, ph, t, p))
                scored.sort(reverse=True)
                best = scored[:3]
                # NB: an absolute score cut-off was WRONG here — the idf sum scales with quote
                # length, so short quotes could never clear it and obviously-correct passages were
                # being labelled unmatched. Score relative to the quote's own vocabulary instead,
                # and never assert "no match" on the tool's authority: rank, and let a human judge.
                cov = (len(qw & set(words(best[0][3]))) / len(qw)) if best else 0.0
                verdict = ("VERBATIM-ISH" if best and best[0][1] >= 3 else
                           "STRONG — likely the source passage" if cov >= 0.45 else
                           "WEAK — read it, may need dropping" if best else
                           "NOTHING SHARES VOCABULARY — drop")
                stats[verdict.split(" —")[0].strip()] += 1
                rows.append((n["id"], bt, q, best, verdict, cov))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# Quote repair — candidates for review  (#164)\n\n")
        f.write("Generated by tools/quotefix.py. NOTHING HAS BEEN EDITED. For each quote currently\n"
                "in graph.json, the best real passages from the cited book are listed. Pick one, or\n"
                "mark the quote for deletion. A quote with no honest match gets DROPPED.\n\n")
        for k, v in stats.most_common():
            f.write(f"- **{k}**: {v}\n")
        f.write("\n---\n\n")
        for nid, bt, q, best, verdict, cov in rows:
            f.write(f"## {nid} — {bt}\n**{verdict}**\n\nCURRENT (not in the book):\n> {q}\n\n")
            if best:
                for sc, ph, t, p in best:
                    f.write(f"- `score {sc:.0f}` `{ph} exact phrases` *{t[:40]}*\n  > {p[:420]}\n\n")
            else:
                f.write("_no paragraph in this book shares enough vocabulary_\n\n")
    print("\n".join(f"{k:34} {v}" for k, v in stats.most_common()))
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
