# Linguistik im Spanischunterricht

Quellrepository des digitalen Lehrbuchs *Linguistik im Spanischunterricht*.

Projektseite: [linguistik.hispanistica.com](https://linguistik.hispanistica.com)

## Projekt

Dieses Repository enthaelt die Quellen fuer das digitale Lehrbuch *Linguistik im Spanischunterricht* (Felix Tacke, Hg., 2026), das an der Philipps-Universitaet Marburg entstanden ist. Das Buch richtet sich an Lehramtsstudierende und Lehrkraefte fuer das Fach Spanisch und verbindet sprachwissenschaftliche Grundlagen mit fachdidaktischer Reflexion.

Die Kapitel behandeln unter anderem Fehlerlinguistik, Aussprache, Orthographie, lexikalische Kreativitaet, Variation und Plurizentrik, Sprachwandel sowie Herkunftssprachen im Spanischunterricht. Die Texte wurden kollaborativ in Seminaren erarbeitet und redaktionell fuer die digitale Publikation zusammengefuehrt.

## Stack und Struktur

Die Site wird mit MkDocs und dem Theme Zensical gebaut. Fuer das Projekt gilt jetzt eine klare Trennung zwischen oeffentlichem Buchinhalt und internen Repo-Materialien:

- `docs/` enthaelt ausschliesslich publizierte Kapitel und publizierte Assets.
- `overrides/` enthaelt die Zensical-Overrides fuer Layout und Partials.
- `repo-docs/` enthaelt interne Repo-Dokumentation, Audits und Design-System-Notizen.
- `tools/audio/` enthaelt die Skripte fuer Audio-Audit und Audio-Normalisierung.
- `scripts/` enthaelt Build-Helfer, derzeit insbesondere die Footer-Release-Metadaten.

Die Versionsanzeige im Footer wird beim Build aus dem neuesten GitHub-Release erzeugt. Falls die GitHub-API im aktuellen Kontext nicht erreichbar ist, faellt der Build automatisch auf den Wert `development` zurueck.

## Lokales Setup

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/generate_footer_release.py
.venv\Scripts\zensical serve
```

Fuer einen sauberen Produktionsbuild:

```powershell
.venv\Scripts\zensical build --clean
```

Die generierte Ausgabe liegt in `site/` und gehoert nicht in die Versionskontrolle.

## Deployment

GitHub Actions baut die Site mit Python 3.12, installiert die Abhaengigkeiten aus `requirements.txt`, erzeugt die Footer-Release-Metadaten und deployt anschliessend die gebaute `site/` nach GitHub Pages.

## Publikation und Zitierweise

Das Lehrbuch ist als Open-Access-Publikation ueber das institutionelle Repositorium der Philipps-Universitaet Marburg archiviert. Der Quellcode ist zusaetzlich auf Zenodo abgelegt.

Tacke, Felix (Hg.) (2026): *Linguistik im Spanischunterricht. Ein digitales Lehrbuch fuer (angehende) Lehrkraefte*. Marburg: Philipps-Universitaet Marburg. Online: [linguistik.hispanistica.com](https://linguistik.hispanistica.com/). DOI: [https://doi.org/10.17192/openumr/598](https://doi.org/10.17192/openumr/598)

## Lizenz

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)