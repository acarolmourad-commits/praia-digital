const CACHE_NAME = 'praia-digital-static-v2';
const HTML_CACHE = 'praia-digital-html-v2';

const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/shared.js',
  '/manifest.json',
  '/img/icons/icon-192x192.png',
  '/img/icons/icon-512x512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(STATIC_ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME && key !== HTML_CACHE)
          .map((key) => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  if (request.method !== 'GET') return;

  if (url.origin === self.location.origin) {
    const isHtml = request.headers.get('accept')?.includes('text/html');

    if (isHtml) {
      event.respondWith(
        fetch(request)
          .then((response) => {
            const clone = response.clone();
            caches.open(HTML_CACHE).then((cache) => cache.put(request, clone));
            return response;
          })
          .catch(() => caches.match(request).then((cached) => cached || caches.match('/index.html')))
      );
      return;
    }

    // Network-first for JS/CSS so fixes (e.g. shared.js nav dedup) reach
    // returning visitors immediately; fall back to cache when offline.
    const isScriptOrStyle = /\.(js|css)$/.test(url.pathname);
    if (isScriptOrStyle) {
      event.respondWith(
        fetch(request)
          .then((response) => {
            if (response && response.status === 200) {
              const clone = response.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
            }
            return response;
          })
          .catch(() => caches.match(request))
      );
      return;
    }

    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) return cached;
        return fetch(request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, clone));
          }
          return response;
        });
      })
    );
  }
});
