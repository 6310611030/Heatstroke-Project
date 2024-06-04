// Define a cache name
var CACHE_NAME = 'my-site-cache-v1';

// List of files to cache
var urlsToCache = [
  '/',
  '/static/user/css/style.css',
  // Add other URLs of static assets to cache here
];

// Install event: Cache all static assets
self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event: Serve from cache if available, otherwise fetch from network
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // Clone the request to make it safe to read and use
        var fetchRequest = event.request.clone();

        // Fetch the request from the network
        return fetch(fetchRequest).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response to make it safe to read and use
            var responseToCache = response.clone();

            // Open the cache
            caches.open(CACHE_NAME)
              .then(function(cache) {
                // Cache the response
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});

// Activate event: Delete old caches
self.addEventListener('activate', function(event) {
  var cacheWhitelist = ['my-site-cache-v1'];

  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
