# -*- coding: utf-8 -*-
"""Draft a felt figure for every Path lesson. Runs for hours on Hassan's PC, on his keys.

    python tools/figs_pipeline.py --status          # coverage: which lessons have figures
    python tools/figs_pipeline.py --track B         # draft one track, write drafts file
    python tools/figs_pipeline.py --track B --n 3   # just three, for a quick look
    python tools/figs_pipeline.py --gallery         # build the review page from drafts
    python tools/figs_pipeline.py --apply           # merge APPROVED drafts into graph.json
    python tools/figs_pipeline.py --selftest        # gates only, no network

WHY THE PROMPT LOOKS LIKE THAT. The first hand-built figure drew expanding circles where a
heartbeat is FELT. Hassan's correction was the whole design principle: a heartbeat does not happen
where you notice it, it leaves the heart and arrives there, and that travel is the thing you are
straining to perceive. Drawing the sensation's location taught nothing; drawing the mechanism
taught it in seconds.

So the model is not asked "illustrate this lesson". It is made to answer three questions first --
what does a beginner get WRONG here, what is actually happening, and what changes over time -- and
only then to choose components. A figure that cannot name the misunderstanding it fixes is
decoration, and this file rejects it.

GATES, all of which refuse rather than repair:
  1. schema     — every component exists, alt present, 1-3 stages, captions sane
  2. grounding  — every content word in a caption appears in the lesson or the library's own
                  vocabulary. A caption teaching a technique the lesson does not teach is a
                  fabricated instruction, which is the one unrecoverable failure here.
  3. voice      — second person, no "the text/lesson/passage", no markdown, <=200 chars
  4. confusion  — the draft must state the misunderstanding, and it must not be boilerplate
Nothing is written to graph.json until a human has looked at the gallery and approved it.
"""
import json, os, re, sys, argparse, collections, time

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH = os.path.join(HERE, "graph.json")
BOOKS = os.path.join(HERE, "books.json")
DRAFTS = os.path.join(HERE, "figs_drafts.json")
REVIEW = os.path.join(HERE, "figs_review")

# Mirrors FIGC in index.html and FIG_COMPONENTS in build.py. Three lists, one truth — the menu
# below is also what the model sees, so a component missing here is a component it cannot use.
MENU = [
    ("body",  "a soft human silhouette that swells; anchors heart/hands/feet/head", "{}"),
    ("hand",  "an open hand, five fingertip pads; anchors fingertips/wrist", "{}"),
    ("feet",  "two soles; anchors soles/ankles", "{}"),
    ("sit",   "a seated meditator; anchors chest/head", "{}"),
    ("flow",  "PRESSURE TRAVELLING from one anchor to others, swelling as it lands",
              '{"from":"heart","to":"whole","rate":1.0,"strength":0.7}'),
    ("pressure", "pulses appearing at an anchor set (use flow instead unless it truly is local)",
              '{"at":"fingertips","rate":1.0}'),
    ("pacer", "a ring that breathes at a stated pace, to match", '{"pace":6,"label":"6s in · 6s out"}'),
    ("wash",  "a soft gradient filling the frame", '{"dir":"up"}'),
    ("halo",  "a wide dashed ring — open awareness", '{"r":40}'),
    ("dot",   "a point of attention; jitter 0-1 for how unsteady", '{"x":100,"y":60,"jitter":0.6}'),
    ("loop",  "a 4-point cycle with a travelling dot", '{"labels":["cue","craving","response","reward"],"pace":8}'),
    ("stages","step dots 1..n with one lit", '{"n":4,"on":1}'),
    ("curve", "two lines with the gap between them shaded — effort vs results over time",
              '{"flat":true,"band_label":"the gap","right":"results"}'),
    ("ripple","a wave arising and passing", '{"label":"arises · passes"}'),
    ("fork",  "one path becoming two, either or both walked", '{"take":1,"a":"option A","b":"option B"}'),
    ("scale", "a balance tilting — one thing outweighing another", '{"tilt":0.6,"left":"vivid","right":"likely"}'),
    ("lanes", "two runners at different speeds", '{"a":"fast","b":"slow","fast":2.4,"slow":6}'),
    ("gauge", "a dial 0-1, optionally settling", '{"v":0.7,"settle":true,"label":"arousal"}'),
    ("tether","one figure anchored, another venturing and returning", '{"far":0.8,"base":"secure base"}'),
    ("crowd", "a grid of dots, a fraction lit — what everyone else seems to do", '{"lit":0.7,"label":""}'),
    ("spot",  "a narrow cone of attention over a wider field", '{"width":0.3,"label":"what you saw"}'),
    ("gap",   "stimulus -> [space] -> response, the space glowing", '{"gap":0.6,"left":"stimulus","right":"response"}'),
    ("grip",  "a closed fist or an open palm", '{"open":true,"label":"letting go"}'),
    ("stack", "translucent layers, together or separated", '{"n":5,"apart":true,"labels":["form","feeling"]}'),
    ("drift", "attention leaving an anchor and being brought back; stage hold|wander|return",
              '{"stage":"return","anchor":"the breath","away":"a thought"}'),
    ("two",   "two people of unequal standing, glow shows status; threat marks a clash",
              '{"high":0.9,"low":0.4,"a":"the master","b":"you","threat":true}'),
    ("ladder","a staged progression with named rungs, lit up to `on`",
              '{"rungs":["first","second","third"],"on":1}'),
    ("magnet","an estimate dragged toward a planted anchor", '{"anchor":0.2,"pull":0.6,"anchor_label":"the number you heard"}'),
    ("label", "a short line of text in the frame", '{"text":"","x":100,"y":62}'),
]
COMPONENTS = {m[0] for m in MENU}

PROMPT = """You design instructional diagrams for a reading app. Not decoration — diagrams that
teach something the prose struggles to convey.

THE LESSON
"{title}"
{text}

HOW TO THINK ABOUT THIS (do this before choosing anything)
1. What does a beginner get WRONG about this idea, or fail to grasp from words alone? Be specific.
2. What is ACTUALLY happening — the mechanism underneath? A diagram of the mechanism teaches; a
   picture of the topic does not.
3. What CHANGES across two or three steps? A figure earns its steps by showing change.

A worked example of the METHOD — not a template. For "feel your own heartbeat internally", the
beginner's error is looking for a tap where they feel it. The mechanism is that the beat LEAVES the
heart and ARRIVES at the fingertips a moment later, filling the body like a balloon. So that figure
shows pressure travelling outward and swelling as it lands, rather than circles pulsing where it is
noticed.

Take the METHOD from that — find the error, draw the mechanism — and nothing else. Do NOT reach for
bodies, pulses or anything else from it unless THIS concept genuinely needs them. A statistical idea
should look statistical; a social one should show people; a sequence should look like a sequence.
The right form comes from the concept in front of you, and a figure that borrows another concept's
shape teaches that concept instead of this one.

Also avoid the lazy fallbacks: a seated figure, a floating dot and a text label can be dropped onto
any lesson at all, which is exactly why they usually teach nothing. If your scene would work
unchanged for a different lesson, it is the wrong scene.

COMPONENTS YOU MAY USE (only these)
{menu}

RULES
- Captions speak to the reader as "you". Concrete, ≤200 characters, no markdown.
- Never write "the text", "the lesson", "the passage" — they are recalling, not reading.
- Teach ONLY what this lesson teaches. Do not add techniques, numbers or claims from elsewhere.
- 2 or 3 stages. Each stage must show a genuine change, not a restatement.
- No medical or therapeutic advice.

Return ONLY this JSON:
{{"confusion":"<the specific thing a beginner gets wrong, one sentence>",
  "mechanism":"<what is actually happening, one sentence>",
  "alt":"<what the diagram shows, for someone who cannot see it>",
  "place":<0-based paragraph index to sit after>,
  "stages":[{{"cap":"<caption>","scene":[{{"c":"<component>", ...params}}]}}]}}"""

BANNED = re.compile(r"\bthe (text|lesson|passage|excerpt|reading|author)\b", re.I)
MD = re.compile(r"[*_`#]|\[[^\]]*\]\(")


# ------------------------------------------------------------------ gates
def gate_schema(d, n):
    if not isinstance(d, dict):
        return "not an object"
    if not d.get("alt"):
        return "no alt text"
    st = d.get("stages")
    if not isinstance(st, list) or not (1 <= len(st) <= 3):
        return "needs 1-3 stages, got %s" % (len(st) if isinstance(st, list) else "none")
    pl = d.get("place")
    if pl is not None and not (0 <= pl < max(1, len(n.get("bridge") or []))):
        return "place %s outside the lesson" % pl
    for i, s in enumerate(st):
        if not isinstance(s, dict) or not s.get("cap"):
            return "stage %d has no caption" % i
        sc = s.get("scene")
        if not isinstance(sc, list) or not sc:
            return "stage %d has an empty scene" % i
        for it in sc:
            if not isinstance(it, dict) or it.get("c") not in COMPONENTS:
                return "stage %d uses unknown component %r" % (i, (it or {}).get("c"))
    return None


def gate_voice(d, n):
    for i, s in enumerate(d["stages"]):
        c = s["cap"]
        if len(c) > 200:
            return "stage %d caption is %d chars" % (i, len(c))
        if BANNED.search(c):
            return "stage %d mentions the text itself" % i
        if MD.search(c):
            return "stage %d caption has markdown" % i
    caps = [s["cap"].strip().lower() for s in d["stages"]]
    if len(set(caps)) != len(caps):
        return "two stages have the same caption"
    return None


WORD = re.compile(r"[A-Za-z][A-Za-z'-]+")
STOP = set("""the a an and or but if then than that this these those of in on at to for with from by
as is are was were be been being it its they them their there here what which who you your yours we
our us i me my he she his her not no nor so too very can will just do does did about into over under
again once all any both each few more most other some such only own same when where why how because
while during before after above below one two three first second third own now new old only ever
also each into upon per via yet still even though both either neither""".split())


def gate_grounding(d, n, vocab):
    """Every content word in a caption must exist in this lesson or in the library's vocabulary.

    A caption is an instruction. One that teaches a technique the lesson never mentions is a
    fabricated instruction with the app's authority behind it — the same class of failure as a
    model-invented quote, and the reason this gate refuses instead of trimming.
    """
    lesson = set(w.lower() for w in WORD.findall(" ".join(n.get("bridge") or []) + " " + n.get("title", "")))
    for i, s in enumerate(d["stages"]):
        for w in WORD.findall(s["cap"]):
            lw = w.lower()
            if len(lw) < 4 or lw in STOP or lw in lesson or lw in vocab:
                continue
            return "stage %d says %r, which is in neither the lesson nor the library" % (i, w)
    return None


BOILER = re.compile(r"^(people|readers|beginners|many|some|most|it)\s+(often|usually|tend|may|might|can)\b", re.I)


def gate_confusion(d, n):
    c = (d.get("confusion") or "").strip()
    if len(c) < 20:
        return "did not state what a beginner gets wrong"
    if BOILER.match(c) and len(c) < 60:
        return "the confusion is boilerplate: %r" % c[:60]
    if not (d.get("mechanism") or "").strip():
        return "did not state the mechanism"
    return None


GATES = [("schema", gate_schema), ("voice", gate_voice), ("confusion", gate_confusion)]


def run_gates(d, n, vocab):
    for name, fn in GATES:
        r = fn(d, n) if fn is not gate_grounding else fn(d, n, vocab)
        if r:
            return "%s: %s" % (name, r)
    r = gate_grounding(d, n, vocab)
    return ("grounding: " + r) if r else None


# ------------------------------------------------------------------ vocab
def library_vocab():
    try:
        data = json.load(open(BOOKS, encoding="utf-8"))
    except Exception:
        return set()
    seen = collections.Counter()
    for b in data["books"]:
        for e in b["episodes"]:
            for p in e["p"]:
                for w in WORD.findall(p):
                    seen[w.lower()] += 1
    return {w for w, c in seen.items() if c >= 3}


# ------------------------------------------------------------------ drafting
def menu_text():
    return "\n".join("  %-9s %s\n            e.g. %s" % (a, b, c) for a, b, c in MENU)


class Local:
    """Draft on Hassan's own GPU through Ollama, so a daily quota stops being the ceiling.

    This work suits a local model unusually well. The output is a small, rigidly-shaped JSON
    object, and every gate in this file REFUSES rather than repairs — so a weaker model does not
    produce worse figures, it produces more rejections, and the rejections cost nothing but time
    on a machine that is already switched on. Quality is defended by the gates and by review, not
    by the size of the model.
    """
    def __init__(self, model="qwen2.5:7b", host="http://127.0.0.1:11434", gap=0.0):
        import urllib.request
        self.ur = urllib.request
        self.model = model; self.host = host.rstrip("/"); self.gap = gap
        self.calls = 0; self.spent = set(); self.broken = set()

    def available(self):
        import json as _json
        try:
            with self.ur.urlopen(self.host + "/api/tags", timeout=6) as r:
                tags = [m["name"] for m in _json.load(r).get("models", [])]
        except Exception:
            return False, "Ollama is not responding on " + self.host
        if not tags:
            return False, "Ollama has no models pulled (try: ollama pull " + self.model + ")"
        if not any(t.split(":")[0] == self.model.split(":")[0] for t in tags):
            return False, "%s is not pulled; available: %s" % (self.model, ", ".join(tags[:4]))
        return True, tags[0]

    def __call__(self, prompt, temp=0.7, schema=None):
        import json as _json, time as _time
        body = _json.dumps({"model": self.model, "prompt": prompt, "stream": False,
                            "format": "json",              # Ollama constrains the output to JSON
                            "options": {"temperature": temp, "num_ctx": 8192}}).encode()
        req = self.ur.Request(self.host + "/api/generate", data=body,
                              headers={"Content-Type": "application/json"})
        with self.ur.urlopen(req, timeout=600) as r:
            d = _json.load(r)
        self.calls += 1
        if self.gap:
            _time.sleep(self.gap)
        return d.get("response", "")


class OutOfQuota(Exception):
    """Every key has spent its DAY. Not a condition to wait out — stop and run again tomorrow."""


class Caller:
    """Rotates keys, picks a model each key can actually use, and stops when the day is spent.

    Two things were wrong before, both found by looking at the actual error bodies rather than the
    status codes:

    * 404 was treated as "this key is broken". The body says
      "This model gemini-2.5-flash is no longer available to new users" — the KEY is fine, the
      hard-coded model just is not offered to newer projects. So a 404 now demotes that key to
      another model instead of retiring it, which reclaims a whole key.
    * 429 was treated as a momentary rate limit worth sleeping through. The body says
      "You exceeded your current quota" — that is the DAILY allowance, and no amount of backoff
      brings it back before tomorrow. Sitting in a retry loop until midnight burns a machine for
      nothing, so the run now stops cleanly and says so.
    """
    # Ordered by preference. The first two are what most keys have; the older ones are the
    # fallbacks for projects that cannot see the newest.
    MODELS = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-2.0-flash-lite"]

    def __init__(self, keys, model=None, gap=4.0):
        import urllib.request, urllib.error
        self.ur, self.ue = urllib.request, urllib.error
        self.keys = list(keys)
        self.models = ([model] if model else []) + [m for m in self.MODELS if m != model]
        self.pick = {}                     # key -> the model that works for it
        self.spent = set()                 # keys out of quota for the day
        self.broken = set()                # keys no model works for at all
        self.i = 0; self.gap = gap; self.calls = 0

    def _post(self, key, model, body):
        url = ("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % model)
        req = self.ur.Request(url, data=body, headers={"Content-Type": "application/json",
                                                       "x-goog-api-key": key})
        with self.ur.urlopen(req, timeout=120) as r:
            import json as _json
            return _json.load(r)

    def usable(self):
        return [k for k in self.keys if k not in self.spent and k not in self.broken]

    def __call__(self, prompt, temp=0.7, schema=None):
        import json as _json, time as _time
        body = _json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {"temperature": temp,
                                                 "responseMimeType": "application/json"}}).encode()
        tried = 0
        while True:
            live = self.usable()
            if not live:
                if self.spent:
                    raise OutOfQuota("all %d usable key(s) are out of quota for today" % len(self.spent))
                raise RuntimeError("no key can reach any model")
            k = live[self.i % len(live)]; self.i += 1
            tried += 1
            for model in ([self.pick[k]] if k in self.pick else self.models):
                try:
                    d = self._post(k, model, body)
                    self.pick[k] = model                       # remember what works for this key
                    self.calls += 1
                    _time.sleep(self.gap)
                    return d["candidates"][0]["content"]["parts"][0]["text"]
                except self.ue.HTTPError as e:
                    msg = ""
                    try:
                        msg = (_json.load(e).get("error", {}).get("message") or "")
                    except Exception:
                        pass
                    if e.code == 429:
                        self.spent.add(k)                       # daily allowance, not a rate limit
                        break
                    if e.code == 404:
                        continue                                # try this key on an older model
                    if e.code in (400, 403):
                        self.broken.add(k); break
                    _time.sleep(2)
                except Exception:
                    _time.sleep(2)
            else:
                self.broken.add(k)                              # no model worked for this key
            if tried > len(self.keys) * 2:
                raise RuntimeError("no key could complete the request")


def draft_one(n, call, vocab, tries=2):
    text = "\n\n".join((n.get("bridge") or [])[:6])[:4000]
    p = PROMPT.format(title=n.get("title", ""), text=text, menu=menu_text())
    last = None
    for attempt in range(tries):
        msg = p if attempt == 0 else p + "\n\nYour previous attempt was rejected: " + last + \
            "\nFix exactly that and return the JSON again."
        try:
            raw = call(msg, temp=0.55, schema=None)
        except Exception as e:
            return None, "call failed: %s" % str(e)[:90]
        s = (raw or "").strip()
        i, j = s.find("{"), s.rfind("}")
        if i < 0 or j <= i:
            last = "reply was not JSON"; continue
        try:
            d = json.loads(s[i:j + 1])
        except Exception:
            last = "reply was not valid JSON"; continue
        bad = run_gates(d, n, vocab)
        if not bad:
            return d, None
        last = bad
    return None, last


def load_drafts():
    try:
        return json.load(open(DRAFTS, encoding="utf-8"))
    except Exception:
        return {}


def save_drafts(d):
    json.dump(d, open(DRAFTS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ gallery
def gallery(graph, drafts):
    """A local page that renders every draft with the app's own components, for approval.

    Gitignored and blocked in ship.py: it quotes lesson text in plaintext, which is exactly the
    mistake integrate_report.txt already made once.
    """
    os.makedirs(REVIEW, exist_ok=True)
    byid = {n["id"]: n for n in graph["nodes"]}
    rows = []
    for nid, rec in sorted(drafts.items()):
        n = byid.get(nid)
        if not n or not rec.get("fig"):
            continue
        rows.append({"id": nid, "title": n.get("title", ""), "track": n.get("track", ""),
                     "confusion": rec.get("confusion", ""), "mechanism": rec.get("mechanism", ""),
                     "fig": rec["fig"]})
    src = open(os.path.join(HERE, "..", "index.html"), encoding="utf-8").read()
    m = re.search(r"const FIG_W=200[\s\S]*?\n};\n", src)
    figc = m.group(0) if m else ""
    css = "\n".join(re.findall(r"^\.feltfig[^\n]*$|^@keyframes fg[^\n]*\{[^\}]*\}[^\n]*$", src, re.M))
    html = """<!doctype html><meta charset="utf-8"><title>figure review</title>
<style>body{background:#12100c;color:#e8e6df;font:15px/1.6 system-ui;margin:0;padding:28px}
.card{max-width:760px;margin:0 auto 30px;background:#1a1712;border:1px solid #2a251c;border-radius:14px;padding:20px}
h2{font-size:17px;margin:0 0 4px}.meta{color:#9a97a5;font-size:12.5px;margin-bottom:14px}
.q{color:#d4af37;font-size:13px;margin:8px 0}.v{display:flex;gap:10px;margin-top:14px}
button.v{padding:8px 16px;border-radius:9px;border:1px solid #2a251c;background:#211d16;color:#e8e6df;cursor:pointer}
button.yes.on{background:#1e4d3a;border-color:#2e7d55}button.no.on{background:#5a2020;border-color:#8a3030}
%s
.feltfig{background:#1a1712;border-color:#2a251c}</style>
<div id="app"></div>
<script>
const A="#d4af37";
%s
const ROWS=%s;
const V=JSON.parse(localStorage.getItem("figv")||"{}");
const app=document.getElementById("app");
for(const r of ROWS){
  const c=document.createElement("div");c.className="card";
  c.innerHTML=`<h2>${r.title}</h2><div class="meta">${r.id} · track ${r.track}</div>`+
    `<div class="q"><b>gets wrong:</b> ${r.confusion}</div>`+
    `<div class="q"><b>mechanism:</b> ${r.mechanism}</div>`;
  for(const st of r.fig.stages){
    const f=document.createElement("figure");f.className="feltfig";
    f.innerHTML=`<div class="ff-svg"><svg viewBox="0 0 200 120" fill="none" stroke="${A}" stroke-width="2.4"
      stroke-linecap="round" stroke-linejoin="round">${figScene(st.scene,A)}</svg></div>
      <figcaption>${st.cap}</figcaption>`;
    c.appendChild(f);
  }
  const v=document.createElement("div");v.className="v";
  const mk=(cls,txt,val)=>{const b=document.createElement("button");b.className="v "+cls+(V[r.id]===val?" on":"");
    b.textContent=txt;b.onclick=()=>{V[r.id]=val;localStorage.setItem("figv",JSON.stringify(V));
      [...v.children].forEach(x=>x.classList.remove("on"));b.classList.add("on");};v.appendChild(b);};
  mk("yes","✓ approve","yes");mk("no","✗ reject","no");
  c.appendChild(v);app.appendChild(c);
}
const dl=document.createElement("button");dl.className="v";dl.textContent="⬇ export verdicts";
dl.onclick=()=>{const a=document.createElement("a");
  a.href=URL.createObjectURL(new Blob([JSON.stringify(V,null,1)],{type:"application/json"}));
  a.download="figs_verdicts.json";a.click();};
app.appendChild(dl);
</script>""" % (css, figc, json.dumps(rows, ensure_ascii=False))
    p = os.path.join(REVIEW, "gallery.html")
    open(p, "w", encoding="utf-8").write(html)
    return p, len(rows)


# ------------------------------------------------------------------ selftest
def selftest():
    fails = []
    def ck(name, cond):
        if cond is not True:
            fails.append("%s -- %s" % (name, cond))
    n = {"title": "Access Concentration", "bridge": ["You rest attention on the breath until it settles."]}
    v = {"breath", "attention", "settles", "steady", "rest"}
    good = {"confusion": "A beginner hunts for a dramatic sign and misses the quiet steadiness.",
            "mechanism": "Attention settles gradually rather than switching on.",
            "alt": "a dot steadying", "place": 0,
            "stages": [{"cap": "You rest attention on the breath.", "scene": [{"c": "dot", "jitter": 0.8}]},
                       {"cap": "It settles until steady.", "scene": [{"c": "dot", "jitter": 0.1}]}]}
    ck("accepts a good draft", run_gates(good, n, v) is None or run_gates(good, n, v))
    bad = {
      "unknown component": dict(good, stages=[{"cap": "You rest.", "scene": [{"c": "teleporter"}]}]),
      "no alt":            dict(good, alt=""),
      "mentions the text": dict(good, stages=[{"cap": "As the passage says, you rest.", "scene": [{"c": "dot"}]}]),
      "markdown":          dict(good, stages=[{"cap": "You **rest** attention.", "scene": [{"c": "dot"}]}]),
      "no confusion":      dict(good, confusion="x"),
      "four stages":       dict(good, stages=good["stages"] * 2),
      "duplicate caption": dict(good, stages=[good["stages"][0], dict(good["stages"][0])]),
      "invented word":     dict(good, stages=[{"cap": "Notice the pranayama rising.", "scene": [{"c": "dot"}]}]),
    }
    for label, d in bad.items():
        ck("refuses " + label, (run_gates(d, n, v) is not None) or "accepted it")
    print("figs_pipeline selftest: " + ("ok" if not fails else "FAIL\n  " + "\n  ".join(fails)))
    return not fails


# ------------------------------------------------------------------ main
def main():
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--track"); ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--status", action="store_true"); ap.add_argument("--gallery", action="store_true")
    ap.add_argument("--apply", action="store_true"); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--local", action="store_true",
                    help="draft on this machine's GPU via Ollama instead of Gemini (no quota)")
    ap.add_argument("--model", default="qwen2.5:7b", help="Ollama model to use with --local")
    ap.add_argument("--gap", type=float, default=4.0,
                    help="seconds between calls — this is meant to run slowly and unattended")
    ap.add_argument("--verdicts", default=os.path.join(REVIEW, "figs_verdicts.json"))
    a = ap.parse_args()

    if a.selftest:
        sys.exit(0 if selftest() else 1)

    graph = json.load(open(GRAPH, encoding="utf-8"))
    drafts = load_drafts()

    if a.status:
        per = collections.Counter(); have = collections.Counter()
        for n in graph["nodes"]:
            per[n["track"]] += 1
            if n.get("fig"): have[n["track"]] += 1
        print("%-6s %-28s %s" % ("track", "name", "figures / lessons"))
        for t in graph["tracks"]:
            print("%-6s %-28s %d / %d" % (t["id"], t.get("name", "")[:28], have[t["id"]], per[t["id"]]))
        print("\ndrafted and awaiting review: %d" % len([k for k, v in drafts.items() if v.get("fig")]))
        return

    if a.gallery:
        p, k = gallery(graph, drafts)
        print("wrote %s (%d figure%s)" % (p, k, "" if k == 1 else "s"))
        print("Open it, approve or reject each, then export the verdicts next to it.")
        return

    if a.apply:
        try:
            verdicts = json.load(open(a.verdicts, encoding="utf-8"))
        except Exception:
            print("no verdicts at %s — run --gallery, review, then export." % a.verdicts); return
        byid = {n["id"]: n for n in graph["nodes"]}
        ok = 0
        for nid, v in verdicts.items():
            if v != "yes" or nid not in byid or nid not in drafts:
                continue
            byid[nid]["fig"] = [drafts[nid]["fig"]]
            ok += 1
        json.dump(graph, open(GRAPH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("applied %d approved figure(s). NEXT: python tools/build.py" % ok)
        return

    sys.path.insert(0, HERE)
    if a.local:
        call = Local(a.model, gap=0.0)
        ok_local, why = call.available()
        if not ok_local:
            print("local model unavailable — " + why); return
        print("drafting on this machine's GPU via Ollama (%s) — no Gemini quota involved" % a.model)
    else:
        import gemini_pipeline as gp
        if not gp.KEYS:
            print("no Gemini keys."); return
        call = Caller(gp.KEYS, gp.MODEL, gap=a.gap)
    vocab = library_vocab()
    todo = [n for n in graph["nodes"]
            if not n.get("stub") and not n.get("fig") and n["id"] not in drafts
            and (not a.track or n["track"] == a.track)]
    if a.n:
        todo = todo[:a.n]
    where = ("this machine's GPU (%s)" % a.model) if a.local else ("%d Gemini key(s)" % len(call.keys))
    print("drafting %d lesson(s) on %s; library vocabulary %d words\n" % (len(todo), where, len(vocab)))
    good = bad = 0
    stopped = None
    for i, n in enumerate(todo):
        t0 = time.time()
        try:
            d, err = draft_one(n, call, vocab)
        except OutOfQuota as e:
            # Nothing to wait for: this is the daily allowance, and it comes back tomorrow, not
            # in fifteen minutes. Everything drafted so far is already on disk, and the next run
            # picks up exactly where this one stopped.
            stopped = str(e)
            break
        if d:
            drafts[n["id"]] = {"fig": {"v": 1, "alt": d["alt"], "place": d.get("place", 1),
                                       "stages": d["stages"]},
                               "confusion": d.get("confusion", ""), "mechanism": d.get("mechanism", ""),
                               "at": int(time.time())}
            good += 1
            print("  [%2d/%d] %-6s OK   %-34s (%.0fs) %s" % (i + 1, len(todo), n["id"],
                  n.get("title", "")[:34], time.time() - t0, d.get("confusion", "")[:44]))
        else:
            bad += 1
            print("  [%2d/%d] %-6s SKIP %-34s %s" % (i + 1, len(todo), n["id"], n.get("title", "")[:34], err))
        save_drafts(drafts)              # incremental: stop any time, resume any time
    print("\n%d drafted, %d refused (%d model calls)." % (good, bad, call.calls))
    if stopped:
        print("STOPPED: %s\n  Everything drafted is saved. Run the same command tomorrow and it\n"
              "  resumes where it left off — or add --local to use this machine's GPU instead."
              % stopped)
    print("Next: python tools/figs_pipeline.py --gallery")


if __name__ == "__main__":
    main()
