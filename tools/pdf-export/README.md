# PDF Export

Dieses Werkzeug reproduziert den lokalen Kapitel-PDF-Export ueber denselben Browser-Print-Pfad wie die manuell erzeugten `print-check-*.pdf`-Dateien:

- lokale Kapitel-URL aus der laufenden Vorschau
- interne Kapitelverweise werden auf die gehostete `site_url` umgeschrieben
- Chromium-basierter Browser im Headless-Modus
- regulaere Kapitel mit `scale=0.7`
- `index.md` zusaetzlich als Titelblatt fuer eine Gesamt-PDF mit `scale=0.92`
- Leerseite nach dem Titelblatt in der Gesamt-PDF
- Seitenzahlen in der Gesamt-PDF 5 mm hoeher als zuvor, unten mittig in der Buchschrift und etwas kleiner gesetzt
- Vorwort mit grossen roemischen Seitenzahlen (`I`, `II`, `III`, ...)
- Hauptteil ab Einleitung mit arabischen Seitenzahlen (`1`, `2`, `3`, ...)
- jedes Kapitel beginnt in der Gesamt-PDF auf einer ungeraden Seite; noetige Leerseiten bleiben ohne sichtbare Seitenzahl, zaehlen intern aber mit
- `print_background=False`
- keine Kopf-/Fusszeilen

## Voraussetzungen

- laufende lokale Vorschau, z. B. `zensical serve`
- lokaler Chromium-basierter Browser wie Microsoft Edge oder Google Chrome
- Python-Umgebung des Projekts
- Python-Pakete `playwright` und `pypdf`

Installation der Tool-Abhaengigkeit:

```powershell
pip install -r tools/pdf-export/requirements.txt
```

## Standardaufruf

```powershell
python tools/pdf-export/export_chapter_pdfs.py
```

Wenn du alles mit einem einzigen PowerShell-Aufruf erledigen willst, nutze stattdessen diesen Universal-Aufruf:

```powershell
$server = $null; $startedServer = $false; try { try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/ -TimeoutSec 2 | Out-Null } catch { $server = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m","zensical","serve" -WorkingDirectory (Get-Location) -PassThru; $startedServer = $true; while ($true) { try { Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/ -TimeoutSec 2 | Out-Null; break } catch { } } } ; .\.venv\Scripts\python.exe .\tools\pdf-export\export_chapter_pdfs.py } finally { if ($startedServer -and $null -ne $server -and -not $server.HasExited) { Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue } }
```

Standardverhalten:

- liest die Kapitelreihenfolge aus `zensical.toml`
- nutzt `project.site_url` aus `zensical.toml` fuer verlinkte Kapitelziele im PDF
- exportiert alle regulaeren Kapitel ohne `index.md`
- schreibt die PDFs nach `docs/exports/einzelkapitel/`
- schreibt zusaetzlich eine Gesamt-PDF nach `docs/exports/<site_name>.pdf`
- haengt in der Gesamt-PDF nach `index.md` eine Leerseite vor den regulaeren Kapiteln ein
- nummeriert das Vorwort roemisch und den Hauptteil ab der Einleitung arabisch
- fuegt vor Kapiteln bei Bedarf eine unnummerierte Leerseite ein, damit jedes Kapitel auf einer ungeraden Seite beginnt; diese Leerseiten zaehlen in der jeweiligen Zaehlung mit
- schreibt bei gesperrter Ziel-PDF automatisch in eine Schwesterdatei mit Suffix `_neu`
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

Anderen Pfad fuer die Gesamt-PDF verwenden:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --combined-output docs/exports/gesamtband.pdf
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

Eigene Skalierung fuer das Titelblatt setzen:

```powershell
python tools/pdf-export/export_chapter_pdfs.py --cover-scale 0.92
```