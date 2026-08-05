# -*- coding: utf-8 -*-
"""#169 — regression test for the mini-path state model.

It does NOT re-implement the rules. It lifts the real functions straight out of index.html
(everything from `let _STEPS=null;` up to `function surpriseMe(`) and runs THOSE in node against
a synthetic graph. A copied-out copy of the logic would keep passing after the shipped code
changed, which is the one thing a test like this must never do.

What is pinned here is the part that cannot be seen by looking:

  * a mini-path's completion is DERIVED from its steps and never stored, so "mini-path done" and
    "every step done" cannot drift apart;
  * a step waits on its parent's AVAILABILITY, not its completion -- the reverse deadlocks,
    because the parent only completes once the step does, and the symptom is silent (a step that
    simply never unlocks);
  * progress counts LEAVES, so a container is not counted alongside the steps it contains.

    python tools/minipath_test.py
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "..", "index.html")

HARNESS = r"""
function reset(nodes){DATA={nodes};S={node:{}};_STEPS=null;}
function done(id){S.node[id]={doneAt:1};}
let fails=0;
function is(label,got,want){const ok=JSON.stringify(got)===JSON.stringify(want);
  if(!ok)fails++;console.log((ok?"  ok   ":"  FAIL ")+label+"  got="+JSON.stringify(got)+" want="+JSON.stringify(want));}
const nodes=[
 {id:"gate",track:"A",tier:0,prereq:[]},
 {id:"mp",  track:"A",tier:1,prereq:["gate"]},
 {id:"s1",  track:"A",tier:1,prereq:[],parent:"mp"},
 {id:"s2",  track:"A",tier:2,prereq:["s1"],parent:"mp"},
 {id:"s3",  track:"A",tier:3,prereq:["s2"],parent:"mp"},
 {id:"after",track:"A",tier:2,prereq:["mp"]},
];
reset(nodes);
console.log("A  mini-path before anything is done");
is("steps come out ordered",stepsOf("mp").map(x=>x.id),["s1","s2","s3"]);
is("parent not done",nodeDone("mp"),false);
is("parent is a container, not a leaf",isLeaf(nodeById("mp")),false);
is("gate available",nodeStatus("gate"),"avail");
is("steps locked while mini-path shut",nodeStatus("s1"),"locked");
console.log("B  open the mini-path");
done("gate");
is("step 1 unlocks",nodeStatus("s1"),"avail");
is("step 2 waits on step 1",nodeStatus("s2"),"locked");
is("parent still not done",nodeDone("mp"),false);
is("the lesson after it is locked",nodeStatus("after"),"locked");
console.log("C  walk the steps");
done("s1");
is("step 2 unlocks",nodeStatus("s2"),"avail");
done("s2");done("s3");
is("parent completes when its steps do",nodeDone("mp"),true);
is("the lesson after it unlocks",nodeStatus("after"),"avail");
console.log("D  counting");
is("counts the 4 leaves, not the container",nodesDone(),4);
reset(nodes);
is("nothing done counts zero",nodesDone(),0);
console.log("E  completion is derived, never stored");
done("s1");done("s2");done("s3");
is("parent done with no doneAt of its own",[nodeDone("mp"),!!S.node["mp"]],[true,false]);
console.log("");
console.log(fails?(fails+" FAILURE(S)"):"all assertions passed");
process.exit(fails?1:0);
"""

START, END = "let _STEPS=null;", "function surpriseMe("


def main():
    src = open(APP, encoding="utf-8").read()
    if START not in src or END not in src:
        print("FAIL: could not find the mini-path model in index.html "
              f"(looked for {START!r} .. {END!r}). If it was renamed, update this test.")
        return 1
    i = src.index(START)
    model = src[i:src.index(END, i)]

    js = "\n".join([
        "let DATA=null,S={node:{}};",
        "const nodeById=id=>DATA.nodes.find(n=>n.id===id)||null;",
        "const privileged=()=>true; const trackVisible=()=>true;",
        model,
        HARNESS,
    ])
    fd, path = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    try:
        open(path, "w", encoding="utf-8").write(js)
        r = subprocess.run(["node", path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        sys.stdout.write(r.stdout or "")
        sys.stderr.write(r.stderr or "")
        return r.returncode
    finally:
        os.unlink(path)


if __name__ == "__main__":
    raise SystemExit(main())
