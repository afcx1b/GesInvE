if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then((registration) => {
        console.log('Service Worker registrado con éxito:', registration);
      })
      .catch((error) => {
        console.log('Error al registrar el Service Worker:', error);
      });
  }

  const CACHE_NAME = 'GESINV-v1';
  const ASSETS = [
    '/',
    '/static/css/styles.css',
    '/static/js/app.js',
    '/static/img/logo.png'
  ];
  
  self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then((cache) => cache.addAll(ASSETS))
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request)
        .then((response) => response || fetch(event.request))
    );
  });

  let deferredPrompt;
window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredPrompt = event;
  mostrarBotonInstalacion();
});

function mostrarBotonInstalacion() {
  const botonInstalar = document.getElementById('instalar-app');
  botonInstalar.style.display = 'block';
  botonInstalar.addEventListener('click', instalarApp);
}

function instalarApp() {
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then((choiceResult) => {
    if (choiceResult.outcome === 'accepted') {
      console.log('App instalada');
    }
    deferredPrompt = null;
  });
}
if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition((position) => {
      console.log('Latitud:', position.coords.latitude);
      console.log('Longitud:', position.coords.longitude);
    });
  }
  