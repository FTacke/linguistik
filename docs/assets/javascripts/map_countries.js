// docs/assets/javascripts/map_countries.js
// Karte zur Verbreitung des Spanischen als Muttersprache.

(function () {
  const MAP_TYPE = 'variation';
  const DATA_PATH = 'assets/data/countries.json';

  function isCoordinatePair(value) {
    return Array.isArray(value) && value.length === 2 && value.every((item) => typeof item === 'number');
  }

  function getCoordinateList(rawCoordinates) {
    if (isCoordinatePair(rawCoordinates)) {
      return [rawCoordinates];
    }

    return Array.isArray(rawCoordinates) ? rawCoordinates.filter(isCoordinatePair) : [];
  }

  function getMarkerColor(share) {
    const lightness = Math.max(30, 70 - share * 1.2);
    return `hsl(0 80% ${lightness}%)`;
  }

  function normalizeCountryItem(raw, maxGdn) {
    const gdn = Number(raw.GDN) || 0;
    const share = Number(raw.Anteil_GDN) || 0;
    const radius = gdn > 0 ? Math.max(4, 4 + 24 * Math.sqrt(gdn / maxGdn)) : 6;
    const color = getMarkerColor(share);

    return {
      title: raw.Land ?? '',
      capital: raw.Hauptstadt ?? '',
      gdn,
      share,
      speakersLabel: gdn ? new Intl.NumberFormat('de-DE').format(gdn) : '',
      shareLabel: share ? `${share.toFixed(1)} %` : '',
      points: getCoordinateList(raw.Koordinaten),
      markerOptions: {
        color,
        fillColor: color,
        radius,
        fillOpacity: 0.7,
        weight: 1
      }
    };
  }

  function buildPopupHtml(item) {
    if (window.MapUI && typeof window.MapUI.renderPopupCard === 'function') {
      return window.MapUI.renderPopupCard({
        title: item.title,
        blocks: [
          {
            type: 'section',
            label: 'Hauptstadt',
            content: {
              type: 'body',
              text: item.capital
            }
          },
          {
            type: 'metric',
            label: 'Sprecher:innen',
            value: item.speakersLabel
          },
          {
            type: 'metric',
            label: 'Anteil Hispanophonie',
            value: item.shareLabel
          }
        ]
      });
    }

    return `
      <div class="popup-sprachenkarte">
        <div class="popup-title">${item.title}</div>
      </div>`;
  }

  function createTileLayer() {
    return L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    });
  }

  function setInitialView(map, isMobile) {
    if (isMobile) {
      map.setView([-10, -65], 3);
      return;
    }

    map.setView([20, -40], 3);
  }

  function fitDesktopBounds(map, bounds) {
    const paddedBounds = bounds.pad(0.1);
    const targetZoom = map.getBoundsZoom(paddedBounds) + 1;
    map.setView(paddedBounds.getCenter(), targetZoom, { animate: false });
  }

  function initContainer(container) {
    if (!container || (window.MapUI && window.MapUI.isMapInitializedForType(container, MAP_TYPE))) {
      return;
    }

    const mapCanvas = container.querySelector('.book-map__canvas');
    const fullscreenButton = container.querySelector('.book-map__control--fullscreen');

    if (!mapCanvas) {
      console.error('Map canvas .book-map__canvas not found');
      return;
    }

    const map = L.map(mapCanvas);
    const isMobile = window.MapUI ? window.MapUI.isMobileViewport() : window.matchMedia('(max-width: 599px)').matches;
    setInitialView(map, isMobile);

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
      .then((countries) => {
        const bounds = L.latLngBounds([]);
        const gdns = countries.map((item) => Number(item.GDN || 0)).filter((value) => !Number.isNaN(value) && value > 0);
        const maxGdn = gdns.length ? Math.max(...gdns) : 1;
        const markerLayer = L.layerGroup().addTo(map);

        countries.map((item) => normalizeCountryItem(item, maxGdn)).forEach((item) => {
          item.points.forEach((point) => {
            const marker = L.circleMarker(point, item.markerOptions).addTo(markerLayer);
            const popupHtml = buildPopupHtml(item);

            if (window.MapUI) {
              window.MapUI.bindClickPopup(map, marker, popupHtml, 'corapan-popup');
            } else {
              marker.bindPopup(popupHtml);
            }

            bounds.extend(point);
          });
        });

        if (bounds.isValid() && !isMobile) {
          fitDesktopBounds(map, bounds);
        }
      })
      .catch((error) => {
        console.error('Fehler beim Laden der Laender-Daten:', error);
      });
  }

  function initVariationMaps() {
    document.querySelectorAll(`.book-map[data-map="${MAP_TYPE}"]`).forEach(initContainer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVariationMaps);
  } else {
    initVariationMaps();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(() => {
      initVariationMaps();
    });
  }
})();