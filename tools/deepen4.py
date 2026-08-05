# -*- coding: utf-8 -*-
"""#181 — deepen track N (The Laws of Human Nature) using the deepen3 model: APPEND the part a
short lesson always omits — the failure the reader will actually produce, and the tell.

For a track about biases this matters more than anywhere else, because there is a specific and
very reliable failure attached to learning about biases: you acquire a vocabulary for diagnosing
other people and your own behaviour does not change at all. Naming that per-bias, with the tell,
is the difference between a glossary and something that operates.

    python tools/deepen4.py --dry
    python tools/deepen4.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")

ADD = {
"n1": [
    "Before the steps, the failure that this whole track is most likely to produce, because it "
    "is nearly universal and it feels like success. You will finish these six with a sharp new "
    "vocabulary for describing OTHER PEOPLE. You will spot confirmation bias in an argument "
    "online, name the conviction bias in someone certain, and your own decisions will go on "
    "exactly as before. That is not a partial win. It is the superiority bias eating the "
    "material, and it is the standard outcome of reading about cognitive bias.",

    "The tell is simple and you can run it after any of these lessons: in the last week, name "
    "one thing YOU did that this describes. Not one thing you observed. If nothing comes, you "
    "have acquired a lens and pointed it outward, which is the comfortable direction and the "
    "useless one. Each step below ends with a move that only works if it is aimed inward, and "
    "that is deliberate.",
],
"n1s1": [
    "The failure you will produce: you will run the test and still not change your mind, and you "
    "will feel more rigorous for having run it. You write down what would change your mind, you "
    "search for it honestly, you find something that half-qualifies, you decide it does not "
    "quite count — and you now hold the same view with the added confidence of having checked. "
    "The procedure has become part of the defence.",

    "The tell is whether you can state, in advance and in one sentence, a result that would "
    "actually move you — and whether that result is the kind of thing that could plausibly turn "
    "up. 'If a major study found the opposite' is not a real test if no such study could exist. "
    "A real disconfirmer is specific, findable, and would genuinely be uncomfortable to find. If "
    "your test could never fail, you built it that way for a reason.",
],
"n1s2": [
    "The failure here is the reverse of the obvious one, and it catches careful people. Having "
    "learned that conviction is performable, you start discounting everyone who sounds sure — "
    "including the people who are sure because they actually know. Confidence is weak evidence, "
    "not negative evidence, and treating it as negative is its own bias with better manners.",

    "The tell that you are using this well is that it changes what you ASK rather than what you "
    "conclude. Someone speaks with total certainty; the right output is a question about how "
    "they know, not a private decision that they are hollow. The strip-the-person test from this "
    "lesson is a tool for locating where to probe. It was never a verdict machine, and used as "
    "one it just replaces credulity with cynicism, which is no more accurate and much less "
    "pleasant to be around.",
],
"n1s3": [
    "The failure: you will apply this to strangers and first impressions, where it is easy, and "
    "never to the people you already have opinions about — which is where nearly all of the cost "
    "sits. A wrong read on someone you met once costs almost nothing. A wrong read on a "
    "colleague you have worked with for two years, built from an early impression and defended "
    "since, has been shaping decisions the whole time.",

    "The tell is discomfort. Run the 'what did they do when it was expensive for them' test on "
    "someone you are confident about — particularly someone you have quietly written off. If the "
    "honest answer is that you have no such evidence and the judgement came from how they came "
    "across in a meeting three years ago, that is the finding. It will not feel like an "
    "insight; it will feel like an unwelcome chore, and that reaction is the reliable sign you "
    "have aimed it somewhere that matters.",
],
"n1s4": [
    "The failure is precise and almost everyone commits it: you will run this test on the group "
    "you are NOT in. Their positions correlate suspiciously; yours were each reasoned "
    "independently. That asymmetry is the bias operating at full strength while you believe you "
    "are examining it, and it is why this particular step so rarely changes anybody.",

    "The tell: take a position held by your own side that you privately find weakest — the one "
    "you would rather not have to defend at a dinner. Now ask whether you would hold it at all "
    "if the people around you did not. If the honest answer is probably not, you have located a "
    "position that arrived as part of a set. That does not make it wrong. It means you have "
    "never tested it, and you should stop spending it in arguments as though you had.",
],
"n1s5": [
    "The failure: you will do the rewrite honestly, feel appropriately accountable, and change "
    "nothing — because self-blame is emotionally satisfying in a way that changing a process is "
    "not. Writing 'I planned with no slack' feels like accountability. It is only accountability "
    "if the next plan has slack in it, and Greene's whole point is that the feeling of having "
    "learned reliably substitutes for the learning.",

    "The tell is whether the rewrite produced a change you could point at afterwards — a "
    "different default, a thing you now check, a step added. If the only output was a clearer "
    "account of what went wrong, you have written a better explanation, which is the exact "
    "activity the bias was already generating. The measure is never the quality of the "
    "post-mortem. It is whether the same shape shows up again next quarter.",
],
"n1s6": [
    "The failure, and it is the funniest and the most common: you will read this step, agree "
    "with it completely, and file it as a description of humanity in general. Everyone thinks "
    "they are above average; how true; what a species we are. That move preserves the bias "
    "entirely while performing insight about it, and it is available at every single reading.",

    "The tell is whether the exercise produced something specific and slightly unpleasant about "
    "you, by name. Not 'I suppose I have blind spots' — an actual instance: the colleague whose "
    "success you have privately attributed to politics, the argument you won that you now "
    "suspect you won on delivery. If reading six lessons on bias has generated no such item, the "
    "material has been absorbed by the thing it was describing, which is precisely what Greene "
    "warns about on the first page and what almost every reader does anyway.",
],
}


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))
    rows = []
    for nid, extra in ADD.items():
        n = next((x for x in graph["nodes"] if x["id"] == nid), None)
        if not n:
            print(f"FAIL: node {nid} not found")
            return 1
        before = sum(len(p.split()) for p in n["bridge"])
        n["bridge"] = n["bridge"] + extra
        # a figure's `place` indexes into bridge; appending never invalidates it, but check
        for f in n.get("fig", []) or []:
            if f.get("place") is not None and f["place"] >= len(n["bridge"]):
                f["place"] = max(0, len(n["bridge"]) // 2)
        rows.append((nid, n["title"], before, sum(len(p.split()) for p in n["bridge"])))

    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
    except SystemExit:
        print("FAIL: validate() rejected the graph")
        return 1
    for nid, t, b, a in rows:
        print(f"  {nid:<6} {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {t[:46]}")
    if dry:
        print("\n--dry: graph.json NOT written")
        return 0
    shutil.copy(GRAPH, GRAPH + ".bak")
    json.dump(graph, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False,
              separators=(",", ":"))
    print("\ngraph.json updated -> next: python tools/build.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
