# -*- coding: utf-8 -*-
"""#178 JOB 5 — track R: The Body Keeps the Score. THE LAST UNCOVERED BOOK.

Grounded in the book's own text (episodes 14, 19, 21, 26 of `bodyscore`).

BUILT AS ONE CAUSAL CHAIN, not a survey. 172,208 words, but the argument is a single line of
reasoning and it should be walked in order: the alarm does not reset -> the experience was never
assembled into a story, only fragments -> the speech centre is measurably offline, which is why
talking about it does not reach it -> and events you could not escape train immobility, which is
why "just do something" misses the mechanism.

EVERY LESSON CARRIES THE CLINICAL EDGE, not just the last one. This is a book about a clinical
subject. These lessons explain mechanisms; they are not diagnosis, not treatment, and not a
substitute for a professional. That line is repeated deliberately in each lesson rather than
stated once and assumed, because a reader arriving mid-track would otherwise never see it.

    python tools/path_bodyscore.py --dry
    python tools/path_bodyscore.py
"""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
BOOK = "The Body Keeps the Score"
TID = "R"

TRACK = {"id": TID, "name": "The Body Keeps the Score", "glyph": "\U0001fac0", "accent": "#b0413e",
         "blurb": "Van der Kolk on why trauma is stored as a physical state rather than a memory "
                  "— and why that means talking about it often does not reach it. Explanatory, "
                  "not clinical advice."}


def src(ref, *q):
    return {"book": BOOK, "ref": ref, "quote": list(q)}


NODES = [
    {
        "id": "r1", "tier": 0, "prereq": [], "glyph": "\U0001f6a8",
        "title": "The Alarm That Doesn't Reset",
        "bridge": [
            "Start with what is measurably different, because the whole book follows from it and "
            "it is not a metaphor. Under ordinary conditions a threat raises your stress "
            "hormones, you deal with the threat, and the hormones dissipate — the system returns "
            "to baseline. That return is the normal part, and it is the part that stops working.",

            "In van der Kolk's scanner studies, people with trauma histories showed stress "
            "hormones that took far longer to come back down, and that spiked quickly and "
            "disproportionately to things that were only mildly stressful. So the difference is "
            "not that something bad happened once. It is that the response system's reset has "
            "been altered, and it now treats small things the way it should treat large ones.",

            "One of his patients, Marsha, was scanned thirteen years after losing her daughter. "
            "Playing back the sounds and images of the accident produced a heart rate and blood "
            "pressure reading of a person in immediate danger. Thirteen years were, as he puts "
            "it, erased. Not remembered vividly — erased. The body was not recalling an old "
            "emergency; it was having one.",

            "This is what the book's title actually means, and it is worth being precise "
            "because the phrase gets used loosely. The score is not kept as a sad memory. It is "
            "kept as a physiological setting: a resting state that is closer to alarm, a "
            "threshold that trips earlier, a recovery that takes longer. That is why the "
            "experience is not reachable by deciding it is over. A decision does not reach a "
            "threshold.",

            "It also explains something that looks irrational from outside and is not. When "
            "someone reacts enormously to something small, the size of the reaction is not a "
            "measure of the trigger — it is a measure of how low the threshold now sits and how "
            "little of the previous alarm has cleared. The reaction is proportionate to a state, "
            "not to the event that happened to tip it.",

            "The obvious objection is that this makes everyone with a bad past permanently "
            "broken. It does not, and van der Kolk's own work is the evidence — the whole "
            "reason he pursued the biology was to find things that shift it. A setting is a "
            "setting. The point of establishing that it is physiological is not that it is "
            "fixed; it is that it will not be moved by the things that move opinions.",

            "**The edge, and it holds for every lesson in this track: this is an explanation of "
            "a mechanism, not a diagnosis and not treatment.** Recognising a pattern in yourself "
            "here is a reason to speak to a professional, never a substitute for it, and "
            "recognising one in someone else is not a licence to tell them what is wrong with "
            "them.",
        ],
        "sources": [
            src("van der Kolk — Stuck in Fight or Flight",
                "Normally stress hormones rise to meet a threat and dissipate once it passes. In "
                "traumatised people they take much longer to return to baseline and spike "
                "quickly and disproportionately to mild stressors."),
            src("van der Kolk — Stuck in Fight or Flight",
                "Thirteen years after the event, activating the stored sounds and images set off "
                "her alarm system as though she were back in that hospital room; the passage of "
                "those years was erased."),
        ],
        "quiz": [
            {"q": "What is physiologically different, on van der Kolk's account?",
             "c": ["the memory is more vivid",
                   "the stress response does not reset — it spikes disproportionately and takes "
                   "far longer to come down",
                   "the person is more emotional", "the event was worse"], "a": 1},
            {"q": "Someone reacts enormously to something small. The size of the reaction "
                  "measures:",
             "c": ["how bad the trigger was",
                   "how low the threshold sits and how little previous alarm has cleared",
                   "how much they care", "how well they remember"], "a": 1},
            {"q": "Why can't this be resolved by deciding the danger is over?",
             "c": ["people are stubborn",
                   "it is a physiological setting, and a decision does not reach a threshold",
                   "the memory is too strong", "it takes more time"], "a": 1},
        ],
        "apply": {"prompt": "Think of a reaction — yours or someone else's — that looked out of "
                            "proportion to what caused it. Write it again treating the size as "
                            "information about a state rather than about the trigger. Note what "
                            "changes about how it reads.", "min": 50},
    },
    {
        "id": "r2", "tier": 1, "prereq": ["r1"], "glyph": "\U0001f9e9",
        "title": "Fragments, Not a Story",
        "why": "The alarm stays on. This is why it cannot be argued with — what got stored was "
               "never a story in the first place.",
        "bridge": [
            "Normal experience gets assembled before you receive it. Sight, sound, smell and "
            "touch arrive separately and converge in the thalamus, which van der Kolk calls the "
            "cook: it stirs the inputs into one blended, coherent thing — *this is what is "
            "happening to me*. That assembly is so reliable you have never once noticed it "
            "occurring.",

            "From there the information goes two ways. Down to the amygdala by what LeDoux named "
            "the low road, which is extremely fast and unconscious. Up to the frontal lobes by "
            "the high road, which reaches awareness several milliseconds later. Under ordinary "
            "conditions those milliseconds do not matter. In an overwhelming event they matter "
            "enormously, because the fast road has already fired the alarm before the slow road "
            "has finished working out what it is looking at.",

            "And under sufficient overwhelm the cook stops cooking. The integration breaks down, "
            "and sights, sounds, smells and sensations are encoded as isolated fragments rather "
            "than as one event. Normal memory processing disintegrates. What is stored is not a "
            "compressed account of what happened — it is unassembled pieces, each of which can "
            "be triggered on its own.",

            "That single fact explains the symptoms that otherwise look bizarre. A smell "
            "producing full-scale panic with no accompanying memory makes no sense if what is "
            "stored is a story; it makes complete sense if a fragment was stored and the "
            "fragment is all that fires. It explains why the trigger is often trivial and "
            "unrelated to meaning — a fragment has no meaning, it is a sensory match. And it "
            "explains why the person frequently cannot say what set it off: the piece that fired "
            "never had a label attached to it.",

            "It also explains the failure of the most natural response available. Telling "
            "someone the danger has passed addresses a story, and there is no story there to "
            "correct. You are supplying a conclusion to a system that never contained premises "
            "— which is not a communication failure, it is an address error.",

            "The objection: is this not just saying memory is unreliable, which is true of all "
            "memory? No, and the distinction matters. Ordinary memory is assembled and then "
            "distorted over time. This is material that was never assembled — the difference is "
            "not degree of accuracy but whether integration happened at all. Ordinary memory can "
            "be corrected because it is a narrative. Fragments cannot be corrected, because "
            "there is nothing there that is making a claim.",

            "**The edge, again and deliberately: this is a mechanism, not a diagnosis.** Plenty "
            "of ordinary experiences are patchily remembered without any of this applying, and "
            "recognising the pattern described here in yourself is a reason to talk to someone "
            "qualified rather than a conclusion you have now reached about yourself.",
        ],
        "sources": [
            src("van der Kolk — Identifying Danger: The Cook and the Smoke Detector",
                "The thalamus acts as the cook, stirring all incoming perception into a single "
                "blended autobiographical experience of 'this is what is happening to me'."),
            src("van der Kolk — Identifying Danger: The Cook and the Smoke Detector",
                "When thalamic processing breaks down, sights, sounds, smells and touch are "
                "encoded as isolated, dissociated fragments and normal memory processing "
                "disintegrates."),
        ],
        "quiz": [
            {"q": "What does the thalamus normally do that fails here?",
             "c": ["stores the memory",
                   "assembles separate senses into one coherent 'this is happening to me'",
                   "controls fear", "produces adrenaline"], "a": 1},
            {"q": "Why can a smell trigger panic with no memory attached to it?",
             "c": ["the memory is repressed",
                   "a fragment was stored rather than an assembled event, and the fragment fires "
                   "on a sensory match",
                   "smell is the strongest sense", "the person is avoiding it"], "a": 1},
            {"q": "Why does 'you're safe now, that was years ago' so often fail?",
             "c": ["it is said unconvincingly",
                   "it corrects a story, and no story was stored — it is addressed to the wrong "
                   "thing",
                   "the person will not listen", "it needs repeating"], "a": 1},
        ],
        "apply": {"prompt": "Write down what you would normally say to reassure someone who is "
                            "distressed about something long past. Then write what that sentence "
                            "assumes is stored in them — and whether it would reach fragments.",
                  "min": 50},
    },
    {
        "id": "r3", "tier": 2, "prereq": ["r2"], "glyph": "\U0001f507",
        "title": "Why Talking About It Doesn't Reach It",
        "why": "The load-bearing lesson. There is a measured, physical reason the obvious "
               "treatment often fails.",
        "bridge": [
            "This is the finding that reorganised the field, and it arrived as a white spot on a "
            "scan. Van der Kolk's team was imaging people while triggering flashbacks, and what "
            "they found was a significant decrease in activity in Broca's area — one of the "
            "brain's speech centres, and the region often knocked out in stroke patients when "
            "its blood supply is cut.",

            "Broca's area is what turns inner experience into words. Without it functioning you "
            "cannot put thoughts and feelings into language. And their scans showed it going "
            "offline whenever a flashback was triggered. His own conclusion is deliberately "
            "stark: the effects of trauma are not necessarily different from the effects of a "
            "physical lesion like a stroke. All trauma is preverbal.",

            "Sit with what that means practically, because it is the reason this track exists. "
            "The standard, obvious, humane response to distress is to get the person to talk "
            "about it. That response requires the speech centre to be online. At the exact "
            "moment the material becomes accessible — when it is activated — the equipment for "
            "describing it is measurably reduced. The method and the moment are incompatible, "
            "and not because anyone is doing it wrong.",

            "This is also why the observed behaviour is what it is, and why it is so easily "
            "misread. People in emergency rooms sit mute and frozen. Someone in a flashback may "
            "scream, or call for their mother, or shut down entirely. That looks like refusal, "
            "or resistance, or being difficult. It is a speech centre that is not currently "
            "available, and treating it as unwillingness is a category error with real "
            "consequences for how the person is then handled.",

            "And it is why van der Kolk's work turned toward approaches that do not depend on "
            "narration — rhythm, movement, breath, bodywork, things that reach a state directly "
            "rather than through a description of it. Not because talking is useless in general, "
            "but because a route that requires a function which is offline is a route that "
            "cannot carry the traffic. The logic is plumbing, not philosophy.",

            "The objection: does this mean talking therapy is worthless? No, and he does not say "
            "so. It means talking cannot be the ONLY route, and that its timing matters — words "
            "work on material that has been assembled and is not currently firing. What the "
            "finding rules out is the assumption that describing something is always the way in. "
            "Sometimes the describing apparatus is precisely the thing that is down.",

            "**The edge, once more and for the same reason: this explains why certain approaches "
            "reach things others do not. It is not a recommendation of a treatment, and nothing "
            "here should be used to talk anyone out of care they are receiving.** If this "
            "describes you, it is information to take to a professional, not instead of one.",
        ],
        "sources": [
            src("van der Kolk — Speechless Horror",
                "Scans showed a marked decrease in Broca's area — a speech centre, the same "
                "region affected in stroke — whenever a flashback was triggered. Without a "
                "functioning Broca's area you cannot put thoughts and feelings into words."),
            src("van der Kolk — Speechless Horror",
                "The effects of trauma are not necessarily different from the effects of a "
                "physical lesion such as a stroke. All trauma is preverbal."),
        ],
        "quiz": [
            {"q": "What did the scans show during a triggered flashback?",
             "c": ["increased activity everywhere",
                   "a marked decrease in Broca's area — a speech centre — comparable to a stroke "
                   "lesion",
                   "no measurable change", "activity only in the amygdala"], "a": 1},
            {"q": "Why is 'tell me what happened' structurally difficult at the moment the "
                  "material is active?",
             "c": ["the person does not want to",
                   "the equipment for putting experience into words is measurably reduced "
                   "precisely then",
                   "the memory is gone", "it takes too long"], "a": 1},
            {"q": "Someone in a flashback goes mute. The correct reading is:",
             "c": ["they are refusing to engage",
                   "the speech centre is not currently available — reading it as unwillingness "
                   "is a category error",
                   "they have forgotten", "they need a direct question"], "a": 1},
        ],
        "apply": {"prompt": "Think of a time you tried to help someone by getting them to talk "
                            "and it went nowhere. Write what you were assuming was available to "
                            "them at that moment, and what might have reached them instead.",
                  "min": 50},
    },
    {
        "id": "r4", "tier": 3, "prereq": ["r3"], "glyph": "\U0001f512",
        "title": "Inescapable Shock — Why 'Just Do Something' Misses",
        "why": "The last piece: why the immobility persists after the situation has changed, and "
               "why urging action does not shift it.",
        "bridge": [
            "The experiment van der Kolk credits with reorganising his thinking is unpleasant "
            "and worth knowing precisely. Maier and Seligman shocked dogs that were locked in "
            "cages and could not get away — a condition they named inescapable shock. Afterwards "
            "they opened the cage doors and shocked them again.",

            "The control dogs, which had never been shocked before, immediately ran. The dogs "
            "that had been through inescapable shock did not. The door was open. The escape was "
            "available and obvious. They stayed and took it.",

            "What that isolates is the specific ingredient, and it is not pain — the control "
            "dogs experienced the same shock and left. It is inescapability. A system that "
            "learns its actions do not affect outcomes stops producing actions, and it goes on "
            "not producing them after the situation has changed. The immobility is not a "
            "conclusion the animal is drawing about the present. It is a setting laid down by "
            "the past that the present is not being consulted about.",

            "This is the piece that makes sense of the question everyone asks from outside — why "
            "don't they just leave, just say something, just do the obvious available thing. The "
            "question assumes the person is assessing the current situation and choosing wrongly. "
            "What the experiment shows is a system that has stopped generating the attempt at "
            "all, which is a different failure and is not reachable by pointing at the open door.",

            "It also explains why encouragement so often makes things worse rather than "
            "neutral. Telling someone the door is open, when the mechanism is that action "
            "generation has been suppressed, adds the information that they are failing at "
            "something obvious. You have not restored agency; you have supplied evidence for "
            "the belief that their actions do not work — which is the very thing that produced "
            "the state.",

            "The objection: is this not just an excuse for passivity, and does it not remove "
            "responsibility entirely? It removes the assumption of a free choice being made "
            "badly, which is different. And it points somewhere more useful than exhortation: "
            "what shifted the animals was not persuasion but being physically moved through the "
            "escape repeatedly until the body relearned that movement produced an outcome. That "
            "is why van der Kolk's interest turned toward action, rhythm and movement — "
            "restoring the sense of effective agency at a level below argument.",

            "**The edge, stated one last time: this is an explanation, not a diagnosis and not "
            "treatment.** Learned helplessness is a laboratory model and human situations are "
            "not laboratories. If any of this track described you rather than merely interested "
            "you, the correct next step is a professional — this material is for understanding "
            "the mechanism, and it does not qualify anyone, including you, to treat it.",
        ],
        "sources": [
            src("van der Kolk — Inescapable Shock",
                "Dogs given repeated shocks they could not escape did not run when the cage was "
                "later opened and the shocks resumed, while control dogs that had never been "
                "shocked left immediately."),
            src("van der Kolk — Inescapable Shock",
                "What mattered was not the pain but the inescapability — a system that learns "
                "its actions do not change outcomes stops producing them, and goes on not "
                "producing them after escape becomes possible."),
        ],
        "quiz": [
            {"q": "What did the experiment isolate as the active ingredient?",
             "c": ["the amount of pain",
                   "inescapability — the control dogs felt the same shock and ran",
                   "the number of shocks", "the size of the cage"], "a": 1},
            {"q": "Why doesn't 'the door is open, just go' work?",
             "c": ["they do not believe you",
                   "action generation itself has been suppressed — it is not a bad choice being "
                   "made about the present",
                   "they are comfortable", "they need more time"], "a": 1},
            {"q": "Why can encouragement actively make it worse?",
             "c": ["it is annoying",
                   "it supplies more evidence that their actions do not produce outcomes, which "
                   "is what created the state",
                   "it is too vague", "it comes too early"], "a": 1},
        ],
        "apply": {"prompt": "Think of someone stuck in something obvious to you from outside. "
                            "Write what your advice assumes about them, and then write what "
                            "would actually restore a sense that their actions produce outcomes "
                            "— starting far smaller than the problem.", "min": 50},
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
