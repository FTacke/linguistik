# PDF Export

Dieses Werkzeug reproduziert den lokalen Kapitel-PDF-Export ueber denselben Browser-Print-Pfad wie die manuell erzeugten `print-check-*.pdf`-Dateien:

- lokale Kapitel-URL aus der laufenden Vorschau
- interne Kapitelverweise werden auf die gehostete `site_url` umgeschrieben
- Chromium-basierter Browser im Headless-Modus
- `scale=0.7`
- `print_background=False`
- keine Kopf-/Fusszeilen

## Voraussetzungen

- laufende lokale Vorschau, z. B. `zensical serve`
- lokaler Chromium-basierter Browser wie Microsoft Edge oder Google Chrome
- Python-Umgebung des Projekts
- Python-Paket `playwright`

Installation der Tool-Abhaengigkeit:

```powershell
pip install -r tools/pdf-export/requirements.txt
```

## Standardaufruf

```powershell
python tools/pdf-export/export_chapter_pdfs.py
```

Standardverhalten:

- liest die Kapitelreihenfolge aus `zensical.toml`
- nutzt `project.site_url` aus `zensical.toml` fuer verlinkte Kapitelziele im PDF
- exportiert alle regulaeren Kapitel ohne `index.md`
- schreibt die PDFs nach `docs/exports/einzelkapitel/`
- nutzt standardmaessig `http://127.0.0.1:8000/`

## Nuetzliche Optionen

Nur bestimmte Kapitel exportieren:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --only aussprache.md "2 Aussprache"
```

Anderen Browser explizit setzen:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --browser "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

Anderen Vorschau-Host verwenden:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --base-url http://127.0.0.1:8001/
```

Andere oeffentliche Basis-URL fuer PDF-Links verwenden:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --public-base-url https://linguistik.hispanistica.com/
```

Nur Kapitelauflistung pruefen:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --dry-run
```