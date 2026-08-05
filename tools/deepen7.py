# -*- coding: utf-8 -*-
"""#185 — bring track R up to the revised length target.

Hassan, on reading a finished ~830w lesson: "looks okayish to me... just increase its overall
size a bit." So the target moved to ~1,000-1,200 words where the idea supports it. Track R was
597-696.

WHAT THE EXTRA LENGTH IS SPENT ON — and it is not more claims. Each lesson gets one more
CONCRETE SITUATION worked to the end, because that is the part he actually needs: he has said
from the start that the gap is applying it, not understanding it. An abstract mechanism plus one
example transfers to that one example. Two worked cases in different settings is what makes the
third one, the real one, recognisable.

    python tools/deepen7.py --dry
    python tools/deepen7.py
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
"r1": [
    "A second case, in a setting that has nothing to do with anything dramatic, because this is "
    "where you will actually meet it. Someone snaps at a colleague over a scheduling change. To "
    "everyone watching, the reaction and the cause do not match, and the available "
    "explanations are all about character: they are difficult, they overreact, they are "
    "unprofessional. Those explanations are cheap, they are satisfying, and they predict "
    "nothing — you cannot use any of them to work out what will happen next week.",

    "The state reading is different and it is testable. If a threshold is low and recovery is "
    "slow, you should see two specific things: reactions clustering around a particular class "
    "of trigger rather than spread evenly, and a return to normal that takes noticeably longer "
    "than it does for anything else. If neither of those is true — if this person spikes at "
    "everything equally and is fine ten minutes later — the state reading is wrong and you "
    "should drop it. That is what makes it a claim rather than a story.",

    "And notice what changes if the state reading holds: your best move stops being to address "
    "the scheduling change. The change was the tip, not the cause, and arguing about it "
    "carefully will accomplish nothing because it is not what the size of the reaction was "
    "about. What is available to you is the thing everyone skips — asking, later, when the "
    "alarm has actually come down, which requires knowing that coming down takes longer here "
    "than you would expect.",
],
"r2": [
    "A second case, and this one you may recognise from the inside rather than from watching "
    "someone else. A song comes on, or a particular light in the afternoon, and your mood drops "
    "hard for no reason you can name. You look for a cause in the present, find nothing "
    "sufficient, and conclude you are being irrational or that something is wrong with you "
    "today. Both conclusions are about your character, and both are wrong in the same way — "
    "they assume the trigger must be in the present, because that is where you were looking.",

    "The fragment reading says the trigger was sensory and the label was never attached to it. "
    "It also predicts something specific: the response arrives BEFORE any memory does, and "
    "often no memory arrives at all. That ordering is the tell, and it is the opposite of "
    "ordinary remembering, where the recollection comes first and the feeling follows from it. "
    "If you notice the feeling preceding any content, you have caught the shape of this rather "
    "than merely applied the word.",

    "What that changes practically is small and worth having. The useful question stops being "
    "'what is wrong with me' — which has no answer and generates its own second layer of "
    "distress — and becomes 'what did I just see, hear or smell'. That question is answerable. "
    "You may still not know why the fragment is loaded, and you do not need to; locating the "
    "sensory trigger is enough to stop the search for a present-day cause that was never there.",
],
"r3": [
    "A second case, and it is the one that costs people relationships rather than treatment. "
    "Someone close to you goes quiet in the middle of something difficult. You ask what is "
    "wrong. Nothing comes back. You ask again, more gently, and still nothing — and now you are "
    "in the interpretation that ruins it: they are shutting me out, they do not trust me, they "
    "are punishing me with silence. Every one of those is a claim about their intentions "
    "toward you, and every one requires the speech route to have been available and declined.",

    "The finding removes that assumption, and removing it changes what you do next rather than "
    "just how you feel about it. If the route may genuinely be out, then repeating the question "
    "is not persistence, it is pressure applied to a system that cannot answer — and pressure "
    "is precisely what keeps it out. What works instead is the thing that feels like giving up "
    "and is not: stop asking, stay, and make it clear you are not leaving. You are waiting for "
    "a route to come back online rather than negotiating for access to it.",

    "There is a version of this you can use on yourself, too. If you have ever been unable to "
    "explain something in the moment and produced a fluent account of it two hours later, that "
    "is the same ordering. The two-hour version is not the truer one because it is more "
    "articulate — it is a reconstruction assembled once the machinery came back. Both people in "
    "a difficult conversation are subject to this, which is a good reason not to treat "
    "whatever gets said in the worst ten minutes as the settled record of what either of you "
    "thinks.",
],
"r4": [
    "A second case, deliberately far from anything clinical, because the mechanism is not "
    "reserved for extremity. Someone has applied for work repeatedly and been rejected "
    "repeatedly, and has now stopped applying. From outside this reads as having given up, and "
    "the available advice writes itself: just keep going, just send more, just put yourself out "
    "there. All of it addresses a decision, and a decision is not what is happening.",

    "What the experiment predicts is that the person is not weighing the odds and choosing not "
    "to act. The generation of the attempt has been suppressed, and it stays suppressed even "
    "when the odds change — which is why news that a role is genuinely gettable does not "
    "produce an application. The evidence arrives at a system that has stopped taking evidence "
    "about this class of action. That is also why the encouragement stings: it says the door is "
    "open, which they can see, and offers nothing about the part that is actually stuck.",

    "The direction that does work follows straight from what shifted the animals, and it is "
    "unglamorous. Not persuasion — movement, repeated, at a scale small enough to succeed. Not "
    "'apply for ten things', which is the same wall in a smaller font, but something so minor "
    "it cannot fail and still produces a visible result: one email that will definitely get a "
    "reply, one task finished today. You are not building confidence in the abstract. You are "
    "re-establishing, at a level below argument, the specific experience of an action producing "
    "an outcome — which is exactly the connection that inescapability broke.",
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
        # keep the closing clinical edge LAST — it is the last thing read for a reason
        edge = None
        if n["bridge"] and "not a diagnosis" in n["bridge"][-1]:
            edge = n["bridge"].pop()
        n["bridge"] = n["bridge"] + extra + ([edge] if edge else [])
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
        print(f"  {nid:<4} {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {t[:42]}")
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
