// Register Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/service-worker.js')
      .then(function(registration) {
        console.log('ServiceWorker registration successful:', registration.scope);
      })
      .catch(function(err) {
        console.log('ServiceWorker registration failed:', err);
      });
  });
}

// Install prompt
var deferredPrompt;
var installButton = document.getElementById('install-button');

window.addEventListener('beforeinstallprompt', function(e) {
  e.preventDefault();
  deferredPrompt = e;
  
  if (installButton) {
    installButton.style.display = 'block';
  } else {
    showInstallBanner();
  }
});

function showInstallBanner() {
  var banner = document.createElement('div');
  banner.id = 'install-banner';
  banner.style.cssText = 'position: fixed; bottom: 0; left: 0; right: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px; text-align: center; z-index: 9999; box-shadow: 0 -2px 10px rgba(0,0,0,0.2);';
  banner.innerHTML = '<p style="margin: 0 0 10px 0; font-weight: bold;">📱 Install Christian Conservative Platform</p><p style="margin: 0 0 10px 0; font-size: 14px;">Get quick access to faith-based content on your device!</p><button id="install-btn" style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 25px; font-weight: bold; cursor: pointer; margin-right: 10px;">Install App</button><button id="dismiss-btn" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid white; padding: 10px 20px; border-radius: 25px; cursor: pointer;">Maybe Later</button>';
  
  document.body.appendChild(banner);
  
  document.getElementById('install-btn').addEventListener('click', installApp);
  document.getElementById('dismiss-btn').addEventListener('click', function() {
    banner.remove();
  });
}

function installApp() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function(choiceResult) {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt');
      }
      deferredPrompt = null;
      var banner = document.getElementById('install-banner');
      if (banner) banner.remove();
    });
  }
}

window.addEventListener('appinstalled', function() {
  console.log('PWA was installed');
  var banner = document.getElementById('install-banner');
  if (banner) banner.remove();
});

// Push notification support
function requestNotificationPermission() {
  if ('Notification' in window && 'serviceWorker' in navigator) {
    Notification.requestPermission().then(function(permission) {
      if (permission === 'granted') {
        console.log('Notification permission granted');
        subscribeUserToPush();
      }
    });
  }
}

function subscribeUserToPush() {
  navigator.serviceWorker.ready.then(function(registration) {
    var subscribeOptions = {
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array('YOUR_PUBLIC_VAPID_KEY_HERE')
    };
    
    return registration.pushManager.subscribe(subscribeOptions);
  }).then(function(pushSubscription) {
    console.log('Push subscription:', JSON.stringify(pushSubscription));
  }).catch(function(err) {
    console.log('Failed to subscribe:', err);
  });
}

function urlBase64ToUint8Array(base64String) {
  var padding = '='.repeat((4 - base64String.length % 4) % 4);
  var base64 = (base64String + padding).replace(/\-/g, '+').replace(/_/g, '/');
  var rawData = window.atob(base64);
  var outputArray = new Uint8Array(rawData.length);
  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

// Check if running as PWA
function isPWA() {
  return window.matchMedia('(display-mode: standalone)').matches || 
         window.navigator.standalone === true;
}

if (isPWA()) {
  console.log('Running as PWA');
  document.body.classList.add('pwa-mode');
}
