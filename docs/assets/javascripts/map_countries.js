// docs/assets/javascripts/map_countries.js

// --- Vollbild-Handling & Map für Variation Countries ---
// Initialisiert nur, wenn die Seite ein entsprechendes data-map="variation" Container hat

// Vollbild-Handling für die Variation-Map (eigener Name, um Konflikte zu vermeiden)
function toggleFullscreenVariation() {
  const container = document.getElementById('map-container');
  if (!container) return;
  const btn = document.getElementById('fullscreen-btn');
  container.classList.toggle('fullscreen');
  btn.innerHTML = container.classList.contains('fullscreen')
    ? '<span class="material-icons">fullscreen_exit</span>'
    : '<span class="material-icons">fullscreen</span>';
  if (window.variationMap) {
    setTimeout(() => window.variationMap.invalidateSize(), 350);
  }
}

// Expose to global scope
window.toggleFullscreenVariation = toggleFullscreenVariation;

function initVariationMap() {
  const container = document.getElementById('map-container');
  
  if (!container || !container.hasAttribute('data-map') || container.getAttribute('data-map') !== 'variation') {
    return; // Kein passender Container auf dieser Seite
  }

  // Verhindere doppelte Initialisierung
  if (window.MapUI && window.MapUI.isMapInitialized(container)) {
    return;
  }

  const mapEl = document.getElementById('mapid');
  if (!mapEl) {
    console.error('Map container #mapid not found');
    return;
  }

  // --- Leaflet Map ---
  const variationMap = L.map(mapEl);
  
  // Setze initiale Ansicht abhängig von der Bildschirmbreite
  const isMobile = window.MapUI ? window.MapUI.isMobileViewport() : window.matchMedia('(max-width: 599px)').matches;
  if (isMobile) {
    // Mobile: zentriere stärker auf Zentral- und Südamerika
    variationMap.setView([-10, -65], 3);
  } else {
    // Desktop/Tablet: breite Atlantik-Übersicht (Amerika + Europa)
    variationMap.setView([20, -40], 2);
  }
  
  window.variationMap = variationMap;

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
  }).addTo(variationMap);

  // Aktiviere UX-Funktionen (Popup-Schließen, Responsive Invalidation)
  if (window.MapUI) {
    window.MapUI.enablePopupCloseUX(variationMap);
    window.MapUI.enableResponsiveInvalidation(variationMap);
  }

  // Daten laden und Marker setzen
  const base = window.ZENSICAL_BASE_PATH || "/";
  fetch(base + 'assets/data/countries.json')
    .then(r => r.json())
    .then(laender => {
      const bounds = L.latLngBounds([]);

      // Vorbereitung: max GDN finden für Skalierung
      const gdns = laender.map(l => Number(l.GDN || 0)).filter(n => !isNaN(n) && n > 0);
      const maxGdn = gdns.length ? Math.max(...gdns) : 1;

      // LayerGroup für Marker
      const markerLayer = L.layerGroup().addTo(variationMap);

      laender.forEach(eintrag => {
        // Länder können eine einzelne Koordinate [lat,lng] oder mehrere Koordinaten [[lat,lng], ...] enthalten
        const raw = eintrag.Koordinaten;
        const coords = Array.isArray(raw) && raw.length && typeof raw[0] === 'number' ? [raw] : (raw || []);

        coords.forEach((coord, i) => {
          if (!coord || coord.length !== 2) return; // skip invalid

          // Radius nach GDN (quadratische Skalierung für bessere Visualisierung)
          const gdn = Number(eintrag.GDN) || 0;
          const radius = gdn > 0 ? Math.max(4, 4 + 24 * Math.sqrt(gdn / maxGdn)) : 6;

          // Farbe nach Anteil_GDN (dunkleres Rot bei höherem Anteil)
          const anteil = Number(eintrag.Anteil_GDN) || 0; // percent
          const lightness = Math.max(30, 70 - anteil * 1.2); // 70% -> light, 30% -> dark
          const color = `hsl(0, 80%, ${lightness}%)`;

          const marker = L.circleMarker(coord, {
            color: color,
            fillColor: color,
            radius: radius,
            fillOpacity: 0.7,
            weight: 1
          }).addTo(markerLayer);

          // Popup HTML
          const popupHtml = `
            <div class="popup-sprachenkarte">
              <div class="popup-title">${eintrag.Land ?? ''}</div>
              <div class="popup-hauptstadt">${eintrag.Hauptstadt ?? ''}</div>
              ${gdn ? `<div class="popup-line"><span class="popup-label">Anzahl Sprecher:innen:</span> <span class="popup-value">${Number(gdn).toLocaleString()}</span></div>` : ''}
              ${eintrag.Anteil_GDN ? `<div class="popup-line"><span class="popup-label">Anteil Hispanophonie:</span> <span class="popup-value">${eintrag.Anteil_GDN}%</span></div>` : ''}
            </div>`;

          // Nutze MapUI für konsistentes Click-Popup-Verhalten (KEIN HOVER!)
          if (window.MapUI) {
            window.MapUI.bindClickPopup(variationMap, marker, popupHtml, 'corapan-popup');
          } else {
            // Fallback wenn MapUI nicht geladen
            marker.bindPopup(popupHtml);
          }

          bounds.extend(coord);
        });
      });

      if (bounds.isValid()) {
        // On mobile we want a Central America focused view; do not override
        // it with fitBounds so the map stays centered on the requested region.
        if (!isMobile) {
          variationMap.fitBounds(bounds.pad(0.1));
        }
      }
    })
    .catch(err => console.error('Fehler beim Laden der Länder-Daten:', err));

  // Markiere als initialisiert
  if (window.MapUI) {
    window.MapUI.markMapInitialized(container);
  }
}

// Initialisiere bei DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initVariationMap);
} else {
  initVariationMap();
}

// Material for MkDocs: Instant Navigation Support
if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initVariationMap();
  });
}