# Audio: Bereinigung, Audit und Normalisierung

## Stand

Die Audio-Arbeit ist im Repository jetzt praktisch abgeschlossen.

- Alle `.m4a`-Referenzen wurden aus den relevanten Quell-Markups entfernt.
- Alle alten `.m4a`-Dateien unter `docs/assets/audiofiles/` wurden geloescht.
- `ffmpeg` und `ffprobe` wurden lokal per `winget` verfuegbar gemacht.
- Alle `64` vorhandenen MP3-Dateien wurden technisch mit echten `ffprobe`- und `ffmpeg`-Daten geprueft.
- Alle `64` MP3-Dateien wurden in einem Zwei-Pass-Lauf mit `loudnorm` neu gerechnet, validiert und wieder in den produktiven Bestand uebernommen.
- Die Reports unter `docs/assets/audio-tools/reports/` spiegeln den Endstand nach der produktiven Uebernahme wider.

## Was konkret geaendert wurde

- `.m4a`-Referenzen in Quell-Markups entfernt: `64`
- geloeschte `.m4a`-Dateien unter `docs/assets/audiofiles/`: `38`
- verbleibende `.m4a`-Referenzen im Repository nach Abschlusspruefung: `0`
- verbleibende `.m4a`-Dateien im Repository nach Abschlusspruefung: `0`
- MP3-Dateien im Voll-Audit geprueft: `64`
- MP3-Dateien im Voll-Lauf normalisiert: `64`
- MP3-Dateien nach Verifikation produktiv uebernommen: `64`

## Angepasste Quell-Dateien

Die Audio-Markups wurden in diesen Quelldateien auf MP3-only reduziert:

- `docs/admonitions.md`
- `docs/aussprache.md`
- `docs/orthographie.md`
- `docs/variation/variation_anrede.md`
- `docs/variation/variation_aussprache.md`
- `docs/variation/variation_morphosyntax.md`

Das Zielmuster ist jetzt durchgaengig MP3-only:

```html
<audio controls preload="metadata">
  <source src="...mp3" type="audio/mpeg">
  Dein Browser unterstuetzt das Audio-Format nicht.
</audio>
```

## Audio-Tooling unter `docs/assets/audio-tools/`

Folgende Struktur ist jetzt aktiv im Einsatz:

- `docs/assets/audio-tools/audio_audit.py`
- `docs/assets/audio-tools/audio_normalize.py`
- `docs/assets/audio-tools/normalized/README.md`
- `docs/assets/audio-tools/reports/audio_audit.csv`
- `docs/assets/audio-tools/reports/audio_manual_review.csv`
- `docs/assets/audio-tools/reports/audio_audit.md`
- `docs/assets/audio-tools/reports/audio_normalization.csv`
- `docs/assets/audio-tools/reports/audio_normalization.md`

## Technischer Endstand

### Realer Audit vor der Uebernahme

Erster Voll-Audit mit verfuegbarem `ffprobe` und `ffmpeg`:

- `64` Dateien gescannt
- `62` mal `pass`
- `2` mal `warn`
- `0` mal `fail`

Die zwei Warnungen betrafen sehr niedrige durchschnittliche Bitraten bei zwei Uruguay-Dateien, aber ohne Codec- oder Dekodierfehler.

### Vollstaendige Normalisierung

Der Produktivlauf wurde mit diesen Zielwerten ausgefuehrt:

- integrierte Lautheit: `-19.0 LUFS`
- True Peak: `-1.5 dBTP`
- Loudness Range: `7.0 LU`

Ergebnis:

- `64` Dateien verarbeitet
- `64` Dateien erfolgreich verifiziert
- `64` Dateien als `promoted` wieder nach `docs/assets/audiofiles/` uebernommen
- `0` fehlgeschlagene Dateien

Die normalisierten Vergleichsdateien bleiben parallel unter `docs/assets/audio-tools/normalized/` erhalten.

### Audit nach der produktiven Uebernahme

Abschluss-Audit auf dem finalen Bestand:

- `64` Dateien gescannt
- `63` mal `pass`
- `1` mal `warn`
- `0` mal `fail`

Der einzige verbliebene Hinweis ist:

- `corapan/URY8b580411c.mp3`
  - `sample_rate_hz`: `16000`
  - `channels`: `1`
  - `bitrate_kbps`: `33.1`
  - `decode_status`: `ok`

Das ist kein Defekt, sondern ein technischer Ausreisser unterhalb der aktuell konfigurierten Bitraten-Warnschwelle von `48 kbps`.

## Zweck der Skripte

### `docs/assets/audio-tools/audio_audit.py`

Dieses Skript untersucht rekursiv alle MP3-Dateien unter `docs/assets/audiofiles/`.

Geprueft werden:

- Datei existiert und ist lesbar
- Audio-Stream vorhanden
- Codec ist MP3
- Dauer vorhanden und groesser als `0`
- Sample Rate
- Kanalzahl
- Bitrate
- Dekodierbarkeit per `ffmpeg -f null`
- einfache Warnregeln fuer Ausreisser bei Dauer, Sample Rate, Kanaelen und Bitrate

Das Skript erkennt `ffmpeg` und `ffprobe` jetzt nicht nur ueber `PATH`, sondern auch ueber typische lokale `winget`-Installationspfade unter Windows. Zusaetzlich koennen die Binaries explizit ueber `--ffmpeg` und `--ffprobe` uebergeben werden.

Es erzeugt:

- `audio_audit.csv`
- `audio_manual_review.csv`
- `audio_audit.md`

### `docs/assets/audio-tools/audio_normalize.py`

Dieses Skript normalisiert rekursiv alle MP3-Dateien unter `docs/assets/audiofiles/` mit einem Zwei-Pass-Ansatz via `ffmpeg loudnorm`.

Eigenschaften:

- schreibt Vergleichsdateien unter `docs/assets/audio-tools/normalized/`
- behaelt die relative Unterordnerstruktur bei
- validiert jede erzeugte Datei mit `ffprobe` und einem `ffmpeg`-Dekodierlauf
- kann erfolgreiche Ergebnisse per `--promote` direkt in den produktiven Audio-Bestand zurueckkopieren
- verarbeitet die Gesamtmenge robust weiter, auch wenn einzelne Dateien scheitern sollten

Es erzeugt:

- `audio_normalization.csv`
- `audio_normalization.md`

## Reale Ausfuehrung in dieser Umsetzung

### ffmpeg lokal verfuegbar machen

```powershell
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
```

### Voll-Audit ausfuehren

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_audit.py
```

### Voll-Normalisierung mit produktiver Uebernahme ausfuehren

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_normalize.py --overwrite --promote
```

### Abschluss-Audit auf dem Endstand ausfuehren

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_audit.py
```

### Nuetzliche Varianten

Nur Analyse ohne Schreiboperationen:

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_normalize.py --dry-run
```

Teilmenge pruefen:

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_normalize.py --filter corapan/URY --limit 5
```

Explizite Tool-Pfade setzen, falls `PATH` oder Alias-Aufloesung nicht greift:

```powershell
c:/dev/linguistik.hispanistica/.venv/Scripts/python.exe docs/assets/audio-tools/audio_audit.py --ffmpeg C:/pfad/zu/ffmpeg.exe --ffprobe C:/pfad/zu/ffprobe.exe
```

## Reports und QS-Grundlage

Die zentrale Arbeitsbasis liegt unter `docs/assets/audio-tools/reports/`.

- `audio_audit.csv`: technischer Audit mit manuellen Review-Spalten
- `audio_manual_review.csv`: direkte Arbeitskopie fuer manuelle Nachpruefung
- `audio_audit.md`: Kurzuebersicht des technischen Zustands
- `audio_normalization.csv`: Datei-fuer-Datei-Status mit Messwerten und verifizierten Ausgabedaten
- `audio_normalization.md`: menschenlesbare Zusammenfassung des Voll-Laufs

## Risiken und Restpunkte

- Technisch ist der Batch abgeschlossen; es gibt keine `fail`-Faelle mehr.
- Ein einzelner Clip bleibt wegen niedriger durchschnittlicher Bitrate als `warn` markiert, obwohl Codec, Dauer und Dekodierbarkeit in Ordnung sind.
- Eine manuelle Hoerpruefung ist weiterhin sinnvoll, wenn redaktionell beurteilt werden soll, ob einzelne Clips subjektiv besser oder schlechter wirken als zuvor.

## Empfehlung fuer spaetere Automation

Sinnvoll fuer GitHub Actions oder einen Deploy-Check:

- Repo-weiter Guard gegen neue `.m4a`-Referenzen
- Repo-weiter Guard gegen neue `.m4a`-Dateien
- automatischer Lauf von `audio_audit.py` mit vorhandenem `ffprobe` und `ffmpeg`
- Build-Abbruch bei echten `fail`-Faellen im Audit
- Upload der CSV- und Markdown-Reports als Build-Artefakte

## Kurzfazit

Der Audio-Workflow ist jetzt nicht nur vorbereitet, sondern praktisch durchgezogen: Das Repository ist MP3-only, alle `64` MP3-Dateien sind technisch geprueft, alle `64` Dateien wurden neu normalisiert und produktiv uebernommen, und der finale Audit zeigt `0` technische Fehler sowie genau `1` verbliebene Warnung ohne Dekodierproblem.