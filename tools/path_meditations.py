# -*- coding: utf-8 -*-
"""#175 JOB 5 — track P: Meditations (Marcus Aurelius). Third uncovered book covered.

Grounded in the book's own text (episode 8, The Second Book), not from memory of Stoicism.

THREE lessons, each carrying the full working per the standard in tools/deepen.py: mechanism down
to why it must be so, one case run to the end, the obvious objection answered, and the edge.

The choice of three is not a summary of Stoicism — it is the three moves Aurelius actually runs
on himself, repeatedly, in a private notebook. That framing is the point of lesson three and it
is the thing that makes the book usable rather than quotable.

    python tools/path_meditations.py --dry
    python tools/path_meditations.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
BOOK = "Meditations"
TID = "P"

TRACK = {"id": TID, "name": "Meditations", "glyph": "\U0001f3db️", "accent": "#8a94a6",
         "blurb": "Not philosophy to agree with — the three moves a Roman emperor ran on himself "
                  "every morning, and why he had to keep writing them down."}


def src(ref, *q):
    return {"book": BOOK, "ref": ref, "quote": list(q)}


NODES = [
    {
        "id": "p1", "tier": 0, "prereq": [], "glyph": "⚖️",
        "title": "The Step You Don't Know You're Taking",
        "bridge": [
            "The Stoic claim that sounds like a platitude is that things do not upset you, your "
            "judgements about them do. Read as a slogan it is useless and slightly insulting — "
            "of course the traffic is annoying. It becomes something else entirely when you "
            "treat it as a claim about MECHANISM, which is what it was, so it is worth going "
            "down to why it has to be true rather than taking it as consolation.",

            "Between an event and your distress there is a step. Something happens; you appraise "
            "it — this is bad, this is unfair, this should not be, this will not stop — and the "
            "distress follows from the appraisal, not from the event. You do not experience "
            "that middle step, which is the entire difficulty. It runs fast and silently, and "
            "what reaches awareness is 'this is upsetting', arriving as though it were a "
            "property of the event itself rather than a conclusion you drew about it.",

            "The proof that the step exists is that the same event produces different distress "
            "in different people, and in you on different days. A delayed flight ruins one "
            "person's week and another person opens a book. Nothing about the delay differed. "
            "If distress were a property of events this could not happen. It happens constantly, "
            "which means something is being added, and the thing being added is yours.",

            "Run a case, because the abstract version is where this stops being useful. Someone "
            "does not reply to your message for two days. The event is: no reply, two days. What "
            "actually reached you was not that. It was 'they are annoyed with me', or 'I said "
            "something wrong', or 'this is how it starts'. Those are not observations. Each one "
            "is a completed story with a cause, a motive and a future in it, assembled from an "
            "absence of data — and every ounce of the distress lives in the story, not in the "
            "silence.",

            "So the practical move is not to think positively, which is just a different story "
            "with the same status. It is to separate the two, on paper if necessary, and see "
            "how little the event actually contains. Event: no reply, two days. Everything else "
            "on the second line. You are not arguing yourself out of anything; you are looking "
            "at where the material actually came from, and the discovery is reliably that the "
            "event is thin and the addition is thick.",

            "The objection is a real one and Stoicism attracts it constantly: this sounds like "
            "telling yourself nothing is wrong when something IS wrong. Some events are "
            "genuinely bad. A diagnosis, a bereavement, a betrayal — is the Stoic claim that "
            "these are neutral and you are choosing to suffer?",

            "No, and the misreading matters because it is what makes people discard the whole "
            "thing. The claim is not that events carry no weight. It is that your suffering has "
            "two components — the event and the appraisal — and only one of them is available "
            "to you. A bereavement is bad and grief is the appropriate response to it. But the "
            "additional layer, 'I should have seen it', 'this ruins everything ahead', 'I "
            "cannot survive this' — that layer is doing an enormous share of the damage and it "
            "is made of sentences. Aurelius was not a man with an easy life telling himself "
            "things were fine. He was running an empire, burying children, and writing these "
            "notes to himself at night because he needed them.",

            "And the edge, which is where people misapply this and then abandon it: separating "
            "event from judgement is a tool for suffering that outruns its cause, not a "
            "universal solvent. If your judgement is that a situation is harmful and should be "
            "changed, the correct response is to change it, not to examine your appraisal until "
            "the urgency dissolves. Used well this frees energy for action. Used badly it "
            "becomes a sophisticated way of tolerating things you should be walking out of.",
        ],
        "sources": [
            src("Aurelius — The Second Book",
                "Go about every action free of vanity, of passion pulling you from reason, of "
                "hypocrisy and self-love, and free of resentment at what has actually happened "
                "to you."),
            src("Aurelius — The Second Book",
                "Only a limited span of time has been given you, and if you do not use it to "
                "calm the disorder of your own mind it will pass, and you with it, and it will "
                "not return."),
        ],
        "quiz": [
            {"q": "Someone doesn't reply for two days and you feel bad. On this account, what is "
                  "actually producing most of the distress?",
             "c": ["the silence itself",
                   "the story assembled around the silence — motive, cause and future added to "
                   "an absence of data",
                   "how long you waited", "the importance of the person"], "a": 1},
            {"q": "What is the evidence that a judgement step exists at all?",
             "c": ["people say so",
                   "the same event produces different distress in different people, and in you "
                   "on different days",
                   "it is an ancient idea", "distress is unpleasant"], "a": 1},
            {"q": "Where does this tool stop being appropriate?",
             "c": ["when the event is small",
                   "when the situation is genuinely harmful and should be changed — then it "
                   "becomes a way of tolerating what you should leave",
                   "when you are tired", "it always applies"], "a": 1},
        ],
        "apply": {"prompt": "Take something bothering you now. Write the bare event on one line "
                            "— only what a camera would have recorded. Put everything else on a "
                            "second line. Then look at how much of the weight was on line two.",
                  "min": 50},
    },
    {
        "id": "p2", "tier": 1, "prereq": ["p1"], "glyph": "\U0001f9ed",
        "title": "Sorting What Is Actually Yours",
        "why": "The first lesson found the step where suffering is added. This is the sort that "
               "tells you which half of any situation you can do anything about.",
        "bridge": [
            "The second move is a sort, and it is cruder than it looks: for anything in front of "
            "you, some of it is up to you and some of it is not. Your own judgements, choices "
            "and actions are yours. Other people's reactions, the outcome, your reputation, the "
            "weather, the past, most of the future — not yours. The instruction is to invest "
            "effort strictly in the first pile and accept the second as given.",

            "Why this works is not resignation, and reading it as resignation is the standard "
            "way to get nothing from it. It is an efficiency argument. Effort spent on the "
            "second pile produces no change in the world and does produce distress — it is pure "
            "cost. Worse, it is usually spent INSTEAD of the first pile, because worrying about "
            "an outcome feels like working on it. The sort is not about lowering your ambitions. "
            "It is about routing all of your available force into the only channel that connects "
            "to anything.",

            "Run a case. You have an exam, or an interview, or a piece of work being judged. Not "
            "yours: whether you are chosen, what the assessor thinks, how the competition "
            "performs, whether the questions suit you. Yours: how many hours you put in, what "
            "you revise, when you sleep, whether you go in having eaten, whether you answer the "
            "question actually asked. Notice that essentially all of the anxiety attaches to "
            "the first list and essentially all of the leverage sits in the second — and that "
            "the hours you spend rehearsing the verdict are hours removed from the preparation "
            "that would have improved it.",

            "There is a sharper version worth carrying, which is Aurelius's own: treat each "
            "action as though it were your last, and do it with full attention and without "
            "resentment at the circumstances you were handed. That is not morbid. It is the "
            "sort applied at the scale of a single task — this piece of work is mine, its "
            "reception is not, so I will do it completely and stop.",

            "The objection: does this not just make you passive? If outcomes are not mine, why "
            "pursue anything? And is 'accept what happens' not an excellent argument for never "
            "changing a situation that ought to be changed?",

            "The reverse, and the confusion comes from what 'not yours' means. It does not mean "
            "you have no influence — it means you do not have CONTROL, which is different. You "
            "influence an outcome entirely through actions, and actions are in the first pile. "
            "So the sort does not reduce what you attempt; it removes the tax on attempting. The "
            "person who has genuinely stopped negotiating with the verdict is the person free to "
            "work hardest at the thing that produces it. Aurelius did not use this to withdraw. "
            "He used it while running an empire he had not asked for.",

            "The edge: the sort is only useful if you do it honestly, and dishonest sorting is "
            "common in both directions. Putting things in the 'not mine' pile that plainly are "
            "yours — the preparation you skipped, the conversation you avoided — is not "
            "acceptance, it is an alibi with a philosophical accent. Putting things in the "
            "'mine' pile that are not, like another person's feelings, produces the specific "
            "misery of trying to control something that was never available and blaming yourself "
            "for failing.",
        ],
        "sources": [
            src("Aurelius — The Second Book",
                "Perform whatever you are about with real seriousness and justice, and let the "
                "rest of your cares go — approach each action as though it were the last, free "
                "of vanity and of resentment at what has befallen you."),
            src("Aurelius — The Second Book",
                "What is needed to live well is not many things; the requirements are few, and "
                "nothing more is asked of anyone who keeps to them."),
        ],
        "quiz": [
            {"q": "Why is worrying about an outcome specifically expensive?",
             "c": ["it is unpleasant",
                   "it produces no change in the world and is usually spent instead of the "
                   "actions that would",
                   "it takes a long time", "it looks bad to others"], "a": 1},
            {"q": "'Not up to you' means:",
             "c": ["you have no influence over it",
                   "you do not have control over it — influence still runs through your actions",
                   "it does not matter", "you should ignore it"], "a": 1},
            {"q": "Which is dishonest sorting?",
             "c": ["putting another person's reaction in the 'not mine' pile",
                   "putting the preparation you skipped in the 'not mine' pile",
                   "putting your own effort in the 'mine' pile",
                   "putting the weather in the 'not mine' pile"], "a": 1},
        ],
        "apply": {"prompt": "Take something you are anxious about. Draw two columns and sort "
                            "every part of it honestly into up-to-me and not-up-to-me. Then pick "
                            "the single item in column one you have been avoiding, and do it.",
                  "min": 50},
    },
    {
        "id": "p3", "tier": 2, "prereq": ["p2"], "glyph": "\U0001f4d3",
        "title": "Why He Had to Keep Writing It Down",
        "why": "The two moves are simple and you already agree with them. This lesson is about "
               "why agreeing has never been enough, which is the actual reason this book exists.",
        "bridge": [
            "Here is the fact about Meditations that changes how you use it, and it is usually "
            "mentioned as trivia rather than treated as the point. It was not written for you. "
            "It was not written for anyone. It is a private notebook, and it was never intended "
            "to be published — which explains the feature everyone notices and nobody explains, "
            "that it repeats itself constantly. The same handful of ideas, restated, year after "
            "year, by a man who plainly understood them perfectly well the first time.",

            "As a book that is a defect. As a record of a practice it is the whole finding. The "
            "most powerful man alive, who had studied this material for decades, needed to write "
            "'do not resent what happens' again this morning — because he had understood it "
            "yesterday and it had not held. Understanding was never the mechanism. Repetition "
            "was. He was not taking notes on a philosophy; he was doing reps.",

            "Why it must work this way follows from the first lesson. The judgement step runs "
            "fast, automatically, and below awareness — it is a trained reflex, and reflexes are "
            "not modified by being informed that they are wrong. You cannot argue a reflex out "
            "of existence. You can only lay down a competing one by running it deliberately, "
            "many times, until it becomes available at the speed the original operates at. That "
            "takes repetition in calm conditions, which is exactly what a morning notebook is.",

            "This is also the answer to the most common failure with Stoicism, which you may "
            "have already had. You read it, you find it true, it changes nothing — and you "
            "conclude it is fine as philosophy but does not survive contact with real life. What "
            "actually happened is that you acquired the idea and never practised it, then tried "
            "to deploy an unpractised reflex in the exact conditions where reflexes matter most. "
            "It failed for the same reason reading about a sport does not make you able to play "
            "it under pressure.",

            "So run it as a drill, small enough to actually survive. Two minutes in the morning: "
            "name the one thing today most likely to disturb you, and rehearse it — this is "
            "likely to happen, it is not up to me, my part is this. Two minutes at night: where "
            "did I add a judgement that was not required, and what was the bare event? That is "
            "the whole practice, and it is precisely what the book you are holding is a record "
            "of somebody doing.",

            "The objection: is this not just journalling with extra steps, and is rehearsing bad "
            "outcomes in the morning not a reliable way to feel worse? Both parts are worth "
            "answering. It differs from journalling because it is rehearsal rather than record — "
            "you are not describing your day, you are running a specific response before you "
            "need it. And it differs from worry in direction: worry loops on the outcome, which "
            "is in the second pile, while this rehearses YOUR RESPONSE, which is in the first. "
            "Same subject matter, opposite pile, completely different result.",

            "The edge, and it is the failure mode this book itself demonstrates: the practice can "
            "become the point. It is possible to keep an excellent notebook, feel philosophical, "
            "and change nothing — Aurelius is repeating himself partly because it kept not "
            "holding, which should be read as honesty rather than as an endorsement. The measure "
            "is never how the notebook reads. It is whether the gap between the event and your "
            "reaction got wider this month than last, in the actual moment, when it counted.",
        ],
        "sources": [
            src("Aurelius — The Second Book",
                "Remember how long you have been putting this off, and how many days set aside "
                "for it you have let pass unused."),
            src("Aurelius — The Second Book",
                "You have only a fixed span of time, and if you do not spend it settling the "
                "disorders of your own mind it will pass away and you with it, and never "
                "return."),
        ],
        "quiz": [
            {"q": "Why does Meditations repeat itself so much?",
             "c": ["it was assembled badly from fragments",
                   "it is a record of a repeated practice — he understood it and it still did "
                   "not hold, so he ran it again",
                   "the translation is poor", "he was forgetful"], "a": 1},
            {"q": "Why can't you fix the judgement step just by understanding it?",
             "c": ["the ideas are too difficult",
                   "it is a fast automatic reflex, and reflexes are not modified by being told "
                   "they are wrong — only by running a competing one repeatedly",
                   "you need a teacher", "it requires belief"], "a": 1},
            {"q": "What separates the morning rehearsal from ordinary worry?",
             "c": ["it is written down", "it is shorter",
                   "worry loops on the outcome; this rehearses your own response — the other "
                   "pile entirely",
                   "it happens in the morning"], "a": 2},
        ],
        "apply": {"prompt": "Tonight, spend two minutes on one question: where today did you add "
                            "a judgement that was not required, and what was the bare event? "
                            "Then tomorrow morning, name the one thing most likely to disturb "
                            "you and rehearse your part in it before it happens.", "min": 50},
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
