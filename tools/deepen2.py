# -*- coding: utf-8 -*-
"""#174 — deepen the rest of track O to the standard set by o1 (see tools/deepen.py).

Same rule: ONE idea per lesson, carried to the length that idea actually needs. Not padded to a
budget, not two ideas welded together. Each lesson below does the four things a 380-word summary
had no room for — the mechanism down to why it must be so, one case run to the end, the obvious
objection answered, and the edge where the idea stops holding.

    python tools/deepen2.py --dry
    python tools/deepen2.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")

O2 = [
    "Almost everyone says 'fight or flight'. Navarro's objection is that the phrase is "
    "two-thirds right and has the order backwards, and the order is not a pedantic detail — it "
    "determines which response you will see most of, and therefore what you should actually be "
    "watching for. The real sequence is FREEZE, then FLIGHT, then FIGHT.",

    "The order follows from cost, and once you see that you will not need to memorise it. "
    "Freezing is nearly free: it costs no energy, it commits you to nothing, and it can be "
    "undone instantly if the threat turns out to be nothing. Fleeing costs energy and abandons "
    "whatever you were doing. Fighting risks injury or death. A survival system that reached for "
    "the expensive option first would have been selected out. So the machinery tries the cheap "
    "move first and escalates only when the cheap move fails.",

    "FREEZE exists because movement is what predators detect. Most carnivores are tuned to "
    "motion — the chase-trip-bite sequence needs something moving to start. Holding still is the "
    "oldest defence there is, and some animals take it to its conclusion and play dead. You "
    "still have it, unmodified, and it fires in rooms containing nothing more dangerous than a "
    "manager.",

    "What it looks like is the part worth learning, because it does not look like fear. It looks "
    "like composure. Hands that were gesturing stop and stay stopped. Feet that were shifting "
    "settle and lock. Breathing goes shallow and high in the chest. A person who had been moving "
    "in their chair becomes strangely, smoothly still. If you are not looking for it you will "
    "read it as 'they took that well', and it is very often the exact opposite. Navarro's "
    "example is a child who has run to hug his uncle every year for eight years and this year "
    "stands rigid in the line. Nothing was said. Everything was said.",

    "FLIGHT comes next, and in a meeting room you cannot actually run from, it degrades into "
    "distancing — the same intention expressed in the space available. Feet rotate toward the "
    "door. The torso angles away by degrees while the face stays politely pointed at you. "
    "Someone leans back. An object migrates into the space between you: a laptop turned "
    "slightly, a bag moved onto the chair, a coffee cup relocated to the midpoint. Blocking "
    "belongs here too — eyes that close a fraction too long, a hand that arrives over the mouth. "
    "Nobody is leaving. The body is doing leaving in miniature because leaving is what it wants.",

    "FIGHT is last, and in modern settings it almost never arrives as violence. It arrives as "
    "aggression that has been laundered into something socially permissible: the argument that "
    "sharpens, the territorial spread of arms and papers across a table, a chest and chin coming "
    "forward, sustained unblinking eye contact, a voice that drops and hardens. It is still the "
    "same system, now committed.",

    "Here is the whole practical payoff, and it is one sentence: if you are seeing fight, you "
    "already missed a freeze and a flight. These are not three separate moods someone might be "
    "in. They are three stages of one escalating response, and the escalation is sequential. By "
    "the time a conversation is visibly going badly, the body announced it twice already — once "
    "as stillness, once as distance — while it was still cheap to fix. A question asked at the "
    "freeze costs nothing. The same question asked at the fight is a concession.",

    "Run a case. You are twenty minutes into explaining a plan. At some point your colleague "
    "goes quiet and still — you register it, if at all, as 'they're thinking'. Five minutes "
    "later they have leaned back and their notebook is now between you. Ten minutes after that "
    "they are arguing about a detail that does not matter, with more heat than the detail "
    "deserves. What you experience is someone becoming unreasonable near the end. What actually "
    "happened is that something in the first part lost them, and you had two clear signals "
    "before the argument started. The fight is not where the problem is. It is where the problem "
    "surfaced.",

    "The objection: is this not just describing an ordinary conversation and calling it "
    "survival machinery? People go quiet because they are thinking. People lean back because "
    "they are comfortable. This is fair, and it is why one signal is worth nothing on its own. "
    "The thing that makes it a freeze rather than thinking is that it is a CHANGE — this person "
    "was moving a minute ago and now is not — and that it began at an identifiable moment. "
    "Someone thinking hard usually shows it: eyes move, they look away and back, a hand comes "
    "up. A freeze is stillness that arrived all at once and stayed.",

    "And the edge, which matters more here than anywhere else in the track: the sequence tells "
    "you the SIZE of a reaction, not its cause. A freeze says something registered as a threat "
    "by a very old system with crude categories. It does not say the threat was you, or your "
    "plan, or that anything is wrong with either. It could be the deadline you mentioned in "
    "passing. It could be that your plan requires them to talk to someone they are avoiding. The "
    "signal is a timestamp and an intensity. What it is about is a question you still have to "
    "ask.",
]

O3 = [
    "This is the highest-value thing in the book and it is almost never taught, so it is worth "
    "being precise about the mechanism rather than treating it as a list of gestures. After a "
    "limbic response, the brain sends the body to comfort itself. Navarro calls these pacifying "
    "behaviours; the research literature calls them adapters. Something unpleasant registers — a "
    "question, a number, a name, someone walking in — and a moment later the hand goes to the "
    "neck, rubs the leg, touches the face; fingers find something to fiddle with; air goes out "
    "through pursed lips; a collar that did not need adjusting gets adjusted.",

    "The reason these exist is physiological rather than psychological. A stress response leaves "
    "the body in a state it is built to come out of — the limbic system's whole purpose, "
    "Navarro's 'prime directive', is to return you to safety and comfort. Touching, stroking and "
    "rubbing produce real calming: they stimulate nerve endings, and the neck in particular is "
    "dense with them and sits over the vagus nerve. The body is not signalling to you. It is "
    "medicating itself, and you happen to be able to see it.",

    "That detail is what makes pacifiers more useful than the stress responses in the previous "
    "lesson, and the argument is worth following because it is not obvious. A freeze is fast, "
    "small and easy to miss — especially since you were probably talking when it happened. The "
    "pacifier arrives AFTER it, is physically larger, and often continues for several seconds. "
    "So you get a second chance at a moment you already missed.",

    "Better than that, it points backwards. A pacifier is a response to something, which means "
    "the thing that caused it happened just BEFORE the hand moved. You do not have to be "
    "watching continuously and you do not have to catch the instant. You catch the soothing, you "
    "rewind two seconds, and you have located what landed badly. That is a genuinely different "
    "skill from staring at someone hoping to detect a flicker.",

    "The neck is where to start. It is vulnerable, richly innervated, and people go there "
    "constantly under stress with no idea they are doing it — covering the hollow at the throat, "
    "stroking down one side, men often adjusting a tie or collar, women often touching or "
    "playing with a necklace at the suprasternal notch. Hands and face come next: the cheek rub, "
    "the forehead wipe, a hand that arrives over the mouth. Legs are the least noticed of all — "
    "under a table, palms sliding down the tops of the thighs, which almost nobody knows they do.",

    "Run a case. You are negotiating and you say a number. Their face does not change; people "
    "practise faces for exactly this situation. Two seconds later their hand comes up and rubs "
    "the back of their neck while they say 'that could work'. What you have learned is not that "
    "they are lying, and not that the number is impossible. You have learned that the number "
    "created enough discomfort to require soothing — which tells you it is near a limit that "
    "matters to them, and that 'that could work' is doing more labour than it appears to be. "
    "That is worth a great deal, and it is available without any confrontation at all.",

    "The objection: people touch themselves constantly. Faces get scratched, necks get rubbed, "
    "hair gets pushed back. If you go looking for pacifiers you will find them in every "
    "conversation you ever have, and the ones you notice will be the ones that suit your theory. "
    "That is a real risk and it is why the discipline in the next lesson is not an appendix.",

    "The answer is that a pacifier is only information when it is TIED to a moment. Not 'they "
    "touched their neck during the meeting' — that is meaningless. 'Their hand went to their "
    "neck immediately after I mentioned the deadline, and it did not do that at any other point "
    "in forty minutes.' The timestamp is the whole content. A pacifier with no identifiable "
    "trigger is somebody with an itch, and you should discard it rather than build on it.",

    "The edge, and it is the same discipline as the rest of the track: this locates a subject, "
    "not a verdict. Discomfort is not guilt and it is not deception. Someone can be entirely "
    "honest and still be uncomfortable — because the topic is embarrassing, because they do not "
    "know the answer, because it touches something unrelated to you. The correct use of a "
    "pacifier is to note the subject and ask about it more carefully. The incorrect use — the "
    "one that has ruined interrogations and marriages — is to treat the neck touch as proof and "
    "then interpret everything afterwards in the light of a conclusion you reached from a "
    "gesture.",
]

O4 = [
    "Everything in the three previous lessons becomes nonsense the moment you read a single "
    "signal on its own, and the failure has a recognisable shape. You learn that crossed arms "
    "mean defensiveness. You see crossed arms. You now believe something about a person that you "
    "invented, and it does not feel invented — it feels like perception. This is confirmation "
    "bias wearing a lab coat, and it is the reason body language has a reputation as pop "
    "psychology despite the underlying mechanism being real.",

    "Navarro spends his opening chapter on the discipline that prevents it, and it is three "
    "requirements that must ALL be satisfied. None of them is optional and each fails "
    "differently.",

    "BASELINE first. You cannot read a deviation without knowing what this person is like when "
    "nothing is happening. Some people fidget constantly. Some are naturally still. Some touch "
    "their face all day. The signal is never the behaviour itself — it is the CHANGE from that "
    "individual's own normal. This is why the uncle example works: the boy's freeze means "
    "something only because eight previous years established that he always ran in for a hug. "
    "Without those eight years there is no signal, just a child standing still. With a stranger "
    "you have no baseline at all, so the first minutes of any conversation are for building one, "
    "not for drawing conclusions.",

    "CLUSTER second. One behaviour is noise. People cross their arms because the room is cold, "
    "touch their neck because a label is scratching, lean back because the chair is bad. You "
    "want three or four things pointing the same direction at the same time — the feet turn "
    "toward the door AND the torso angles away AND an object moves into the gap AND the hand "
    "goes to the neck. A cluster is evidence. A single tell is a coincidence you have decided is "
    "meaningful, and you will always be able to find one.",

    "CONTEXT third, and it is the one people skip because it is the least fun. The same "
    "behaviour means different things in different situations. Someone stiff, still and "
    "self-soothing throughout a job interview is a person in a job interview — that is what the "
    "situation does to almost everybody, and it tells you close to nothing about their character "
    "or their honesty. The identical cluster appearing when you mention one specific project, in "
    "an otherwise relaxed conversation, is worth everything. Same signals. The context supplied "
    "all of the meaning.",

    "There is a hard number behind this, and it is worth carrying because it is more sobering "
    "than any argument. Across 206 studies and 24,483 observers, people reading a single "
    "encounter identify truth and lies at 54% accuracy — and on actual lies specifically, 47%, "
    "which is worse than guessing. Reading one conversation is a coin toss. That finding is not "
    "an argument against the method; it is an argument that the unit of observation was never "
    "one encounter, which is exactly what baseline and cluster fix.",

    "Put together, the three requirements turn this from mind-reading into something far more "
    "modest and considerably more useful. You are noticing that THIS person, compared to how "
    "they were ten minutes ago, changed in several ways at once, at a moment you can point to. "
    "That is the entire claim. It happens to be enough, because it tells you where to ask the "
    "next question, and the next question is the only thing you needed.",

    "The objection: this makes the skill so hedged as to be useless. If you need a baseline and "
    "a cluster and the right context before you can conclude anything, what use is it in a "
    "single meeting with someone you have never met? The answer is that you get less from a "
    "stranger, and you should. But you spend most of your life around people you see repeatedly "
    "— colleagues, family, friends — and for them you have years of baseline already, "
    "unrecorded but real. You have always known when someone close to you is 'off' without being "
    "able to say why. That intuition IS a baseline comparison running unconsciously. This "
    "lesson does not replace it; it tells you what it was measuring, so you can point it "
    "deliberately.",

    "And the edge, which is the last thing to carry out of this track: none of this reveals WHY. "
    "You can establish, carefully and correctly, that a specific subject produced discomfort in "
    "a specific person at a specific moment. You cannot establish the reason, and the reason is "
    "usually the thing you actually want. Discomfort is a pointer to a subject, never a verdict "
    "on a person. Every serious failure in this field — the wrongful interrogation, the "
    "destroyed relationship, the confident hiring mistake — has the same structure: someone "
    "treated a pointer as a verdict, and then defended it harder because it had come with a "
    "scientific vocabulary attached.",
]

PATCH = {"o2": O2, "o3": O3, "o4": O4}


def main():
    dry = "--dry" in sys.argv
    graph = json.load(open(GRAPH, encoding="utf-8"))
    books = json.load(open(BOOKS, encoding="utf-8"))
    rows = []
    for nid, bridge in PATCH.items():
        node = next((n for n in graph["nodes"] if n["id"] == nid), None)
        if not node:
            print(f"FAIL: node {nid} not found")
            return 1
        before = sum(len(p.split()) for p in node["bridge"])
        # a figure's `place` indexes into bridge — keep it valid after the rewrite
        for f in node.get("fig", []) or []:
            if f.get("place") is not None and f["place"] >= len(bridge):
                f["place"] = max(0, len(bridge) // 2)
        node["bridge"] = bridge
        rows.append((nid, node["title"], before, sum(len(p.split()) for p in bridge)))

    sys.path.insert(0, HERE)
    import build
    try:
        build.validate(books, graph)
    except SystemExit:
        print("FAIL: validate() rejected the graph")
        return 1

    for nid, title, b, a in rows:
        print(f"  {nid}  {b:>4} -> {a:>5} words ({a/200:.0f}-{a/150:.0f} min)  {title}")
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
