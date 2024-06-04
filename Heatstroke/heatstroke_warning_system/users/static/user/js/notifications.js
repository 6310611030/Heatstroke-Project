var high_risk = document.currentScript.getAttribute('data-high-risk');
if ('serviceWorker' in navigator) {
   window.addEventListener('load', function() {
       navigator.serviceWorker.register('/static/user/js/service-worker.js')
       .then(function(registration) {
           console.log('Service Worker registered with scope:', registration.scope);

           // Request permission for notifications
           if ("Notification" in window) {
               Notification.requestPermission(permission => {
                   if (permission === "granted") {
                       console.log("Permission granted");

                       if (registration.active) {

                        if (high_risk === "High Risk") {
                            let options = {
                                body: "High Risk Alert! Please take necessary actions.",
                            }
                            registration.showNotification("High Risk Alert! ", options);
                        }
                    } else {
                           console.warn("No active service worker found!");
                       }
                   } else {
                       console.log("Permission is not granted");
                   }
               });
           } else {
               console.warn("Web Notification is not supported!");
           }
       })
       .catch(function(error) {
           console.error('Service Worker registration failed:', error);

           // Handle the case where service worker registration fails
           console.warn("Service worker is not supported or registration failed!");
       });
   });
} else {
   console.warn("Service worker is not supported!");
}
