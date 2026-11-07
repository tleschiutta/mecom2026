// Service worker: guarda la app para usarla sin conexión.
const CACHE = "mecom2026-2026-11-07-193551";
const SHELL = ["./", "index.html", "manifest.json", "icon-192.png", "icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return; // la planilla la maneja la página
  // Primero la red (para tomar versiones nuevas). Si no hay conexión, o la red tarda más de 3 s
  // (señal débil), se usa la copia guardada: la app nunca queda en blanco.
  const red = fetch(e.request).then(r => {
    if (r.ok) { const c = r.clone(); caches.open(CACHE).then(k => k.put(e.request, c)); }
    return r;
  });
  const guardada = () => caches.match(e.request, {ignoreSearch: true}).then(r => r || caches.match("index.html"));
  const espera = new Promise(res => setTimeout(res, 3000)).then(guardada);
  e.respondWith(
    Promise.race([red.catch(guardada), espera.then(r => r || red)])
      .then(r => r || red)
      .catch(guardada)
  );
  e.waitUntil(red.catch(() => {}));
});
