// Base path helper for GH Project Pages + custom domain
// - GitHub project pages: https://<user>.github.io/<repo>/  -> basePath="/<repo>/"
// - Custom domain:        https://linguistik.hispanistica.com/  -> basePath="/"
(function () {
  const host = window.location.hostname;
  const path = window.location.pathname;

  // Detect GitHub Pages project site: host ends with github.io and first path segment is repo name
  let basePath = "/";

  if (host.endsWith("github.io")) {
    // e.g. /linguistik.hispanistica/variation/... -> first segment is the repo name
    const seg = path.split("/").filter(Boolean)[0];
    if (seg) basePath = "/" + seg + "/";
  }

  // Expose globally
  window.ZENSICAL_BASE_PATH = basePath;
})();
