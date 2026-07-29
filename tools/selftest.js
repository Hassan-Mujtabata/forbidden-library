/* Logic self-test for The Vault.
 *
 * Paste into the browser once (javascript_tool), with the vault UNLOCKED, then:
 *
 *     VT.run()          // -> {passed, failed, ms, failures:[...]}
 *
 * WHY THIS EXISTS. tools/audit.js checks how the app LOOKS. Nothing checked how it THINKS, and
 * the bugs that actually shipped were all logic: a merge that resurrected un-marked chapters, a
 * guard that fired on every device without sync, a text repair that invented a letter. Each was
 * caught by hand, once, and then never checked again. These assertions are the ones I had to
 * reason through anyway -- written down so a later change that breaks them says so immediately.
 *
 * It mutates S (progress state) while running and restores the snapshot afterwards, even if an
 * assertion throws. It never calls save() mid-run, so nothing partial can reach localStorage or
 * sync; it saves once at the end, after the original state is back.
 *
 * Top-level `const` in the app lives in the global LEXICAL scope, not on window, so this file has
 * to be evaluated as global code (indirect eval) to see fold/sane/mergeState/DATA at all.
 */
(function () {
  var out = [], t0;

  function check(name, fn) {
    try {
      var r = fn();
      if (r === true) out.push({ name: name, ok: true });
      else out.push({ name: name, ok: false, detail: String(r) });
    } catch (e) {
      out.push({ name: name, ok: false, detail: "threw: " + (e && e.message || e) });
    }
  }

  // Report the actual values on failure -- "expected X, got Y" is the whole value of a suite like
  // this. A bare `false` would send the next reader straight back to the console.
  function is(actual, expected, label) {
    var a = JSON.stringify(actual), b = JSON.stringify(expected);
    return a === b ? true : (label || "") + " expected " + b + ", got " + a;
  }

  function st(o) { return JSON.parse(JSON.stringify(o)); }

  /* ---------------------------------------------------------------- fold() */

  function foldTests() {
    check("fold: strips accents", function () {
      return is(fold("Jhāna"), "jhana");
    });
    check("fold: preserves length (offsets index the ORIGINAL string)", function () {
      var s = "Viññāṇa — Ñāṇamoli’s Pāli";
      return fold(s).length === s.length ? true : "len " + fold(s).length + " vs " + s.length;
    });
    check("fold: idempotent", function () {
      return is(fold(fold("Jhāna")), fold("Jhāna"));
    });
    check("fold: a lone combining mark falls back rather than shortening", function () {
      var s = "a\u0336b";                      // combining long stroke with no precomposed form
      return fold(s).length === s.length ? true : "len " + fold(s).length + " vs " + s.length;
    });
    check("fold: substring offset lands on the accented original", function () {
      var p = "Entering the Jhānas is the point.", q = fold("jhanas");
      var i = fold(p).indexOf(q);
      if (i < 0) return "query not found";
      // This is the invariant the search snippet depends on: slicing the RAW paragraph at an
      // offset found in the FOLDED copy must return the same word, accents intact.
      return fold(p.slice(i, i + q.length)) === q ? true : "sliced " + JSON.stringify(p.slice(i, i + q.length));
    });
  }

  /* ---------------------------------------------------------------- sane() */

  function saneTests() {
    check("sane: strips control bytes", function () {
      return is(sane("a\u0000b\u0001c"), "abc");
    });
    check("sane: private-use ligature becomes Th, not nothing", function () {
      // Dropping it instead of mapping it is the bug that made "Then" read as "en".
      return is(sane("\ue053en he paused"), "Then he paused");
    });
    check("sane: all three PUA code points map", function () {
      return is(sane("\ue002e \ue04ee \ue053e"), "The The The");
    });
    check("sane: leaves ordinary prose untouched", function () {
      var s = "Ordinary — text, with “quotes” and jhāna.";
      return is(sane(s), s);
    });
    check("sane: esc() runs text through it", function () {
      return esc("x\u0000y") === "xy" ? true : "got " + JSON.stringify(esc("x\u0000y"));
    });
  }

  /* ------------------------------------------------------- read tombstones */

  function readTests() {
    check("tombstone: key/time round-trip", function () {
      var k = readKey("laws48", 7), t = k + "@" + 1730000000000;
      return tombKey(t) === k && tombAt(t) === 1730000000000
        ? true : "tombKey=" + tombKey(t) + " tombAt=" + tombAt(t);
    });
    check("tombstone: a legacy entry with no @ parses as time 0", function () {
      return tombKey("laws48|7") === "laws48|7" && tombAt("laws48|7") === 0 ? true : "parsed wrong";
    });
    check("markUnread: removes the chapter and records a timestamped tombstone", function () {
      S.read.laws48 = [0, 1, 2]; S.readDel = [];
      markUnread("laws48", [1]);
      if (S.read.laws48.indexOf(1) >= 0) return "chapter still marked read";
      if (S.readDel.length !== 1) return "expected 1 tombstone, got " + S.readDel.length;
      return tombAt(S.readDel[0]) > 0 ? true : "tombstone carries no timestamp";
    });
    check("markRead: lifts the tombstone, or the merge would delete it again", function () {
      S.read.laws48 = [0, 2]; S.readDel = ["laws48|1@" + Date.now()];
      markRead("laws48", [1]);
      return S.readDel.length === 0 && S.read.laws48.indexOf(1) >= 0
        ? true : "readDel=" + JSON.stringify(S.readDel);
    });
    check("markRead: never duplicates an already-read chapter", function () {
      S.read.laws48 = [0, 1]; S.readDel = [];
      markRead("laws48", [1]);
      return is(S.read.laws48.slice().sort(), [0, 1]);
    });
  }

  /* ---------------------------------------------------------- mergeState() */

  function mergeTests() {
    var NOW = Date.now();

    check("merge: plain union when nothing is tombstoned", function () {
      var a = { read: { laws48: [0, 1] }, _mtime: NOW };
      var b = { read: { laws48: [2] }, _mtime: NOW };
      return is(mergeState(a, b).read.laws48.slice().sort(function (x, y) { return x - y; }), [0, 1, 2]);
    });

    check("merge: a stale device does NOT resurrect an un-marked chapter", function () {
      var a = { read: { laws48: [0, 2] }, readDel: ["laws48|1@" + NOW], _mtime: NOW };
      var b = { read: { laws48: [0, 1, 2] }, readDel: [], _mtime: NOW - 60000 };
      return mergeState(a, b).read.laws48.indexOf(1) < 0 ? true : "chapter 1 came back";
    });

    check("merge: that same stale device keeps its OWN unrelated progress", function () {
      // The bug this pins down: tombstoning the chapters an undo touched must not also delete
      // chapters another device genuinely read.
      var a = { read: { laws48: [0, 2] }, readDel: ["laws48|1@" + NOW], _mtime: NOW };
      var b = { read: { laws48: [0, 1, 2, 50] }, readDel: [], _mtime: NOW - 60000 };
      return mergeState(a, b).read.laws48.indexOf(50) >= 0 ? true : "chapter 50 was wrongly dropped";
    });

    check("merge: a device that read it AFTER the un-mark wins", function () {
      var a = { read: { laws48: [0, 2] }, readDel: ["laws48|1@" + NOW], _mtime: NOW };
      var b = { read: { laws48: [1] }, readDel: [], _mtime: NOW + 60000 };
      return mergeState(a, b).read.laws48.indexOf(1) >= 0 ? true : "later real progress was lost";
    });

    check("merge: books present on only one side survive", function () {
      var a = { read: { laws48: [0] }, _mtime: NOW };
      var b = { read: { bliss: [3] }, _mtime: NOW };
      var m = mergeState(a, b);
      return m.read.laws48 && m.read.bliss ? true : "lost a book: " + JSON.stringify(m.read);
    });

    check("merge: missing read/readDel fields don't throw", function () {
      var m = mergeState({ _mtime: NOW }, { _mtime: NOW });
      return m && typeof m.read === "object" ? true : "no read map produced";
    });

    check("merge: highlight tombstones still respected (pre-existing behaviour)", function () {
      var h = { b: "laws48", e: 1, t: "kept" }, g = { b: "laws48", e: 2, t: "deleted" };
      var a = { hl: [h], hlDel: [hlKey(g)], _mtime: NOW };
      var b = { hl: [h, g], hlDel: [], _mtime: NOW };
      var m = mergeState(a, b);
      return m.hl.length === 1 && m.hl[0].t === "kept" ? true : "hl=" + JSON.stringify(m.hl);
    });

    check("merge: favourites are unioned", function () {
      var m = mergeState({ faves: ["a"], _mtime: NOW }, { faves: ["b"], _mtime: NOW });
      return m.faves.indexOf("a") >= 0 && m.faves.indexOf("b") >= 0 ? true : JSON.stringify(m.faves);
    });

    // THE CLASS GUARD. mergeState carries only the fields it names, so any field added to S later
    // is silently dropped the first time another device syncs. Five had piled up before anyone
    // noticed — forged lessons, gauntlet scores, council sittings, followed hooks, dispatch state.
    // ADD NEW S FIELDS TO THIS FIXTURE when you add them to the app; that is what makes this fail.
    check("merge: no field from the other device is silently dropped", function () {
      var b = { _mtime: 2, xp: 7, bestStreak: 3, rvN: 2, ritesN: 1,
                streak: { count: 2, day: "2026-07-29" },
                faves: ["laws48"], hl: [{ b: "laws48", e: 1, t: "a kept highlight" }], hlDel: [],
                vocab: [{ t: "jhana" }], read: { laws48: [3] }, readDel: [],
                node: { n1: { quizBest: 2 } },
                forged: [{ id: "fg1", at: 9, title: "Forged lesson" }],
                council: [{ q: "why do I procrastinate", at: 9, seats: [] }],
                gauntlet: { best: 4, played: 2, streak: 1 },
                hookSeen: ["laws48|1|something"], dispatchSeen: "2026-07-29" };
      var m = mergeState({ _mtime: 1 }, b);
      var dropped = Object.keys(b).filter(function (k) {
        if (k === "_mtime") return false;
        var v = m[k];
        if (v === undefined || v === null) return true;
        if (Array.isArray(v)) return b[k].length > 0 && v.length === 0;
        if (typeof v === "object") return Object.keys(b[k]).length > 0 && Object.keys(v).length === 0;
        return false;
      });
      return dropped.length ? "dropped from sync: " + dropped.join(", ") : true;
    });

    check("merge: forged lessons from both devices are kept, newest first", function () {
      var m = mergeState({ forged: [{ id: "x", at: 1 }], _mtime: 1 },
                         { forged: [{ id: "y", at: 2 }], _mtime: 2 });
      return m.forged.length === 2 && m.forged[0].id === "y"
        ? true : "got " + JSON.stringify(m.forged.map(function (f) { return f.id; }));
    });
    check("merge: a forged lesson is never duplicated by its own id", function () {
      var n = { id: "same", at: 5 };
      return mergeState({ forged: [n], _mtime: 1 }, { forged: [n], _mtime: 2 }).forged.length === 1
        ? true : "duplicated";
    });
    check("merge: the gauntlet keeps the better score, not the newer one", function () {
      var m = mergeState({ gauntlet: { best: 5, played: 9 }, _mtime: 2 },
                         { gauntlet: { best: 2, played: 1 }, _mtime: 1 });
      return m.gauntlet.best === 5 && m.gauntlet.played === 9
        ? true : "got " + JSON.stringify(m.gauntlet);
    });

    check("merge: xp takes the higher value, never the sum", function () {
      return is(mergeState({ xp: 500, _mtime: NOW }, { xp: 700, _mtime: NOW }).xp, 700);
    });

    // Pinning an accepted trade-off rather than a nice property. Once a chapter IS tombstoned,
    // an older device's claim on it loses -- including chapters it genuinely read. That is why
    // the mass "mark all read" undo must not tombstone unless the change already escaped the
    // device (see pushEscaped): the protection lives in the caller, not here.
    check("merge: a tombstoned chapter beats an older device, by design", function () {
      var a = { read: { laws48: [0] }, readDel: ["laws48|50@" + NOW], _mtime: NOW };
      var b = { read: { laws48: [0, 50] }, readDel: [], _mtime: NOW - 60000 };
      return mergeState(a, b).read.laws48.indexOf(50) < 0
        ? true : "expected the tombstone to win over the stale claim";
    });
  }

  /* ------------------------------------------------- when a change has escaped */

  function pushTests() {
    var token = localStorage.getItem("vault_gh"), wasSync = _syncOn, wasT = _pushT;
    try {
      check("canPush: false with sync on but no token", function () {
        _syncOn = true; localStorage.removeItem("vault_gh");
        return canPush() === false ? true : "canPush() was true without a token";
      });
      check("canPush: true only with sync on AND a token", function () {
        _syncOn = true; localStorage.setItem("vault_gh", "x");
        return canPush() === true ? true : "canPush() was false with both present";
      });
      check("canPush: false when sync is off", function () {
        _syncOn = false; localStorage.setItem("vault_gh", "x");
        return canPush() === false ? true : "canPush() ignored sync being off";
      });
      // The bug this pins: an unsynced device rests at _pushT === null forever, so treating that
      // as "already pushed" made every undo tombstone hundreds of chapters for no reason.
      // The exact configuration that shipped broken: sync flagged on, no token, so no push is
      // ever scheduled and _pushT rests at null forever. Testing this with _syncOn=false instead
      // passes under the buggy predicate too, and pins nothing.
      check("pushEscaped: false when sync is on but has no token and nothing is pending", function () {
        _syncOn = true; localStorage.removeItem("vault_gh"); _pushT = null;
        return pushEscaped() === false ? true : "a device that cannot push claimed its change had escaped";
      });
      check("pushEscaped: false when sync is off entirely", function () {
        _syncOn = false; localStorage.removeItem("vault_gh"); _pushT = null;
        return pushEscaped() === false ? true : "sync off still claimed the change had escaped";
      });
      check("pushEscaped: false while a push is still pending", function () {
        _syncOn = true; localStorage.setItem("vault_gh", "x"); _pushT = 1;
        return pushEscaped() === false ? true : "claimed escaped while still coalescing";
      });
      check("pushEscaped: true once the pending push has fired", function () {
        _syncOn = true; localStorage.setItem("vault_gh", "x"); _pushT = null;
        return pushEscaped() === true ? true : "missed a change that had already gone out";
      });
    } finally {
      _syncOn = wasSync; _pushT = wasT;
      if (token === null) localStorage.removeItem("vault_gh"); else localStorage.setItem("vault_gh", token);
    }
  }

  /* ------------------------------------------------- search index alignment */

  function indexTests() {
    check("epFold: folded copy lines up with the raw paragraphs", function () {
      // Sampled, not exhaustive: folding all 2,716 episodes here would populate the cache for the
      // whole library and make the suite pay for memory the app has not asked for yet.
      var bad = [], n = 0;
      for (var i = 0; i < DATA.books.length; i++) {
        var eps = DATA.books[i].episodes;
        for (var j = 0; j < eps.length; j += 17) {
          var f = epFold(eps[j]); n++;
          if (f.length !== eps[j].p.length) { bad.push(DATA.books[i].id + "/" + j + " count"); continue; }
          for (var k = 0; k < f.length; k++)
            if (f[k].length !== eps[j].p[k].length) { bad.push(DATA.books[i].id + "/" + j + "/" + k); break; }
        }
      }
      return bad.length ? bad.length + " misaligned (" + bad.slice(0, 3).join(", ") + ") of " + n
        : true;
    });

    check("nodeFold: folded copy lines up with nodeHay", function () {
      var bad = [];
      for (var i = 0; i < DATA.nodes.length; i++) {
        var nd = DATA.nodes[i], hay = nodeHay(nd), f = nodeFold(nd);
        if (hay.length !== f.length) { bad.push(nd.id + " count"); continue; }
        for (var k = 0; k < hay.length; k++)
          if (hay[k].length !== f[k].length) { bad.push(nd.id + "/" + k); break; }
      }
      return bad.length ? bad.length + " misaligned: " + bad.slice(0, 3).join(", ") : true;
    });

    check("library text carries no unprintable code points", function () {
      var RE = new RegExp("[\\u0000-\\u0008\\u000b\\u000c\\u000e-\\u001f\\u007f-\\u009f" +
        "\\ue000-\\uf8ff\\ufb00-\\ufb06]");
      if (!RE.test("a\u0000b") || RE.test("clean text")) return "the probe regex itself is wrong";
      var hits = [];
      for (var i = 0; i < DATA.books.length; i++) {
        var eps = DATA.books[i].episodes;
        for (var j = 0; j < eps.length && hits.length < 3; j++)
          for (var k = 0; k < eps[j].p.length; k++)
            if (RE.test(eps[j].p[k])) { hits.push(DATA.books[i].id + "/" + j); break; }
      }
      return hits.length ? "damaged text in " + hits.join(", ") : true;
    });
  }

  /* -------------------------------------------------------------- formatting */

  function fmtTests() {
    check("fmtDur: hours and minutes", function () { return is(fmtDur(1027), "17h 7m"); });
    check("fmtDur: whole hours drop the minutes", function () { return is(fmtDur(120), "2h"); });
    check("fmtDur: under an hour stays in minutes", function () { return is(fmtDur(59), "59 min"); });
    check("fmtWords: thousands", function () { return is(fmtWords(235156), "235k words"); });
    check("bookWords: cache agrees with a fresh count", function () {
      var b = DATA.books[0];
      var fresh = b.episodes.reduce(function (n, ep) { return n + epWords(ep); }, 0);
      return is(bookWords(b), fresh);
    });
  }

  /* -------------------------------------------------------- lure / hooks */

  function hookTests() {
    check("parseHooks: reads '<n> :: <hook>' and maps back to the right episode", function () {
      var picks = [{ e: 4, text: "a" }, { e: 91, text: "b" }];
      var got = parseHooks("1 :: Power is taken, never given away quietly.\n2 :: The mind wanders because it is unpractised.", picks);
      if (got.length !== 2) return "parsed " + got.length + " of 2";
      return got[0].e === 4 && got[1].e === 91 ? true : "episodes " + got[0].e + "," + got[1].e;
    });
    check("parseHooks: drops malformed lines rather than showing them", function () {
      // A half-parsed lure on the home screen reads as a broken app, so anything odd is dropped.
      var got = parseHooks("here is some preamble\n1 :: A genuinely arresting claim about power.\n99 :: out of range\nno number here", [{ e: 2, text: "a" }]);
      return got.length === 1 ? true : "kept " + got.length + ": " + JSON.stringify(got);
    });
    check("parseHooks: rejects a hook citing a passage that was never sent", function () {
      return parseHooks("7 :: invented from nowhere at all", [{ e: 1, text: "a" }]).length === 0
        ? true : "accepted a hook for a passage index that does not exist";
    });
    check("parseHooks: de-duplicates repeats", function () {
      var p = [{ e: 1, text: "a" }, { e: 2, text: "b" }];
      return parseHooks("1 :: The very same arresting line here.\n2 :: The very same arresting line here.", p).length === 1
        ? true : "duplicate hook kept";
    });
    check("hookSample: spreads across the whole book, not just the opening", function () {
      var b = DATA.books.reduce(function (a, x) { return x.episodes.length > a.episodes.length ? x : a; });
      var s = hookSample(b, 8);
      if (s.length < 2) return "only " + s.length + " samples";
      var last = s[s.length - 1].e;
      return last > b.episodes.length / 2 ? true : "last sample at episode " + last + " of " + b.episodes.length;
    });
    // The whole point of the daily refresh. If hookSample ever goes back to being deterministic —
    // "take the longest paragraph of every nth episode" — then every refresh re-sends the same
    // pages, the model returns the same five facts, and the library is static again while still
    // spending quota to look busy. This is the assertion that catches that.
    check("hookSample: a different day reads different pages", function () {
      var b = DATA.books.reduce(function (a, x) { return x.episodes.length > a.episodes.length ? x : a; });
      var d1 = hookSample(b, 8, 1001).map(function (p) { return p.e; });
      var d2 = hookSample(b, 8, 2002).map(function (p) { return p.e; });
      if (!d1.length || !d2.length) return "no samples produced";
      var same = d1.filter(function (e) { return d2.indexOf(e) >= 0; }).length;
      return same < d1.length ? true : "both days sampled identical episodes: " + d1.join(",");
    });
    check("hookSample: the same day is stable, so the shelf doesn't churn on every render", function () {
      var b = DATA.books[0];
      var a1 = hookSample(b, 6, 777).map(function (p) { return p.e + ":" + p.text.slice(0, 12); }).join("|");
      var a2 = hookSample(b, 6, 777).map(function (p) { return p.e + ":" + p.text.slice(0, 12); }).join("|");
      return a1 === a2 ? true : "same seed produced different passages";
    });
    check("hookId: stable for the same hook, distinct across books", function () {
      var h = { e: 3, t: "Play the fool to hide dangerous ambitions." };
      return hookId("laws48", h) === hookId("laws48", h) && hookId("laws48", h) !== hookId("atomic", h)
        ? true : "ids collided or drifted";
    });
    check("hooks live outside S, so sync never carries them", function () {
      return S.hooks === undefined ? true : "hooks leaked into synced state";
    });
  }

  /* ------------------------------------------------------------- gauntlet */

  function gauntletTests() {
    var Q = "Q: What is the core claim?\nA) alpha\nB) bravo\nC) charlie\nD) delta\nANSWER: B";
    check("parseQuestion: reads a well-formed question", function () {
      var q = parseQuestion(Q);
      return q && q.opts.length === 4 && q.opts.indexOf("bravo") >= 0 ? true : "got " + JSON.stringify(q);
    });
    check("parseQuestion: the correct answer survives the shuffle", function () {
      // The shuffle reorders options, so `a` must be recomputed — if it kept pointing at the old
      // index the game would mark right answers wrong, which is worse than no game at all.
      for (var i = 0; i < 50; i++) {
        var q = parseQuestion(Q);
        if (!q || q.opts[q.a] !== "bravo") return "run " + i + " marked '" + (q && q.opts[q.a]) + "' as correct";
      }
      return true;
    });
    check("parseQuestion: answer position is not always the same slot", function () {
      // Models put the correct option in B with startling regularity — a real five-book run came
      // back B,B,B,B, which makes the game "always press B". The shuffle is what stops that.
      var seen = {};
      for (var i = 0; i < 120; i++) { var q = parseQuestion(Q); if (q) seen[q.a] = 1; }
      return Object.keys(seen).length >= 3 ? true : "answer only ever landed in " + Object.keys(seen).length + " slot(s)";
    });
    check("parseQuestion: rejects a missing ANSWER line", function () {
      return parseQuestion("Q: x\nA) a\nB) b\nC) c\nD) d") === null ? true : "accepted a question with no answer";
    });
    check("parseQuestion: rejects duplicate options", function () {
      return parseQuestion("Q: x\nA) same\nB) same\nC) c\nD) d\nANSWER: A") === null ? true : "accepted duplicate options";
    });
    check("parseQuestion: rejects a question missing options", function () {
      return parseQuestion("Q: x\nA) a\nB) b\nANSWER: A") === null ? true : "accepted a two-option question";
    });
  }

  /* ----------------------------------------------------- retrieval matching */

  function matchTests() {
    // These are the exact false hits that shipped: a lesson about holding your TEMPER cited
    // Thinking, Fast and Slow on "barometric TEMPERature", because the matcher was a substring test.
    check("hasWord: 'temper' does not match 'temperature'", function () {
      return hasWord("much as daily temperature or barometric pressure", "temper") === false
        ? true : "still matching inside a longer word";
    });
    check("hasWord: 'hold' does not match 'household'", function () {
      return hasWord("the household accounts", "hold") === false ? true : "matched inside household";
    });
    check("hasWord: 'power' does not match 'powerfully'", function () {
      return hasWord("a powerfully built man", "power") === false ? true : "matched inside powerfully";
    });
    check("hasWord: still matches the word itself", function () {
      return hasWord("if your opponent is of a hot temper", "temper") === true ? true : "lost a real hit";
    });
    check("hasWord: still matches a short inflection", function () {
      // Demanding an exact word would lose most real hits, so up to two trailing letters are fine.
      return hasWord("he tempers his speech", "temper") && hasWord("she held and folded", "fold")
        ? true : "rejected a legitimate inflection";
    });
    check("hasWord: matches at the very start of the text", function () {
      return hasWord("temper is a signal", "temper") === true ? true : "missed a match at index 0";
    });
    check("parseQuizBlock: reads several questions from one reply", function () {
      // Options must be >1 char — parseQuestion drops single letters as malformed, which is why
      // this fixture spells them out rather than using a/b/c/d.
      var t = "Q: First question?\nA) alpha\nB) bravo\nC) charlie\nD) delta\nANSWER: A\n\n" +
              "Q: Second question?\nA) echo\nB) foxtrot\nC) golf\nD) hotel\nANSWER: C";
      var got = parseQuizBlock(t);
      return got.length === 2 ? true : "parsed " + got.length + " of 2";
    });
  }

  /* ------------------------------------------------------ library integrity */

  function libraryTests() {
    check("every book flagged partial carries a reason string", function () {
      var bad = DATA.books.filter(function (b) { return b.partial && !String(b.partial).trim(); });
      return bad.length ? bad.length + " partial books with an empty reason" : true;
    });
    check("no episode is empty", function () {
      var bad = [];
      for (var i = 0; i < DATA.books.length; i++)
        for (var j = 0; j < DATA.books[i].episodes.length; j++)
          if (!DATA.books[i].episodes[j].p.length) bad.push(DATA.books[i].id + "/" + j);
      return bad.length ? bad.length + " empty: " + bad.slice(0, 3).join(", ") : true;
    });
    check("every highlight points at a book and episode that exist", function () {
      var bad = (S.hl || []).filter(function (h) {
        if (h.n) return false;                                  // Path highlights key off node id
        var b = bookById(h.b);
        return !b || !(h.e >= 0 && h.e < b.episodes.length);
      });
      return bad.length ? bad.length + " dangling highlight(s)" : true;
    });
  }

  /* ------------------------------------------------------- the top bar (#127)
   * The phone layout broke because the icon row grew one button at a time, over three
   * releases, and nothing anywhere knew how wide a phone is. These are width-independent
   * on purpose -- they hold even when the suite runs in a 1200px pane, which is the only
   * place it ever actually runs.
   */
  function chromeTests() {
    var icons = function () {
      return [].slice.call(document.querySelectorAll("#topbar .iconrow .iconbtn"))
        .filter(function (b) { return b.id !== "btn-menu"; });
    };

    check("topbar: the phone bar still fits on a phone", function () {
      // Deliberately NOT icons(): that drops btn-menu, and ☰ takes up exactly as much room as
      // anything else. Written the other way first, this measured 3 buttons where the bar had 4
      // and sailed straight through a mutation that added a fifth.
      var keep = [].slice.call(document.querySelectorAll("#topbar .iconrow .iconbtn.keep"));
      // 360px is the narrowest phone worth supporting; 11px of padding each side leaves 338.
      // Buttons are pinned to a 44px tap target with a 4px gap, and the brand eats ~105px.
      var need = keep.length * 44 + Math.max(0, keep.length - 1) * 4 + 105;
      return need <= 338 ? true :
        keep.length + " .keep buttons need " + need + "px beside the brand, a 360px phone has 338. " +
        "Move one into the ☰ menu -- do not shrink the tap target.";
    });

    check("topbar: every icon is reachable on a phone (bar or menu)", function () {
      if (typeof renderMenu !== "function") return "renderMenu is gone";
      renderMenu();
      var listed = {};
      [].slice.call(document.querySelectorAll("#menu-body .mrow")).forEach(function (r) {
        listed[r.dataset.go] = 1;
      });
      var lost = icons().filter(function (b) {
        // an icon hidden for this device (non-admin, no face unlock) is not lost, it is absent
        return b.style.display !== "none" && !b.classList.contains("keep") && !listed[b.id];
      }).map(function (b) { return b.id; });
      return lost.length ? "off-screen on a phone and not in the menu: " + lost.join(", ") : true;
    });

    check("topbar: every menu row points at a live button", function () {
      renderMenu();
      var dead = [].slice.call(document.querySelectorAll("#menu-body .mrow")).filter(function (r) {
        var b = document.getElementById(r.dataset.go);
        return !b || typeof b.onclick !== "function";
      }).map(function (r) { return r.dataset.go; });
      return dead.length ? "menu row wired to nothing: " + dead.join(", ") : true;
    });

    check("topbar: every icon's title carries a description for the menu", function () {
      var bare = icons().filter(function (b) {
        return (b.title || "").indexOf(" — ") < 0;      // em dash, the menu splits on it
      }).map(function (b) { return b.id; });
      return bare.length ? "title needs 'Name — what it does': " + bare.join(", ") : true;
    });
  }

  window.VT = {
    run: function () {
      out = []; t0 = performance.now();
      var snap = st(S);                       // progress state is real data -- never leave it edited
      try {
        foldTests(); saneTests(); readTests(); mergeTests(); pushTests();
        indexTests(); fmtTests(); hookTests(); gauntletTests(); matchTests(); libraryTests();
        chromeTests();
      } finally {
        S = snap;
        if (typeof save === "function") save();
      }
      var fails = out.filter(function (r) { return !r.ok; });
      return {
        passed: out.length - fails.length,
        failed: fails.length,
        ms: Math.round(performance.now() - t0),
        failures: fails.map(function (f) { return f.name + " -- " + f.detail; })
      };
    }
  };
  return "VT ready -- VT.run()";
})();
