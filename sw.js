const CACHE = "vault-v137";
const ASSETS = ["./", "./index.html", "./content.enc", "./manifest.json", "./icon.svg",
  "./icon-192.png", "./icon-512.png", "./apple-touch-icon.png",
  // #89: precache access/status so the visibility rules and pipeline card survive offline (they're network-first below)
  "./access.json", "./status.json",
  // #90: precache the PDF reader so "add a book" works offline instead of throwing a raw load error
  "./pdf.min.js", "./pdf.worker.min.js"];

// On install, fetch every asset bypassing the HTTP cache ({cache:"reload"}) so a new
// version always precaches the freshest files (otherwise a stale content.enc can pin).
self.addEventListener("install", e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await Promise.all(ASSETS.map(async u => {
      try { const r = await fetch(u, { cache: "reload" }); if (r.ok) await c.put(u, r); } catch (_) {}
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", e => {
  e.waitUntil((async () => {
    // #170: do NOT drop the previous cache until this one actually holds the app shell.
    // install() skips any asset whose fetch failed (deliberately — one missing icon should not
    // abort the upgrade), so a flaky moment can leave the new cache without index.html. Deleting
    // the old cache at that point throws away the only working copy, and the next reload has
    // nothing to serve. That is how a version bump turns into a blank page.
    const c = await caches.open(CACHE);
    const shell = await c.match("./index.html", { ignoreSearch: true })
               || await c.match("./", { ignoreSearch: true });
    if (shell) {
      const keys = await caches.keys();
      await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    } else {
      // keep the old cache as the safety net and try once more to fill this one
      await Promise.all(ASSETS.map(async u => {
        try { const r = await fetch(u, { cache: "reload" }); if (r.ok) await c.put(u, r); } catch (_) {}
      }));
    }
    await self.clients.claim();
  })());
});

// #33: daily-rite reminder for installed PWAs (Chrome/Android). minInterval is a hint; the browser
// decides when to fire, and only for installed apps with notification permission.
self.addEventListener("periodicsync", e => {
  if (e.tag === "vault-rite") {
    e.waitUntil(self.registration.showNotification("The Vault", {
      body: "Your daily rite is waiting — learn one idea, sharpen another, and sit.",
      icon: "./icon-192.png", badge: "./icon-192.png", tag: "vault-rite", renotify: false
    }));
  }
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window" }).then(cs => cs.length ? cs[0].focus() : self.clients.openWindow("./")));
});

// stale-while-revalidate: serve instantly from cache, refresh in the background
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || !e.request.url.startsWith(self.location.origin)) return;
  // pipeline progress + access settings must never be stale — always network, fall back to cache offline
  if (e.request.url.includes("status.json") || e.request.url.includes("access.json")) {
    e.respondWith(fetch(e.request)
      .catch(() => caches.match(e.request))
      .then(r => r || new Response("{}", { status: 503, headers: { "Content-Type": "application/json" } })));
    return;
  }
  // #170 BLANK PAGE. respondWith() MUST resolve to a Response. The previous version ended in
  //     const net = fetch(req).catch(() => hit);  return hit || net;
  // so when nothing was cached AND the fetch rejected, `net` resolved to undefined — and
  // respondWith(undefined) does not fall back to the network, it fails the navigation. The whole
  // app renders as an empty white page with no error anywhere on it. That state is also
  // self-sustaining: every reload takes the same path.
  // Every branch below now returns a real Response, and a failed NAVIGATION falls back to the
  // cached app shell so a reload still boots with no network at all.
  e.respondWith((async () => {
    const c = await caches.open(CACHE);
    const hit = await c.match(e.request, { ignoreSearch: true });
    if (hit) {
      // refresh in the background, but never let that failure touch what we hand back
      e.waitUntil(fetch(e.request)
        .then(r => (r.ok ? c.put(e.request, r.clone()) : null))
        .catch(() => {}));
      return hit;
    }
    try {
      const r = await fetch(e.request);
      if (r.ok) c.put(e.request, r.clone());
      return r;
    } catch (_) {
      if (e.request.mode === "navigate") {
        // search EVERY cache, not just the current one — during an upgrade the only intact shell
        // may still be sitting in the previous version's cache
        const shell = await caches.match("./index.html", { ignoreSearch: true })
                   || await caches.match("./", { ignoreSearch: true });
        if (shell) return shell;
      }
      return new Response("offline", { status: 503, statusText: "offline" });
    }
  })());
});
