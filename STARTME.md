# Projekt starten - Lokale Entwicklung

## Einmaliges Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/generate_footer_release.py
```

## Dev-Server starten

```powershell
.venv\Scripts\zensical serve
```

Die Site ist dann unter `http://localhost:8000` verfuegbar.

## Sauberen Build erzeugen

```powershell
.venv\Scripts\zensical build --clean
```

Die gebaute Ausgabe landet in `site/`.

## Orientierung

- `docs/` enthaelt nur publizierte Buchinhalte und publizierte Assets.
- `repo-docs/` enthaelt interne Repo-Dokumentation.
- `tools/audio/` enthaelt Audio-Hilfsskripte; Reports bleiben lokal.
- `overrides/` enthaelt die Template-Overrides fuer Zensical.

## Nuetzliche Varianten

```powershell
.venv\Scripts\zensical --help
.venv\Scripts\zensical serve --port 8080
```

## Hinweise

- Aenderungen in `docs/` werden bei `serve` automatisch neu gebaut.
- CSS- oder JS-Aenderungen koennen einen Hard-Refresh im Browser erfordern.
- Fuer neue oeffentliche Kapitel gehoert der Inhalt nach `docs/`; interne Notizen gehoeren nach `repo-docs/`.
