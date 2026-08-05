# -*- coding: utf-8 -*-
"""#177 JOB 5 — track Q: How to Win Friends and Influence People. Fourth uncovered book covered.

THE DESIGN DECISION. Carnegie's book is a numbered list — 4 parts, ~30 principles, each stated
outright in the chapter titles. The obvious move is to mirror that: 4 parents, 30 steps. That
would make it HARDER, not easier, and Hassan's rule decides it: thirty rules is thirty things to
remember and gives you no way to produce a thirty-first.

Underneath the thirty there are four mechanisms. "Give honest appreciation", "remember names",
"be a good listener", "make them feel important" and "praise the slightest improvement" are one
mechanism. "Don't criticise", "show respect for opinions", "let them save face", "talk about your
own mistakes first" are another. Learn four things that generate thirty, and the thirty stop
needing memorising — they become obvious consequences.

Carnegie's own principles are the worked instances inside each lesson, so nothing is lost: the
list is still all there, it is just no longer the organising idea.

    python tools/path_winfriends.py --dry
    python tools/path_winfriends.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
BOOK = "How to Win Friends and Influence People"
TID = "Q"

TRACK = {"id": TID, "name": "Dealing With People", "glyph": "\U0001f91d", "accent": "#4a90b8",
         "blurb": "Carnegie's thirty rules are four mechanisms wearing thirty coats. Learn the "
                  "four and the rules stop needing to be remembered."}


def src(ref, *q):
    return {"book": BOOK, "ref": ref, "quote": list(q)}


NODES = [
    {
        "id": "q1", "tier": 0, "prereq": [], "glyph": "\U0001f31f",
        "title": "The Importance Deficit",
        "bridge": [
            "Roughly a third of Carnegie's principles are the same instruction in different "
            "clothes: give honest appreciation, become genuinely interested in people, remember "
            "names, be a good listener, talk in terms of their interests, make the other person "
            "feel important, praise the slightest improvement, give them a fine reputation to "
            "live up to. Learn them as eight rules and you have eight things to remember. Learn "
            "the mechanism underneath and they become obvious.",

            "The mechanism is this: almost everyone is running a permanent deficit of feeling "
            "significant, and almost nobody around them is doing anything about it. Their "
            "colleagues are thinking about themselves. Their family has stopped noticing. The "
            "deficit is not a weakness in insecure people — it is the default condition, because "
            "attention is scarce and self-interest is not. Which means supplying it is unusually "
            "cheap and unusually powerful, and that asymmetry is the whole engine.",

            "Why this must be so is worth a moment, because it explains the strange strength of "
            "the effect. Nearly every interaction someone has is transactional in its attention: "
            "people listen in order to reply, ask questions in order to get to their own point, "
            "and remember what is useful to them. Genuine attention is therefore rare, and rare "
            "things are valuable. You are not manipulating a lever. You are supplying something "
            "in short supply, and the response is proportional to the shortage.",

            "That is also why the specific rules take the shape they do. A name is the single "
            "sound a person is most attached to and the one strangers reliably fail to retain, "
            "so using it is a costless proof of attention. Listening works for the same reason: "
            "most 'listening' is waiting, and the difference is detectable. Asking about what "
            "they care about rather than steering to what you care about is the same act again. "
            "You do not need the list once you have the mechanism — you can generate the "
            "thirty-first rule yourself.",

            "Run a case. Someone on your team has done something competent but unremarkable. The "
            "ordinary response is nothing at all, because nothing went wrong. Carnegie's move is "
            "to name it specifically — not 'good job', which is noise, but the particular thing "
            "they did and why it mattered. Specificity is what separates it from flattery, and "
            "it is also what makes it land: general praise proves nothing, while 'you caught "
            "that the numbers were from the wrong quarter' proves you were paying attention, "
            "which was the scarce thing all along.",

            "The objection, and Carnegie gets it constantly: this is just flattery with better "
            "manners, and people can smell it. Half right. Flattery is telling someone what they "
            "want to hear regardless of truth, and it fails precisely because it is unfalsifiable "
            "— it proves no attention was paid. Appreciation is reporting something true that "
            "you noticed. The reason Carnegie keeps saying HONEST appreciation is not moral "
            "decoration; it is the load-bearing part. Insincere praise fails at exactly the thing "
            "the mechanism runs on.",

            "The edge: this is not a technique for getting things from people, and used that way "
            "it degrades fast. Attention supplied in order to extract something is detectable "
            "over any period longer than one conversation, because the pattern shows — the "
            "interest appears when something is needed and vanishes afterwards. What survives "
            "contact with time is the habit of actually noticing people, which is a slower and "
            "much less impressive-sounding thing than a technique.",
        ],
        "sources": [
            src("Carnegie — Principle 2, Part One",
                "Give honest and sincere appreciation. The emphasis on honest is not politeness "
                "— insincere praise fails because it proves no attention was paid."),
            src("Carnegie — Part Two, Principles 1-6",
                "Become genuinely interested in other people, remember their names, listen and "
                "encourage them to talk about themselves, speak in terms of their interests, and "
                "make them feel important."),
        ],
        "quiz": [
            {"q": "Why is genuine attention so disproportionately powerful?",
             "c": ["people are vain",
                   "it is scarce — most listening is waiting to reply, so real attention is a "
                   "rare good",
                   "it is hard to do", "it flatters people"], "a": 1},
            {"q": "What actually separates appreciation from flattery?",
             "c": ["how warmly it is said",
                   "specificity — a specific true observation proves attention was paid; general "
                   "praise proves nothing",
                   "who says it", "saying it in public"], "a": 1},
            {"q": "Where does this stop working?",
             "c": ["with strangers",
                   "when the attention is supplied in order to extract something — the pattern "
                   "shows over time",
                   "in writing", "with senior people"], "a": 1},
        ],
        "apply": {"prompt": "Today, tell one person the specific thing you noticed them do and "
                            "why it mattered. Not 'good job'. The particular thing. Write what "
                            "you said and what happened.", "min": 50},
    },
    {
        "id": "q2", "tier": 1, "prereq": ["q1"], "glyph": "\U0001f6e1️",
        "title": "A Threatened Ego Stops Processing",
        "why": "The first mechanism is about supplying something. This one is about the thing "
               "that shuts the whole channel down.",
        "bridge": [
            "Another large block of the book is one mechanism: don't criticise or condemn, show "
            "respect for the other person's opinions, never say 'you're wrong', talk about your "
            "own mistakes first, let the other person save face, call attention to errors "
            "indirectly, begin with praise. Eight rules, one fact.",

            "The fact: when a person's self-image is threatened, they stop processing "
            "information and start defending. This is not stubbornness and it is not a character "
            "flaw in difficult people — it is what everyone does, including you, and it happens "
            "before you have decided anything. Once it fires, every subsequent thing you say is "
            "being evaluated for threat rather than for truth, which means the accuracy of your "
            "argument has stopped mattering entirely.",

            "That is the part worth sitting with, because it explains a thing you have "
            "experienced many times: being completely right and getting nowhere. Correctness "
            "operates on the channel that closed. You can be right, have evidence, be patient — "
            "and none of it reaches a system that has switched from evaluating to defending. "
            "Carnegie's rules are not about being nice. They are about keeping the channel open "
            "long enough for anything to get through it.",

            "This also explains why each specific rule works. Talking about your own mistakes "
            "first lowers the status gap, so the correction is no longer an attack from above. "
            "Letting someone save face means they can change position without the change being "
            "a public defeat — you are removing the cost of agreeing with you. Indirect "
            "correction lets them arrive at the error themselves, so nothing has to be conceded. "
            "Every one of them is doing the same job: making it cheap to be wrong.",

            "Run a case. A colleague's document has a real error in it. Version A: 'this is "
            "wrong, the figures are from the wrong quarter.' Accurate, efficient, and now you "
            "are in a defence. Version B: 'I've done this exact thing — can you check which "
            "quarter these came from?' Same information, same outcome required, but the second "
            "does not require them to accept a loss in front of you to act on it. The error gets "
            "fixed either way; the difference is whether the next thing you say still lands.",

            "The objection: is this not just avoiding hard conversations, and is it not a bit "
            "dishonest — dressing up a correction so nobody has to feel anything? It would be, "
            "if the content were softened. It is not. The error still gets named and still gets "
            "fixed. What is removed is the STATUS cost, not the substance, and those are "
            "separable. Carnegie is not saying avoid the correction. He is saying that a "
            "correction delivered so it triggers defence has not been delivered at all, however "
            "clearly it was stated.",

            "The edge, and it is a real one: this can become conflict-avoidance wearing a "
            "technique. Some things need to be said flatly, and some people use 'begin with "
            "praise' to bury the point so thoroughly that nobody notices a correction happened. "
            "The test is whether the substance survived intact. If softening the delivery also "
            "softened the message, you have not applied this — you have used it as cover for not "
            "wanting the conversation.",
        ],
        "sources": [
            src("Carnegie — Part Three, Principles 1-3",
                "Show respect for the other person's opinions and never say 'you're wrong'; if "
                "you are wrong, admit it quickly and emphatically."),
            src("Carnegie — Part Four, Principles 2-5",
                "Call attention to mistakes indirectly, talk about your own errors before "
                "criticising, ask questions rather than giving orders, and let the other person "
                "save face."),
        ],
        "quiz": [
            {"q": "Why does being right so often achieve nothing?",
             "c": ["people are irrational",
                   "once the ego is threatened the channel switches from evaluating to "
                   "defending, and accuracy stops being what is measured",
                   "you explained it badly", "they did not hear you"], "a": 1},
            {"q": "What are 'let them save face' and 'admit your own mistakes first' both doing?",
             "c": ["being polite",
                   "making it cheap to be wrong, so changing position costs no status",
                   "delaying the correction", "building rapport"], "a": 1},
            {"q": "You have used this badly when:",
             "c": ["the other person felt fine",
                   "softening the delivery also softened the message — the substance did not "
                   "survive",
                   "you began with praise", "it took longer"], "a": 1},
        ],
        "apply": {"prompt": "Take a correction you need to give. Write it twice — once flatly, "
                            "once so the person can act on it without conceding anything. Check "
                            "the second still contains the whole of the first.", "min": 50},
    },
    {
        "id": "q3", "tier": 2, "prereq": ["q2"], "glyph": "\U0001f9f2",
        "title": "Nobody Acts On Your Reasons",
        "why": "You can keep the channel open and still be refused. This is why — you have been "
               "supplying the wrong reasons.",
        "bridge": [
            "The third mechanism is the one Carnegie states most directly and that people ignore "
            "most completely: arouse in the other person an eager want. Alongside it sit 'talk "
            "in terms of the other person's interests', 'try honestly to see things from their "
            "point of view', and 'appeal to the nobler motives'. Same machinery.",

            "The mechanism: people act on their own reasons, never on yours. This sounds "
            "obvious and is almost universally violated, because when you want something you "
            "have a vivid set of reasons — they are yours, they are compelling, and they are "
            "immediately available. So you present those. And the other person, who does not "
            "share your situation, is being handed an argument built for someone else's "
            "circumstances.",

            "Why it is so hard to avoid is worth naming, because knowing the rule does not fix "
            "it. Your reasons feel like THE reasons rather than like yours specifically. There "
            "is no felt difference between 'this is important' and 'this is important to me', "
            "which is why the mistake survives being pointed out. Correcting it takes a "
            "deliberate step: before asking, work out what this person wants, and check whether "
            "what you want can be routed through it.",

            "Run a case. You need a colleague to take over a piece of work. Your reasons: you "
            "are overloaded, the deadline is close, you have too much on. All true, all "
            "concerning your situation, none concerning theirs — and the honest translation of "
            "your request is 'please absorb my problem'. Now find theirs. Maybe they want "
            "visibility with a team this work touches. Maybe they have said they want to learn "
            "this system. Maybe they would rather have this than the thing they are on. If any "
            "of those is real, the same request becomes an offer, and it is not a trick — the "
            "work genuinely does deliver that for them. You changed which true thing you led with.",

            "The objection: is this not manipulation — dressing up what you want as what they "
            "want? The test is whether the benefit is real. If the work genuinely gives them "
            "visibility, saying so is information they need in order to decide well. If it "
            "does not and you imply it does, that is a lie, and it has the usual half-life. "
            "Carnegie's version fails exactly here for people who use it cynically: the "
            "technique is durable only when the thing you claim is actually true.",

            "The edge, and it is where this stops applying: sometimes there is no overlap. What "
            "you want genuinely offers them nothing, and no amount of reframing will invent an "
            "interest that does not exist. At that point this mechanism is finished, and the "
            "honest move is to ask plainly as a favour, which is a real and respectable thing "
            "to do. Pretending an interest exists when it does not is worse than asking "
            "directly, because it insults them and it does not work twice.",
        ],
        "sources": [
            src("Carnegie — Principle 3, Part One",
                "Arouse in the other person an eager want — the only way to influence anyone is "
                "to talk about what they want and show them how to get it."),
            src("Carnegie — Part Three, Principles 8-10",
                "Try honestly to see things from the other person's point of view, be "
                "sympathetic with their ideas and desires, and appeal to the nobler motives."),
        ],
        "quiz": [
            {"q": "Why do people keep leading with their own reasons despite knowing better?",
             "c": ["they are selfish",
                   "your reasons feel like THE reasons — there is no felt difference between "
                   "'this is important' and 'important to me'",
                   "they forget", "it is faster"], "a": 1},
            {"q": "What separates this from manipulation?",
             "c": ["how you phrase it",
                   "whether the benefit you name is actually real — if it is, you supplied "
                   "information they needed to decide",
                   "asking permission", "doing it in person"], "a": 1},
            {"q": "There is genuinely no overlap between what you want and their interests. The "
                  "honest move is:",
             "c": ["find a better angle", "ask plainly, as a favour",
                   "offer something in exchange", "drop it"], "a": 1},
        ],
        "apply": {"prompt": "Take something you need from someone this week. Write your reasons, "
                            "then write theirs. If there is a real overlap, lead with it. If "
                            "there genuinely isn't, ask plainly as a favour.", "min": 50},
    },
    {
        "id": "q4", "tier": 3, "prereq": ["q3"], "glyph": "\U0001f511",
        "title": "A Conclusion They Reached Is One They'll Defend",
        "why": "The first three get you heard and get you agreement. This is the one that makes "
               "the agreement survive after you leave the room.",
        "bridge": [
            "The last mechanism is the least intuitive and the most useful: ask questions "
            "instead of giving orders, let the other person do the talking, let them feel the "
            "idea is theirs, give them a fine reputation to live up to, throw down a challenge. "
            "Every one is doing the same work.",

            "The mechanism: people defend conclusions they reached far more reliably than "
            "conclusions they were handed. An instruction you accepted is external — it lives "
            "outside your self-image, it can be dropped when circumstances change, and "
            "abandoning it costs nothing. A conclusion you arrived at is part of how you see "
            "yourself, and abandoning it means admitting you were wrong. So it gets defended, "
            "maintained, and acted on without supervision.",

            "This is why compliance decays and ownership does not, and it explains something "
            "you have watched happen: a plan everyone agreed to in the meeting quietly not "
            "happening afterwards. Nobody lied. They agreed to your conclusion, which was never "
            "theirs, and the agreement had no roots in anything they would defend. The work of "
            "the meeting did not fail — it was never done.",

            "That makes the rules mechanical rather than moral. A question instead of an order "
            "means they produce the answer, so the answer is theirs. Letting them talk lets them "
            "assemble the reasoning rather than receive it. 'Give them a fine reputation to live "
            "up to' works because a stated identity is something people become consistent with — "
            "tell someone they are the sort of person who is careful about detail and you have "
            "created something they now have to defend, and they will defend it without you.",

            "Run a case. You want a process changed. Version A: you explain the new process, "
            "they agree, and in three weeks it has quietly reverted. Version B: you describe the "
            "problem, ask how they would solve it, and shape from what they produce. It is "
            "slower, it may not land exactly where you would have put it, and it holds — because "
            "reverting now means contradicting themselves rather than contradicting you.",

            "The objection, and it is the strongest one against Carnegie generally: is this not "
            "just deception with good manners? Engineering someone into thinking your idea was "
            "theirs? It would be if you had a fixed answer and were merely staging a "
            "consultation, and people detect that quickly — the tell is that no answer they give "
            "changes the outcome. Done honestly you are genuinely giving up control of the "
            "solution. You bring the problem; the answer is actually open; you accept a result "
            "different from the one you had in mind. That is the price, and the durability is "
            "what you buy with it.",

            "The edge: this is wrong when the answer genuinely is not open. If there is a legal "
            "requirement, a safety rule, or a decision already made above you, running a fake "
            "consultation is worse than giving the instruction — it wastes their time and it "
            "teaches them their input does not matter, which poisons the next occasion when it "
            "would have. Say plainly that it is decided, and use the previous mechanism to "
            "explain why in terms that connect to them.",
        ],
        "sources": [
            src("Carnegie — Part Four, Principles 4 and 7",
                "Ask questions instead of giving direct orders, and give the other person a fine "
                "reputation to live up to."),
            src("Carnegie — Part Three and Four",
                "Let the other person do a great deal of the talking and feel that the idea is "
                "theirs; throw down a challenge when you want something done well."),
        ],
        "quiz": [
            {"q": "Why does an instruction decay while a conclusion holds?",
             "c": ["instructions are forgotten",
                   "a conclusion you reached is part of your self-image, so dropping it means "
                   "admitting you were wrong",
                   "people dislike being told", "conclusions are better reasoned"], "a": 1},
            {"q": "The tell that a consultation is fake is:",
             "c": ["it is short", "no answer they give would change the outcome",
                   "it happens by email", "the boss is present"], "a": 1},
            {"q": "The decision is already made above you and cannot change. You should:",
             "c": ["ask for their ideas anyway to build ownership",
                   "say plainly that it is decided and explain why in terms that connect to them",
                   "give the order with no explanation", "delay telling them"], "a": 1},
        ],
        "apply": {"prompt": "Take something you want changed. Instead of proposing the change, "
                            "describe the problem to the person and ask how they would fix it — "
                            "and genuinely accept an answer different from yours. Write what "
                            "they said.", "min": 50},
    },
]


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))
    ids = {n["id"] for n in graph["nodes"]}
    nodes = []
    for n in NODES:
        d = {"id": n["id"], "track": TID, "tier": n["tier"], "prereq": n["prereq"],
             "glyph": n["glyph"], "title": n["title"], "bridge": n["bridge"],
             "sources": n["sources"], "quiz": n["quiz"], "apply": n["apply"]}
        if n.get("why"):
            d["whyreq"] = n["why"]
        nodes.append(d)
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
    for n in nodes:
        w = sum(len(p.split()) for p in n["bridge"])
        print(f"  {n['id']}  {w:>5} words ({w/200:.0f}-{w/150:.0f} min)  {n['title']}")
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
