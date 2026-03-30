# Repo Audit

> Archivnotiz: Dieses Audit dokumentiert den Zustand vor dem strukturellen Cleanup vom 30.03.2026. Pfadangaben und Befunde sind bewusst historisch.

Stand: 30.03.2026

## Gelöst


- Der Build ist nicht reproduzierbar versioniert: `.github/workflows/docs.yml:37` installiert ungepinnt `pip install zensical`, `.github/workflows/docs.yml:40` baut damit direkt produktiv, und im Repo existiert weder ein `requirements*.txt` noch ein `pyproject.toml` oder Lockfile.

## Hoch

- Interne Test-, Analyse- und Dokumentationsseiten werden mitpubliziert und landen in der Suche: `docs/admonitions.md:1` ist explizit ein Test-/Referenzdokument; `site/search.json:1` enthaelt Treffer fuer `admonitions/`, `assets/documentation/admonitions_digital_book/` sowie `assets/audio-tools/reports/audio_normalization/` und `Audio Audit Report`.
- `.claude/settings.local.json` ist versioniert, obwohl die Datei lokale Tool-Freigaben und benutzerspezifische Arbeitskontexte enthaelt: `.claude/settings.local.json:4-10` erlaubt konkrete Shell-Kommandos, `.claude/settings.local.json:12` beginnt den Block `additionalDirectories`, der auf einen benutzerlokalen Pfad verweist.
- `docs/assets/pdf/` ist vollstaendig versioniert, aber im Repo ist kein nachvollziehbarer Erzeugungsprozess fuer diese Release-Artefakte dokumentiert; `git ls-files docs/assets/pdf` liefert alle Kapitel-PDFs und das Sammelwerk als getrackte Binaerdateien.
- In `docs/assets/javascripts/map_variation_tempora.js` ist produktives Debug-Logging aktiv: `10`, `14`, `19`, `23`, `148`, `156`, `168`, `289` und weitere Stellen schreiben ungefiltert in die Browser-Konsole.

## Mittel

- Der Homepage-Override in `overrides/main.html` enthaelt toten CSS-Code: `overrides/main.html:17` definiert `.md-content__inner > h1:first-child`, obwohl auf der gebauten Startseite kein solches Element existiert; das einzige `h1` steht innerhalb des Covers in `site/index.html:796`.
- Im Repo liegt ein lokales Cache-Verzeichnis `.cache/`, waehrend `.gitignore:2-7` nur `site/`, `.venv/`, `__pycache__/` und `*.pyc` ignoriert; lokale Build-/Tool-Caches bleiben damit prinzipiell commitbar.

## Niedrig

- Der Root-Ordner `scripts/` ist leer; entweder entfaellt er ganz oder seine kuenftige Rolle sollte expliziter dokumentiert werden.
- Der Dokumentationsordner `docs/assets/documentation/zenscial_base/` ist gegenueber dem Projektnamen/Theme-Namen `zensical` inkonsistent benannt; funktional unkritisch, aber unordentlich.