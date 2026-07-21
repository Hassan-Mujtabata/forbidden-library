const CACHE = "vault-v39";
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
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// stale-while-revalidate: serve instantly from cache, refresh in the background
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET" || !e.request.url.startsWith(self.location.origin)) return;
  // pipeline progress + access settings must never be stale — always network, fall back to cache offline
  if (e.request.url.includes("status.json") || e.request.url.includes("access.json")) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }
  e.respondWith(
    caches.open(CACHE).then(async c => {
      const hit = await c.match(e.request, { ignoreSearch: true });
      const net = fetch(e.request).then(r => {
        if (r.ok) c.put(e.request, r.clone());
        return r;
      }).catch(() => hit);
      return hit || net;
    })
  );
});
