# Icon-Integration im Projekt

## Kurzfazit

Das Projekt verwendet keine einheitliche, lokal installierte Icon-Library fuer alle Faelle. Stattdessen gibt es drei Integrationswege:

1. Theme-seitige Icons ueber Zensical/MkDocs per Icon-Identifier in `zensical.toml`
2. Projektlokale Icons als eingebettete SVG-Data-URIs in CSS
3. Leaflet als vendorte Kartenbibliothek mit eigener, theoretisch vorhandener Marker-Icon-Mechanik

Die praktisch wichtigsten projektspezifischen Icons werden lokal in CSS definiert und nicht zur Laufzeit aus einer externen Bibliothek geladen.

## 1. Theme-Icons ueber Zensical

Die globale Theme-Konfiguration verwendet Icon-Identifier direkt in `zensical.toml`.

### Nachweis

- `toggle.icon = "lucide/sun"`
- `toggle.icon = "lucide/moon"`
- `icon = "fontawesome/brands/creative-commons"`

### Bedeutung

Diese Schreibweise zeigt, dass das Theme Zensical die Icon-Aufloesung selbst uebernimmt. Verwendet werden hier:

- `Lucide` fuer den Light/Dark-Mode-Toggle
- `Font Awesome` fuer das Social-/Lizenz-Icon

Die Icons liegen dabei nicht als lokale SVG-Dateien in diesem Repository vor, sondern werden vom Theme ueber die jeweiligen Icon-Namen gerendert.

## 2. Native Theme-Icons aus Zensical

Einige Oberflaechenicons kommen direkt aus dem Theme-Markup und werden im Projekt nur optisch angepasst.

### Navigation Chevron

In `docs/assets/styles/20_book.css` ist explizit dokumentiert, dass das Navigations-Chevron nativ von Zensical gerendert wird:

- `.md-nav__icon` wird vom Theme ausgegeben
- das Projekt aendert nur die Farbe
- es wird bewusst kein eigenes `::after`-Icon erzeugt, um doppelte Chevron-Symbole zu vermeiden

Das bedeutet: Die Navigationsicons stammen aus dem Theme, nicht aus projektspezifischem HTML oder JavaScript.

## 3. Projektlokale Icons als eingebettete SVGs

Der groesste Teil der sichtbaren Fach- und UI-Icons wird lokal in CSS definiert. Die Grundlage ist `docs/assets/styles/40_custom.css`.

### Technische Form

Die Icons sind dort als CSS-Variablen mit `data:image/svg+xml` hinterlegt, zum Beispiel:

- `--md-typeset-hoermal-icon`
- `--md-typeset-expand-icon`
- `--md-typeset-context-icon`
- `--md-typeset-tip-icon`
- `--md-typeset-praxis-icon`
- `--md-typeset-oton-icon`
- `--md-typeset-regel-icon`
- `--md-typeset-cite-icon`
- `--md-typeset-copy-icon`
- `--md-typeset-check-icon`
- `--md-typeset-weiterlesen-icon`

Diese SVGs werden anschliessend per `mask-image` bzw. `-webkit-mask-image` auf Pseudo-Elemente oder Buttons gelegt.

### Typische Einbindung

Das Muster ist ueberall gleich:

1. SVG als CSS-Variable definieren
2. Variable auf `--md-admonition-icon` oder direkt auf `mask-image` legen
3. sichtbare Farbe ueber `background-color` oder `currentColor` steuern

### Konsequenz

Die projektspezifischen Icons sind zwar stilistisch oft an Lucide-Outline-Icons angelehnt, werden hier aber nicht als externe Laufzeit-Library geladen. Sie sind direkt als eingebettete SVG-Pfade in der CSS-Datei verankert.

## 4. Admonitions: Icons ueber CSS und Theme-Hook

Fuer Admonitions nutzt das Projekt die vom Theme vorgesehene Variable `--md-admonition-icon`, ueberschreibt deren Inhalt aber lokal.

### Beispiele

- `.admonition.hoermal { --md-admonition-icon: var(--md-typeset-hoermal-icon); }`
- `.admonition.expand { --md-admonition-icon: var(--md-typeset-expand-icon); }`
- `.admonition.cite { --md-admonition-icon: var(--md-typeset-cite-icon); }`
- weitere Varianten: `tip`, `context`, `praxis`, `regel`, `oton`, `weiterlesen`

Zusaetzlich setzen die jeweiligen `:before`-Pseudo-Elemente die Maske explizit erneut, etwa ueber:

- `-webkit-mask-image: var(--md-typeset-...-icon)`
- `mask-image: var(--md-typeset-...-icon)`

Damit ist die Integration hybrid:

- das Theme liefert den Admonition-Mechanismus
- das Projekt liefert die eigentlichen Iconformen lokal nach

## 5. Copy-Button in Zitationskaesten

Die Copy-Funktion fuer `cite`-Admonitions besteht aus JavaScript plus CSS-Iconmasken.

### Ablauf

`docs/assets/javascripts/cite-copy.js` injiziert einen Button mit der Klasse `.cite-copy-btn` in den Admonition-Titel.

Die sichtbaren Icons kommen nicht aus JavaScript, sondern aus `docs/assets/styles/40_custom.css`:

- Standardzustand: `--md-typeset-copy-icon`
- Erfolg nach Copy: `--md-typeset-check-icon`

Der Wechsel erfolgt rein ueber Klassenumschaltung:

- JS setzt `.is-copied`
- CSS tauscht daraufhin die `mask-image`

Das ist eine rein lokale UI-Icon-Implementierung ohne externe Runtime-Abhaengigkeit.

## 6. Karten-UI: Icons ebenfalls lokal in CSS

Die Kartensteuerung verwendet denselben technischen Ansatz.

In `docs/assets/styles/50_map.css` bekommt `.book-map__control::before` ein eingebettetes SVG per `mask-image`. Beim Zustand `[aria-pressed="true"]` wird auf ein zweites eingebettetes SVG umgeschaltet.

Auch hier gilt:

- kein separates Icon-Font-Paket
- keine externe SVG-Datei
- kein JS-Rendering des Icons selbst
- das Icon ist direkt als Data-URI in CSS eingebettet

## 7. Leaflet: vorhandene, aber faktisch kaum genutzte Icon-Mechanik

Leaflet ist lokal vendort unter `docs/assets/vendor/leaflet/` und wird ueber `zensical.toml` als CSS- und JavaScript-Asset eingebunden.

### Was Leaflet mitbringt

In `leaflet.css` gibt es die Standard-Mechanik fuer Markerbilder:

- `.leaflet-default-icon-path`
- `background-image: url(images/marker-icon.png);`

In `leaflet.js` ist ausserdem die uebliche `L.Icon`-/`L.Icon.Default`-Logik vorhanden.

### Projektstand

Im Projektcode werden die Karten jedoch mit `L.circleMarker(...)` aufgebaut, nicht mit `L.marker(...)` oder `L.icon(...)`.

In den drei Map-Skripten wurden keine eigenen Leaflet-Markericons gefunden:

- `docs/assets/javascripts/map.js`
- `docs/assets/javascripts/map_countries.js`
- `docs/assets/javascripts/map_variation_tempora.js`

Zusaetzlich liegen im Quellordner `docs/assets/vendor/leaflet/` nur diese Dateien:

- `leaflet.css`
- `leaflet.js`

Dateien wie `marker-icon.png` oder `marker-shadow.png` sind dort nicht vorhanden.

### Bewertung

Die Leaflet-Icon-Infrastruktur ist durch die Bibliothek prinzipiell vorhanden, spielt fuer die aktuelle Projektoberflaeche aber offenbar keine tragende Rolle. Verwendet werden stattdessen:

- Vektor-Marker via `L.circleMarker(...)`
- projektspezifische Control-Icons via CSS-Masken

## 8. Gesamtbewertung

Die Icon-Integration im Projekt basiert auf einer Kombination aus Theme-Unterstuetzung und lokalen SVG-Masken:

- Theme-Ebene: `Lucide` und `Font Awesome` ueber Icon-Identifier in `zensical.toml`
- Theme-eigene UI-Icons: z. B. das Navigations-Chevron aus Zensical
- Projekt-Ebene: eingebettete SVG-Icons in `40_custom.css` und `50_map.css`
- Leaflet-Ebene: vorhandene Standard-Icon-Logik, im Projekt aber praktisch nicht der zentrale Weg

Der dominante projektinterne Mechanismus ist eindeutig:

`data:image/svg+xml` in CSS + `mask-image` auf Pseudo-Elementen oder Buttons.