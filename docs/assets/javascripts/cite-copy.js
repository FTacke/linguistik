/* cite-copy.js – Copy-to-Clipboard für !!! cite Admonitions
   Injiziert automatisch einen Clipboard-Button in jede .admonition.cite.
   Kopiert den Zitationstext (ohne Titel, ohne CC-Zeilen).
   <br>-Elemente werden beim Kopieren als Zeilenumbrüche übernommen.
   Feedback: Icon-Swap Clipboard → Check für ~900ms (keine Farbänderung).
   ------------------------------------------------------------------ */

(function () {
  'use strict';

  function initCiteCopy() {
    var boxes = document.querySelectorAll('.md-typeset .admonition.cite');
    boxes.forEach(function (box) {
      var title = box.querySelector('.admonition-title');
      if (!title) return;
      if (title.querySelector('.cite-copy-btn')) return; // Kein Doppel-Inject

      var btn = document.createElement('button');
      btn.className = 'cite-copy-btn';
      btn.setAttribute('aria-label', 'Zitation kopieren');
      btn.setAttribute('title', 'Zitation kopieren');
      btn.setAttribute('type', 'button');
      title.appendChild(btn);

      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var text = extractCiteText(box);
        copyToClipboard(text, btn);
      });
    });
  }

  /* Rekursiv: Text aus DOM-Node extrahieren, <br> → '\n' */
  function getTextWithLineBreaks(node) {
    if (node.nodeType === Node.TEXT_NODE) return node.textContent;
    if (node.nodeName === 'BR') return '\n';
    var text = '';
    node.childNodes.forEach(function (child) {
      text += getTextWithLineBreaks(child);
    });
    /* Absätze (<p>) mit Zeilenumbruch abschließen */
    if (node.nodeName === 'P') text += '\n';
    return text;
  }

  function extractCiteText(box) {
    var parts = [];
    box.childNodes.forEach(function (node) {
      if (node.nodeType === Node.ELEMENT_NODE &&
          node.classList.contains('admonition-title')) return;
      var raw = getTextWithLineBreaks(node).trim();
      if (raw) parts.push(raw);
    });

    var full = parts.join('\n');

    /* Zeilen filtern: CC-Zeilen entfernen (Sicherheitsnetz) */
    var lines = full.split('\n');
    var filtered = lines.filter(function (line) {
      var t = line.trim();
      if (!t) return false;
      if (/^CC[:\s]/i.test(t)) return false;
      return true;
    });

    return filtered.join('\n').trim();
  }

  function copyToClipboard(text, btn) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        showCopied(btn);
      }).catch(function () {
        fallbackCopy(text, btn);
      });
    } else {
      fallbackCopy(text, btn);
    }
  }

  function fallbackCopy(text, btn) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try { document.execCommand('copy'); } catch (err) { /* silent */ }
    document.body.removeChild(ta);
    showCopied(btn);
  }

  /* Setzt .is-copied → CSS swappt Clipboard-Icon auf Check-Icon */
  function showCopied(btn) {
    btn.classList.add('is-copied');
    setTimeout(function () {
      btn.classList.remove('is-copied');
    }, 1800);
  }

  /* ── Initialisierung ─────────────────────────────────────────────── */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCiteCopy);
  } else {
    initCiteCopy();
  }

  /* MkDocs Material / Zensical – Instant Navigation */
  document.addEventListener('DOMContentSwitch', initCiteCopy);

  /* Fallback: Material for MkDocs document$ observable */
  if (typeof document$ !== 'undefined') {
    document$.subscribe(function () { initCiteCopy(); });
  }
})();
