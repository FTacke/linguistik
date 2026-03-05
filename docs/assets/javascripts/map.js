// docs/assets/javascripts/map.js

// --- Vollbild-Handling & Map für Herkunftssprachen ---
// Initialisiert nur, wenn die Seite ein entsprechendes data-map="herkunft" Container hat

function initHerkunftMap() {
  const herkunftContainer = document.querySelector('[data-map="herkunft"]');
  
  if (!herkunftContainer) {
    return; // Kein Container auf dieser Seite
  }

  // Verhindere doppelte Initialisierung
  if (window.MapUI && window.MapUI.isMapInitialized(herkunftContainer)) {
    return;
  }

  function toggleFullscreen() {
    const container = herkunftContainer;
    const btn = container.querySelector('#fullscreen-btn');
    container.classList.toggle('fullscreen');
    btn.innerHTML = container.classList.contains('fullscreen')
      ? '<span class="material-icons">fullscreen_exit</span>'
      : '<span class="material-icons">fullscreen</span>';
    if (window.herkunftMap) setTimeout(() => window.herkunftMap.invalidateSize(), 350);
  }

  // Expose toggle to global scope for the button onclick
  window.toggleFullscreen = toggleFullscreen;

  // --- Leaflet Map ---
  const mapEl = herkunftContainer.querySelector('#mapid');
  if (mapEl) {
    const map = L.map(mapEl).setView([45, 15], 3);
    window.herkunftMap = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    }).addTo(map);

    // Aktiviere UX-Funktionen (Popup-Schließen, Responsive Invalidation)
    if (window.MapUI) {
      window.MapUI.enablePopupCloseUX(map);
      window.MapUI.enableResponsiveInvalidation(map);
    }

    // Daten laden und Marker setzen
    fetch('../assets/data/herkunftssprachen.json')
      .then(r => r.json())
      .then(sprachen => {
        const bounds = L.latLngBounds([]);

        sprachen.forEach(eintrag => {
          (eintrag.koordinaten || []).forEach((coord, i) => {
            if (!coord || coord.length !== 2) return;
            
            const marker = L.circleMarker(coord, {
              color: eintrag.farbe,
              radius: 8,
              fillOpacity: 0.7,
              weight: 2
            }).addTo(map);

            const popupHtml = `
              <div class="popup-sprachenkarte">
                <span class="popup-title">${eintrag.sprache}</span><br>
                <span class="popup-familie">${eintrag.sprachfamilie}</span><br>
                <div class="popup-herkunft">${eintrag.herkunft?.[i] ?? ''}</div>
              </div>`;

            // Nutze MapUI für konsistentes Click-Popup-Verhalten
            if (window.MapUI) {
              window.MapUI.bindClickPopup(map, marker, popupHtml, 'corapan-popup');
            } else {
              // Fallback wenn MapUI nicht geladen
              marker.bindPopup(popupHtml);
            }

            bounds.extend(coord);
          });
        });

        if (bounds.isValid()) map.fitBounds(bounds.pad(0.1));
      })
      .catch(err => console.error('Fehler beim Laden der Herkunftssprachen-Daten:', err));

    // Markiere als initialisiert
    if (window.MapUI) {
      window.MapUI.markMapInitialized(herkunftContainer);
    }
  }
}

// Initialisiere bei DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHerkunftMap);
} else {
  initHerkunftMap();
}

// Material for MkDocs: Instant Navigation Support
if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initHerkunftMap();
  });
}
