# -*- coding: utf-8 -*-
"""#171 JOB 5 — the first mini-path: The Law of Irrationality (The Laws of Human Nature).

HAND-AUTHORED, not generated, and NOT a summary.

The first draft of this file was a summary of Greene's chapter and was thrown away. Hassan's
correction, twice given: "if I read books I should not just understand concept I should be easily
apply it in real life — I been understanding it for years, that's why the figures are there for."
He does not need the chapter explained. He needs to catch the thing happening and have something
to do about it.

So every step below is built in three moves and nothing else:
    THE TELL   — the sentence you actually hear in your own head when it is running. Written in
                 the first person, because that is the form you will meet it in.
    WHERE      — the specific place it will catch him, not a generic example from 1650.
    THE MOVE   — one action small enough to actually perform, in the moment.
The author's claim is the floor of the lesson, not the lesson. It lives in `sources`.

The quizzes test RECOGNITION IN A SITUATION, not recall of what Greene wrote — being able to
name the bias is the thing Hassan already has and does not need more of.

SIX steps, not five: the extractor folded "The Blame Bias" into the Group Bias chapter, so
reading chapter titles alone would have dropped one. Restored here.

FIGURES ARE STILL OWED. Hassan is explicit that figures are what make this applicable, and they
are built through the research protocol in tools/figs_research/ (read LOG.md first). Writing
them here from intuition is exactly what that protocol exists to prevent, so the specs are the
next piece of work, not a thing to fake now.

    python tools/path_irrationality.py --dry     # validate only, write nothing
    python tools/path_irrationality.py           # merge into graph.json (keeps a .bak)
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
BOOK = "The Laws of Human Nature"
TID = "N"

TRACK = {"id": TID, "name": "The Laws of Human Nature", "glyph": "\U0001f989",
         "accent": "#8e6f47",
         "blurb": "Catching yourself in the act — six things your mind does to you, and what to "
                  "do the moment you notice."}


def src(ref, *quotes):
    return {"book": BOOK, "ref": ref, "quote": list(quotes)}


PARENT = {
    "id": "n1", "track": TID, "tier": 0, "prereq": [], "glyph": "\U0001f3ad",
    "title": "The Law of Irrationality",
    "bridge": [
        "You already know people are irrational. Knowing it has never once stopped you being it, "
        "and that is the actual problem this law is about. The gap is not in your understanding. "
        "It is that the thing runs BEFORE the understanding gets a turn.",
        "Here is the whole mechanism in one line, because one line is all it needs: you move "
        "toward what is pleasant to believe and away from what is painful to believe, and the "
        "reasoning shows up afterwards to make that look like a decision. Six well-known biases "
        "are not six separate faults to memorise. They are that one move wearing six coats.",
        "Which means there is exactly one skill worth having here, and it is not recognising "
        "biases in an argument online. It is catching the move in yourself while it is still "
        "warm. Every step under this one gives you the sentence you will hear in your own head "
        "when it fires, the place it is most likely to catch you, and one thing to do about it "
        "that takes under a minute.",
        "One warning before you start, and it is Greene's, not mine. If you go down these six "
        "and find yourself thinking you are mostly clear of them, that thought is not you "
        "passing the test. It is the mechanism, running, right then.",
    ],
    "sources": [
        src("Greene — Step One: Recognize the Biases",
            "Emotions work on our thinking constantly and below awareness, and the strongest of "
            "them is wanting pleasure and avoiding pain. We believe we are after the truth when "
            "we are holding on to whatever relieves tension and flatters us."),
        src("Greene — Step One: Recognize the Biases",
            "Believing yourself immune to these biases is not evidence that you are. It is the "
            "pleasure principle operating on you at that moment."),
    ],
    "quiz": [
        {"q": "You have just spent an hour reading about cognitive biases and feel sharper for "
              "it. On Greene's account, what has actually changed about your own thinking?",
         "c": ["it is now largely bias-free",
               "close to nothing — knowing the list does not slow the move, which runs before "
               "the knowing gets a turn",
               "your intelligence has increased",
               "you will now only be biased about unfamiliar topics"], "a": 1},
        {"q": "What is the single skill these six steps are actually training?",
         "c": ["naming biases in other people's arguments",
               "catching the move in yourself while it is still happening",
               "memorising the six names",
               "winning debates"], "a": 1},
        {"q": "You read the six and conclude that four don't really apply to you. That is:",
         "c": ["a reasonable self-assessment", "evidence you understood the material",
               "the mechanism running, right at that moment",
               "only a problem if you say it out loud"], "a": 2},
    ],
    "apply": {"prompt": "Name one belief you hold that would genuinely hurt to lose — about your "
                        "work, someone close to you, or yourself. Do not argue with it. Just "
                        "write what it would cost you if it turned out to be wrong. That cost is "
                        "the exact size of the pressure bending your thinking on that subject.",
              "min": 50},
}

STEPS = [
    {
        "sid": "n1s1", "glyph": "\U0001f50d", "title": "Confirmation Bias",
        "why": "The parent names the move. This is the coat it wears most often.",
        "bridge": [
            "THE TELL — “I looked into it and the evidence backs me up.” Specifically: "
            "you went looking, and the looking went WELL. Research that confirms you feels "
            "smooth and quick. That smoothness is the signal. Research that is actually testing "
            "something feels like work and usually turns up mess.",
            "WHERE IT WILL CATCH YOU — the moment you have half-decided something and start "
            "“checking”. Deciding on a build, a course, a purchase, a plan you already "
            "want. Also every time you ask someone for advice: notice that you can predict which "
            "answer would annoy you. Greene's point about plans is the sharpest version — a plan "
            "exists to reach a wanted outcome, so weighing the bad honestly would often stop you "
            "acting at all, and the pull toward the rosy version is what keeps the plan alive.",
            "THE MOVE — before you search, write down the one finding that would change your "
            "mind. One sentence. Then go and look for THAT. If you cannot name anything that "
            "would change your mind, you were never checking, and you can stop pretending the "
            "next hour is research.",
        ],
        "sources": [
            src("Greene — Confirmation Bias",
                "Holding an idea, we go hunting for evidence that supports it, and because the "
                "pleasure principle works on us unnoticed, we duly find it."),
            src("Greene — Confirmation Bias",
                "Never grant an idea validity because someone produced evidence for it. Make "
                "your first move the search for what would disconfirm what you most want to "
                "believe."),
        ],
        "quiz": [
            {"q": "You are 20 minutes into researching a decision and everything you find "
                  "supports what you already wanted. The most useful reading of that is:",
             "c": ["the decision is well supported",
                   "the search is going too smoothly — that ease is the tell, not the proof",
                   "you should search another 20 minutes",
                   "the topic is simple"], "a": 1},
            {"q": "The one-sentence test to run BEFORE you start looking is:",
             "c": ["what do I already believe?", "what would change my mind?",
                   "who else agrees with me?", "how long will this take?"], "a": 1},
            {"q": "You cannot name anything that would change your mind. That means:",
             "c": ["your position is very strong",
                   "you are not checking, and calling it research is the lie",
                   "you need better sources", "the question is unanswerable"], "a": 1},
        ],
        "apply": {"prompt": "Take a decision you are currently leaning toward. Write the one "
                            "finding that would flip you. Then spend ten minutes looking only "
                            "for that, and write what you actually found.", "min": 50},
    },
    {
        "sid": "n1s2", "glyph": "\U0001f4e3", "title": "Conviction Bias",
        "why": "Confirmation bias is how you supply your own evidence. This is how someone else "
               "supplies it for you.",
        "bridge": [
            "THE TELL — two of them, and you need both. In yourself: you notice you are arguing "
            "LOUDER than you are certain, and there is a small unpleasant wobble underneath that "
            "the volume is covering. In other people: you walk away convinced and, if asked, "
            "cannot actually list what they showed you — only how sure they were.",
            "WHERE IT WILL CATCH YOU — anywhere confident delivery is the product. A creator who "
            "is certain about something you cannot verify. Anyone selling. Anyone whose "
            "authority is their tone. Watch how you rate the careful person who says “it "
            "depends, here is what we know and here is what we don't” — that person reads "
            "as weak or evasive, and Greene's point is that the reading is exactly inverted. "
            "Certainty is cheap to perform. The examination it imitates is not.",
            "THE MOVE — after anything that convinced you, take 30 seconds and write down the "
            "claim WITHOUT the person. No name, no tone, no story. Just the bare assertion. Most "
            "of the persuasion was carried by things that do not survive that sentence, and you "
            "will see immediately how much is left.",
        ],
        "sources": [
            src("Greene — Conviction Bias",
                "We keep an idea that quietly pleases us while harbouring a doubt about it, so "
                "we overcompensate — believing it fiercely, shouting down anyone who questions "
                "it, then treating our own vehemence as proof that it is true."),
            src("Greene — Conviction Bias",
                "Certainty delivered with heat and colour reads as carefully considered, while "
                "a hesitant or qualified tone reads as weakness. That misreading is what makes "
                "us easy for people who perform conviction deliberately."),
        ],
        "quiz": [
            {"q": "You leave a video convinced, but cannot list what was actually shown — only "
                  "how certain the speaker was. What just happened?",
             "c": ["you learned something and forgot the details",
                   "the conviction did the persuading, not the evidence",
                   "the topic was too advanced", "you were distracted"], "a": 1},
            {"q": "Someone answers your question with “it depends — here is what we know "
                  "and what we don't.” Greene's claim is that you will tend to read this as:",
             "c": ["careful and probably honest",
                   "weak or evasive, which is the inverted reading",
                   "expert", "rude"], "a": 1},
            {"q": "Noticing you are arguing louder than you are actually certain usually means:",
             "c": ["you care about the truth",
                   "the volume is covering a doubt you have not admitted",
                   "the other person is wrong", "you should keep going"], "a": 1},
        ],
        "apply": {"prompt": "Take the last thing that convinced you and write the claim with the "
                            "person stripped out — no name, no tone, no story, just the bare "
                            "assertion. Then write how much of your belief survived it.",
                  "min": 50},
    },
    {
        "sid": "n1s3", "glyph": "\U0001f3ad", "title": "Appearance Bias",
        "why": "The first two were about ideas. From here it is about people, where being wrong "
               "costs you more.",
        "bridge": [
            "THE TELL — you catch yourself making a confident claim about someone's CHARACTER "
            "from evidence that was only ever about their PERFORMANCE. “He's solid.” "
            "“She's not trustworthy.” Ask what you actually saw and it turns out to be "
            "how they came across, not anything they did when it cost them something.",
            "WHERE IT WILL CATCH YOU — first impressions you then defend for months. Anyone "
            "successful, where success quietly gets read as proof they earned it honestly. "
            "Anyone whose front is well-built, because a front that is well-built is exactly the "
            "one you will not notice. Greene's halo effect is the engine: you register one "
            "quality and your mind fills in the matching set for free.",
            "THE MOVE — when you catch a character judgement, ask one question: what did they do "
            "when it was expensive for them? Behaviour under cost is the only evidence about "
            "character that is not a performance. If you have none, you do not have a judgement. "
            "You have an impression, and you can hold it loosely without it costing you anything.",
        ],
        "sources": [
            src("Greene — Appearance Bias",
                "People have trained themselves to present whatever front will be judged well, "
                "and we take the mask for the face."),
            src("Greene — Appearance Bias",
                "Noticing one quality in a person, we infer others that fit it. Success gets "
                "read as evidence of being ethical and deserving, which hides how often "
                "advancement came by means later disguised."),
        ],
        "quiz": [
            {"q": "You are sure a colleague is trustworthy. Which of these is actually evidence "
                  "about their character rather than their performance?",
             "c": ["they are well-spoken and confident",
                   "they told the truth once when lying would have been cheaper for them",
                   "they are successful", "everyone likes them"], "a": 1},
            {"q": "Why is a well-built front the dangerous one?",
             "c": ["it is used only by dishonest people",
                   "being well-built is precisely what stops you noticing it is a front",
                   "it is easy to spot", "it only appears at work"], "a": 1},
            {"q": "The halo effect is doing its work when you:",
             "c": ["notice one quality and get the matching set thrown in free",
                   "dislike someone immediately", "forget a person's name",
                   "judge someone by their job"], "a": 0},
        ],
        "apply": {"prompt": "Pick someone you rate highly but do not know well. Write what you "
                            "have actually watched them do when it cost them something — and if "
                            "the answer is nothing, write that instead.", "min": 50},
    },
    {
        "sid": "n1s4", "glyph": "\U0001f465", "title": "The Group Bias",
        "why": "Appearance bias bends how you read one person. This one bends where your "
               "opinions came from before you ever examined them.",
        "bridge": [
            "THE TELL — relief. Not argument, not evidence: the small physical easing when you "
            "find people who think as you do, and the low discomfort when you are the odd one "
            "out. Greene's claim is that we take up positions partly to GET that relief, and "
            "because relief does not feel like pressure, the position feels self-generated.",
            "WHERE IT WILL CATCH YOU — the test is brutal and you can run it on yourself in "
            "seconds. Take your views on four or five completely unrelated issues. Could someone "
            "predict all of them from knowing your position on one? Unrelated questions have no "
            "business correlating. If yours line up, they did not each get decided on their "
            "merits; they arrived as a set, and the set came from somewhere.",
            "THE MOVE — take one opinion your circle also holds and try to reconstruct the actual "
            "moment you were convinced. What specifically changed your mind, and when? If you "
            "cannot find it, you did not conclude it — you absorbed it. That does not make it "
            "wrong. It means you have never tested it, and you should stop spending it like it "
            "is earned.",
        ],
        "sources": [
            src("Greene — The Group Bias",
                "Isolation from the group is frightening and depressing, and finding others who "
                "think as we do brings enormous relief — so we adopt ideas partly because they "
                "supply that relief, without ever feeling the pull."),
            src("Greene — The Group Bias",
                "An orthodoxy settles over a party or ideology with nobody stating it and no "
                "overt pressure applied, and yet positions line up across dozens of separate "
                "issues while almost nobody will admit the influence."),
        ],
        "quiz": [
            {"q": "Someone can predict your view on five unrelated issues from knowing one. The "
                  "reason that matters is:",
             "c": ["it shows you are consistent",
                   "unrelated questions have no reason to correlate — they arrived as a set",
                   "it means you are well informed", "it shows you have strong principles"],
             "a": 1},
            {"q": "What does group influence actually feel like from the inside?",
             "c": ["pressure to conform", "relief at finding people who agree",
                   "anger", "nothing at all"], "a": 1},
            {"q": "You cannot reconstruct the moment an opinion convinced you. That means:",
             "c": ["the opinion is false",
                   "you absorbed it rather than concluded it — untested, not necessarily wrong",
                   "your memory is poor", "you should drop it immediately"], "a": 1},
        ],
        "apply": {"prompt": "Take one opinion your circle shares. Try to write down the specific "
                            "moment and thing that convinced you. If you cannot find one, write "
                            "that plainly — that is the finding.", "min": 50},
    },
    {
        "sid": "n1s5", "glyph": "\U0001f501", "title": "The Blame Bias",
        "why": "The group shapes what you believe. This is why experience never corrects any of "
               "it.",
        "bridge": [
            "THE TELL — you have an explanation for the failure, and it arrived FAST. Fluent, "
            "complete, ready before you had really looked. Real examination is slow and comes "
            "out ugly. A smooth account of why something went wrong is almost always the "
            "explaining reflex, not the looking.",
            "WHERE IT WILL CATCH YOU — every repeat. This is the bias with a signature: the same "
            "mistake, twice, with a different explanation each time. Greene's mechanism for why "
            "it repeats is time — whatever small share of blame you did accept fades, the "
            "pleasure principle comes back up, and the mistake is available again. His test is "
            "hard to argue with: if people genuinely learned from experience, mistakes would be "
            "rare and careers would climb steadily instead of repeating the same shapes.",
            "THE MOVE — rewrite the failure with yourself as the subject of every sentence. Not "
            "“the deadline moved” but “I planned with no slack.” Not "
            "“they were unclear” but “I did not ask.” You are not looking to "
            "feel bad; feeling bad is the thing that made you look away. You are looking for the "
            "one sentence that is yours, because that is the only part you can change next time.",
        ],
        "sources": [
            src("Greene — The Blame Bias",
                "Failure creates a need to explain, but we do not look closely; introspection is "
                "shallow and the reflex is to blame others, circumstances or a momentary lapse, "
                "because examining the mistake costs us our sense of superiority."),
            src("Greene — The Blame Bias",
                "If people truly learned from experience there would be few mistakes in the "
                "world, and careers would climb steadily upward."),
        ],
        "quiz": [
            {"q": "Your explanation for a failure came out fluent and complete within a minute. "
                  "The most likely reading is:",
             "c": ["you understand the situation well",
                   "that is the explaining reflex, not looking — real examination is slow and "
                   "comes out ugly",
                   "the failure was simple", "you have done this before"], "a": 1},
            {"q": "The signature of this bias is:",
             "c": ["blaming yourself too much",
                   "the same mistake repeating, with a different explanation each time",
                   "forgetting the mistake entirely", "arguing with colleagues"], "a": 1},
            {"q": "The point of rewriting a failure with yourself as the subject is to:",
             "c": ["feel appropriately guilty",
                   "find the one part you can actually change next time",
                   "prepare an apology", "assign blame fairly"], "a": 1},
        ],
        "apply": {"prompt": "Take something that went wrong recently where your first account "
                            "blamed circumstances or another person. Rewrite it with yourself as "
                            "the subject of every sentence, and mark the one line you could act "
                            "on next time.", "min": 50},
    },
    {
        "sid": "n1s6", "glyph": "\U0001fa9e", "title": "Superiority Bias",
        "why": "The five before this described the traps. This one explains why you have been "
               "reading them as descriptions of other people.",
        "bridge": [
            "THE TELL — the asymmetry in your explanations, and it is easy to catch once you "
            "look for it. Their success came from luck, connections, playing the game. Yours "
            "came from talent and work. Their opinions come from their tribe. Yours came from "
            "thinking. Same evidence, two different machines for reading it, and you only own "
            "one of them.",
            "WHERE IT WILL CATCH YOU — reading these six. Greene points out that almost nobody "
            "says “I am more rational and more ethical than most” aloud, because it "
            "sounds arrogant, and yet it is roughly what people report when polls ask them to "
            "compare themselves with others. He calls it an optical illusion, and the word is "
            "exact: other people's irrationality is visible, your own is not — not hidden, "
            "genuinely not visible from where you are standing.",
            "THE MOVE — go back through the five and find the one you were most confident did "
            "not apply to you. That confidence is a pointer, and it points at the blind spot, "
            "not away from it. Build the case that it does apply. Write it as if you were "
            "arguing against yourself and had good material.",
            "One last thing, and it is why the whole law is worth the walk rather than just "
            "depressing. Greene ends by saying being rational and being decent are not the "
            "settings you come with — if they were, the world would look nothing like it does. "
            "They are things you get to, through noticing and effort, over time. Which means "
            "every one of these six is workable, and that is the entire reason for doing the "
            "steps instead of reading the chapter.",
        ],
        "sources": [
            src("Greene — Superiority Bias",
                "We readily believe the other side reaches its opinions without rational "
                "principle while our own side reasons its way there, and we credit everything "
                "we have to talent and hard work while attributing other people's success to "
                "manoeuvring."),
            src("Greene — Superiority Bias",
                "Rationality and ethical quality do not arrive on their own. They are reached "
                "through awareness and effort, as a maturing process."),
        ],
        "quiz": [
            {"q": "The most reliable way to catch this one in yourself is to look at:",
             "c": ["how often you are right",
                   "the asymmetry — how you explain their success versus your own",
                   "what other people say about you", "your exam results"], "a": 1},
            {"q": "Greene calls it an optical illusion because:",
             "c": ["it involves eyesight",
                   "your own irrationality is not hidden from you, it is genuinely not visible "
                   "from where you stand",
                   "it goes away in good light", "others create it deliberately"], "a": 1},
            {"q": "Being confident that one of the six does not apply to you is best treated as:",
             "c": ["a fair result", "a pointer at the blind spot",
                   "a reason to move on", "evidence you learned the material"], "a": 1},
        ],
        "apply": {"prompt": "Name the one bias of the five before this that you were most sure "
                            "did not apply to you. Now write the case that it does — properly, "
                            "as if you were arguing against yourself with good material.",
                  "min": 50},
    },
]


def build_nodes():
    out = [PARENT]
    prev = None
    for i, s in enumerate(STEPS):
        n = {"id": s["sid"], "track": TID, "tier": i + 1, "parent": PARENT["id"],
             "prereq": [prev] if prev else [], "glyph": s["glyph"], "title": s["title"],
             "bridge": s["bridge"], "sources": s["sources"], "quiz": s["quiz"],
             "apply": s["apply"]}
        if prev:
            n["whyreq"] = s["why"]
        out.append(n)
        prev = s["sid"]
    return out


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))

    ids = {n["id"] for n in graph["nodes"]}
    nodes = build_nodes()
    clash = [n["id"] for n in nodes if n["id"] in ids]
    if clash:
        print("FAIL: these ids already exist:", clash)
        return 1
    if any(t["id"] == TID for t in graph["tracks"]):
        print(f"FAIL: track {TID} already exists — pick another id")
        return 1

    graph["tracks"].append(TRACK)
    graph["nodes"].extend(nodes)

    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
    except SystemExit:
        print("FAIL: validate() rejected the merged graph")
        return 1

    steps = [n for n in nodes if n.get("parent")]
    words = sum(len(p.split()) for n in nodes for p in n["bridge"])
    print(f"track {TID} — {TRACK['name']}")
    print(f"  1 main-path lesson + {len(steps)} steps, {words:,} words of lesson text")
    for n in nodes:
        kind = "  step" if n.get("parent") else "PATH  "
        print(f"  {kind} {n['id']:<7} tier={n['tier']} prereq={n['prereq'] or '[]'}  {n['title']}")
    if dry:
        print("\n--dry: graph.json NOT written")
        return 0
    shutil.copy(GRAPH, GRAPH + ".bak")
    json.dump(graph, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False,
              separators=(",", ":"))
    print("\ngraph.json updated (backup at graph.json.bak) -> next: python tools/build.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
