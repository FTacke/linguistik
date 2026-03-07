document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll("a[href]");

  links.forEach(link => {
    const isHttp = link.protocol === "http:" || link.protocol === "https:";
    const isExternal = isHttp && link.hostname !== window.location.hostname;

    if (isExternal) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
  });
});
