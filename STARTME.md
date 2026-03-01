# 🚀 Projekt starten – Lokale Entwicklung

## Vorbereitung (einmalig)

### 1. Virtual Environment aktivieren

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

## Lokale Entwicklung starten

### Variante 1: Dev-Server (empfohlen)
```powershell
.venv\Scripts\zensical serve
```

Dies startet einen lokalen Webserver mit Hot-Reload. Die Site ist dann verfügbar unter:
```
http://localhost:8000
```

### Variante 2: Nur Bauen (ohne Server)
```powershell
.venv\Scripts\zensical build
```

Das gebaut Material landet im `site/` Verzeichnis.

## Projektstruktur

- **docs/** – Markdown-Quellen und Assets (Bilder, Audio, JS, CSS, Daten)
- **docs/assets/audiofiles/** – Audio-Beispiele (CO.RA.PAN, MAR.ELE)
- **docs/assets/data/** – JSON-Daten für Interaktive Karten
- **docs/assets/javascripts/** – Leaflet-Karten und UI-Funktionen
- **docs/assets/styles/** – CSS (Tokens, Typographie, Layout, Komponenten)
- **overrides/partials/** – Jinja2-Template Overrides
- **site/** – Gebaute HTML-Site (nicht committen!)
- **zensical.toml** – Konfigurationsdatei

## Weitere Befehle

```powershell
# Help anzeigen
.venv\Scripts\zensical --help

# Spezifische Ports oder Optionen
.venv\Scripts\zensical serve --port 8080
```

## Hinweise

- Änderungen in `docs/` werden bei `serve` automatisch neu gebaut
- CSS/JS-Änderungen können einen Hard-Refresh im Browser erfordern (Strg+Shift+R)
- Für neue Markdown-Dateien: YAML-Frontmatter mit `authors` verwenden (siehe DEV.md)
