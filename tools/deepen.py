# -*- coding: utf-8 -*-
"""#173 — bring a lesson up to the reading budget Hassan actually has.

HIS CAPACITY, NOT A QUOTA. "i can sit for 10 to 20 min on single stage reading when free
properly" — and then, correcting the obvious misreading: "i am saying i can or even 30 min if
alot which means u can put 1 lesson in there if needed not squeeze there 2 of them to fill time
its all about understanding."

So this is a CEILING, not a target. Roughly 30 minutes of study reading is available for a single
stage if the idea needs it. What must never happen is padding to reach it, or welding two ideas
together to use up the room. ONE idea per lesson, carried to the length that idea actually
requires — which may be six minutes or may be thirty.

WHY TRACK O NEEDED DEEPENING ANYWAY. It shipped at ~380 words a lesson, and that was not a
judgement that the ideas were small — it was a summary reflex. There is no room in 380 words to
carry a mechanism down to why it must be so, run one case to the end, answer the obvious
objection, or mark the edge where the idea stops holding. Every one of those omissions becomes
homework for the reader, which is the exact trade he refuses.

WHAT LENGTH IS FOR, when the idea earns it:
  * the mechanism carried down to why it must be so, not asserted;
  * one concrete case run start to finish, including what getting it wrong looks like;
  * the obvious objection raised and answered — an unanswered objection is homework;
  * the edge, because an unbounded rule gets misapplied once and then discarded.
None of those is padding. All of them are the working.

`o1` below is the worked exemplar. Match its depth, not its subject.

    python tools/deepen.py --dry
    python tools/deepen.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")

O1 = [
    "Every claim in this track rests on one piece of anatomy, and if you take it on trust the "
    "rest becomes a list of superstitions — crossed arms mean this, touching your nose means "
    "that. So it is worth going all the way down to why it must be true, because once you can "
    "see the mechanism you can work out the signals yourself, including ones nobody has written "
    "down.",

    "You have two systems relevant here. The limbic system is old survival machinery, shared "
    "with animals that have no language at all. It monitors what is happening to you and reacts "
    "— fast, automatically, and without consulting you. The neocortex is the newer part: it "
    "thinks, plans, speaks, and it composes. The single most useful fact about this arrangement "
    "is that the two run on different timescales and only one of them takes instructions.",

    "Consider what actually happens when someone asks you a question you did not want. The "
    "limbic response fires in a fraction of a second, before you have decided anything — a "
    "spike of unease, and with it a set of physical consequences you did not order: a shift in "
    "blood flow, a change in breathing, small muscles tightening. Only afterwards does the "
    "neocortex arrive with 'sure, happy to talk about that.' The sentence is a product. It was "
    "manufactured, on purpose, several hundred milliseconds after your body had already "
    "answered honestly.",

    "That gap is the whole reason body language is readable at all. It is not that the body has "
    "some mystical honesty. It is that the reaction is produced by a system with no capacity "
    "for presentation, and it is produced FIRST. Anything that arrives later has been through "
    "the part of you that manages impressions.",

    "Now push on why this leads Navarro away from the face, because this is where most popular "
    "advice gets it backwards. The rule is not 'the body is honest and the face is not.' The "
    "rule is that honesty tracks ATTENTION — specifically, how little of it a region has "
    "received over your lifetime. Your face has been managed since you were a small child. You "
    "were told to smile at relatives you did not like. You have watched your own face in mirrors "
    "and cameras for years and adjusted what it does. It is the most rehearsed surface you own, "
    "and the rehearsal is now automatic.",

    "Your feet have had none of that. Nobody ever coached your feet. You have almost never "
    "watched them during a conversation, and neither has anyone else, which is why they were "
    "never worth training. So when your limbic system decides it wants out of a conversation, "
    "the neocortex dresses the face in polite interest — and the feet, unsupervised, quietly "
    "rotate toward the door. Same person, same moment, two different levels of management. This "
    "is also why the rule generalises: any region you have never thought about is a region "
    "currently telling the truth about you, and you can work out which those are without a list.",

    "Run a whole case through it. You ask a colleague whether they can take on a piece of work. "
    "They say 'yeah, no problem, happy to.' Their voice is warm. Their face is pleasant. And in "
    "the half second before they answered, their torso rocked back a couple of centimetres and "
    "one foot slid under the chair. What has actually happened is not that they lied. It is "
    "that their limbic system registered a load it does not want, produced a small withdrawal, "
    "and then the social part of them — which likes you, and wants to be useful, and does not "
    "want to be the person who says no — composed a cooperative sentence on top of it.",

    "Notice what that gives you, because it is more useful than 'catching' them. You now know "
    "there is a cost here that was not mentioned. The right move is not to announce that their "
    "body betrayed them; that makes you insufferable and it makes them defensive, and you still "
    "will not learn what the cost was. The right move is a question that gives the unsaid thing "
    "a door: 'what would you have to drop to fit that in?' If there was nothing, they will say "
    "so and you have lost nothing. If there was something, you have just found it while it was "
    "still cheap to find.",

    "Here is the objection, and it is a fair one. Everything above could be hindsight. You "
    "noticed the foot AFTER they hesitated, or after the project went badly, and now the memory "
    "obligingly supplies a foot. This is a real failure and it is the main way people go wrong "
    "with body language: the signal gets recruited to support a conclusion that was reached some "
    "other way, and it feels exactly like observation.",

    "The answer is not to distrust the method; it is to notice that a single observation was "
    "never the unit. One movement is noise — people shift because chairs are uncomfortable, "
    "because their leg is asleep, because they are cold. What carries information is a change "
    "from how this particular person normally is, several things moving together, at a moment "
    "you can point to. That discipline is the last lesson in this track, and it exists precisely "
    "because the first three lessons are dangerous without it. If you only ever take one thing "
    "from this track, take that one.",

    "And mark the edge, because an idea applied past its limit gets discarded when it fails. "
    "This does not tell you WHY. A body that has gone quiet is a body under some load; it does "
    "not say the load is guilt, or dishonesty, or anything about you. It could be the topic. It "
    "could be something that happened before you arrived. Discomfort is a pointer to a subject, "
    "never a verdict on a person — and every disaster in this field comes from someone treating "
    "a pointer as a verdict and then defending it because they had a scientific-sounding reason.",

    "There is one more objection worth taking seriously, because it is the one people use to "
    "dismiss the whole subject: what about someone who has trained themselves? Poker players, "
    "practised negotiators, people who lie for a living. Does this not all collapse against "
    "anyone with self-control?",

    "Partly, and the partly is the interesting bit. What training buys is suppression of the "
    "regions you are attending to, and attention is finite. A poker player has drilled the face "
    "and the hands, because that is what is visible across a table — and under a table their "
    "feet are as unmanaged as anyone's. More importantly, suppression is itself effortful, and "
    "effort has its own signature: a person controlling their body is doing a second task while "
    "talking to you, and it shows as stiffness, as unusual stillness, as a strangely narrow "
    "range of movement compared to how they were ten minutes earlier. You do not get a clean "
    "read on a trained person. You get a different tell — not the emotion, but the fact that "
    "management is occurring, which is itself information about how much this matters to them.",

    "Now turn it around, because the half of this you can act on immediately is yourself. Pick a "
    "conversation this week where you expect to be uncomfortable — asking for something, "
    "delivering bad news, negotiating. Before you go in, decide what your feet are going to do, "
    "because that is the region you have never once thought about and therefore the one "
    "currently broadcasting. Plant them. Not rigidly; just deliberately, pointed at the person "
    "rather than the exit.",

    "Two things follow from that and both are real. The obvious one is that you stop leaking the "
    "withdrawal. The less obvious one, and the more valuable, is that you will feel the impulse "
    "to move them — and feeling that impulse is the earliest possible warning that your own "
    "limbic system has registered something you have not consciously noticed yet. You have "
    "turned an involuntary broadcast into a private alarm. That is the practical shape of "
    "everything in this track: you are not learning to catch people out. You are learning to "
    "notice a system that has been running underneath every conversation you have ever had, "
    "starting with your own.",

    "Two consequences worth carrying out of this lesson. First: when words and body disagree, "
    "the disagreement is itself the finding, and the correct response is a question rather than "
    "an accusation. You have not caught a liar; you have found a place where what someone feels "
    "and what they are willing to say have come apart, and that is one of the most useful things "
    "you can locate in any conversation. Second: this runs on you, continuously, and you are the "
    "person you can actually do something about. In your next difficult conversation your face "
    "will be doing its trained job while your feet, hands and torso report the real state of "
    "affairs to anyone who has read this. Knowing which parts of you were never coached tells "
    "you exactly which parts are currently speaking for you.",
]


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))
    node = next((n for n in graph["nodes"] if n["id"] == "o1"), None)
    if not node:
        print("FAIL: node o1 not found")
        return 1
    before = sum(len(p.split()) for p in node["bridge"])
    node["bridge"] = O1
    after = sum(len(p.split()) for p in O1)

    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
    except SystemExit:
        print("FAIL: validate() rejected the graph")
        return 1

    print(f"o1 '{node['title']}': {before} -> {after:,} words "
          f"({after/200:.0f}-{after/150:.0f} min at study pace)")
    print(f"  paragraphs: {len(O1)}")
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
