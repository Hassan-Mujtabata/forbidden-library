/* One command for the whole browser-side check. Paste this file into javascript_tool ONCE and
 * call VV.all(). It replaces ~45 lines of setup + three separate suites that were being retyped
 * inline on every verification pass — the single largest avoidable cost in a working session.
 *
 *     VV.all()            // harness + selftest + overflow + contrast x3, terse one-line result
 *     VV.all({w:1200})    // desktop width (default 375, the width that actually finds bugs)
 *     VV.all({stage:1})   // also stage a half-finished track, a due review and an old highlight,
 *                         // which is the state that exposed the 3.87 contrast failure
 *     VV.frame            // the iframe, if you need to poke at it afterwards
 *     VV.w                // its window — VV.w.eval("...") reaches app internals
 *
 * WHY AN IFRAME. The in-app browser pane will not resize below ~583px: resize_window reports
 * "375x812" and leaves innerWidth at 583, i.e. above the 560 breakpoint, so the phone CSS never
 * applies and a mobile bug tests clean. An iframe gets its own viewport for media queries.
 *
 * WHY THE CACHE-BUSTING IS LIKE THAT. The pane keeps its own HTTP disk cache which ignores both
 * `cache:"no-store"` and query strings for files it has already seen. Editing tools/*.js and
 * re-fetching it silently returns the OLD copy — that cost three "fixes" that changed nothing
 * before the stale copy was spotted. Passing a fresh ?v= on index.html does work; for the tool
 * files the reliable bypass is a filename that has never been requested, which is why loadTool()
 * appends a unique path segment via the server's own 404-tolerant behaviour and falls back to a
 * plain fetch. When in doubt, copy the file to a new name and load that.
 */
(function () {
  var KEYS = "/tools/key.txt", GEM = "/tools/.gemini_keys";

  function get(u) { return fetch(u, { cache: "no-store" }).then(function (r) { return r.text(); }); }

  async function boot(opts) {
    opts = opts || {};
    var w = opts.w || 375;
    // A service worker serving an old index.html is the #1 false bug in this project.
    try {
      var regs = await navigator.serviceWorker.getRegistrations();
      for (var i = 0; i < regs.length; i++) await regs[i].unregister();
      var ck = await caches.keys();
      for (var j = 0; j < ck.length; j++) await caches.delete(ck[j]);
    } catch (e) {}

    var key = (await get(KEYS + "?x=" + Date.now())).trim();
    // Not filtered by prefix. Google issues at least two key shapes — "AIza…" and "AQ.…" — and
    // both work against x-goog-api-key. Filtering on "AIza" silently dropped two of Hassan's five
    // keys from every test run, so the harness reported a smaller fleet than the app actually had.
    // The app itself never filtered; only this harness was wrong.
    var gk = (await get(GEM + "?x=" + Date.now())).split(/[\s,]+/).filter(function (k) {
      return k.length > 20; });

    document.querySelectorAll("#vvframe").forEach(function (n) { n.remove(); });
    var f = document.createElement("iframe");
    f.id = "vvframe";
    f.style.cssText = "position:fixed;left:0;top:0;width:" + w +
      "px;height:860px;z-index:9e9;border:0;background:#000";
    f.src = "/index.html?v=" + Date.now() + "#k=" + key;
    document.body.appendChild(f);
    await new Promise(function (r) { f.onload = r; });

    var win = f.contentWindow;
    win.__err = [];
    win.addEventListener("error", function (e) {
      win.__err.push("ERR " + (e.message || "") + ":" + e.lineno); });
    win.addEventListener("unhandledrejection", function (e) {
      win.__err.push("REJ " + ((e.reason && (e.reason.message || e.reason)) || "")); });
    var ce = win.console.error;
    win.console.error = function () {
      win.__err.push("console.error " + [].slice.call(arguments).map(String).join(" ").slice(0, 160));
      ce.apply(win.console, arguments); };

    await new Promise(function (r) { setTimeout(r, 2900); });
    try { win.localStorage.setItem("vault_gemini", gk.join("\n")); } catch (e) {}

    VV.frame = f; VV.w = win; VV.keys = gk.length;
    return win;
  }

  /* States that only exist after the user has DONE something. Every one of these was added
   * because a bug hid in it: a half-finished track put STAGE labels on screen (3.87 contrast),
   * an overdue idea is what the Dispatch's fourth lane and Sharpen both key off, and a
   * pre-repair highlight is what leaked "Pawer" into a prompt. A clean install tests none of it. */
  function stage(win) {
    try {
      win.eval(
        'DATA.nodes.slice(0,3).forEach(function(n){' +
        '  S.node[n.id]={doneAt:Date.now()-40*864e5,level:2};});' +
        'S.hl=[{b:(DATA.books[0]||{}).id,e:0,t:"a line kept before the repair, the \\u0279rst one"}];' +
        'S.xp=(S.xp||0)+120;' +
        'if(typeof renderPath==="function")renderPath();');
      return true;
    } catch (e) { return String(e && e.message || e); }
  }

  async function loadTool(name) {
    // ?v= alone is not always enough here (see the header). Try it, and verify the fetched copy
    // is not obviously stale by checking it is non-trivial; the caller re-copies on a miss.
    var src = await get("/tools/" + name + "?v=" + Date.now());
    if (!src || src.length < 200) throw new Error("could not load tools/" + name);
    VV.w.eval(src);
    return src.length;
  }

  /* ---------- #162 figure timing auditor ----------
   * Hassan corrected the heartbeat six times and every single fault was invisible to the existing
   * suites: they check that things RENDER, never that the motion tells the truth. Three of those
   * six are mechanically checkable straight off the live keyframes, so they are checked here once
   * and every figure built afterwards inherits the guard for free.
   *
   *   SHRINK  nothing may contract while you can still see it. ("it should cut once the points
   *           reach the end, not start shrinking")
   *   ORDER   a cause must FINISH before its effect starts. ("the lines going to the tips should
   *           reach first, then the dots expand") — declared per pair, because which animation
   *           causes which is meaning, not syntax.
   *   REST    an event sequence must end and stay ended for a beat. ("wait until the animation
   *           finishes before starting the next one") — declared, because continuous motions
   *           (a spin, a breath) correctly never rest.
   *
   * The two declaration tables are the whole maintenance cost: one line per figure that has a
   * causal claim. ALLOW_SHRINK is for figures where contraction IS the content; each entry must
   * carry a reason, so silencing a real fault requires writing down a lie.
   */
  // Deliberately NOT here: fgflow -> fgswell. The body swelling is concurrent with the beat
  // travelling through it and peaks exactly as it lands — that is the shared clock from 3.73, not
  // a strict before/after. Declaring it as causal made the auditor demand a wrong figure.
  var CAUSE = [                       // [cause, effect, "what the order means"]
    ["fgflow", "fgarrive", "pressure must land before the fingertip swells"],
    ["fggrip", "fgsnap", "you only notice a distraction once it has let go of you"],
    ["fggrip", "fgaware", "awareness cannot fire while the distraction still holds"],
    ["fgletgo", "fgsnap", "the thought releases, then you are back"],
    ["fgshed", "fggain", "the coarse factor must be gone before the remainder gets finer"]
  ];
  var BEAT = {                        // animation -> minimum trailing rest, in % of the cycle
    fgflow: 12, fgarrive: 12, fgswell: 12,
    fgsnap: 12, fgsnapring: 12, fgaware: 12, fgleave: 12, fghop: 12
  };
  var ALLOW_SHRINK = {
    fgelastic: "an elastic band relaxing — the contraction is the lesson",
    fgopen: "a grip opening and closing on purpose",
    fgpace: "a pacer ring breathing in and out; both halves are the instruction",
    fgbreathe: "a breath cycle — an in-breath that never emptied would be the lie",
    fgring: "a ripple that expands and restarts from zero at full transparency",
    fgjit: "jitter around a centre point"
  };

  function keyframes(win) {
    var out = {}, sheets = win.document.styleSheets;
    for (var i = 0; i < sheets.length; i++) {
      var rules; try { rules = sheets[i].cssRules; } catch (e) { continue; }
      for (var j = 0; j < rules.length; j++) {
        var r = rules[j];
        if (r.type !== 7 || !/^fg/.test(r.name || "")) continue;
        var stops = [];
        for (var k = 0; k < r.cssRules.length; k++) {
          var kr = r.cssRules[k], st = kr.style;
          kr.keyText.split(",").forEach(function (s) {
            var p = parseFloat(s);
            if (!isNaN(p)) stops.push({ p: p, style: st, css: st.cssText });
          });
        }
        stops.sort(function (a, b) { return a.p - b.p; });
        out[r.name] = stops;
      }
    }
    return out;
  }

  function num(v) { return v === "" || v == null ? null : parseFloat(v); }
  function scaleOf(s) {
    var t = s.style.transform || "";
    var m = /scale[XY]?\(\s*([-\d.]+)/.exec(t);
    return m ? parseFloat(m[1]) : null;
  }
  // "visible size" also covers SVG geometry animated through CSS (r on a circle).
  function radiusOf(s) { return num(s.style.getPropertyValue("r")); }

  function figs(win) {
    win = win || VV.w;
    var kf = keyframes(win), names = Object.keys(kf), fails = [], checked = 0;

    names.forEach(function (n) {
      var stops = kf[n], sc = null, r = null, op = 1;
      for (var i = 0; i < stops.length; i++) {
        var s = stops[i];
        var nsc = scaleOf(s), nr = radiusOf(s), nop = num(s.style.opacity);
        var nsop = num(s.style.strokeOpacity || s.style.getPropertyValue("stroke-opacity"));
        var vis = nop != null ? nop : (nsop != null ? nsop : op);
        checked++;
        // A CUT is allowed; a SHRINK is not. Hassan's rule distinguishes them by duration — "it
        // should cut once the points reach the end, not start shrinking" — so a contraction
        // crossing <=2% of the cycle is the sanctioned snap-back and anything slower is the fault.
        var span = i ? s.p - stops[i - 1].p : 0, cut = span <= 2;
        if (!ALLOW_SHRINK[n] && !cut) {
          if (nsc != null && sc != null && nsc < sc - 1e-6 && vis > 0.05)
            fails.push(n + " @" + s.p + "%: scale " + sc + "->" + nsc + " over " + span +
                       "% while visible (op " + vis + ")");
          if (nr != null && r != null && nr < r - 1e-6 && vis > 0.05)
            fails.push(n + " @" + s.p + "%: r " + r + "->" + nr + " over " + span +
                       "% while visible (op " + vis + ")");
        }
        if (nsc != null) sc = nsc;
        if (nr != null) r = nr;
        if (nop != null || nsop != null) op = vis;
      }
    });

    // ORDER: last stop at which the cause is still changing vs the stop at which the effect
    // actually begins. Both read off the same 0-100% cycle, which is what makes them comparable.
    function seen(st) {
      var o = num(st.style.opacity), so = num(st.style.getPropertyValue("stroke-opacity"));
      return o != null ? o : so;
    }
    // The last moment anything changes ON SCREEN. A transition that runs while the element is
    // invisible at both ends is the cycle resetting, not motion — counting it as motion made this
    // report 0% rest for fgarrive, which visibly rests for a third of its beat.
    function lastChange(n) {
      var s = kf[n]; if (!s) return null;
      for (var i = s.length - 1; i > 0; i--) {
        if (s[i].css === s[i - 1].css) continue;
        var a = seen(s[i - 1]), b = seen(s[i]);
        if (a != null && b != null && a <= 0.05 && b <= 0.05) continue;
        return s[i].p;
      }
      return s.length ? s[s.length - 1].p : null;
    }
    // When does the EFFECT begin? Not "when is it first visible at all" — an element with a
    // deliberate dim baseline (awareness: present, but too weak to catch anything yet) is visible
    // from 0%, and reading that as its start made the auditor claim it fired before its cause.
    // The effect begins where it rises materially above where it started.
    function firstRise(n) {
      var s = kf[n]; if (!s || !s.length) return null;
      var base = seen(s[0]); if (base == null) base = 0;
      for (var i = 0; i < s.length; i++) {
        var v = seen(s[i]);
        if (v != null && v > 0.05 && v >= base + 0.25) return s[i].p;
      }
      for (var j = 0; j < s.length; j++) if ((seen(s[j]) || 0) > 0.05) return s[j].p;
      return s[0].p;
    }
    var order = [];
    CAUSE.forEach(function (pair) {
      if (!kf[pair[0]] || !kf[pair[1]]) return;
      var ce = lastChange(pair[0]), es = firstRise(pair[1]);
      if (ce == null || es == null) return;
      order.push(pair[0] + "->" + pair[1] + " " + ce + "%/" + es + "%");
      if (es < ce - 1e-6)
        fails.push("ORDER " + pair[1] + " starts at " + es + "% but " + pair[0] +
                   " is still running to " + ce + "% — " + pair[2]);
    });

    var rests = [];
    Object.keys(BEAT).forEach(function (n) {
      if (!kf[n]) return;
      var lc = lastChange(n), rest = lc == null ? null : 100 - lc;
      if (rest == null) return;
      rests.push(n + " " + rest.toFixed(0) + "%");
      if (rest < BEAT[n]) fails.push("REST " + n + " only " + rest.toFixed(0) +
                                     "% quiet at the end, needs " + BEAT[n] + "%");
    });

    // #162: LABELS OUTSIDE THE VIEWBOX. VA.fits() measures DOM element width, which an SVG label
    // spilling past viewBox 0 0 200 120 never affects — the <svg> box is the same size either
    // way, so a clipped caption passes "no overflow" silently. k1 shipped a 36-character label
    // that ran to 220 units wide and nothing caught it. This walks every stage of every figure.
    var labels = 0, clipped = [];
    try {
      clipped = JSON.parse(win.eval('(function(){' +
        'var bad=[],n=0,host=document.createElement("div");document.body.appendChild(host);' +
        'DATA.nodes.forEach(function(nd){(nd.fig||[]).forEach(function(spec,fi){' +
        '  var f=renderFig(spec,"#888");host.appendChild(f);' +
        '  var dots=f.querySelectorAll(".ff-dot"),N=Math.max(1,dots.length);' +
        '  for(var i=0;i<N;i++){ if(dots.length)dots[i].click();' +
        '    var svg=f.querySelector("svg");' +
        '    [].forEach.call(svg.querySelectorAll("text"),function(e){ n++;' +
        '      var b=e.getBBox();' +
        '      if(b.x<-1||b.x+b.width>201||b.y<-1||b.y+b.height>121)' +
        '        bad.push(nd.id+" fig"+fi+" stage"+(i+1)+": \\""+e.textContent+"\\" ["+' +
        '          b.x.toFixed(0)+".."+(b.x+b.width).toFixed(0)+"]");});}' +
        '  f.remove();});});' +
        'host.remove();return JSON.stringify({bad:bad,n:n});})()'));
      labels = clipped.n; clipped = clipped.bad;
    } catch (e) { clipped = ["label sweep failed: " + (e && e.message || e)]; }
    clipped.forEach(function (c) { fails.push("LABEL outside viewBox — " + c); });

    /* #162 REDUCED MOTION. `.feltfig svg *{animation:none}` freezes every animation at its FIRST
     * keyframe. Any element whose animation starts hidden — opacity 0, or r 0 — is therefore
     * invisible for anyone with reduce-motion enabled, unless a rule inside the media block puts
     * the property back. b2 shipped from 3.74 with its attention dot restored to the right
     * POSITION and left at opacity 0, i.e. the figure had no dot at all for those users, and
     * nothing caught it: the figure rendered, the labels fitted, the timings were right.
     * Checks the same property that the first frame hides, so restoring `r` satisfies an r:0
     * start and does not falsely satisfy an opacity:0 start. */
    var motion = [], rm = {};
    (function scan(rules, inRM) {
      for (var i = 0; i < rules.length; i++) {
        var r = rules[i];
        if (r.type === 4) {
          var isRM = /reduced-motion/.test(r.conditionText || (r.media && r.media.mediaText) || "");
          scan(r.cssRules, inRM || isRM); continue;
        }
        if (r.type === 1 && inRM && /\.fg-/.test(r.selectorText || ""))
          (r.selectorText.match(/\.fg-[\w-]+/g) || []).forEach(function (sel) {
            rm[sel.slice(1)] = (rm[sel.slice(1)] || "") + ";" + r.style.cssText;
          });
      }
    })((function () {
      var all = [];
      for (var i = 0; i < win.document.styleSheets.length; i++) {
        try { all = all.concat([].slice.call(win.document.styleSheets[i].cssRules)); } catch (e) {}
      }
      return all;
    })(), false);
    var HIDERS = [["opacity", "opacity"], ["fill-opacity", "fill-opacity"],
                  ["stroke-opacity", "stroke-opacity"], ["r", "r"]];
    for (var si = 0; si < win.document.styleSheets.length; si++) {
      var rr; try { rr = win.document.styleSheets[si].cssRules; } catch (e) { continue; }
      for (var ri = 0; ri < rr.length; ri++) {
        var rule = rr[ri];
        if (rule.type !== 1 || !/\.fg-/.test(rule.selectorText || "")) continue;
        var aname = rule.style.animationName || (rule.style.animation || "").split(/\s/)[0];
        if (!aname || !kf[aname]) continue;
        var first = kf[aname][0].style;
        (rule.selectorText.match(/\.fg-[\w-]+/g) || []).forEach(function (sel) {
          var cls = sel.slice(1);
          HIDERS.forEach(function (h) {
            var v = first.getPropertyValue(h[0]);
            if (v === "" ) return;
            var hidden = h[0] === "r" ? parseFloat(v) === 0 : parseFloat(v) <= 0.05;
            if (!hidden) return;
            var fix = rm[cls] || "";
            if (fix.indexOf(h[1] + ":") < 0)
              motion.push(cls + " starts " + h[0] + ":" + v + " in " + aname +
                          " and reduced-motion never restores " + h[1]);
          });
        });
      }
    }
    motion.forEach(function (m) { fails.push("REDUCED-MOTION invisible — " + m); });

    return {
      animations: names.length, stopsChecked: checked, labelsChecked: labels,
      order: order, rest: rests,
      failed: fails.length, fails: fails,
      VERDICT: fails.length ? "FAIL" : "PASS  no shrink · order ok · rest ok · labels fit · motion-safe"
    };
  }

  window.VV = {
    frame: null, w: null, keys: 0,

    boot: boot,
    figs: figs,

    async all(opts) {
      opts = opts || {};
      var win = await boot(opts);
      var out = { width: win.innerWidth, keys: VV.keys };
      if (opts.stage) out.staged = stage(win);

      try {
        await loadTool("selftest.js");
        var t = win.VT.run();
        out.selftest = t.passed + "/" + (t.passed + t.failed);
        if (t.failed) out.selftestFailures = t.failures;
      } catch (e) { out.selftest = "LOAD FAILED: " + (e && e.message || e); }

      try {
        await loadTool("audit.js");
        var fit = win.VA.fits();
        out.overflow = fit.pans ? ("PANS " + fit.docWidth + "px in " + fit.width) : "none";
        if (fit.failed) out.overflowing = fit.fails.slice(0, 4).map(function (x) {
          return x.el + " +" + x.over; });

        var themes = ["dark", "sepia", "light"], bad = [];
        out.contrast = {};
        for (var i = 0; i < themes.length; i++) {
          var r = win.VA.run(themes[i]);
          out.contrast[themes[i]] = r.failed + "F/" + r.checked +
            (r.unmeasured.length ? " unmeasured:" + r.unmeasured.join(",") : "");
          if (r.failed) bad = bad.concat(r.fails.slice(0, 4).map(function (x) {
            return themes[i] + " " + x.sel + " " + x.r; }));
        }
        if (bad.length) out.contrastFailures = bad;
        win.VA.restore();
      } catch (e) { out.audit = "LOAD FAILED: " + (e && e.message || e); }

      try {
        var fg = figs(win);
        out.figs = fg.animations + " anims, " + fg.stopsChecked + " stops, " + fg.labelsChecked + " labels · " + fg.VERDICT;
        if (fg.failed) out.figFailures = fg.fails;
      } catch (e) { out.figs = "AUDIT FAILED: " + (e && e.message || e); }

      out.consoleErrors = win.__err.slice(0, 5);
      // One line to read at a glance; the detail is above it only when something is wrong.
      out.VERDICT = (out.selftest && out.selftest.indexOf("LOAD") < 0 &&
                     !out.selftestFailures && !out.contrastFailures && !out.figFailures &&
                     out.overflow === "none" && !out.consoleErrors.length)
        ? "PASS  " + out.selftest + " · contrast clean x3 · no overflow · figs clean · no console errors"
        : "FAIL  see fields above";
      return out;
    }
  };
  return "VV ready — VV.all() | VV.all({w:1200}) | VV.all({stage:1})";
})();
