const CACHE_NAME = 'my-pwa-cache-v1';
const urlsToCache = [
    // '/',
    // '/static/css/styles.css',
    // '/static/js/scripts.js',
    '/static/icons/icon_192x192.png',
    '/static/icons/icon_360x360.png',
    '/login/' // A custom offline page
];

// Install Service Worker and Cache Files
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

// Intercept Network Requests
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            // Serve cached response if found, else fetch from the network
            return response || fetch(event.request);
        })
    );
});

// Update Service Worker
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
