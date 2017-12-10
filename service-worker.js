var cacheName = 'RaghavaDhanyaCache';
var filesToCache = [
  '/',
  '/index.html',
  '/js/zepto.min.js',
  '/js/index.js',
  '/css/style.css',
  '/images/icon.png',
  '/images/icon_512.png',
  '/images/2_w_c.jpg',
  '/images/fb.svg',
  '/images/git.svg',
  '/images/link.svg',
  '/images/twitter.svg',
  '/images/overflow.svg'
];
self.addEventListener('install', function(e) {
  console.log('[ServiceWorker] Install');
  e.waitUntil(
    caches.open(cacheName).then(function(cache) {
      console.log('[ServiceWorker] Caching app shell');
      return cache.addAll(filesToCache);
    })
  );
});
self.addEventListener('activate', function(e) {
  console.log('[ServiceWorker] Activate');
  e.waitUntil(
    caches.keys().then(function(keyList) {
      return Promise.all(keyList.map(function(key) {
        if (key !== cacheName) {
          console.log('[ServiceWorker] Removing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});
self.addEventListener('fetch', function(e) {
  console.log('[Service Worker] Fetch', e.request.url);
    e.respondWith(
      caches.match(e.request).then(function(response) {
        return response || fetch(e.request);
      })
    );
});