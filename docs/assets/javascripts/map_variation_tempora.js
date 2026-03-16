// docs/assets/javascripts/map_variation_tempora.js
// Karte zur Tempusvariation.

(function () {
  const MAP_TYPE = 'variation_tempora';
  const DATA_PATH = 'assets/data/variation_tempora.json';

  function debugLog(message, details) {
    if (typeof details === 'undefined') {
      console.info(`[variation_tempora] ${message}`);
      return;
    }

    console.info(`[variation_tempora] ${message}`, details);
  }

  function debugError(message, details) {
    if (typeof details === 'undefined') {
      console.error(`[variation_tempora] ${message}`);
      return;
    }

    console.error(`[variation_tempora] ${message}`, details);
  }

  debugLog('map_variation_tempora.js geladen');

  const SYSTEM_STYLES = {
    prototypical: {
      fillColor: '#8fb7d9',
      markerColor: '#3f6f99'
    },
    simple_dominant: {
      fillColor: '#d9b38c',
      markerColor: '#c96a1b'
    },
    aspectual: {
      fillColor: '#9cc9a3',
      markerColor: '#3f7f52'
    },
    compound_expansion: {
      fillColor: '#b7a1d6',
      markerColor: '#6d4ea8'
    },
    transition: {
      fillColor: '#c7b8a3',
      markerColor: '#8a6f52'
    },
    fallback: {
      fillColor: '#c7d2de',
      markerColor: '#64748b'
    }
  };

  const SYSTEM_CONTENT = {
    prototypical: {
      label: 'Prototypischer Gebrauch des perfecto compuesto',
      example: [
        { type: 'line', text: 'Hoy he hablado con Ana.' },
        { type: 'line', text: 'Ayer hablé con Ana.' }
      ]
    },
    simple_dominant: {
      label: 'Dominanz des perfecto simple',
      example: [
        { type: 'line', text: 'Hoy hablé con Ana.' }
      ]
    },
    aspectual: {
      label: 'Aspektuelles Gebrauchssystem',
      example: [
        { type: 'line', text: 'Viví en Puebla dos años.' },
        { type: 'interpretation', text: '→ Zeitraum abgeschlossen' },
        { type: 'line', text: 'He vivido en Puebla dos años.' },
        { type: 'interpretation', text: '→ bis heute, meist weiterhin' }
      ]
    },
    compound_expansion: {
      label: 'Expansion des perfecto compuesto',
      example: [
        { type: 'line', text: 'He llegado ayer.' }
      ]
    },
    fallback: {
      label: 'Dominanz des perfecto simple',
      example: [
        { type: 'line', text: 'Hoy hablé con Ana.' }
      ]
    }
  };

  function isCoordinatePair(value) {
    return Array.isArray(value) && value.length === 2 && value.every((item) => typeof item === 'number');
  }

  function getCoordinateList(rawCoordinates) {
    if (isCoordinatePair(rawCoordinates)) {
      return [rawCoordinates];
    }

    return Array.isArray(rawCoordinates) ? rawCoordinates.filter(isCoordinatePair) : [];
  }

  function inferSystemKey(label) {
    if (!label) {
      return 'fallback';
    }

    if (label.includes('Prototypischer')) {
      return 'prototypical';
    }

    if (label.includes('Dominanz')) {
      return 'simple_dominant';
    }

    if (label.includes('Aspekt')) {
      return 'aspectual';
    }

    if (label.includes('Expansion')) {
      return 'compound_expansion';
    }

    if (label.includes('Übergangszone')) {
      return 'transition';
    }

    return 'fallback';
  }

  function parsePercentValue(value) {
    if (typeof value !== 'string') {
      return Number.NaN;
    }

    return Number.parseFloat(value.replace('%', '').replace(',', '.').trim());
  }

  function getCanonicalSystemKey(raw) {
    const inferredKey = raw.Systemschluessel ?? inferSystemKey(raw['Regionales System'] ?? '');

    if (inferredKey === 'transition') {
      const compuestoValue = parsePercentValue(raw['Perfecto compuesto']);
      const simpleValue = parsePercentValue(raw['Perfecto simple']);

      if (Number.isFinite(compuestoValue) && Number.isFinite(simpleValue)) {
        return compuestoValue > simpleValue ? 'compound_expansion' : 'simple_dominant';
      }

      return 'simple_dominant';
    }

    return SYSTEM_CONTENT[inferredKey] ? inferredKey : 'fallback';
  }

  function getSystemContent(systemKey) {
    return SYSTEM_CONTENT[systemKey] || SYSTEM_CONTENT.fallback;
  }

  function getSystemStyle(systemKey) {
    return SYSTEM_STYLES[systemKey] || SYSTEM_STYLES.fallback;
  }

  function hasDirectPercentValues(raw) {
    return raw['Perfecto compuesto'] !== 'keine direkten Daten' && raw['Perfecto simple'] !== 'keine direkten Daten';
  }

  function isNationalPrimaryPoint(raw) {
    return raw.type === 'national' || raw.tier === 'primary' || raw.category === 'national' || raw.primary === true || raw.capital === true;
  }

  function isRegionalCategorizedPoint(raw) {
    return raw.type === 'regional' || raw.tier === 'secondary' || raw.category === 'regional';
  }

  function isDidacticPoint(raw, hasDirectData) {
    return !hasDirectData || raw.Land === 'Didaktische Region' || Boolean(raw.Hinweis);
  }

  function isRegionalPoint(raw, hasDirectData) {
    if (!hasDirectData) {
      return false;
    }

    return typeof raw.Code === 'string' && raw.Code.includes('-');
  }

  function getPointStatus(raw, hasDirectData) {
    if (isDidacticPoint(raw, hasDirectData)) {
      return 'didactic';
    }

    if (isNationalPrimaryPoint(raw)) {
      return 'national';
    }

    if (isRegionalCategorizedPoint(raw)) {
      return 'regional';
    }

    if (isRegionalPoint(raw, hasDirectData)) {
      return 'regional';
    }

    return 'national';
  }

  function getInfluenceCircleOptions(systemStyle, pointStatus) {
    if (pointStatus === 'national') {
      return {
        radius: 750000,
        fillColor: systemStyle.fillColor,
        fillOpacity: 0.35
      };
    }

    if (pointStatus === 'regional') {
      return {
        radius: 270000,
        fillColor: systemStyle.fillColor,
        fillOpacity: 0.20
      };
    }

    return {
      radius: 340000,
      fillColor: systemStyle.fillColor,
      fillOpacity: 0.08
    };
  }

  function ensureCanvasSize(mapCanvas) {
    if (!mapCanvas) {
      return;
    }

    mapCanvas.style.width = '100%';
    mapCanvas.style.height = '30rem';
    mapCanvas.style.minHeight = '420px';
    mapCanvas.style.display = 'block';
  }

  function formatFrequencyLine(perfectoCompuesto, perfectoSimple) {
    return `${perfectoCompuesto} compuesto | ${perfectoSimple} simple`;
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function buildExampleHtml(exampleLines) {
    return exampleLines
      .map((line) => {
        const className = line.type === 'interpretation' ? 'popup-interpretation' : 'popup-example-line';
        return `<div class="${className}">${escapeHtml(line.text)}</div>`;
      })
      .join('');
  }

  function normalizeTemporaItem(raw) {
    const systemKey = getCanonicalSystemKey(raw);
    const systemContent = getSystemContent(systemKey);
    const systemStyle = getSystemStyle(systemKey);
    const hasDirectData = hasDirectPercentValues(raw);
    const pointStatus = getPointStatus(raw, hasDirectData);
    const influenceCircle = getInfluenceCircleOptions(systemStyle, pointStatus);

    return {
      title: raw.Ort ?? raw.Hauptstadt ?? raw.Land ?? '',
      perfectoCompuesto: raw['Perfecto compuesto'] ?? '',
      perfectoSimple: raw['Perfecto simple'] ?? '',
      hasDirectData,
      frequencyLine: hasDirectData ? formatFrequencyLine(raw['Perfecto compuesto'] ?? '', raw['Perfecto simple'] ?? '') : '',
      systemLabel: systemContent.label,
      exampleLines: systemContent.example,
      points: getCoordinateList(raw.Koordinaten),
      pointStatus,
      influenceCircle,
      markerOptions: {
        color: systemStyle.markerColor,
        fillColor: systemStyle.markerColor,
        radius: hasDirectData ? 8 : 6,
        fillOpacity: hasDirectData ? 0.8 : 0.28,
        weight: 2,
        opacity: 1,
        dashArray: hasDirectData ? undefined : '4 3'
      }
    };
  }

  function buildPopupHtml(item) {
    const frequencyBlock = item.hasDirectData
      ? `
        <div class="popup-frequency-label">Frequenz (freie Rede)</div>
        <div class="popup-frequency">${escapeHtml(item.frequencyLine)}</div>`
      : '';

    return `
      <div class="popup-sprachenkarte">
        <div class="popup-title">${escapeHtml(item.title)}</div>
        ${frequencyBlock}
        <div class="popup-section-label">Gebrauchssystem</div>
        <div class="popup-system">${escapeHtml(item.systemLabel)}</div>
        <div class="popup-section-label">Beispiel</div>
        <div class="popup-example">${buildExampleHtml(item.exampleLines)}</div>
      </div>`;
  }

  function createTileLayer() {
    return L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a>'
    });
  }

  function renderInfluenceCircles(map, items) {
    const areaLayer = L.layerGroup().addTo(map);
    let circleCount = 0;

    items.forEach((item) => {
      item.points.forEach((point) => {
        const circle = L.circle(point, {
          radius: item.influenceCircle.radius,
          stroke: false,
          fillColor: item.influenceCircle.fillColor || item.markerOptions.fillColor,
          fillOpacity: item.influenceCircle.fillOpacity
        }).addTo(areaLayer);

        circle.bringToBack();
        circleCount += 1;
      });
    });

    debugLog('renderInfluenceCircles ausgefuehrt', {
      circleCount,
      renderedLayerCount: areaLayer.getLayers().length
    });

    return {
      areaLayer,
      areaCount: circleCount
    };
  }

  function setInitialView(map, isMobile) {
    if (isMobile) {
      map.setView([-10, -65], 3);
      return;
    }

    map.setView([20, -40], 3);
  }

  function refreshMapLayout(map) {
    map.invalidateSize({ animate: false, pan: false });

    window.requestAnimationFrame(() => {
      map.invalidateSize({ animate: false, pan: false });
    });

    window.setTimeout(() => {
      map.invalidateSize({ animate: false, pan: false });
    }, 120);
  }

  function fitDesktopBounds(map, bounds) {
    map.fitBounds(bounds.pad(0.1), {
      animate: false,
      padding: [24, 24]
    });
  }

  function initContainer(container) {
    if (!container) {
      return;
    }

    const initializedType = window.MapUI ? window.MapUI.getInitializedMapType(container) : null;
    const isInitializedForTempora = window.MapUI ? window.MapUI.isMapInitializedForType(container, MAP_TYPE) : false;

    debugLog('passender Container gefunden', {
      mapType: container.dataset.map || null,
      initializedFlag: container.dataset.mapInitialized || null,
      initializedType,
      isInitializedForTempora
    });

    if (isInitializedForTempora) {
      debugLog('Container fuer variation_tempora bereits initialisiert, init wird uebersprungen');
      return;
    }

    if (initializedType && initializedType !== MAP_TYPE) {
      debugError('Container wurde bereits von anderem Kartentyp initialisiert', {
        initializedType,
        requestedType: MAP_TYPE
      });
      return;
    }

    if (typeof L === 'undefined') {
      debugError('Leaflet wurde nicht geladen.');
      return;
    }

    const mapCanvas = container.querySelector('.book-map__canvas');
    const fullscreenButton = container.querySelector('.book-map__control--fullscreen');

    if (!mapCanvas) {
      debugError('Kein .book-map__canvas gefunden.');
      return;
    }

    ensureCanvasSize(mapCanvas);

    const computedCanvasStyle = window.getComputedStyle(mapCanvas);
    debugLog('Canvas-Status ermittelt', {
      height: computedCanvasStyle.height,
      width: computedCanvasStyle.width,
      leafletId: mapCanvas._leaflet_id || null
    });

    if (computedCanvasStyle.height === '0px') {
      debugError('Canvas hat Hoehe 0.');
      return;
    }

    const map = L.map(mapCanvas);
    debugLog('Karte fuer variation_tempora tatsaechlich erzeugt');

    const isMobile = window.MapUI ? window.MapUI.isMobileViewport() : window.matchMedia('(max-width: 599px)').matches;
    setInitialView(map, isMobile);
    debugLog('Standard-Overlay-Rendering aktiv', {
      overlayPane: Boolean(map.getPane('overlayPane')),
      markerPane: Boolean(map.getPane('markerPane'))
    });

    createTileLayer().addTo(map);

    if (window.MapUI) {
      window.MapUI.enablePopupCloseUX(map);
      window.MapUI.enableResponsiveInvalidation(map);
      window.MapUI.enableFullscreenUI(container, map, fullscreenButton);
      window.MapUI.markMapInitialized(container, MAP_TYPE);
    }

    refreshMapLayout(map);

    const base = window.ZENSICAL_BASE_PATH || '/';
    debugLog('JSON-Fetch gestartet', {
      url: `${base}${DATA_PATH}`
    });

    fetch(`${base}${DATA_PATH}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        return response.json();
      })
      .then((regions) => {
        debugLog('JSON-Fetch erfolgreich', {
          isArray: Array.isArray(regions),
          datasetCount: Array.isArray(regions) ? regions.length : null
        });

        const bounds = L.latLngBounds([]);
        const items = regions.map(normalizeTemporaItem);
        const areaRenderResult = renderInfluenceCircles(map, items);
        const markerLayer = L.layerGroup().addTo(map);
        let markerCount = 0;

        items.forEach((item) => {
          item.points.forEach((point) => {
            const marker = L.circleMarker(point, item.markerOptions).addTo(markerLayer);
            marker.bringToFront();
            const popupHtml = buildPopupHtml(item);

            if (window.MapUI) {
              window.MapUI.bindClickPopup(map, marker, popupHtml, 'corapan-popup');
            } else {
              marker.bindPopup(popupHtml);
            }

            bounds.extend(point);
            markerCount += 1;
          });
        });

        debugLog('Marker-Erzeugung abgeschlossen', {
          markerCount,
          areaCount: areaRenderResult.areaCount,
          markerLayerCount: markerLayer.getLayers().length
        });

        if (bounds.isValid() && !isMobile) {
          fitDesktopBounds(map, bounds);
        }

        refreshMapLayout(map);
      })
      .catch((error) => {
        debugError('JSON-Fetch fehlgeschlagen', error);
      });
  }

  function initTemporaMaps() {
    const containers = document.querySelectorAll(`.book-map[data-map="${MAP_TYPE}"]`);
    debugLog('initTemporaMaps gestartet', {
      containerCount: containers.length
    });
    containers.forEach(initContainer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTemporaMaps);
  } else {
    initTemporaMaps();
  }

  if (typeof document$ !== 'undefined') {
    document$.subscribe(() => {
      initTemporaMaps();
    });
  }
})();

