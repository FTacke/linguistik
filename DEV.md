# DEV.md - Developer Notes: linguistik.hispanistica

## Projektkontext

Dieses Repository enthaelt die Quelltexte des digitalen Lehrbuchs **Linguistik im Spanischunterricht** mit dem Untertitel **Ein digitales Lehrbuch fuer (angehende) Lehrkraefte**.

- Repository-Name: `linguistik.hispanistica`
- Produktionsdomain: <https://linguistik.hispanistica.com>
- Herausgeber: Felix Tacke
- Institutioneller Kontext: Philipps-Universitaet Marburg / Hispanistica @ Marburg
- Publikationstyp: digitales Lehrbuch
- DOI: `10.5281/zenodo.15348687`

Technisch basiert das Projekt auf **MkDocs** mit dem Theme **Zensical**. Das Theme wird fuer ein digitales Lehrbuch mit Fokus auf Lesbarkeit, Metadaten, Audio, Karten und didaktische Komponenten angepasst.

## Zentrale Dateien auf Root-Ebene

- `README.md` - Projektbeschreibung, Zitierweise, Lizenz
- `STARTME.md` - Kurzstart fuer lokale Entwicklung
- `DEV.md` - technische Entwicklerdokumentation
- `zensical.toml` - Site-Konfiguration, Navigation, Theme, Asset-Reihenfolge
- `CITATION.cff` - maschinenlesbare Zitationsdaten
- `scripts/` - Hilfsskripte fuer Migration und Formatierung
- `docs/` - Quellen fuer Inhalte und Assets
- `overrides/` - Zensical-/Template-Overrides
- `site/` - generierte Ausgabe der Website

## Projektstruktur (`docs/`)

```text
docs/
|- index.md
|- einleitung.md
|- fehlerlinguistik.md
|- aussprache.md
|- orthographie.md
|- kreativitaet.md
|- herkunftssprachen.md
|- wandel.md
|- anhang.md
|- impressum.md
|- lizenz.md
|- admonitions.md
|- variation/
|  |- variation_plurizentrik.md
|  |- variation_aussprache.md
|  |- variation_anrede.md
|  |- variation_tempora.md
|  |- variation_morphosyntax.md
|  `- variation_klassenraum.md
`- assets/
   |- audiofiles/
   |  |- corapan/
   |  |- marele/
   |  `- promat/
   |- data/
   |  |- countries.json
   |  |- herkunftssprachen.json
   |  `- variation_tempora.json
   |- documentation/
   |- fonts/
   |- images/
   |  |- favicon.png
   |  |- hispanistica_badge.png
   |  |- map_countries.png
   |  `- map_countries_detail.png
   |- javascripts/
   |  |- base_path.js
   |  |- audio_src_fixup.js
   |  |- cite-copy.js
   |  |- external-links.js
   |  |- map_ui.js
   |  |- map.js
   |  |- map_countries.js
   |  `- map_variation_tempora.js
   |- styles/
   |  |- 00_tokens.css
   |  |- 10_typography.css
   |  |- 20_book.css
   |  |- 25_cover.css
   |  |- 30_components.css
   |  |- 40_custom.css
   |  `- 50_map.css
   `- vendor/
      `- leaflet/
```

## Lokale Entwicklung

### Voraussetzungen

- Windows PowerShell
- lokales virtuelles Environment in `.venv`
- `zensical` innerhalb des Environments installiert

### Environment aktivieren

```powershell
.venv\Scripts\Activate.ps1
```

### Dev-Server starten

```powershell
.venv\Scripts\zensical serve
```

Standardmaessig ist die Seite lokal unter <http://localhost:8000> verfuegbar.

### Nur bauen

```powershell
.venv\Scripts\zensical build
```

Die Ausgabe landet im Verzeichnis `site/`.

### Nuetzliche Varianten

```powershell
.venv\Scripts\zensical --help
.venv\Scripts\zensical serve --port 8080
```

## Konfiguration (`zensical.toml`)

### Projekt-Metadaten

Die aktuelle Konfiguration verwendet:

- `site_name = "Linguistik im Spanischunterricht"`
- `site_description = "Digitales Lehrbuch zur linguistischen Fundierung des Spanischunterrichts fuer (angehende) Lehrkraefte."`
- `site_url = "https://linguistik.hispanistica.com/"`
- `site_author = "Felix Tacke"`

### Navigation

Die Navigation ist kapitelorientiert aufgebaut und fuehrt Kapitel 5 als verschachtelten Variationsblock:

- Titel & Vorwort
- Einleitung
- 1 Fehlerlinguistik
- 2 Aussprache
- 3 Orthographie
- 4 Lexikalische Kreativitaet
- 5 Variation & Plurizentrik
- 6 Sprachwandel
- 7 Herkunftssprachen
- Anhang

### CSS-Ladereihenfolge

Die Stylesheets werden aktuell in dieser Reihenfolge geladen:

```text
00_tokens.css
-> 10_typography.css
-> 20_book.css
-> 25_cover.css
-> 30_components.css
-> assets/vendor/leaflet/leaflet.css
-> 40_custom.css
-> 50_map.css
```

### JavaScript-Ladereihenfolge

Die JavaScript-Dateien werden aktuell in dieser Reihenfolge geladen:

```text
base_path.js
-> audio_src_fixup.js
-> assets/vendor/leaflet/leaflet.js
-> map_ui.js
-> map.js
-> map_countries.js
-> map_variation_tempora.js
-> cite-copy.js
-> external-links.js
```

## Kapitel-Metadaten unter dem ersten H1

Template-Override: `overrides/partials/content.html`

CSS: `docs/assets/styles/30_components.css`

Direkt unter dem ersten `h1` rendert das Projekt einen Meta-Block, wenn YAML-Frontmatter vorhanden ist. Die Daten werden beim Build injiziert, nicht clientseitig per JavaScript.

### Unterstuetztes Frontmatter-Schema

```yaml
---
authors:
  - "Marlon Merte"
  - "Felix Tacke"
peer_review:
  - "Gloria Gabriel"
created: "18.09.2025"
last_modified: "23.09.2025"
---
```

Felder:

- `authors` - erforderlich fuer das Meta-Rendering
- `peer_review` - optional
- `created` - optional
- `last_modified` - optional

### Renderlogik

- Wenn `authors` gesetzt ist und der Seiteninhalt ein `</h1>` enthaelt, wird der Meta-Block direkt nach dem ersten Heading eingefuegt.
- Strings werden defensiv zu Listen normalisiert.
- `created` und `last_modified` werden als eigener Datumsblock ausgegeben.
- Keine Fussnoten-Auswertung, kein DOM-Parsing, kein `document$.subscribe()`.

### Ergebnis-HTML

```html
<div class="doc-chapter-meta" role="note" aria-label="Kapitelmetadaten">
  <div class="doc-chapter-meta__byline">
    <span class="doc-chapter-meta__name">Marlon&nbsp;Merte</span>
    <span class="doc-chapter-meta__name">Felix&nbsp;Tacke</span>
  </div>
  <div class="doc-chapter-meta__details">
    <div class="doc-chapter-meta__peer">Peer Review: Gloria&nbsp;Gabriel</div>
    <div class="doc-chapter-meta__dates">
      <div class="doc-chapter-meta__created">Erstellt: 18.09.2025</div>
      <div class="doc-chapter-meta__modified">Geaendert: 23.09.2025</div>
    </div>
  </div>
</div>
```

## Custom-Komponenten und projektbezogene UI

### Cover auf der Startseite

Dateien:

- `docs/index.md`
- `docs/assets/styles/25_cover.css`

Das Buchcover auf der Startseite ist kein allgemeiner Admonition-Stil mehr in `40_custom.css`, sondern ein isolierter, eigener Layer in `25_cover.css`.

Wesentliche Merkmale der aktuellen Implementierung:

- Container: `.md-typeset .admonition.cover`
- feste Groessen statt fluider `clamp()`-Logik
- Desktopformat: `460px x 790px`
- Mobile-Variante: `360px x 620px`
- Footer bleibt ueber `margin-top: auto` am unteren Rand
- Titel, Untertitel, Herausgeber, Autor:innen und Footer sind klar getrennt
- die Startseite verwendet den aktuellen Buchtitel und Untertitel des Lehrbuchs

Zentrale Klassen:

- `.cover-title-block`
- `.cover-title-accent`
- `.cover-subtitle`
- `.cover-coordination`
- `.cover-authors`
- `.cover-authors-list`
- `.cover-footer`

### Hoermal-Admonitions und Audio-Layouts

Datei: `docs/assets/styles/40_custom.css`

Die Admonition `hoermal` ist weiterhin eine projektspezifische Kernkomponente, wurde aber aus der frueheren dokumentierten Struktur weiterentwickelt.

Container:

- `.admonition.hoermal`
- `details.hoermal`

Audio-Layout-Klassen:

- `.audio-comparison` - Wrapper fuer mehrere Vergleiche
- `.audio-pair` - responsives Zweierlayout innerhalb eines Vergleichs
- `.audio-grid` - Grid fuer gleichrangige Beispiele
- `.audio-block` - einzelne Audio-Karte
- `.audio-label` - Label innerhalb eines Audio-Blocks
- `.example`
- `.example-ipa`
- `.example-text`
- `.ipa`
- `.token-id`
- `.audio-source`

Audio-Dateien liegen derzeit in:

- `docs/assets/audiofiles/corapan/`
- `docs/assets/audiofiles/marele/`
- `docs/assets/audiofiles/promat/`

Typische Einsatzorte:

- `docs/aussprache.md`
- `docs/orthographie.md`
- `docs/fehlerlinguistik.md`
- `docs/variation/variation_aussprache.md`
- `docs/variation/variation_anrede.md`
- `docs/variation/variation_morphosyntax.md`

### Weitere Custom-Admonitions und Inline-Komponenten

Datei: `docs/assets/styles/40_custom.css`

Neben `hoermal` definiert das Projekt weitere projektspezifische UI-Bausteine, darunter:

- `expand`
- `context`
- `tip`
- `praxis`
- `oton`
- `regel`
- `cite`
- `weiterlesen`
- `.impuls` fuer hervorgehobene Reflexionsimpulse

Ausserdem werden Heading-Permalinks projektspezifisch angepasst:

- `h1` ohne sichtbaren Permalink
- `h2` bis `h4` mit positionsabhaengiger Link-Darstellung fuer Desktop und Mobile

### Citation- und Link-UX

JavaScript-Dateien:

- `docs/assets/javascripts/cite-copy.js`
- `docs/assets/javascripts/external-links.js`
- `docs/assets/javascripts/audio_src_fixup.js`
- `docs/assets/javascripts/base_path.js`

Funktionen:

- `cite-copy.js` erweitert Zitationsboxen um Copy-UX
- `external-links.js` behandelt externe Links projektspezifisch
- `audio_src_fixup.js` korrigiert Audioquellen fuer die gebaute Site
- `base_path.js` setzt `window.ZENSICAL_BASE_PATH` fuer Custom Domain und GitHub Pages

## Interaktive Karten (Leaflet)

Die Kartenarchitektur hat sich gegenueber aelteren Projektphasen sichtbar geaendert. Relevante Bestandteile:

### CSS

- `docs/assets/styles/50_map.css`

### JavaScript

- `docs/assets/javascripts/map_ui.js` - gemeinsame UI-Funktionen fuer alle Karten
- `docs/assets/javascripts/map.js` - Karte fuer Herkunftssprachen (`data-map="herkunft"`)
- `docs/assets/javascripts/map_countries.js` - Karte fuer die Hispanophonie im Anhang (`data-map="variation"`)
- `docs/assets/javascripts/map_variation_tempora.js` - Tempusvariation (`data-map="variation_tempora"`)

### Daten

- `docs/assets/data/herkunftssprachen.json`
- `docs/assets/data/countries.json`
- `docs/assets/data/variation_tempora.json`

### Aktuelles Markup

Statt des frueheren `#map-container` verwendet das Projekt jetzt den wiederverwendbaren Container:

```html
<div class="book-map" data-map="herkunft"></div>
```

Weitere `data-map`-Werte:

- `variation`
- `variation_tempora`

### Kartenfunktionen

`map_ui.js` zentralisiert heute u. a.:

- Popup-Rendering
- responsives Popup-Verhalten
- Fullscreen-Handling
- Resize-/Invalidation-Logik
- Escape-to-close fuer Popups
- Registry fuer Fullscreen-Zustand mehrerer Karten

### Typische Einsatzorte

- `docs/herkunftssprachen.md` - `data-map="herkunft"`
- `docs/anhang.md` - `data-map="variation"`
- `docs/variation/variation_tempora.md` - `data-map="variation_tempora"`

## Overrides

### `overrides/main.html`

Globaler Theme-Override fuer das Projekt.

### `overrides/partials/content.html`

Wichtigster projektspezifischer Partial-Override. Aufgaben:

- Einbinden der Actions-Partial
- Fallback-H1 fuer Seiten ohne eigenes `h1`
- Build-Time-Injektion der Kapitelmetadaten aus Frontmatter
- anschliessende Standard-Partial-Einbindung fuer Tags, Source-File, Feedback und Kommentare

## Skripte (`scripts/`)

Der Ordner enthaelt Hilfsskripte fuer Pflege- und Migrationsaufgaben:

- `fix_indentation.py`
- `migrate_expand.py`
- `migrate_hoermal.py`

Die Skripte sind Hilfswerkzeuge fuer Content-/Markup-Migrationen und nicht Teil des produktiven Site-Builds.

## Externe Abhaengigkeiten

### Lokal eingebundene Vendor-Assets

- **Leaflet** wird aktuell lokal aus `docs/assets/vendor/leaflet/` geladen, nicht mehr ueber ein CDN.

### Weitere externe Dienste

- **GoatCounter** ist in `zensical.toml` fuer Analytics konfiguriert:
  - Endpoint: `https://linguistik.goatcounter.com/count`
  - Script: `//gc.zgo.at/count.js`

### Nicht mehr aktuell

Historische Hinweise auf extern geladene Leaflet-CDNs oder auf den alten Projektordner `school-zensical` sind fuer den aktuellen Stand nicht mehr massgeblich.

## Historische Umbenennungen und veraltete Begriffe

Bei Aenderungen an Dokumentation und Code auf diese Umstellungen achten:

- Projektname heute: `linguistik.hispanistica`
- Titel des Lehrbuchs heute: *Linguistik im Spanischunterricht*
- Untertitel heute: *Ein digitales Lehrbuch fuer (angehende) Lehrkraefte*
- alter Kartencontainer `#map-container` wurde durch `.book-map` ersetzt
- `variation_grammatik.md` ist nicht mehr der aktuelle Dateiname; relevante Kapiteldateien sind heute `variation_anrede.md`, `variation_tempora.md` und `variation_morphosyntax.md`
- Cover-Stile liegen nicht mehr gesammelt in `40_custom.css`, sondern in `25_cover.css`

## Praktische Hinweise fuer weitere Entwicklung

- Bei neuen Kapiteln nach Moeglichkeit YAML-Frontmatter mit `authors`, optional `peer_review`, `created` und `last_modified` pflegen.
- Fuer neue Karten immer das `.book-map`-Markup und die bestehenden `data-map`-Konventionen nutzen.
- Cover-spezifische Anpassungen gehoeren nach `25_cover.css`, nicht nach `40_custom.css`.
- Generische Komponenten in `30_components.css`, projekt- oder inhaltsspezifische Sonderfaelle in `40_custom.css`, Kartenlayout in `50_map.css`.
- Bei Audio-Beispielen die vorhandenen `hoermal`-Layouts wiederverwenden, statt neue Einzelformate einzufuehren.
