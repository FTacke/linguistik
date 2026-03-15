// docs/assets/javascripts/map.js
// Herkunftssprachen-Karte.

(function () {
  const MAP_TYPE = 'herkunft';
  const DATA_PATH = 'assets/data/herkunftssprachen.json';

  function isCoordinatePair(value) {
    return Array.isArray(value) && value.length === 2 && value.every((item) => typeof item === 'number');
  }

  function normalizeLanguageItem(raw) {
    return {
      title: raw.sprache ?? '',
      family: raw.sprachfamilie ?? '',
      origins: Array.isArray(raw.herkunft) ? raw.herkunft : [],
      points: Array.isArray(raw.koordinaten) ? raw.koordinaten.filter(isCoordinatePair) : [],
      markerOptions: {
        color: raw.farbe,
        fillColor: raw.farbe,
        radius: 8,
        fillOpacity: 0.7,
        weight: 2
      }
    };
  }

  function buildPopupHtml(item, index) {
    return `
      <div class="popup-sprachenkarte">
        <span class="popup-title">${item.title}</span>
        <span class="popup-familie">${item.family}</span>
        <div class="popup-herkunft">${item.origins[index] ?? ''}</div>
      </div>`;
  }

  function createTileLayer() {
    return L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    });
  }

  function initContainer(container) {
    if (!container || (window.MapUI && window.MapUI.isMapInitializedForType(container, MAP_TYPE))) {
      return;
    }

    const mapCanvas = container.querySelector('.book-map__canvas');
    const fullscreenButton = container.querySelector('.book-map__control--fullscreen');

    if (!mapCanvas) {
      return;
    }

    const map = L.map(mapCanvas).setView([45, 15], 3);
    createTileLayer().addTo(map);

    if (window.MapUI) {
      window.MapUI.enablePopupCloseUX(map);
      window.MapUI.enableResponsiveInvalidation(map);
      window.MapUI.enableFullscreenUI(container, map, fullscreenButton);
      window.MapUI.markMapInitialized(container, MAP_TYPE);
    }

    const base = window.ZENSICAL_BASE_PATH || '/';
    fetch(`${base}${DATA_PATH}`)
      .then((response) => response.json())
      .then((entries) => {
        const bounds = L.latLngBounds([]);

        entries.map(normalizeLanguageItem).forEach((item) => {
          item.points.forEach((point, index) => {
            const marker = L.circleMarker(point, item.markerOptions).addTo(map);
            const popupHtml = buildPopupHtml(item, index);

            if (window.MapUI) {
              window.MapUI.bindClickPopup(map, marker, popupHtml, 'corapan-popup');
            } else {
              marker.bindPopup(popupHtml);
            }

            bounds.extend(point);
          });
        });

        if (bounds.isValid()) {
          map.fitBounds(bounds.pad(0.1));
        }
      })
      .catch((error) => {
        console.error('Fehler beim Laden der Herkunftssprachen-Daten:', error);
      });
  }

  function initHerkunftMaps() {
    document.querySelectorAll(`.book-map[data-map="${MAP_TYPE}"]`).forEach(initContainer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHerkunftMaps);
  } else {
    initHerkunftMaps();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(() => {
      initHerkunftMaps();
    });
  }
})();
