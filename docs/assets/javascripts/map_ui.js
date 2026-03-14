// docs/assets/javascripts/map_ui.js
// Gemeinsame UI-Funktionen fuer alle Leaflet-Karten im Projekt.

const fullscreenRegistry = new Map();

function isMobileViewport() {
  return window.matchMedia('(max-width: 599px)').matches;
}

function popupOptions(className) {
  const mobile = isMobileViewport();
  return {
    className: className || 'corapan-popup',
    closeButton: true,
    autoClose: true,
    closeOnClick: false,
    autoPan: true,
    keepInView: true,
    maxWidth: mobile ? 280 : 320,
    minWidth: mobile ? 180 : 200,
    autoPanPaddingTopLeft: mobile ? [20, 80] : [50, 100],
    autoPanPaddingBottomRight: mobile ? [20, 20] : [50, 50]
  };
}

function bindClickPopup(map, marker, html, className) {
  marker.bindPopup(html, popupOptions(className));
  marker.on('click', (event) => {
    L.DomEvent.stopPropagation(event);
    map.panTo(event.latlng, { animate: true, duration: 0.3 });
    marker.openPopup();
  });
}

function enablePopupCloseUX(map) {
  map.on('click', () => {
    map.closePopup();
  });

  if (!window.__mapUIEscPopupHandlerBound) {
    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') {
        return;
      }

      document.querySelectorAll('.leaflet-popup-close-button').forEach((button) => button.click());
    });
    window.__mapUIEscPopupHandlerBound = true;
  }
}

function invalidateMap(map) {
  if (!map || typeof map.invalidateSize !== 'function') {
    return;
  }

  map.invalidateSize();
  window.setTimeout(() => map.invalidateSize(), 60);
  window.setTimeout(() => map.invalidateSize(), 220);
}

function getFullscreenTargetZoom(map) {
  if (!map || typeof map.getZoom !== 'function') {
    return null;
  }

  const currentZoom = map.getZoom();
  const viewportWidth = window.innerWidth;

  if (isMobileViewport()) {
    return Math.max(currentZoom, 3);
  }

  if (viewportWidth >= 1600) {
    return currentZoom + 2;
  }

  if (viewportWidth >= 1024) {
    return currentZoom + 1;
  }

  return currentZoom;
}

function applyFullscreenView(map, entry, isFullscreen) {
  if (!map || typeof map.getCenter !== 'function' || typeof map.setView !== 'function') {
    return;
  }

  if (isFullscreen) {
    entry.previousView = {
      center: map.getCenter(),
      zoom: map.getZoom()
    };

    const targetZoom = getFullscreenTargetZoom(map);
    if (targetZoom !== null && targetZoom !== entry.previousView.zoom) {
      window.setTimeout(() => {
        map.setView(entry.previousView.center, targetZoom, { animate: false });
      }, 80);
    }
    return;
  }

  if (entry.previousView) {
    const { center, zoom } = entry.previousView;
    window.setTimeout(() => {
      map.setView(center, zoom, { animate: false });
    }, 80);
  }
}

function enableResponsiveInvalidation(map) {
  const handler = () => invalidateMap(map);
  window.addEventListener('resize', handler);
  window.addEventListener('orientationchange', handler);
}

function isMapInitialized(container) {
  return container?.dataset.mapInitialized === 'true';
}

function markMapInitialized(container) {
  if (container) {
    container.dataset.mapInitialized = 'true';
  }
}

function getHeaderOffset() {
  const header = document.querySelector('.md-header');
  if (!header) {
    return 72;
  }

  const rect = header.getBoundingClientRect();
  return Math.max(0, Math.ceil(rect.bottom || rect.height || 72));
}

function syncMapHeaderOffset() {
  document.documentElement.style.setProperty('--map-header-offset', `${getHeaderOffset()}px`);
}

function updateFullscreenBodyState() {
  const hasFullscreenMap = Array.from(fullscreenRegistry.values()).some(
    (entry) => entry.container.classList.contains('is-fullscreen')
  );
  document.body.classList.toggle('has-map-fullscreen', hasFullscreenMap);
  document.documentElement.classList.toggle('has-map-fullscreen', hasFullscreenMap);
}

function setFullscreenButtonState(button, isFullscreen) {
  button.setAttribute('aria-pressed', String(isFullscreen));
  button.setAttribute(
    'aria-label',
    isFullscreen ? 'Vollbildmodus beenden' : 'Karte im Vollbild öffnen'
  );
}

function setFullscreenButtonAvailability(button, isAvailable) {
  button.hidden = !isAvailable;
  button.disabled = !isAvailable;
  button.tabIndex = isAvailable ? 0 : -1;
  button.setAttribute('aria-hidden', String(!isAvailable));
}

function bindGlobalFullscreenEvents() {
  if (window.__mapUIFullscreenHandlersBound) {
    return;
  }

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') {
      return;
    }

    fullscreenRegistry.forEach((entry) => {
      if (entry.container.classList.contains('is-fullscreen')) {
        entry.setState(false);
      }
    });
  });

  const resizeHandler = () => {
    syncMapHeaderOffset();
    fullscreenRegistry.forEach((entry) => {
      const fullscreenAvailable = !isMobileViewport();

      setFullscreenButtonAvailability(entry.button, fullscreenAvailable);

      if (!fullscreenAvailable && entry.container.classList.contains('is-fullscreen')) {
        entry.setState(false);
      }

      if (entry.container.classList.contains('is-fullscreen')) {
        invalidateMap(entry.map);
      }
    });
  };

  window.addEventListener('resize', resizeHandler);
  window.addEventListener('orientationchange', resizeHandler);

  window.__mapUIFullscreenHandlersBound = true;
}

function enableFullscreenUI(container, map, button) {
  if (!container || !map || !button) {
    return;
  }

  if (fullscreenRegistry.has(container)) {
    syncMapHeaderOffset();
    return;
  }

  bindGlobalFullscreenEvents();

  const entry = {
    container,
    map,
    button,
    previousView: null,
    setState: null
  };

  const setState = (isFullscreen) => {
    if (isFullscreen && isMobileViewport()) {
      return;
    }

    if (isFullscreen) {
      fullscreenRegistry.forEach((entry) => {
        if (entry.container !== container && entry.container.classList.contains('is-fullscreen')) {
          entry.setState(false);
        }
      });
    }

    container.classList.toggle('is-fullscreen', isFullscreen);
    setFullscreenButtonState(button, isFullscreen);
    syncMapHeaderOffset();
    updateFullscreenBodyState();
    invalidateMap(map);
    applyFullscreenView(map, entry, isFullscreen);
  };

  entry.setState = setState;

  button.addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    setState(!container.classList.contains('is-fullscreen'));
  });

  fullscreenRegistry.set(container, entry);

  setFullscreenButtonState(button, false);
  setFullscreenButtonAvailability(button, !isMobileViewport());
  syncMapHeaderOffset();
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    isMobileViewport,
    popupOptions,
    bindClickPopup,
    enablePopupCloseUX,
    enableResponsiveInvalidation,
    isMapInitialized,
    markMapInitialized,
    syncMapHeaderOffset,
    enableFullscreenUI
  };
}

window.MapUI = {
  isMobileViewport,
  popupOptions,
  bindClickPopup,
  enablePopupCloseUX,
  enableResponsiveInvalidation,
  isMapInitialized,
  markMapInitialized,
  syncMapHeaderOffset,
  enableFullscreenUI
};

syncMapHeaderOffset();
