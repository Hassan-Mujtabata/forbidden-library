# -*- coding: utf-8 -*-
"""#182 — second pass on track N: work the mechanism further down, add a second case, and mark
the EDGE on every step.

deepen4.py added the failure and the tell. What is still missing is the part that stops the idea
being discarded the first time it does not fit: every one of these six has a limit, and a rule
with no stated limit gets misapplied once and then thrown away wholesale. "You are biased" with
no boundary is unusable advice — it applies to everything, so it changes nothing.

    python tools/deepen5.py --dry
    python tools/deepen5.py
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
    "One more thing about the mechanism, because it explains why the six take the shapes they "
    "do rather than being an arbitrary list. The pleasure principle does not produce random "
    "errors — random errors would be much easier to live with, because they would cancel out. "
    "It produces errors that all point the same way: toward you being right, capable, decent, "
    "and not responsible. That directional quality is why they compound instead of averaging "
    "away, and it is why you cannot correct for them by simply being more careful in general.",

    "And the edge, which matters because the material invites the wrong conclusion. None of this "
    "says reasoning is worthless or that you should distrust everything you think — that "
    "position is unusable, and people who adopt it for a week abandon it permanently. Almost all "
    "of your thinking is fine. The bias concentrates precisely where an outcome matters to you "
    "emotionally, which is a small and identifiable subset. The skill is not universal "
    "suspicion. It is knowing which questions you are the wrong person to assess, and getting "
    "those particular ones checked.",
],
"n1s1": [
    "Work the mechanism one level further, because 'we look for supporting evidence' is not "
    "quite it. The search is ASYMMETRIC in effort rather than in direction. You do look at "
    "opposing evidence — but you examine it hard, looking for the flaw, and you find one, "
    "because everything has a flaw. Supporting evidence gets waved through on a glance. Neither "
    "step feels dishonest in isolation; each is just ordinary scrutiny applied unevenly, and "
    "the unevenness is invisible from inside because you never see the two standards side by "
    "side.",

    "Second case, away from the obvious ones. You are ill and you look up a symptom. Whatever "
    "you already fear, you will find, because the internet contains every possibility and your "
    "search terms are shaped by the fear. This is the same machinery with no argument and no "
    "opponent — which shows it is not about winning debates at all. It is about which evidence "
    "you go looking for and how hard you inspect what you find.",

    "The edge: you cannot run this on everything, and trying is how people abandon it. Most "
    "beliefs do not warrant a disconfirming search — you would never get anything done. The "
    "test is worth spending where a wrong answer is expensive and hard to reverse: a big "
    "purchase, a job, ending something, a medical decision. Ordinary opinions can stay "
    "unexamined. Reserve the effort for the questions that would actually cost you.",
],
"n1s2": [
    "The mechanism underneath is worth having explicitly, because it explains a thing you have "
    "felt. Certainty is a FEELING, produced by fluency — how easily a thing comes to mind and "
    "how smoothly it can be said. It is not produced by how well the thing was checked. Those "
    "two are separate processes that happen to feel identical from inside, which is why you "
    "cannot tell the difference in yourself by introspecting harder. Fluency is buildable by "
    "repetition alone: say something enough times and it becomes easy to say, and easy to say "
    "registers as true.",

    "Second case: you have explained something several times — a plan, an opinion, a version of "
    "events. By the fifth telling it comes out polished, and you feel more sure of it than you "
    "did at the first. Nothing was verified between telling one and telling five. What changed "
    "was fluency, and your certainty tracked the fluency because it always does. This is why "
    "people become most confident about the stories they tell most often.",

    "The edge: sometimes loudness is just how a person talks. Cultures and individuals differ "
    "enormously in expressiveness, and reading emphasis as a symptom of hidden doubt will make "
    "you badly wrong about entire categories of people. The signal is not volume — it is volume "
    "that RISES when a claim is questioned, in someone who was not otherwise emphatic. Change, "
    "as everywhere else in this library, not level.",
],
"n1s3": [
    "The mechanism, stated properly: the halo effect is not laziness, it is compression. You "
    "cannot hold a separate estimate for every trait of every person you meet, so the mind "
    "stores something much cheaper — a single overall impression — and regenerates the "
    "individual traits from it on demand. That is why the traits agree with each other so "
    "neatly: they are not independent observations, they are the same one observation being "
    "read out repeatedly in different words.",

    "Second case, and it runs the other way, which is the version that does real damage. "
    "Someone made a poor first impression — nervous, said something clumsy — and every "
    "subsequent thing they do is now read through it. Competent work reads as surprising rather "
    "than as evidence. The negative halo is harder to notice than the positive one, because "
    "thinking well of people feels like generosity while thinking poorly of them just feels "
    "like accuracy.",

    "The edge: you have to judge people, and quickly, and often on very little. This is not an "
    "instruction to suspend judgement — that is not available, and pretending otherwise means "
    "you simply judge unconsciously instead. It is an instruction to hold the judgement at the "
    "confidence it actually earned. 'I have one meeting's worth of impression' is a usable "
    "state. It is only when the impression hardens into a fact you would defend that it starts "
    "costing you.",
],
"n1s4": [
    "Why relief rather than pressure is the mechanism, and why that makes it nearly invisible: "
    "pressure is something you could resist, and resisting it would feel like something. Relief "
    "arrives as the absence of a discomfort you had not consciously registered. There is no "
    "moment of yielding to be noticed, because nothing was applied to you — you simply moved "
    "toward the position that was easier to hold among the people you spend time with, and "
    "arrived experiencing it as a conclusion.",

    "Second case, deliberately outside politics, where everyone can see it and nobody applies "
    "it to themselves. Your opinion of a film, a game, a piece of work — formed alone, then "
    "discussed with people whose taste you respect. Notice how rarely the final position is far "
    "from theirs, and how completely it feels like your own considered view. The mechanism does "
    "not care that the stakes are low; it runs on any question where being out of step is "
    "uncomfortable, which is most of them.",

    "The edge, and it is the one people miss: the group is frequently RIGHT. Most of what you "
    "believe you took from other people, and had to, because a life is too short to verify "
    "anything from scratch. Deference is not the flaw. The flaw is deference that reports itself "
    "as independent reasoning — because then you defend a borrowed position with the confidence "
    "of an earned one, and you cannot update it when the people you borrowed it from turn out "
    "to be wrong.",
],
"n1s5": [
    "The mechanism has a specific timing to it that is worth knowing, because it tells you when "
    "to act. Immediately after a failure there IS a window where you can see your own part — it "
    "is uncomfortable and it is accurate. What Greene describes is what happens next: over days, "
    "the pleasure principle re-seals the account, your share shrinks, and the circumstances "
    "grow. The memory does not merely fade; it is actively rewritten in a favourable direction, "
    "and the rewritten version is what you will have permanently.",

    "So the second case is a timing case, and it is the practical consequence. You mess "
    "something up on Monday and feel it sharply. By Friday you have a version in which the brief "
    "was unclear and the timeline was unrealistic — both possibly true, and neither the part you "
    "could have controlled. Nothing dishonest happened in between. This is why writing it down "
    "on Monday matters: not for the record, but because Monday's account is the only one you "
    "will ever have that was not composed by the mechanism.",

    "The edge, and it needs saying because this material can become a stick: plenty of things "
    "genuinely are not your fault. Bad managers, bad luck, and impossible timelines exist, and "
    "a person who has learned to always find their own contribution will find one whether or not "
    "it is there — which is its own distortion and a much more miserable one. The rewrite is a "
    "tool for locating the part you control, not a doctrine that everything is that part.",
],
"n1s6": [
    "The mechanism, and this is the one that makes the whole track cohere. Your own reasoning "
    "reaches you from the INSIDE — you experience the deliberation, the weighing, the reasons. "
    "Other people's reasoning reaches you only as OUTPUT: the conclusion, the behaviour, the "
    "result. So you are comparing your process against their product, which is not a comparison "
    "at all. Of course yours looks more considered. You are the only person whose considering "
    "you can see.",

    "That single asymmetry generates most of the six. It is why their evidence looks motivated "
    "and yours looks like evidence, why their certainty looks like bluster and yours like "
    "conviction, why their group loyalty is obvious and yours is reasoning. Not six separate "
    "faults — one vantage point, applied to six subjects. Which is also why the corrective is "
    "always the same shape: get the outside view of yourself somehow, from someone else, from "
    "writing it down, from a rule you set before you were invested.",

    "The edge, and it is real. Some belief in your own judgement is necessary and healthy — "
    "people who genuinely lose it do not become calibrated, they become unable to decide "
    "anything. Greene is not asking for that, and his ending is the opposite of deflating: "
    "rationality and decency are not the settings you come with, they are reached through "
    "awareness and effort over time. The point of seeing the asymmetry clearly is not to think "
    "less of yourself. It is that you cannot correct a distortion you believe is a clear view.",
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
        print(f"  {nid:<6} {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {t[:44]}")
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
