// Asset source fixup: resolves data-zc-src attributes against the runtime base path.
// Handles <source class="zc-audio-src"> (audio) and <img class="zc-img-src"> (images).
// Works on GitHub Project Pages (/<repo>/) and custom domains (/).
(function () {
  function fixAssetSources() {
    const base = window.ZENSICAL_BASE_PATH || "/";

    // Audio sources
    document.querySelectorAll("source.zc-audio-src[data-zc-src]").forEach(function (el) {
      const rel = el.getAttribute("data-zc-src");
      if (!rel) return;
      const newSrc = base + rel.replace(/^\/+/, "");
      if (el.getAttribute("src") === newSrc) return; // already correct, skip
      el.setAttribute("src", newSrc);
      // Reload the parent <audio> so the browser picks up the updated src
      const audio = el.closest("audio");
      if (audio) audio.load();
    });

    // Images
    document.querySelectorAll("img.zc-img-src[data-zc-src]").forEach(function (el) {
      const rel = el.getAttribute("data-zc-src");
      if (!rel) return;
      const newSrc = base + rel.replace(/^\/+/, "");
      if (el.getAttribute("src") === newSrc) return; // already correct, skip
      el.setAttribute("src", newSrc);
    });
  }

  // Alias for back-compat
  var fixAudioSources = fixAssetSources;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", fixAudioSources);
  } else {
    fixAudioSources();
  }

  // MkDocs Material / Zensical instant navigation support
  if (typeof document$ !== "undefined") {
    document$.subscribe(function () { fixAudioSources(); });
  }
})();
