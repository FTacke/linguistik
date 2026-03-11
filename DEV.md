# DEV.md – Developer Notes: school-zensical

## Projektstruktur (docs/)

```
docs/
├── assets/
│   ├── audiofiles/
│   │   ├── corapan/        ← CO.RA.PAN-Audio-Beispiele (arg/bol/chi/col/cr/ecu/es-can/es-mad/mex/nic/per)
│   │   └── marele/         ← MAR.ELE-Audio-Beispiele (agua, baron_varon, bebedor, glottis, r)
│   ├── data/
│   │   ├── countries.json          ← Hispanophonie-Länder (für anhang)
│   │   ├── herkunftssprachen.json  ← Herkunftssprachen-Daten (für map.js)
│   │   └── variation_tempora.json  ← Tempusvariation-Daten (für map_variation_tempora)
│   ├── images/
│   │   ├── toolkit_logo.png         ← Logo (Kopfzeile)
│   │   ├── toolkit_favicon.png      ← Favicon
│   │   ├── hispanistica_badge.png   ← Hispanistica-Badge (Startseite)
│   │   ├── anhang.png              ← Map-Vorschaubild (Desktop)
│   │   └── anhang_detail.png       ← Map-Vorschaubild (Detail)
│   ├── javascripts/
│   │   ├── map_ui.js               ← Gemeinsame Leaflet-UX-Funktionen (MapUI)
│   │   ├── map.js                  ← Herkunftssprachen-Karte (data-map="herkunft")
│   │   ├── anhang.js               ← Hispanophonie-Karte (data-map="variation")
│   │   └── map_variation_tempora.js ← Tempusvariation-Karte (data-map="variation_tempora")
│   └── styles/
│       ├── 00_tokens.css    ← Nur CSS Custom Properties / Design Tokens
│       ├── 10_typography.css ← Content-Typographie (.md-typeset)
│       ├── 20_book.css      ← Layout-/Publikations-Overrides
│       ├── 30_components.css ← Generische Komponenten-Overrides
│       └── 40_custom.css    ← Projektspezifische Sonderfälle (Cover, Audio, Maps)
├── index.md          ← Startseite (Buchcover + Vorwort)
├── einleitung.md
├── fehlerlinguistik.md
├── aussprache.md
├── orthographie.md
├── kreativitaet.md
├── wandel.md
├── herkunftssprachen.md
├── anhang.md
└── variation/
    ├── variation_plurizentrik.md
    ├── variation_aussprache.md
    ├── variation_grammatik.md
    └── variation_klassenraum.md
```

`overrides/partials/content.html` – Template-Override für Kapitel-Meta (s.u.)

## Laden / Starten

### Build
```bash
cd school-zensical
.venv/Scripts/zensical build   # Windows

# oder
.venv/Scripts/zensical serve   # Build + lokaler Dev-Server
```

### CSS-Ladereihenfolge
Die Stylesheets werden in dieser Reihenfolge geladen (konfiguriert in `zensical.toml`):
```
00_tokens.css → 10_typography.css → 20_book.css → 30_components.css → 40_custom.css → leaflet.css
```

## Custom-Komponenten (`40_custom.css`)

### Kapitel-Meta / Byline (global)
Klassen: `.doc-chapter-meta`, `.doc-chapter-meta__byline`, `.doc-chapter-meta__name`,  
`.doc-chapter-meta__details`, `.doc-chapter-meta__detail`, `.doc-chapter-meta__sep`  
Template: `overrides/partials/content.html` (Jinja2-Override, Build-Zeit)  
CSS: `docs/assets/styles/30_components.css` + Token `--hairline-color` in `00_tokens.css`

Rendert beim Build automatisch eine Byline-/Meta-Zeile direkt **unter dem ersten H1**,
wenn die Seite YAML-Frontmatter mit dem Feld `authors` enthält.

**Frontmatter-Schema** (YAML-Block am Anfang jeder Markdown-Datei):
```yaml
---
authors:
  - "Marlon Merte"
  - "Felix Tacke"
peer_review:
  - "Gloria Gabriel"
last_modified: "26.08.2025"
---
```

Felder:
- `authors` – Liste von Namen → Byline-Zeile (Pflicht für Meta-Rendering)
- `peer_review` – Liste von Namen (optional; weglassen wenn leer)
- `last_modified` – Datum als String `DD.MM.YYYY` (optional)

**Kein JS.** Kein Footnote-Parsing. Kein `document$.subscribe()`. Reines Build-Time-Rendering.

Die alten `[^*]`-Fußnoten in bestehenden Docs bleiben als normaler Fußnotentext erhalten
(kein Parsing mehr). Neue Docs tragen Metadaten nur noch als Frontmatter ein.

**Ergebnis-HTML** (direkt nach dem `</h1>` im gebauten HTML):
```html
<div class="doc-chapter-meta" role="note" aria-label="Kapitelmetadaten">
  <div class="doc-chapter-meta__byline">
    <span class="doc-chapter-meta__name">Marlon Merte</span>
    <span class="doc-chapter-meta__sep" aria-hidden="true">·</span>
    <span class="doc-chapter-meta__name">Felix Tacke</span>
  </div>
  <div class="doc-chapter-meta__details">
    <span class="doc-chapter-meta__detail">Peer Review: Gloria Gabriel</span>
    <span class="doc-chapter-meta__sep" aria-hidden="true">·</span>
    <span class="doc-chapter-meta__detail">Letzte Änderung: 26.08.2025</span>
  </div>
</div>
```

### Buchcover (Startseite)
Klassen: `.cover-container`, `.logo-image`, `.cover-caption`, `.cover-caption .subtitle/.coordination/.authors` etc.  
Verwendet in: `docs/index.md`

### „Hör mal"-Audio-Kästen
Klassen: `details.hoermal`, `.audio-comparison`, `.audio-block`, `.audio-source`, `.example`  
Verwendet in: `docs/aussprache.md`, `docs/orthographie.md` u.a.  
Audio-Dateien liegen in: `docs/assets/audiofiles/marele/` und `docs/assets/audiofiles/corapan/`

### Karten (Leaflet.js)
Klassen: `#map-container[data-map="..."]`, `.corapan-popup`, `.popup-*`  
JS-Dateien: `assets/javascripts/map*.js` (4 Dateien)  
Daten: `assets/data/countries.json`, `herkunftssprachen.json`, `variation_tempora.json`  
Karten-Seiten: `anhang.md`, `herkunftssprachen.md`, `variation/variation_grammatik.md`

### Hilfklassen
- `.meta`: Inline-Kennzeichnung von IPA/Kategorie-Werten (`<span class="meta">`)
- `.literatur`: Literaturabschnitte (kleinere Schrift)
- `.cc-text`: CC-Lizenzhinweis (rechts ausgerichtet, gedimmt)

## Externe Abhängigkeiten / CDN

- **Leaflet.js**: Map-Library (geladen via CDN, konfiguriert in `zensical.toml`)
  - CSS: `https://unpkg.com/leaflet/dist/leaflet.css`
  - JS: `https://unpkg.com/leaflet/dist/leaflet.js`
  - Keine API-Keys nötig, verwendet OpenStreetMap-Tiles (ebenfalls keine Keys)
- **Material Icons**: Google Fonts Icon-Font für Fullscreen-Button in Maps
  - `https://fonts.googleapis.com/icon?family=Material+Icons`
  - Keine API-Keys nötig

## Umbenannte / verschobene Dateien (Migration von school/)

| Alt (school/) | Neu (school-zensical/) | Änderung |
|---|---|---|
| `docs/assets/stylesheets/overrides.css` | `docs/assets/styles/40_custom.css` (+ 00-30) | Aufgeteilt in Layers |
| `docs/assets/stylesheets/maps.css` | `docs/assets/styles/40_custom.css` | In 40_custom.css integriert |
| `docs/assets/maps/*.json` | `docs/assets/data/*.json` | Ordner umbenannt zu `data/` |
| `fetch('../../assets/maps/...')` in JS | `fetch('/assets/data/...')` | Absolute Pfade, neuer Ordner |

## Neue Komponenten: Cover Admonition (v4 – Buchcover-Hochformat)

### Cover – Hochkantiges Buchcover-Format (Portrait)
Modernes Poster-Design mit **hochkantigem Buchcover-Aspekt** (3:4 approx), intelligenter Responsive-Handhabung, 3-Zonen-Layout.

**Location:** `docs/assets/styles/40_custom.css` (lines 18–246) + `docs/index.md` (lines 1–49)

**Buchcover-Prinzipien (v4):**
- **Breite**: max-width `580px` (schmaler als vorher, buchtypisch)
- **Höhe ab 768px**: `min-height: calc(min(580px, 100vw - 40px) * 1.15)` (macht Cover spürbar höher, ~666px)
- **Mobile (<768px)**: Keine feste Höhe, sauberes Fließen, kein Overflow
- **3-Zonen-Layout**: Header (Titel/Subtitle), Main (Koordination/Autor:innen), Footer (mit margin-top: auto)
- **Footer immer unten**: `.cover-footer { margin-top: auto; }` nutzt Flexbox

**Responsive Verhalten:**
- Mobile (≤767px): Linear Layout, normales Fließen, keine Höhenbegrenzung
- Tablet/Desktop (768px+): min-height erzwingt Buchcover-Proportion, Footer sitzt unten

**Typografi-Update (v4):**
- Titel: `clamp(2rem, 3.8vw, 2.8rem)` (etwas kleiner, realistischer)
- Titel max-width: `15ch` (enger statt 18ch, erzwingt, dass "@School" typischerweise in separate Zeile geht)
- Subtitle, Labels, Namen: Unverändert (optimale Werte behalten)

**Padding-Asymmetrie (für vertikale Luftigkeit):**
```css
padding: clamp(22px, 3vw, 36px) clamp(18px, 2.6vw, 32px);
/* oben/unten: 22–36px, seiten: 18–32px → mehr vertikal, weniger horizontal */
```

**Zonen-Spacing:**
- Header zu Main: `margin-top: clamp(14px, 2vw, 22px);` (in `.cover-coordination` + `.cover-authors`)
- Main zu Footer: automatisch via `margin-top: auto;`

**CSS-Variablen (Spacing):**
```css
--cover-gap-lg: clamp(16px, 2.4vw, 24px);  /* Large (zwischen Zonen) */
--cover-gap-md: clamp(10px, 1.8vw, 14px);  /* Medium (Standard Gap) */
--cover-gap-sm: clamp(6px, 1.2vw, 10px);   /* Small (in Labels) */
```

**3-Zonen-Layout Struktur:**
```
┌─────────────────────────┐
│  ZONE 1: Header         │  (Titel + Subtitle)
│                         │
├─────────────────────────┤
│  ZONE 2: Main           │  (Koordination + Autor:innen)
│                         │
│                         │  ← Flexbox wächst hier
├─────────────────────────┤
│  ZONE 3: Footer         │  (margin-top: auto pinnt nach unten)
└─────────────────────────┘
```

**Visuelles Resultat:**
- **Mobile**: Poster, oben kompakt, einfach scrollbar
- **Desktop**: Echtes Buchcover-Feeling (schmaler, höher, Footer unten)
- **Keine Überläufe**: Mobile bleibt flexibel, Desktop nutzt min-height statt aspect-ratio

**Font-Weight-Hierarchie (unverändert):**
| Element | Weight | Größe | Opacity |
|---------|--------|-------|---------|
| Titel | 700 | 2.0–2.8rem | 1.0 |
| Subtitle | 500 | 1.0–1.25rem | 0.8 |
| Labels | 500 | 0.75rem | 0.55 |
| Koordination Name | 500 | 0.95rem | 0.9 |
| Autor:innen | 450 | 0.92rem | 0.8 |
| Footer | 400 | 0.9rem | 0.65 |

**CSS-Highlight - Flexbox 3-Zone:**
```css
.md-typeset .admonition.cover {
  display: flex;
  flex-direction: column;
  gap: var(--cover-gap-md);
}

.md-typeset .admonition.cover .cover-footer {
  margin-top: auto;  /* Pinnt Footer nach unten */
}

@media (min-width: 768px) {
  .md-typeset .admonition.cover {
    min-height: calc(min(580px, 100vw - 40px) * 1.15);
  }
}
```

**Testing-Status:**
- [x] max-width 580px (buchformat-typisch)
- [x] min-height 768px+ erzwingt Hochformat
- [x] Mobile <768px: flexibel, kein Overflow
- [x] Footer immer unten (margin-top: auto)
- [x] Titel enger (15ch statt 18ch)
- [x] 3-Zonen sauber separiert
- [x] Dark Mode kompatibel
- [x] Build: 0.28s, 0 Fehler

## Migrationsstatus

- [x] Alle Markdown-Seiten vorhanden (wandel.md, herkunftssprachen.md hinzugefügt zu Nav)
- [x] Bilder/Logos kopiert nach `assets/images/`
- [x] Audiofiles kopiert nach `assets/audiofiles/`
- [x] JS-Dateien kopiert nach `assets/javascripts/`
- [x] Kartendaten kopiert nach `assets/data/`
- [x] `40_custom.css` angelegt mit allen custom-Stilen
- [x] Inline-Leaflet `<link>`-Tags aus Markdown entfernt
- [x] Logo + Favicon konfiguriert
- [x] Build sauber (0 Fehler)
