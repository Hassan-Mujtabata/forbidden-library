# -*- coding: utf-8 -*-
"""#172 JOB 5 — track O: What Everybody Is Saying (Joe Navarro).

HAND-AUTHORED and grounded in the book's own text (episodes 8, 10, 12, 17, 18, 22, 23 of
`navarro`), not written from memory of it.

DELIBERATELY FOUR FULL LESSONS, NOT TWELVE SMALL ONES. Hassan's correction: "dont try to cut too
much in to many mini paths that also makes it harder to understand... if you think the 2 stages
should be 1 you can make them in one." Freeze, flight and fight are ONE mechanism with three
faces, so they are one lesson, not three. The goal is that it makes sense, not that it is finely
diced.

And it is not a summary — see THE POINT in CONTINUE.md. Each lesson gives the mechanism (because
without it the signals are just superstition), what it actually looks like in a room, and one
thing to do. Lesson 4 exists because the first three are DANGEROUS without it: read singly,
without a baseline, body language becomes confident mind-reading. Navarro spends his opening
chapter on that discipline and it is not optional here either.

    python tools/path_navarro.py --dry
    python tools/path_navarro.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
BOOK = "What Everybody Is Saying"
TID = "O"

TRACK = {"id": TID, "name": "Reading the Body", "glyph": "\U0001f440", "accent": "#5d6d7e",
         "blurb": "Navarro's FBI work on why the body answers before the mouth does — and how "
                  "to read it without talking yourself into things."}


def src(ref, *q):
    return {"book": BOOK, "ref": ref, "quote": list(q)}


NODES = [
    {
        "id": "o1", "tier": 0, "prereq": [], "glyph": "\U0001f9e0",
        "title": "Why the Body Answers First",
        "bridge": [
            "Everything else in this book rests on one piece of anatomy, so it is worth getting "
            "right rather than taking on trust. You have a limbic system — the old survival "
            "machinery — and you have a neocortex, the thinking, speaking, planning part. The "
            "limbic system reacts to what is happening to you. It does it fast, it does it "
            "without asking, and crucially you cannot switch it off by deciding to.",
            "The neocortex is the part that can lie. It composes the sentence, arranges the "
            "face, picks the reassuring word. That is exactly why words are weak evidence about "
            "what someone actually feels: the organ producing them is the organ built for "
            "presentation. The limbic system has no such talent. It reacts, and the reaction "
            "shows up in the body whether or not it suits the story being told.",
            "This is what makes body language readable at all, and it is also the reason the "
            "usual advice to 'watch the face' is close to backwards. The face is the most "
            "rehearsed surface a person owns — it has been managed since childhood, and people "
            "are good at it. The further you get from the face, the less rehearsal there has "
            "been. Navarro's whole method points downward, toward the parts nobody thinks to "
            "arrange, because honesty in the body is a matter of how little attention a region "
            "gets, not of anything mystical.",
            "Two things follow, and both are practical. First: when the words and the body "
            "disagree, the disagreement itself is the finding — you have not caught a liar, you "
            "have caught a person whose limbic response does not match what they are choosing "
            "to say, and that is worth a question rather than an accusation. Second: this works "
            "on you too. Your own body is broadcasting during every negotiation, every "
            "difficult conversation, every time you claim to be fine. Knowing which parts you "
            "have never thought to manage tells you which parts are currently telling the truth "
            "about you.",
        ],
        "sources": [
            src("Navarro — Mastering the Secrets of Nonverbal Communication",
                "Anyone of normal intelligence can learn to decode nonverbal behaviour and use "
                "it, but it is a skill that takes real practice and proper training rather than "
                "a knack you either have or lack."),
            src("Navarro — Living Our Limbic Legacy",
                "The limbic brain is the honest one. It reacts to the world reflexively and "
                "immediately, without thought, which is precisely why its signals are worth "
                "more than the words assembled by the thinking part of the brain."),
        ],
        "quiz": [
            {"q": "Why are words weaker evidence of feeling than the body is?",
             "c": ["people are usually lying",
                   "words come from the part of the brain built for composing and presenting; "
                   "the limbic reaction is not built for that",
                   "words are ambiguous", "the body is easier to see"], "a": 1},
            {"q": "Navarro's method points away from the face because:",
             "c": ["faces are hard to see",
                   "the face is the most rehearsed surface a person owns — honesty tracks how "
                   "little attention a region gets",
                   "faces do not move enough", "expressions are universal"], "a": 1},
            {"q": "Someone's words and body disagree. The correct reading is:",
             "c": ["they are lying to you",
                   "their limbic response does not match what they are choosing to say — which "
                   "is a reason to ask, not to accuse",
                   "the body is always right about the topic", "you misread the body"], "a": 1},
        ],
        "apply": {"prompt": "In your next real conversation, spend one minute watching below the "
                            "neck instead of the face. Write what you noticed and whether it "
                            "agreed with what was being said.", "min": 50},
    },
    {
        "id": "o2", "tier": 1, "prereq": ["o1"], "glyph": "\U0001f6d1",
        "title": "Freeze, Flight, Fight — In That Order",
        "why": "You know where the signals come from. This is what the machinery actually does, "
               "and the order is the part everyone gets wrong.",
        "bridge": [
            "Almost everyone says 'fight or flight'. Navarro is blunt that this is two-thirds "
            "right and backwards besides. The real sequence, the one your body has run for a "
            "million years, is FREEZE first, then FLIGHT, then FIGHT — and knowing the order "
            "matters because the first response is the one you will actually see most often and "
            "the one you are least likely to notice.",
            "FREEZE comes first because movement is what attracts a predator. Hold still and you "
            "may not be seen at all. In a room with no predators in it this shows up as sudden "
            "stillness: the hands that were gesturing stop, someone's feet lock, breathing goes "
            "shallow, a person who was shifting in their chair becomes strangely composed. It "
            "reads as calm. It is very often the opposite of calm, and Navarro's example is a "
            "child who has always run to hug an uncle and this year stands rigid — nothing was "
            "said, and everything was said.",
            "FLIGHT comes second, and in a room you cannot actually flee from, it becomes "
            "distancing. Feet angle toward the exit. The torso turns away by degrees. Someone "
            "leans back, puts an object between you — a bag, a laptop, a coffee cup moved into "
            "the space. Blocking behaviours belong here too: eyes shut a moment too long, a hand "
            "that covers. Nobody is leaving, but the body is doing leaving in miniature.",
            "FIGHT is last, because it is the most expensive and the most dangerous, which is "
            "why it is a final resort rather than a first move. In modern settings it rarely "
            "arrives as violence; it arrives as aggression that has been made socially "
            "acceptable — the argument that sharpens, territorial spreading, a chest and chin "
            "that come forward, sustained staring, a voice that hardens. The useful thing to "
            "know is that if you are seeing fight, you have very likely already missed a freeze "
            "and a flight earlier in the same conversation.",
            "That last point is the practical one. These are stages of one escalating system, "
            "not three separate moods. If you learn to catch the freeze — the stillness that "
            "looks like composure — you get the earliest possible warning that something has "
            "gone wrong, at the point where a question can still fix it. Wait for fight and you "
            "are negotiating with someone whose survival machinery is already fully engaged.",
        ],
        "sources": [
            src("Navarro — Our Limbic Responses: The Three F's",
                "The brain's answer to threat took three forms — freeze, flight, and fight — and "
                "in that order. The familiar phrase 'fight or flight' is only two-thirds "
                "accurate and has the order backwards."),
            src("Navarro — The Freeze Response",
                "Movement draws attention, so the limbic system's first defence was to hold "
                "still. Predators are drawn to what moves, which is why freezing in the face of "
                "danger kept our ancestors alive."),
        ],
        "quiz": [
            {"q": "Mid-conversation, someone who had been gesturing goes completely still and "
                  "their feet stop moving. The most likely reading is:",
             "c": ["they have relaxed and are listening",
                   "a freeze response — the earliest sign something just went wrong",
                   "they are bored", "they are about to agree"], "a": 1},
            {"q": "Why does Navarro insist the order is freeze, flight, fight?",
             "c": ["it is alphabetical",
                   "freezing is the cheapest and safest first move, and fighting the most "
                   "expensive last resort",
                   "it is easier to remember", "the order does not matter"], "a": 1},
            {"q": "You are seeing clear fight behaviour — spreading, hard voice, chin forward. "
                  "What does that tell you about earlier in the conversation?",
             "c": ["nothing, fight can start cold",
                   "you very likely missed a freeze and a flight already",
                   "the person is aggressive by nature",
                   "the conversation was fine until now"], "a": 1},
        ],
        "apply": {"prompt": "Think back to a conversation that went badly. Write down the "
                            "earliest moment you can now identify where the other person went "
                            "still or turned away slightly — and what you would have asked if "
                            "you had caught it then.", "min": 50},
    },
    {
        "id": "o3", "tier": 2, "prereq": ["o2"], "glyph": "\U0001f590",
        "title": "Pacifiers — The Tell After the Tell",
        "why": "The three responses are fast and easy to miss. What follows them is slow, "
               "obvious, and lasts long enough to actually see.",
        "bridge": [
            "This is the highest-value thing in the book and it is almost never taught, so it is "
            "worth stating plainly: after a limbic response, the brain sends the body to comfort "
            "itself. Navarro calls these pacifying behaviours. Something unpleasant registers — "
            "a question, a name, a number, a person walking in — and then the hand goes to the "
            "neck, or rubs the leg, or touches the face; the fingers find something to play "
            "with; someone exhales through pursed lips or adjusts a collar that did not need "
            "adjusting.",
            "Why this beats watching for the stress response itself is simple mechanics. The "
            "freeze is fast and easy to miss, especially if you were talking. The pacifier "
            "arrives after it, is larger, and often continues for several seconds. You get a "
            "second chance at a moment you already missed — and the pacifier points backwards, "
            "which is what makes it useful. Whatever was happening a beat BEFORE the hand went "
            "to the neck is the thing that caused it.",
            "The neck is the region worth learning first. It is vulnerable, it is loaded with "
            "nerve endings, and people go there constantly under stress without any idea they "
            "are doing it — covering the hollow at the throat, stroking the side, men often "
            "adjusting a tie or collar. Hands and face come next: the cheek rub, the forehead "
            "wipe, the mouth that gets covered. None of these is a lie detector. Each one is a "
            "timestamp saying discomfort, right here.",
            "So the discipline is to stop asking 'is this person lying' — a question the body "
            "cannot answer — and start asking 'what just happened'. Say a number in a "
            "negotiation and watch for the neck. Mention a name and watch the hands. You are not "
            "reading minds; you are noticing which of the things you said landed badly enough "
            "that a nervous system had to be soothed afterwards. That is a real and specific "
            "piece of information, and it is available to you several times in any difficult "
            "conversation.",
        ],
        "sources": [
            src("Navarro — The Importance of Pacifying Behaviors",
                "Whenever there is a limbic response, especially to something negative or "
                "threatening, it is followed by pacifying behaviours — actions that calm us "
                "after something unpleasant, as the brain enlists the body to restore normal "
                "conditions."),
            src("Navarro — Comfort/Discomfort and Pacifiers",
                "The limbic brain is built to seek safety and avoid discomfort, and it leaks "
                "that state through the body: comfort shows as body language that matches it, "
                "and distress shows as behaviour that mirrors the distress."),
        ],
        "quiz": [
            {"q": "You name a figure in a negotiation and the other person's hand goes to their "
                  "neck. The useful conclusion is:",
             "c": ["they are lying about their budget",
                   "that figure landed badly enough to need soothing — the pacifier timestamps "
                   "what came just before it",
                   "they are uncomfortable in the room", "they have a sore neck"], "a": 1},
            {"q": "Why is a pacifier often easier to catch than the stress response itself?",
             "c": ["it is more honest",
                   "it comes afterwards, is larger, and lasts longer — a second chance at a "
                   "moment you missed",
                   "it only happens when lying", "it is always the neck"], "a": 1},
            {"q": "The question to replace 'is this person lying?' with is:",
             "c": ["what are they hiding?", "what just happened?",
                   "are they trustworthy?", "what do they want?"], "a": 1},
        ],
        "apply": {"prompt": "In your next difficult conversation, watch only for hands going to "
                            "the neck or face. When you see one, write down what was said in the "
                            "two seconds before it.", "min": 50},
    },
    {
        "id": "o4", "tier": 3, "prereq": ["o3"], "glyph": "\U0001f4d0",
        "title": "Baseline, Cluster, Context — Or You Are Just Guessing",
        "why": "The three lessons before this are actively dangerous without this one. It is "
               "what separates reading someone from talking yourself into things.",
        "bridge": [
            "Everything above becomes nonsense the moment you read a single signal on its own, "
            "and the failure has a shape worth naming: you learn that crossed arms mean "
            "defensiveness, you see crossed arms, and you now believe something about a person "
            "that you invented. It feels like perception. It is confirmation bias wearing a "
            "lab coat. Navarro opens his book with the discipline that prevents this, and it is "
            "three requirements that all have to be met.",
            "BASELINE first. You cannot read a deviation without knowing what the person is like "
            "normally. Some people fidget constantly; some are still by nature; some touch their "
            "face all day long. The signal is never the behaviour — it is the CHANGE from that "
            "person's own normal. Navarro's example is exact: the child who has hugged his uncle "
            "every year and this year stands frozen. The freeze means something only because "
            "eight previous years established what he usually does. With a stranger you have no "
            "baseline yet, so spend the first minutes building one instead of drawing "
            "conclusions.",
            "CLUSTER second. One behaviour is noise. People cross their arms because the room is "
            "cold, touch their neck because their collar itches, lean back because the chair is "
            "uncomfortable. You want three or four things pointing the same way at the same "
            "time — the feet turn toward the door AND the torso angles away AND an object gets "
            "moved into the space between you. A cluster is evidence. A single tell is a "
            "coincidence you have decided to find meaningful.",
            "CONTEXT third, and it is the one people skip. The same behaviour means different "
            "things in different situations. Someone stiff and self-soothing in a job interview "
            "is a person in a job interview; that is what the situation does to nearly everyone, "
            "and it tells you almost nothing about their character or their honesty. The same "
            "cluster appearing when you mention one particular project, in an otherwise relaxed "
            "chat, is worth everything.",
            "Put together, these three turn the whole skill from mind-reading into something "
            "much more modest and much more useful: you are noticing that this particular "
            "person, compared to how they were five minutes ago, changed in several ways at "
            "once, right after a specific thing occurred. That is all you ever get. It happens "
            "to be enough — it tells you where to ask the next question, which is the only thing "
            "you actually needed. And the honest limit is worth keeping: none of this reveals "
            "WHY. Discomfort is not guilt. It is a pointer to a subject, not a verdict on a "
            "person, and the moment you treat it as a verdict you have gone back to inventing "
            "things and given it a scientific name.",
        ],
        "sources": [
            src("Navarro — It's a Relative Matter",
                "What matters is the deviation from a person's own baseline. The boy had always "
                "run to hug his uncle and this time stood frozen — the change from his usual "
                "behaviour is the signal that something warrants attention."),
            src("Navarro — Mastering the Secrets of Nonverbal Communication",
                "Reading people is collecting nonverbal intelligence about thoughts, feelings "
                "and intentions, and it demands constant practice and proper guidelines rather "
                "than a single behaviour read in isolation."),
        ],
        "quiz": [
            {"q": "You notice someone has crossed their arms and conclude they are defensive. "
                  "What has actually happened?",
             "c": ["you read the signal correctly",
                   "you read a single behaviour with no baseline, cluster or context — that is "
                   "invention, not observation",
                   "you need to check their feet too", "you were right but should confirm"],
             "a": 1},
            {"q": "A candidate is stiff and touching their neck throughout a job interview. This "
                  "mainly tells you:",
             "c": ["they are hiding something",
                   "almost nothing — that is what the situation does to nearly everyone",
                   "they are unsuitable", "they are lying on their CV"], "a": 1},
            {"q": "What is the honest limit of everything in this track?",
             "c": ["it reveals what someone is thinking",
                   "it points at a subject worth asking about — it never tells you WHY, and "
                   "discomfort is not guilt",
                   "it detects lies reliably", "it works best on strangers"], "a": 1},
        ],
        "apply": {"prompt": "Pick someone you see often. Spend one conversation building only "
                            "their baseline — how much they normally move, touch their face, "
                            "shift position. Write it down. Do not interpret anything yet.",
                  "min": 50},
        # The `pattern` component was built for exactly this claim and comes with the research
        # already done (tools/figs_research, Bond & DePaulo 2006: 206 studies, 24,483 observers —
        # 54% accuracy reading a single encounter, and 47% on actual lies, i.e. worse than a coin
        # toss). Navarro's baseline rule and that meta-analysis are the same finding from two
        # directions, so this is a correct reuse rather than a component picked because it looked
        # nice. Its stages are "one" -> "run" -> "trend"; the noise in the run is real noise.
        "fig": [{
            "v": 1,
            "alt": "A single conversation plotted against a neutral line, unreadable on its own; "
                   "then nine conversations with the same person, two of them positive; then the "
                   "downward trend across the nine, which is the only thing that was ever the "
                   "signal",
            "cap": "One conversation tells you nothing",
            "place": 2,
            "dur": 11,
            "stages": [
                {"cap": "Here is one encounter, slightly negative. Read it honestly and there is "
                        "nothing there — it could be the chair, the day, the coffee, you.",
                 "feel": "This is the moment you normally decide, and it feels like reading "
                         "someone. Across 206 studies it is a coin toss: 54% on one encounter, "
                         "47% on actual lies — worse than guessing.",
                 "scene": [{"c": "pattern", "stage": "one", "mid": "their normal",
                            "n1": "one conversation"}]},
                {"cap": "Now nine, with the same person. Two of them are positive, because that "
                        "is what real noise looks like — a run you had to cherry-pick is not a "
                        "run.",
                 "feel": "This is what a baseline actually is. Not a theory about them: nine "
                         "observations of how they normally are, which you can only get by "
                         "watching without concluding.",
                 "scene": [{"c": "pattern", "stage": "run", "mid": "their normal",
                            "n2": "nine of them"}]},
                {"cap": "And there it is — the drift the single encounter could never have shown "
                        "you. The signal was never in any one of these. It was only ever in the "
                        "set.",
                 "feel": "Which is why the discipline is baseline, cluster, context. Not caution "
                         "for its own sake — it is the only arrangement in which there is "
                         "anything real to see.",
                 "scene": [{"c": "pattern", "stage": "trend", "mid": "their normal",
                            "n3": "that's the signal"}]},
            ],
        }],
    },
]


def build_nodes():
    out = []
    for n in NODES:
        d = {"id": n["id"], "track": TID, "tier": n["tier"], "prereq": n["prereq"],
             "glyph": n["glyph"], "title": n["title"], "bridge": n["bridge"],
             "sources": n["sources"], "quiz": n["quiz"], "apply": n["apply"]}
        if n.get("why"):
            d["whyreq"] = n["why"]
        if n.get("fig"):
            d["fig"] = n["fig"]
        out.append(d)
    return out


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))
    ids = {n["id"] for n in graph["nodes"]}
    nodes = build_nodes()
    clash = [n["id"] for n in nodes if n["id"] in ids]
    if clash:
        print("FAIL: ids already exist:", clash)
        return 1
    if any(t["id"] == TID for t in graph["tracks"]):
        print(f"FAIL: track {TID} already exists")
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
    words = sum(len(p.split()) for n in nodes for p in n["bridge"])
    print(f"track {TID} — {TRACK['name']}: {len(nodes)} lessons, {words:,} words")
    for n in nodes:
        print(f"  {n['id']:<5} tier={n['tier']} prereq={n['prereq'] or '[]'}  {n['title']}")
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
