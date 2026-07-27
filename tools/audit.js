/* Composited WCAG contrast audit for The Vault.
 *
 * Paste this whole file into the browser (javascript_tool) once. It installs window.VA.
 * Then call it PER THEME — one combined call sweeps too many elements and hits the 30s
 * JS timeout:
 *
 *     VA.run("dark")     VA.run("sepia")     VA.run("light")     VA.restore()
 *
 * Returns a terse {theme, checked, failed, fails:[...]} so the result costs ~20 tokens
 * instead of dumping every computed style through the conversation.
 *
 * This encodes three fixes for bugs that were in the AUDIT, not the app — each one cost
 * real debugging time. Do not "simplify" them away:
 *
 *   1. TRANSITIONS. .navbtn/.iconbtn/.nt animate on theme change. Reading getComputedStyle
 *      right after flipping the theme catches elements mid-transition still holding the old
 *      theme's colours -> ~300 phantom failures. We inject transition:none first.
 *   2. GRADIENTS. A walk-up-for-background cannot composite a linear-gradient. .goldbtn read
 *      as 1.06 but is black-on-gold-gradient and perfectly legible. We skip gradient-backed text.
 *   3. BLIND SPOTS. Only offsetParent-visible nodes get measured, so closed overlays and
 *      inactive state branches are never tested. A hardcoded #d4af37 hid in the daily-rite
 *      "complete" banner for several releases that way. We force every overlay open.
 */
(function () {
  var AA = 4.5, AA_LARGE = 3.0, MAX_REPORT = 12;

  function parse(c) {
    var m = /rgba?\(([^)]+)\)/.exec(c || "");
    if (!m) return null;
    var p = m[1].split(",").map(function (x) { return parseFloat(x); });
    return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1];
  }

  function over(fg, bg) {            // composite fg (with alpha) onto opaque bg
    var a = fg[3];
    return [fg[0] * a + bg[0] * (1 - a), fg[1] * a + bg[1] * (1 - a), fg[2] * a + bg[2] * (1 - a), 1];
  }

  function lum(c) {
    var v = c.slice(0, 3).map(function (x) {
      x /= 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  }

  function ratio(a, b) {
    var l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }

  // Walk up compositing every semi-transparent background until we hit an opaque one.
  // Returns null if any ancestor uses a gradient (fix #2 — we cannot composite those).
  function effBg(el) {
    var stack = [], n = el;
    while (n && n !== document.documentElement) {
      var cs = getComputedStyle(n);
      if (cs.backgroundImage && cs.backgroundImage !== "none") return null;
      var bg = parse(cs.backgroundColor);
      if (bg && bg[3] > 0) {
        stack.push(bg);
        if (bg[3] === 1) break;
      }
      n = n.parentElement;
    }
    var root = parse(getComputedStyle(document.documentElement).backgroundColor);
    var base = root && root[3] === 1 ? root : [0, 0, 0, 1];
    for (var i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return base;
  }

  function visible(el) {
    if (!el.offsetParent && getComputedStyle(el).position !== "fixed") return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  function ownText(el) {
    var t = "";
    for (var i = 0; i < el.childNodes.length; i++) {
      var n = el.childNodes[i];
      if (n.nodeType === 3) t += n.nodeValue;
    }
    return t.trim();
  }

  function sel(el) {
    return el.tagName.toLowerCase() +
      (el.id ? "#" + el.id : "") +
      (el.className && typeof el.className === "string"
        ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".") : "");
  }

  var killer = null;
  function killMotion() {                       // fix #1 — must run BEFORE any measurement
    if (killer) return;
    killer = document.createElement("style");
    killer.id = "va-killer";
    killer.textContent = "*,*::before,*::after{transition:none!important;animation:none!important}";
    document.head.appendChild(killer);
  }

  function scan(out, seen) {
    var els = document.body.querySelectorAll("*");
    var checked = 0;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var txt = ownText(el);
      if (!txt || !visible(el)) continue;
      var cs = getComputedStyle(el);
      if (cs.visibility === "hidden" || parseFloat(cs.opacity) < 0.15) continue;

      var bg = effBg(el);
      if (!bg) continue;                        // gradient-backed — skip, cannot composite
      var fgRaw = parse(cs.color);
      if (!fgRaw) continue;
      var fg = fgRaw[3] < 1 ? over(fgRaw, bg) : fgRaw;

      checked++;
      var size = parseFloat(cs.fontSize), weight = parseInt(cs.fontWeight, 10) || 400;
      var large = size >= 24 || (size >= 18.66 && weight >= 700);
      var r = ratio(fg, bg);
      if (r < (large ? AA_LARGE : AA)) {
        var s = sel(el);
        if (seen[s]) continue;                  // one report per selector, not per instance
        seen[s] = 1;
        out.push({ sel: s, r: +r.toFixed(2), need: large ? AA_LARGE : AA, text: txt.slice(0, 40) });
      }
    }
    return checked;
  }

  // fix #3 — force-open every overlay so closed surfaces get measured too.
  // Renderers are called when they exist; an overlay with stale content is still worth scanning.
  var RENDERERS = {
    hls: "renderJournal", ach: "renderAch", settings: "renderSettings", patch: "renderPatch",
    account: "renderAccount", progress: "renderProgress", queue: "renderQueue",
    addbook: "renderAddBook", search: "renderSearch", sit: "openSit", cards: "renderCards"
  };

  function sweepOverlays(out, seen) {
    var ovs = document.querySelectorAll(".overlay"), checked = 0;
    for (var i = 0; i < ovs.length; i++) {
      var o = ovs[i], was = o.classList.contains("on");
      if (!was) {
        var fn = RENDERERS[o.id];
        if (fn && typeof window[fn] === "function") { try { window[fn](); } catch (e) {} }
        o.classList.add("on");
      }
      try { checked += scan(out, seen); } catch (e) {}
      if (!was) o.classList.remove("on");
    }
    return checked;
  }

  var original = null;

  window.VA = {
    run: function (theme) {
      if (original === null) original = document.documentElement.dataset.theme || "";
      killMotion();
      document.documentElement.dataset.theme = theme;
      void document.documentElement.offsetHeight;            // force a synchronous reflow
      var out = [], seen = {};
      var checked = scan(out, seen) + sweepOverlays(out, seen);
      return {
        theme: theme, checked: checked, failed: out.length,
        fails: out.sort(function (a, b) { return a.r - b.r; }).slice(0, MAX_REPORT)
      };
    },
    restore: function () {
      if (original !== null) document.documentElement.dataset.theme = original;
      var k = document.getElementById("va-killer");
      if (k) k.remove();
      killer = null; original = null;
      return "restored";
    }
  };
  return "VA ready — VA.run('dark'|'sepia'|'light'), then VA.restore()";
})();
