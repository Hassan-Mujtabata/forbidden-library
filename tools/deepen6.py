# -*- coding: utf-8 -*-
"""#183 — deepen tracks P (Meditations) and R (The Body Keeps the Score), the last two below the
standard. Same model as deepen3/4/5: append the failure the reader will actually produce, the
tell that they are producing it, and where the idea stops.

Track R needed this most and for a particular reason. Its clinical edge was already stated in
every lesson, but it had no "how you will get this wrong" anywhere — and the ways to get THIS
material wrong are unusually harmful: explaining everyone's behaviour as trauma, diagnosing
people who did not ask, and reading "talking does not reach it" as a reason to dismiss someone's
therapy. Naming those explicitly is part of handling the subject responsibly, not an extra.

    python tools/deepen6.py --dry
    python tools/deepen6.py
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
# ---------------------------------------------------------------- Meditations
"p1": [
    "The failure you will produce is not disagreeing with this — it is using it to skip the "
    "feeling. You separate event from judgement, you note that the distress is added, and you "
    "arrive at a tidy position where nothing needs to be felt. That is not Stoicism, it is "
    "intellectualising, and it works for about a week before the unfelt thing returns with "
    "interest. Aurelius is not writing to stop feeling. He is writing to stop the SECOND layer "
    "— the commentary — from running unchecked on top of the first.",

    "The tell is speed. If the separation took ten seconds and left you feeling clean, you "
    "performed the technique rather than used it. Done properly it is slow and often makes "
    "things worse briefly, because writing the bare event down forces you to look at the thing "
    "without the story that was managing it. Discomfort during the exercise is a sign it "
    "reached something. Immediate relief usually means you rewrote the story rather than "
    "separated it.",
],
"p2": [
    "The failure here is specific and very easy: the sort becomes an alibi. Things quietly "
    "migrate into the 'not up to me' column because that column requires nothing — the deadline "
    "was unrealistic, the brief was unclear, they never replied. Each may be true. But a sort "
    "that only ever grows on one side is not a sort, it is a defence, and it produces the calm "
    "of having decided nothing is your problem.",

    "The tell: after sorting, the 'up to me' column should contain at least one item you do not "
    "want to do. If it contains only things you were going to do anyway, you have not sorted, "
    "you have described. The whole value of this move is that it removes the excuses AND the "
    "worry at the same time — and if it only removed the worry, you ran half of it.",
],
"p3": [
    "The failure is the one this book itself demonstrates, which is why it is worth naming "
    "plainly: the practice becomes the identity. You keep the notebook, you think of yourself as "
    "someone who does this, and the reps stop being reps and start being a description of the "
    "kind of person you are. At that point it is producing feeling, not capacity, and it will "
    "not be there when something actually happens.",

    "The tell is where the evidence lives. If the only evidence that this is working is in the "
    "notebook, it is not working. The measure is entirely outside it: is the gap between "
    "something happening and your reaction to it wider this month than last, in the moment, when "
    "it counted? That is a question you can answer honestly in about five seconds, and it is the "
    "only one that matters.",
],
# ---------------------------------------------------------------- Body Keeps the Score
"r1": [
    "Now the way this material gets misused, and it needs saying because it is the most common "
    "outcome of reading this book. You will start explaining people with it. A colleague who is "
    "prickly, a relative who withdraws, someone who reacts hugely to something small — and you "
    "now have a mechanism that accounts for all of it. It is an enormously satisfying lens and "
    "it is almost always applied without any of the information it would actually require.",

    "The tell is whether your explanation is falsifiable. 'Their alarm system is dysregulated' "
    "explains every possible behaviour, which means it predicts none and cannot be wrong. A real "
    "observation would be something like: this specific person reacts far past baseline to this "
    "specific class of thing, and returns to normal much more slowly than they do with anything "
    "else. That is a pattern. The general version is a story you are telling about someone who "
    "did not ask you to.",
],
"r2": [
    "The failure here is treating every patchy memory as evidence of this. Ordinary memory is "
    "fragmentary, reconstructed, and full of holes — that is simply how memory works, and it "
    "does not indicate anything. Reading this lesson and then re-examining your own past for "
    "gaps will reliably find them, because they are there in everybody, and the finding will "
    "mean nothing at all.",

    "The tell is the alarm, not the gap. What this describes is not incomplete recall; it is "
    "fragments that FIRE — that produce a physiological response disproportionate to the "
    "present, on a sensory trigger, often without any accompanying memory. A hole in your "
    "recollection of a holiday is a hole. A smell that produces a full alarm response with no "
    "narrative attached is a different phenomenon, and the difference is the reaction, not the "
    "missing information.",
],
"r3": [
    "The most harmful misreading of this whole track lives here, so it is worth being blunt: "
    "'talking does not reach it' is not a reason to tell anyone their therapy is useless. That "
    "is not what the finding says. It says the speech centre is measurably reduced AT THE MOMENT "
    "the material is active, which is a statement about timing and about relying on narration "
    "alone — not a verdict on talking therapies, which van der Kolk does not deliver and which "
    "you are in no position to deliver on his behalf.",

    "The tell that you have understood it correctly is that it changes what you EXPECT rather "
    "than what you recommend. Expect that someone in the middle of it may not be able to "
    "describe it, and stop reading that as evasion. Expect that 'just talk to me about it' can "
    "be the wrong instrument at the wrong moment. Those are adjustments to your own patience and "
    "your own interpretation. Prescribing anything to anyone on the basis of one lesson is the "
    "failure, and it is the one with real consequences for other people.",
],
"r4": [
    "The failure with this one runs in two directions and both do damage. Used on someone else "
    "it becomes a way of writing them off — they are helpless, so nothing you offer could help, "
    "so you stop offering. Used on yourself it becomes a permission slip: this is learned "
    "helplessness, so not acting is explained and therefore fine. The experiment says neither of "
    "those things. It describes a suppression that can shift, which is precisely why van der "
    "Kolk followed it rather than filing it as a curiosity.",

    "The tell is direction of travel. Applied usefully, this changes the SIZE of what you "
    "suggest — you stop pointing at the door and start looking for something small enough that "
    "the person could actually produce it and see it produce an outcome. Applied badly, it "
    "changes nothing except your explanation for why nothing changes. If the only thing this "
    "lesson gave you was a better account of why someone is stuck, it has been absorbed by the "
    "state it describes.",

    "And once more, because it belongs at the end of the track rather than only inside it: this "
    "is a mechanism, not a diagnosis, and nothing here qualifies anyone to treat it. If any of "
    "this described you rather than merely interested you, the useful next step is a "
    "professional — not a technique from a lesson, and not a conclusion you reached about "
    "yourself at eleven at night.",
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
        print(f"  {nid:<5} {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {t[:44]}")
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
