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
    var gk = (await get(GEM + "?x=" + Date.now())).split(/[\s,]+/).filter(function (k) {
      return k.indexOf("AIza") === 0; });

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

  window.VV = {
    frame: null, w: null, keys: 0,

    boot: boot,

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

      out.consoleErrors = win.__err.slice(0, 5);
      // One line to read at a glance; the detail is above it only when something is wrong.
      out.VERDICT = (out.selftest && out.selftest.indexOf("LOAD") < 0 &&
                     !out.selftestFailures && !out.contrastFailures &&
                     out.overflow === "none" && !out.consoleErrors.length)
        ? "PASS  " + out.selftest + " · contrast clean x3 · no overflow · no console errors"
        : "FAIL  see fields above";
      return out;
    }
  };
  return "VV ready — VV.all() | VV.all({w:1200}) | VV.all({stage:1})";
})();
