# -*- coding: utf-8 -*-
"""#180 — deepen track Q (Carnegie) toward the standard set by tools/deepen.py.

APPENDS to each lesson rather than rewriting it. What was there already does the four things;
what it had no room for is the part that turns a mechanism you agree with into one you can run:
a SECOND case that goes wrong, the failure mode you will actually produce, and the tell that you
are doing it badly. Agreeing with Carnegie is easy and nearly useless — everyone agrees with
Carnegie. Executing him is where it falls apart, and that is what these additions cover.

One idea per lesson still. Nothing here introduces a new mechanism; it works the existing one
further down.

    python tools/deepen3.py --dry
    python tools/deepen3.py
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
"q1": [
    "Now the failure you will actually produce, because it is not flattery — you already know to "
    "avoid flattery. It is APPRECIATION THAT COSTS YOU NOTHING TO GIVE. 'Thanks, great work' at "
    "the end of a meeting is free: it required no attention, it names nothing, and everyone in "
    "the room can tell. It does not fail because it is dishonest. It fails because it carries no "
    "evidence that anything was noticed, and evidence of attention was the entire product.",

    "The tell that you are doing it right is that it took effort to say. If you had to recall "
    "something specific, or you noticed you were slightly unsure whether to mention it, you are "
    "supplying the scarce thing. If it came out automatically, you supplied noise. That is a "
    "usable test in the moment and it does not require you to interrogate your own sincerity, "
    "which is unreliable anyway.",

    "There is a second-order effect worth knowing, because it changes how you spend the effort. "
    "Attention paid in private is worth more per unit than attention paid in public. Public "
    "praise is partly performance — for the room, for your own standing as a generous person — "
    "and everyone present can read that ambiguity into it. A specific observation given to "
    "someone one-to-one, where you gain nothing socially, has no such reading available. It is "
    "also the version people remember years later, which is not sentimentality; it is because "
    "the unambiguous version is the one that actually proved attention.",

    "And a case where this mechanism should NOT be your first move. Someone who is genuinely "
    "struggling and knows it does not need to be told what they did well — that reads as either "
    "not-seeing or as softening a blow that has not landed yet. What they need is the thing "
    "that is true and useful, which may be help, or the removal of a task. The mechanism is "
    "about a shortage of noticing, and if the person is already being watched closely there is "
    "no shortage to supply.",
],
"q2": [
    "Now the way you will get this wrong, and it is not being too harsh. It is the SANDWICH — "
    "praise, criticism, praise — which is what most people produce when they try to apply this, "
    "and which is worse than either component alone. Everyone has learned to recognise it, so "
    "the opening praise is heard as a warning that something is coming, which means you have "
    "poisoned your own appreciation for future use AND announced the attack in advance. Carnegie "
    "does not describe a sandwich. He describes lowering the status cost of the correction, "
    "which is a different operation.",

    "The tell is the word 'but'. 'You did a great job on this, BUT the figures are wrong' — "
    "everything before 'but' has been deleted by everything after it, and both of you know it. "
    "If you find yourself building that sentence, the fix is not better wording; it is that you "
    "are trying to do two jobs in one breath. Say the correction cleanly, and pay the "
    "appreciation on a different day when it is not doing work for you.",

    "A harder case, because the easy cases make this look simpler than it is. Someone is "
    "defending a position you know to be wrong, in front of other people, and their standing is "
    "now attached to it. Every additional piece of evidence you produce makes it more expensive "
    "for them to move, because the retreat gets larger the longer they hold. The mechanism says "
    "the winning move is to stop supplying evidence and start supplying an exit — a route by "
    "which the position can change without a visible defeat. 'That's a fair point, and it might "
    "be different now the numbers came in' hands them a reason that is not their own error.",

    "And notice what this costs, because it is not free and pretending it is makes it easy to "
    "abandon. You do not get the moment of being seen to be right. That moment is the thing "
    "you are trading away, and it is worth more to most people than they admit. If you want "
    "both the correction and the credit, you can usually have one.",
],
"q3": [
    "The failure mode here is specific and almost everyone produces it: you find their interest "
    "and then LEAD WITH YOURS ANYWAY, because yours is what is urgent to you. You genuinely did "
    "the work — you know they want visibility with that team — and then you open with 'I'm "
    "completely swamped'. The preparation was real and it never reached the conversation, "
    "because under any pressure you revert to the reasons that are live in your own head.",

    "The fix is mechanical rather than motivational: decide the first sentence in advance and do "
    "not improvise it. Your opening line is the whole of what this mechanism controls. After the "
    "first sentence the conversation is shared and your reasons can come in as context, where "
    "they belong. But the opening establishes whose problem is being discussed, and it is very "
    "hard to move that afterwards.",

    "A harder case: what do you do when their real interest is one you cannot say out loud? "
    "Somebody wants the work because it makes them look good relative to a colleague. That is "
    "genuinely their eager want, and naming it would be insulting. Carnegie's 'appeal to the "
    "nobler motives' is usually read as a euphemism for flattery, and it is not — it is the "
    "observation that people have several real motives at once, and that you get to choose "
    "which true one you address. Speaking to the version of the motive they would be willing to "
    "own is not a lie, provided it is actually one of the reasons.",

    "The edge on that is sharp and worth stating: it works because the motive is real, so this "
    "collapses the moment you name a motive they do not have. 'I know you care deeply about "
    "the team' to someone who plainly does not is heard as a demand that they perform caring, "
    "and it produces resentment rather than compliance. Pick a true motive that they are "
    "comfortable being seen to hold. If none exists, you are back to asking plainly.",
],
"q4": [
    "The failure here has a name you will recognise the moment you read it: the FAKE QUESTION. "
    "'What do you think we should do?' asked by someone who has already decided. It is worse "
    "than an instruction on two counts — it wastes the other person's thinking, and when the "
    "predetermined answer arrives anyway, it teaches them that their input is decorative. You "
    "have spent a real resource, which is their willingness to think in front of you, and you "
    "spent it to buy nothing.",

    "The tell, and it is uncomfortable to run honestly: before asking, name a specific answer "
    "they could give that you would actually adopt. Not 'I'm open to ideas' — an actual "
    "alternative outcome you would accept and could live with. If you cannot produce one, you "
    "are not consulting, and the honest move is to say what has been decided and use the "
    "previous mechanism to explain it in terms that connect to them.",

    "There is a version of this that scales past single conversations, and it is the most "
    "valuable thing in the mechanism. 'Give them a fine reputation to live up to' works because "
    "a stated identity becomes something people defend on their own time, without you present. "
    "Told once, sincerely, that they are the person who catches things others miss, someone "
    "starts catching things — not to please you, but because the description has become part of "
    "how they see themselves, and self-image maintains itself. That is why it outlasts "
    "supervision when instructions do not.",

    "Which is also the reason it is dangerous, and Carnegie does not say this part. The same "
    "mechanism runs on descriptions that are careless or unkind. Tell someone repeatedly that "
    "they are disorganised and you have handed them an identity to be consistent with, and it "
    "will be maintained with exactly the same machinery. You are not choosing whether to assign "
    "people identities — that happens whether you attend to it or not. You are only choosing "
    "whether you noticed you were doing it.",
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
        rows.append((nid, n["title"], before, sum(len(p.split()) for p in n["bridge"])))

    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
    except SystemExit:
        print("FAIL: validate() rejected the graph")
        return 1
    for nid, t, b, a in rows:
        print(f"  {nid}  {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {t}")
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
