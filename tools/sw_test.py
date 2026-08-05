# -*- coding: utf-8 -*-
"""#170 — regression test for the service worker's fetch handler.

THE BUG THIS PINS. `respondWith()` must be handed a Response. The old handler ended in

    const net = fetch(req).then(...).catch(() => hit);
    return hit || net;

so with nothing cached AND a failing fetch, it resolved to `undefined`. respondWith(undefined)
does not quietly fall back to the network — it fails the navigation, and the app paints as a
completely blank page with no error visible anywhere. The state is self-sustaining: every reload
takes the same branch. That is the single worst failure this app can have, because it looks
identical to "the whole thing is gone".

It runs the REAL sw.js against stubbed globals rather than a copy of its logic, so it fails if
the handler is rewritten back into that shape.

    python tools/sw_test.py
"""
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SW = os.path.join(HERE, "..", "sw.js")

HARNESS = r"""
let fails=0;
function is(label,got,want){const ok=JSON.stringify(got)===JSON.stringify(want);
  if(!ok)fails++;console.log((ok?"  ok   ":"  FAIL ")+label+"  got="+JSON.stringify(got)+" want="+JSON.stringify(want));}

// drive the registered fetch handler and report what respondWith actually received
async function ask(url,{cached=[],netFails=false,mode="navigate"}={}){
  STORE=new Map(cached.map(u=>[u,new Response("cached:"+u,{status:200})]));
  NET_FAILS=netFails;
  const req={url:SELF_ORIGIN+"/"+url,method:"GET",mode};
  let handed;
  const ev={request:req,respondWith:p=>{handed=p},waitUntil:p=>{if(p&&p.catch)p.catch(()=>{});}};
  HANDLERS.fetch(ev);
  if(handed===undefined)return {resolved:"respondWith NEVER CALLED"};
  const r=await handed;
  if(r===undefined)return {resolved:"undefined"};
  if(!(r instanceof Response))return {resolved:"not-a-Response"};
  return {resolved:"Response",status:r.status,body:await r.text()};
}

(async()=>{
console.log("A  network is up");
is("serves from network when cache is empty",(await ask("index.html",{netFails:false})).resolved,"Response");
is("serves from cache when cached",(await ask("index.html",{cached:["./index.html","index.html"]})).status,200);

console.log("B  network is DOWN — this is where the blank page came from");
const cold=await ask("index.html",{cached:[],netFails:true});
is("offline + empty cache still yields a Response",cold.resolved,"Response");
const warm=await ask("index.html",{cached:["./index.html"],netFails:true,mode:"navigate"});
is("offline navigation falls back to the app shell",warm.resolved,"Response");
is("shell fallback is the real shell, not an error",warm.status,200);

console.log("C  cached hit must survive a failing background refresh");
const hit=await ask("index.html",{cached:["index.html"],netFails:true,mode:"no-cors"});
is("cache hit returned even though revalidate threw",hit.status,200);

console.log("D  the always-network files (access/status) also never resolve undefined");
is("access.json offline with nothing cached",(await ask("access.json",{netFails:true,mode:"cors"})).resolved,"Response");
is("status.json offline with nothing cached",(await ask("status.json",{netFails:true,mode:"cors"})).resolved,"Response");

console.log("");
console.log(fails?(fails+" FAILURE(S)"):"all assertions passed");
process.exit(fails?1:0);
})();
"""

STUBS = r"""
const SELF_ORIGIN="https://example.test";
let STORE=new Map(), NET_FAILS=false;
const HANDLERS={};
const cacheObj={
  match:async(req,opts)=>{
    const u=typeof req==="string"?req:req.url;
    const keys=[u,u.replace(SELF_ORIGIN+"/",""),"./"+u.replace(SELF_ORIGIN+"/","")];
    for(const k of keys){if(STORE.has(k))return STORE.get(k).clone();}
    return undefined;
  },
  put:async(req,res)=>{const u=typeof req==="string"?req:req.url;STORE.set(u,res);},
};
global.caches={open:async()=>cacheObj, match:async(r,o)=>cacheObj.match(r,o),
               keys:async()=>[], delete:async()=>true};
global.fetch=async()=>{ if(NET_FAILS) throw new Error("offline"); return new Response("net",{status:200}); };
global.self={
  location:{origin:SELF_ORIGIN},
  addEventListener:(k,fn)=>{HANDLERS[k]=fn;},
  skipWaiting:async()=>{}, clients:{claim:async()=>{},matchAll:async()=>[],openWindow:async()=>{}},
  registration:{showNotification:async()=>{}},
};
"""


def main():
    src = open(SW, encoding="utf-8").read()
    fd, path = tempfile.mkstemp(suffix=".js")
    os.close(fd)
    try:
        open(path, "w", encoding="utf-8").write(STUBS + "\n" + src + "\n" + HARNESS)
        r = subprocess.run(["node", path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        sys.stdout.write(r.stdout or "")
        sys.stderr.write(r.stderr or "")
        return r.returncode
    finally:
        os.unlink(path)


if __name__ == "__main__":
    raise SystemExit(main())
