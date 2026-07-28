/* Composited WCAG contrast audit for The Vault.
 *
 * Paste this whole file into the browser (javascript_tool) once. It installs window.VA.
 * Then call it PER THEME — one combined call sweeps too many elements and hits the 30s
 * JS timeout:
 *
 *     VA.run("dark")     VA.run("sepia")     VA.run("light")     VA.restore()
 *
 * Returns a terse {theme, checked, failed, unmeasured, fails:[...]} so the result costs ~20
 * tokens instead of dumping every computed style through the conversation.
 *
 * ALWAYS read `unmeasured`. It lists overlays that rendered no text, meaning they were not
 * actually audited -- eplist and flow need a book/word-list argument, and review no-ops when
 * nothing is due. A "0 failures" run with a long unmeasured list is not a clean run.
 *
 * This encodes three fixes for bugs that were in the AUDIT, not the app — each one cost
 * real debugging time. Do not "simplify" them away:
 *
 *   1. TRANSITIONS. .navbtn/.iconbtn/.nt animate on theme change. Reading getComputedStyle
 *      right after flipping the theme catches elements mid-transition still holding the old
 *      theme's colours -> ~300 phantom failures. We inject transition:none first.
 *   2. GRADIENTS. A walk-up-for-background cannot composite a linear-gradient. .goldbtn read
 *      as 1.06 but is black-on-gold-gradient and perfectly legible. We skip text whose
 *      background IS a gradient -- but NOT text merely descended from one. body carries a
 *      decorative wash over an opaque colour, and skipping on that alone measured 0 elements
 *      across the whole app while cheerfully reporting "0 failures". See effBg.
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
  // Returns null only when a gradient genuinely IS the background (fix #2).
  //
  // The rule has to distinguish two very different cases, and getting this wrong silently
  // voids the entire audit:
  //   - .goldbtn: linear-gradient with a transparent background-color. The gradient is the
  //     only background there is, so the composite is unknowable -> skip.
  //   - body: a decorative 7%-alpha radial wash layered OVER an opaque rgb(10,12,18). Bailing
  //     here skips every element in the app, because everything inherits from body. Composite
  //     onto the opaque colour and accept the tiny error the wash introduces.
  function effBg(el) {
    var stack = [], n = el;
    while (n && n !== document.documentElement) {
      var cs = getComputedStyle(n);
      var bg = parse(cs.backgroundColor);
      var opaque = bg && bg[3] === 1;
      if (cs.backgroundImage && cs.backgroundImage !== "none" && !opaque) return null;
      if (bg && bg[3] > 0) {
        stack.push(bg);
        if (opaque) break;
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

  function dropKillers() {                      // a re-paste of this file orphans the old one,
    var k = document.querySelectorAll("#va-killer");   // which would freeze transitions for good
    for (var i = 0; i < k.length; i++) k[i].remove();
  }

  function killMotion() {                       // fix #1 — must run BEFORE any measurement
    if (killer) return;
    dropKillers();
    killer = document.createElement("style");
    killer.id = "va-killer";
    killer.textContent = "*,*::before,*::after{transition:none!important;animation:none!important}";
    document.head.appendChild(killer);
  }

  function scan(out, seen, root) {
    var els = (root || document.body).querySelectorAll("*");
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

  // Placeholder text is structurally invisible to the sweep above: it lives in a pseudo-element
  // with no node of its own, so querySelectorAll can never return it and every "0 failures" run
  // was silently ignoring it. All 14 placeholders in this app sat at the UA default grey
  // (#757575) -- 3.42:1 on sepia, 4.02:1 on dark, both below AA -- through every previous audit.
  // Ask for the ::placeholder computed style explicitly, and honour its opacity: Firefox dims
  // placeholders by default, so the colour alone overstates the real contrast.
  function scanPlaceholders(out, seen, root) {
    var els = (root || document.body).querySelectorAll("input[placeholder],textarea[placeholder]");
    var n = 0;
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (!visible(el)) continue;
      var bg = effBg(el);
      if (!bg) continue;
      var cs = getComputedStyle(el, "::placeholder");
      var fg = parse(cs.color);
      if (!fg) continue;
      var op = parseFloat(cs.opacity);
      if (!isNaN(op) && op < 1) fg = [fg[0], fg[1], fg[2], fg[3] * op];
      n++;
      var r = ratio(fg[3] < 1 ? over(fg, bg) : fg, bg);
      if (r < AA) {
        var s = sel(el) + "::placeholder";
        if (seen[s]) continue;
        seen[s] = 1;
        out.push({ sel: s, r: +r.toFixed(2), need: AA, text: (el.getAttribute("placeholder") || "").slice(0, 40) });
      }
    }
    return n;
  }

  function click(id) { var b = document.getElementById(id); if (b) b.click(); }

  function call(fn) {
    var a = [].slice.call(arguments, 1);
    if (typeof window[fn] === "function") { try { window[fn].apply(null, a); } catch (e) {} }
  }

  // fix #3 — force-open every overlay so closed surfaces get measured too.
  // Open by the real UI path where one exists: several overlays (achs, search, hls) are populated
  // by an inline onclick handler, NOT by a named render function, so clicking the button is the
  // only way to fill them. Guessing render-fn names silently yields an empty overlay.
  var OPENERS = {
    hls:      function () { click("btn-hl"); },
    achs:     function () { click("btn-ach"); },
    settings: function () { click("btn-settings"); },
    patches:  function () { click("btn-patch"); },
    search:   function () { click("btn-search"); },
    account:  function () { click("btn-account"); },
    progress: function () { call("renderProgress"); },
    queue:    function () { call("renderQueue"); },
    addbook:  function () { call("renderAddBook"); },
    sit:      function () { call("openSit"); },
    review:   function () { call("startReview"); },   // no-ops when nothing is due -> reported unmeasured
    booklanding: function () {
      // DATA is a top-level `const`, so it lives in the global LEXICAL scope and is NOT a
      // property of window -- window.DATA is undefined. Reference the binding directly.
      var d = (typeof DATA !== "undefined") ? DATA : null;
      if (!d || !d.books || !d.books.length) return;
      // Prefer a book flagged `partial`: its landing page renders everything a normal book
      // does PLUS the .bl-len.partial warning. Opening books[0] measured the common case only
      // and reported a clean sweep while never touching that label at all.
      var pick = d.books.filter(function (b) { return b.partial; })[0] || d.books[0];
      call("openBookLanding", pick.id);
    }
    // eplist and flow need a specific book / word list. Rather than fake them, they get
    // reported in `unmeasured` so a false clean is visible instead of silent.
  };

  function sweepOverlays(out, seen) {
    var ovs = document.querySelectorAll(".overlay"), checked = 0, unmeasured = [];
    for (var i = 0; i < ovs.length; i++) {
      var o = ovs[i], was = o.classList.contains("on");
      if (!was) {
        if (OPENERS[o.id]) { try { OPENERS[o.id](); } catch (e) {} }
        o.classList.add("on");
      }
      var n = 0, ph = 0;
      try { n = scan(out, seen, o); } catch (e) {}   // scoped to THIS overlay, not the whole body
      try { ph = scanPlaceholders(out, seen, o); } catch (e) {}
      if (!n) unmeasured.push(o.id);                 // judged on real text only: an overlay whose
      checked += n + ph;                             // only content is a placeholder is still empty
      if (!was) o.classList.remove("on");
    }
    return { checked: checked, unmeasured: unmeasured };
  }

  var original = null, hadTheme = false;

  // fix #4 — switch themes the way the APP does, not by poking the attribute.
  // Colours baked into inline styles at render time (the continue-card accent) only refresh
  // when refreshRoot() re-renders. Setting data-theme directly leaves them stale, and the
  // audit then reports a colour the user can never actually see -- 2.09 for a tag that is
  // really 5.1. Note S.theme must be the literal "dark", never "" : the app treats "" as
  // "follow the OS", which on a light-mode machine silently audits the wrong palette.
  function setTheme(t) {
    if (typeof S === "object" && S && typeof applyReadingPrefs === "function") {
      S.theme = t;
      applyReadingPrefs();
      if (typeof refreshRoot === "function") refreshRoot();
    } else {
      document.documentElement.dataset.theme = t;            // plain page / test fixture
    }
  }

  window.VA = {
    run: function (theme) {
      if (original === null) {
        hadTheme = (typeof S === "object" && S && "theme" in S);
        original = hadTheme ? S.theme : (document.documentElement.dataset.theme || "");
      }
      killMotion();
      setTheme(theme);
      void document.documentElement.offsetHeight;            // force a synchronous reflow
      var out = [], seen = {};
      var base = scan(out, seen) + scanPlaceholders(out, seen);
      var ov = sweepOverlays(out, seen);
      return {
        theme: theme, checked: base + ov.checked, failed: out.length,
        // overlays that rendered no measurable text -- these were NOT audited. A clean run
        // with a long unmeasured list is not a clean run; open those by hand and re-check.
        unmeasured: ov.unmeasured,
        fails: out.sort(function (a, b) { return a.r - b.r; }).slice(0, MAX_REPORT)
      };
    },
    restore: function () {
      if (original !== null) {
        if (hadTheme) setTheme(original);
        else document.documentElement.dataset.theme = original;
      }
      dropKillers();
      killer = null; original = null; hadTheme = false;
      return "restored";
    }
  };
  return "VA ready — VA.run('dark'|'sepia'|'light'), then VA.restore()";
})();
