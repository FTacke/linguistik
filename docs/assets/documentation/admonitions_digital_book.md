# Admonitions im digitalen Buch

Strukturierte Übersicht der im Projekt verwendeten Admonition-Typen – mit Beschreibung von **Form (Gestaltung)**, **Funktion (didaktische Rolle)** und **empfohlener Verwendung**.

---

# I. Inhaltsebene

## 1. `!!! context`

### Icon: (i)

### Form

* Neutrale Hintergrundfarbe (leicht akzentuiert)
* Linke Akzentlinie oder dezente Icon-Markierung
* Titel optional sichtbar
* Normale Blockbreite (Textbreite)

### Funktion

* Sachliche Zusatzinformation
* Präzisierungen
* Terminologische Hinweise
* Ergänzende Kontextualisierung

Didaktische Rolle: unterstützt das Verständnis ohne Hierarchisierung.

**Länge:** kurz bis mittellang
**Ausklappbar:** technisch möglich (`??? context`), empfohlen nur bei rein ergänzendem Zusatzmaterial.

---

## 2. `!!! expand`

### Icon: Kompass

### Form

* Klar als Vertiefung gekennzeichnet
* Optional einklappbar
* Visuell ruhiger als `regel`, aber klar abgegrenzt

### Funktion

* Vertiefung
* Exkurs
* Erweiterte Differenzierung
* Komplexitätserhöhung

Didaktische Rolle: inhaltliche Erweiterung ohne Überladung des Haupttexts.

**Länge:** variabel
**Ausklappbar:** empfohlen (Standard: `??? expand`)

---

# II. Didaktische Ebene

## 3. `!!! regel`

### Icon: Check-Haken

### Form

* Klar abgegrenzter Block
* Deutliche, aber nicht alarmierende Akzentfarbe
* Titel sichtbar und knapp formuliert
* Kompakte, prägnante Struktur

### Funktion

* Explizite Formulierung einer grammatischen oder fachlichen Regel
* Merksatzcharakter
* Systematische Verdichtung

Didaktische Rolle: Markierung zentraler Wissenspunkte.

**Länge:** kurz bis mittellang (max. 5–8 Zeilen)
**Ausklappbar:** technisch möglich, aber **nicht empfohlen** – Regeln sollen sichtbar bleiben.

---

## 4. `!!! tip`

### Icon: Flamme (noch Standard-Mkdocs)

### Form

* Positiv konnotierte Farbgebung
* Icon (z.B. Glühbirne)
* Klar abgegrenzter Container

### Funktion

* Lernstrategie
* Anwendungshinweis
* Vereinfachende Eselsbrücke
* Praktischer Mehrwert

Didaktische Rolle: Unterstützung des Lernprozesses.

**Länge:** kurz
**Ausklappbar:** technisch möglich, aber in der Regel **nicht empfohlen**.

---

## 5. `!!! praxis`

### Icon: Glühbirne

### Form

* Deutlich strukturiert
* Praxisnahe Farbnuance
* Klare Arbeitsaufforderung oder Szenario

### Funktion

* Anwendung in realistischen Kontexten
* Transferaufgaben
* Handlungsorientierte Übungen
* Reflexionsimpulse

Didaktische Rolle: Transfer und Aktivierung.

**Länge:** mittellang bis länger
**Ausklappbar:** möglich (`??? praxis`), empfohlen bei umfangreichen Aufgaben oder Szenarien.

---

# III. Methodisch / medial

## 6. `!!! hoermal`

### Icon: Lautsprecher

### Form

* Spezifisches Audio-Icon
* Akzentfarbe des Projekts
* Optional integrierter Audio-Player

### Funktion

* Hörbeispiele
* Phonetik-/Aussprachematerial
* Auditive Analyse

Didaktische Rolle: multimodale Erweiterung.

**Länge:** kurz bis mittellang
**Ausklappbar:** optional, abhängig vom Umfang.

---

## 7. `!!! oton`

### Icon: Anführungszeichen

### Form

* Spezifisches Zitat-Icon
* Akzentfarbe des Projekts
* Optional Audio oder längerer Textblock

### Funktion

* Erfahrungsberichte
* Perspektiven
* Stimmen aus Praxis oder Forschung

Didaktische Rolle: diskursive und erfahrungsbezogene Erweiterung.

**Länge:** mittellang
**Ausklappbar:** optional bei längeren Beiträgen.

---

# Systematische Hierarchie

| Ebene    | Typ     | Kernfunktion           | Typische Länge | Ausklappbar (technisch) | Empfohlener Standard |
| -------- | ------- | ---------------------- | -------------- | ----------------------- | -------------------- |
| Inhalt   | note    | Kontext / Präzisierung | kurz–mittel    | ja                      | nur bei Zusatz       |
| Inhalt   | expand  | Vertiefung             | variabel       | ja                      | ja                   |
| Didaktik | regel   | Verdichtung / Merksatz | kurz–mittel    | ja                      | nein                 |
| Didaktik | tip     | Lernhilfe              | kurz           | ja                      | nein                 |
| Didaktik | praxis  | Anwendung / Transfer   | mittel–lang    | ja                      | bei Bedarf           |
| Methodik | hoermal | Multimodalität (Audio) | kurz–mittel    | ja                      | optional             |
| Methodik | oton    | Erfahrungsdimension    | mittel         | ja                      | optional             |

---

# Grundprinzipien

1. **Alle Admonitions können technisch ein- oder ausgeklappt werden** (`!!!` / `???`).
2. Die Entscheidung zur Ausklappbarkeit ist **didaktisch**, nicht technisch motiviert.
3. Zentrale Inhalte (`regel`) bleiben sichtbar.
4. Vertiefungen (`expand`) sind standardmäßig einklappbar.
5. Übernutzung schwächt Hierarchie und Lesefluss.

---

Dieses Dokument dient als verbindliche Referenz für Struktur- und Designentscheidungen im Projekt.
