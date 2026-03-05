// docs/assets/javascripts/map_variation_tempora.js

// --- Vollbild-Handling & Map für Variation Tempora ---
// Initialisiert nur, wenn die Seite ein entsprechendes data-map="variation_tempora" Container hat

function initTemporaMap() {
  const temporaContainer = document.querySelector('[data-map="variation_tempora"]');
  
  if (!temporaContainer) {
    return; // Kein Container auf dieser Seite, nichts zu tun
  }

  // Verhindere doppelte Initialisierung
  if (window.MapUI && window.MapUI.isMapInitialized(temporaContainer)) {
    return;
  }

  function toggleFullscreenTempora() {
    const container = temporaContainer;
    const btn = container.querySelector('#fullscreen-btn');
    container.classList.toggle('fullscreen');
    btn.innerHTML = container.classList.contains('fullscreen')
      ? '<span class="material-icons">fullscreen_exit</span>'
      : '<span class="material-icons">fullscreen</span>';
    if (window.temporaMap) setTimeout(() => window.temporaMap.invalidateSize(), 350);
  }

  // Expose toggle to global scope for the button onclick
  window.toggleFullscreenTempora = toggleFullscreenTempora;

  // --- Leaflet Map ---
  const mapEl = temporaContainer.querySelector('#mapid');
  if (mapEl) {
    // Zentriere auf Lateinamerika + Spanien
    const map = L.map(mapEl);
    
    // Setze initiale Ansicht abhängig von der Bildschirmbreite
    const isMobile = window.MapUI ? window.MapUI.isMobileViewport() : window.matchMedia('(max-width: 599px)').matches;
    if (isMobile) {
      // Mobile: zentriere auf Lateinamerika
      map.setView([-10, -65], 3);
    } else {
      // Desktop/Tablet: breite Atlantik-Übersicht (Amerika + Spanien)
      map.setView([20, -40], 2);
    }
    
    window.temporaMap = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    }).addTo(map);

    // Aktiviere UX-Funktionen (Popup-Schließen, Responsive Invalidation)
    if (window.MapUI) {
      window.MapUI.enablePopupCloseUX(map);
      window.MapUI.enableResponsiveInvalidation(map);
    }

    // Daten laden und Marker setzen
    const base = window.ZENSICAL_BASE_PATH || "/";
    fetch(base + 'assets/data/variation_tempora.json')
      .then(r => r.json())
      .then(regionen => {
        const bounds = L.latLngBounds([]);

        // LayerGroup für Marker
        const markerLayer = L.layerGroup().addTo(map);

        regionen.forEach(eintrag => {
          // Länder/Regionen haben eine Koordinate [lat, lng]
          const raw = eintrag.Koordinaten;
          const coords = Array.isArray(raw) && raw.length && typeof raw[0] === 'number' ? [raw] : (raw || []);

          coords.forEach((coord, i) => {
            if (!coord || coord.length !== 2) return; // skip invalid

            // Einheitlicher Radius für alle Marker (da keine Größenmetrik vorhanden)
            const radius = 8;

            // Farbe basierend auf "Verwendung der Tempora" (wenn vorhanden)
            // Standard: blau; könnte später differenziert werden
            let color = '#1976d2'; // Standardfarbe
            const verwendung = eintrag['Verwendung der Tempora'];
            
            // Optional: Farben für verschiedene Verwendungsmuster
            // (kann später verfeinert werden, wenn die Daten gefüllt sind)
            if (verwendung) {
              if (verwendung.includes('Prototyp')) color = '#d32f2f'; // Rot für prototypisch
              else if (verwendung.includes('Neutralisierung')) color = '#f57c00'; // Orange
              else if (verwendung.includes('Andenraum')) color = '#388e3c'; // Grün
            }

            const marker = L.circleMarker(coord, {
              color: color,
              fillColor: color,
              radius: radius,
              fillOpacity: 0.7,
              weight: 2
            }).addTo(markerLayer);

            // Popup HTML
            const popupHtml = `
              <div class="popup-sprachenkarte">
                <div class="popup-title">${eintrag.Land ?? ''}</div>
                <div class="popup-hauptstadt">${eintrag.Hauptstadt ?? ''}</div>
                ${eintrag['Perfecto compuesto'] ? `<div class="popup-line"><span class="popup-label">Perfecto compuesto:</span> <span class="popup-value">${eintrag['Perfecto compuesto']}</span></div>` : ''}
                ${eintrag['Perfecto simple'] ? `<div class="popup-line"><span class="popup-label">Perfecto simple:</span> <span class="popup-value">${eintrag['Perfecto simple']}</span></div>` : ''}
                ${eintrag['Verwendung der Tempora'] ? `<div class="popup-line"><span class="popup-label">Verwendung:</span> <span class="popup-value">${eintrag['Verwendung der Tempora']}</span></div>` : ''}
              </div>`;

            // Nutze MapUI für konsistentes Click-Popup-Verhalten (KEIN HOVER!)
            if (window.MapUI) {
              window.MapUI.bindClickPopup(map, marker, popupHtml, 'corapan-popup');
            } else {
              // Fallback wenn MapUI nicht geladen
              marker.bindPopup(popupHtml);
            }

            bounds.extend(coord);
          });
        });

        // Fitze die Bounds nur auf Desktop, nicht auf Mobile
        if (bounds.isValid() && !isMobile) {
          map.fitBounds(bounds.pad(0.1));
        }
      })
      .catch(err => console.error('Fehler beim Laden der Variation-Tempora-Daten:', err));

    // Markiere als initialisiert
    if (window.MapUI) {
      window.MapUI.markMapInitialized(temporaContainer);
    }
  }
}

// Initialisiere bei DOMContentLoaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initTemporaMap);
} else {
  initTemporaMap();
}

// Material for MkDocs: Instant Navigation Support
if (typeof document$ !== 'undefined') {
  document$.subscribe(() => {
    initTemporaMap();
  });
}

