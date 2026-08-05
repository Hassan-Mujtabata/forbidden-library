# -*- coding: utf-8 -*-
"""#176 — regression test for the reset controls (JOB 6).

Runs the REAL functions lifted out of index.html, not a copy, so it fails if they are renamed or
rewritten. What it pins is the part that is easy to get wrong and silent when wrong:

  * clearing a stage removes the WHOLE S.node entry -- leaving `rv` behind means the spaced
    review scheduler still treats a reset lesson as one you have already seen;
  * a mini-path PARENT stores nothing of its own (completion is derived from its steps), so
    resetting a parent must clear its children or it is a no-op that looks like it worked;
  * pointers into deleted state (S.nodePos, S.lastTrack) are dropped, or the CONTINUE card
    offers a lesson whose progress no longer exists;
  * declining the confirm changes nothing, and "nothing to reset" says so rather than
    reporting a successful reset.

    python tools/reset_test.py
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")
CORE_A, CORE_B = "/* ============ #176 JOB 6", "function nodeAvail(id){const n=nodeById(id);if(!n)return false;"
STEP_A, STEP_B = "let _STEPS=null;", "function nodeDone(id){"

HARNESS = r"""
let CONFIRM=true, TOASTS=[], SAVED=0, RENDERS=0;
global.confirm=()=>CONFIRM; global.toast=t=>TOASTS.push(t);
global.save=()=>SAVED++; global.renderPath=()=>RENDERS++;
let DATA=null,S=null;
const nodeById=id=>DATA.nodes.find(n=>n.id===id)||null;
const trackById=id=>DATA.tracks.find(t=>t.id===id)||null;
const bookById=id=>DATA.books.find(b=>b.id===id)||null;
const trackVisible=()=>true;
"""


def main():
    src = open(APP, encoding="utf-8").read()
    for a, b in ((CORE_A, CORE_B), (STEP_A, STEP_B)):
        if a not in src or b not in src:
            print(f"FAIL: could not find {a!r}..{b!r} in index.html. If renamed, update this test.")
            return 1
    i = src.index(CORE_A); core = src[i:src.index(CORE_B, i)]
    k = src.index(STEP_A); steps = src[k:src.index(STEP_B, k)]
    fd, path = tempfile.mkstemp(suffix=".js"); os.close(fd)
    try:
        open(path, "w", encoding="utf-8").write(HARNESS + steps + core + TAIL)
        r = subprocess.run(["node", path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        sys.stdout.write(r.stdout or ""); sys.stderr.write(r.stderr or "")
        return r.returncode
    finally:
        os.unlink(path)


TAIL = r"""
let fails=0;
function is(l,g,w){const ok=JSON.stringify(g)===JSON.stringify(w);if(!ok)fails++;
  console.log((ok?"  ok   ":"  FAIL ")+l+"  got="+JSON.stringify(g)+" want="+JSON.stringify(w));}
function fresh(){
  DATA={tracks:[{id:"A",name:"Alpha",glyph:"a"},{id:"B",name:"Beta",glyph:"b"}],
    books:[{id:"bk",title:"Book One"}],
    nodes:[{id:"a1",track:"A",tier:0,prereq:[],sources:[{book:"Book One"}]},
           {id:"mp",track:"A",tier:1,prereq:["a1"]},
           {id:"s1",track:"A",tier:1,prereq:[],parent:"mp"},
           {id:"s2",track:"A",tier:2,prereq:["s1"],parent:"mp"},
           {id:"b1",track:"B",tier:0,prereq:[],sources:[{book:"Book One"}]}]};
  S={node:{a1:{doneAt:1,rv:{k:3,due:9}},s1:{doneAt:1,rv:{k:2}},s2:{doneAt:1},b1:{doneAt:1}},
     nodePos:{id:"s1"},lastTrack:"A"};
  _STEPS=null;TOASTS=[];
}
console.log("A  reset a single leaf stage");
fresh(); resetStage("a1");
is("whole entry gone, not just doneAt",S.node.a1,undefined);
is("review record went with it",!!(S.node.a1&&S.node.a1.rv),false);
is("other lessons untouched",!!S.node.s1,true);
console.log("B  reset a mini-path parent (stores nothing of its own)");
fresh(); resetStage("mp");
is("both steps cleared",[S.node.s1,S.node.s2],[undefined,undefined]);
is("unrelated lesson kept",!!S.node.a1,true);
is("stale nodePos dropped",S.nodePos,null);
console.log("C  reset a whole path");
fresh(); resetPath("A");
is("every node in track cleared",[S.node.a1,S.node.mp,S.node.s1,S.node.s2],[undefined,undefined,undefined,undefined]);
is("other track survives",!!S.node.b1,true);
is("stale lastTrack dropped",S.lastTrack,null);
console.log("D  declining the confirm changes nothing");
fresh(); CONFIRM=false; resetPath("A");
is("still there",!!S.node.a1,true); CONFIRM=true;
console.log("E  nothing to reset is reported, not faked");
fresh(); S.node={}; TOASTS=[]; resetStage("a1");
is("said so",/Nothing to reset/.test(TOASTS[0]||""),true);
console.log("F  which book is in which path");
fresh();
is("book feeds both tracks",tracksForBook("bk").map(t=>t.id),["A","B"]);
console.log("");
console.log(fails?(fails+" FAILURE(S)"):"all assertions passed");
process.exit(fails?1:0);
"""


if __name__ == "__main__":
    raise SystemExit(main())
