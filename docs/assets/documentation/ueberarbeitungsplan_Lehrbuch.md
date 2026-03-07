# Überarbeitungsplan – Linguistik im Spanischunterricht

## Gesamtbewertung

Das Lehrbuch ist insgesamt auf einem guten bis sehr guten Niveau. Die jüngeren Kapitel (5.1 Variation & Plurizentrik, 5.2 Aussprachevariation, 5.3 Variation in Grammatik und Pragmatik) sowie die Kernkapitel Aussprache und Orthographie bilden die stilistische Referenz. Das älteste Kapitel (1 Fehlerlinguistik) und das Kapitel 4 (Lexikalische Kreativität) weisen im Vergleich den größten Überarbeitungsbedarf auf. Im Folgenden werden zunächst systematische Uneinheitlichkeiten kapitelübergreifend dokumentiert, anschließend wird jedes Kapitel einzeln bewertet.

---

## I. Systematische Uneinheitlichkeiten (kapitelübergreifend)

### 1. Anrede und Ton

Die Anrede der Leser:innen ist nicht durchgängig einheitlich.

- Kap. 2 Aussprache, 5.2 Aussprachevariation: konsequentes Du (*Du kannst*, *liest Du*)
- Kap. 5.3 Grammatische Variation: ebenfalls konsequentes Du (*wenn Du*)
- Kap. 7 Herkunftssprachen: wechselt zwischen Du (*findest du*) und Sie-nahem formalem Ton; in der Empfehlungssektion dann plötzlich Fettdruck-Imperative (*Lehrkräfte sensibilisieren:*, *Schüler:innen sensibilisieren:*)
- Kap. 4 Lexikalische Kreativität: schwankt zwischen unpersönlichem Stil und direkter Anrede; in den Praxis-Admonitions durchgängig Sie-Form (*Sammeln Sie*, *Bitten Sie*, *Lassen Sie*)
- Kap. 1 Fehlerlinguistik: mischt Du (*Dir als Lehrkraft*) und informelles Du mit Kleinschreibung (*findest Du* vs. Infobox *findest Du unten*)
- Kap. 6 Sprachwandel: überwiegend unpersönlich, gelegentlich Du

Empfehlung: Einheitlich Du mit Großschreibung im gesamten Buch festlegen. Admonitions sollten ebenfalls Du verwenden, nicht Sie. Besonders betroffen: Kap. 4, 7.

### 2. Admonition-Typen: Konsistenz und Funktionalität

Die verwendeten Admonition-Klassen sind nicht durchgängig einheitlich und entsprechen nicht immer dem Admonition-Leitfaden.

| Kapitel | Verwendete Klassen | Abweichungen / Probleme |
|---|---|---|
| 1 Fehlerlinguistik | `context`, `summary`, `expand` | `context` für Lernendensprache-Definition: korrekt. Kein `tip`. |
| 2 Aussprache | `hoermal`, `info`, `regel`, `summary`, `expand` | `regel` ist nicht im Admonition-Leitfaden definiert (müsste `tip` sein). `info` statt `note`. |
| 3 Orthographie | `hoermal`, `context`, `summary`, `expand` | Korrekte Verwendung. |
| 4 Kreativität | `context`, `praxis`, `summary`, `expand` | `praxis` ist nicht im Admonition-Leitfaden definiert (müsste `tip` sein). Sechs (!) `praxis`-Boxen im Kapitel – zu viele, verdünnt die Wirkung. |
| 5.1 Plurizentrik | `tip`, `oton`, `summary`, `expand` | Korrekte Verwendung. |
| 5.2 Aussprache-V. | `hoermal`, `summary`, `expand` | Korrekte Verwendung. |
| 5.3 Grammatik-V. | `context`, `expand` | Kein `summary` vorhanden (Kapitel noch beta). |
| 6 Sprachwandel | `context`, `expand` | Kein `summary` vorhanden. Fehlend. |
| 7 Herkunftssprachen | `praxis`, `summary`, `expand` | `praxis` wieder nicht im Leitfaden. |

Empfehlung: Die Klassen `regel` und `praxis` entweder offiziell in den Admonition-Leitfaden aufnehmen oder durch `tip` ersetzen. Kapitel 6 benötigt eine Zusammenfassungsbox. Die Dichte der Admonitions in Kap. 4 reduzieren.

### 3. Bedeutungsangaben

Der MkDocs-Leitfaden schreibt typographische einfache Anführungszeichen ‚...' für Bedeutungsangaben vor. In den meisten Kapiteln wird dies befolgt, aber nicht immer konsequent.

- Kap. 2 Aussprache: weitgehend korrekt (‚gerolltes R', ‚Lispellaut')
- Kap. 4 Kreativität: teils mit einfachen runden Klammern als Bedeutungsangabe (*'Fußball'*), teils korrekt
- Kap. 6 Sprachwandel: überwiegend korrekt, aber vereinzelt gerade Anführungszeichen

Empfehlung: Systematisch in allen Kapiteln prüfen und auf ‚...' normalisieren.

### 4. Fettdruck im Fließtext

Der MkDocs-Leitfaden schließt Fettdruck in finalen Textversionen aus, außer bei systematischen Kategorienmarkierungen. Mehrere Kapitel verwenden dennoch Fettdruck im Fließtext.

- Kap. 1 Fehlerlinguistik: *Lernendensprache*, *Kriterium der Korrektheit*, *Kriterium der Angemessenheit*, *Varietätenabweichungen* – teils funktional, teils dekorativ
- Kap. 4 Kreativität: sechs fettgedruckte Wortbildungsprozess-Bezeichnungen in der Auflistung; zahlreiche Fettdrucke in Expand-Boxen (*Rekursive Derivation*, *Parasynthese* etc.)
- Kap. 5.1 Plurizentrik: *Mexiko*, *Argentinien*, *Kolumbien*, *rezeptive Varietätenkompetenz* – teilweise funktional
- Kap. 7 Herkunftssprachen: *Lehrkräfte sensibilisieren:*, *Schüler:innen sensibilisieren:*, *Mehrsprachigkeit als Ressource:*, *Didaktische Konsequenz:* – als Quasi-Überschriften verwendet, verstößt gegen Barrierefreiheitsregel

Empfehlung: Fettdruck systematisch reduzieren. In Kap. 7 die fettgedruckten Quasi-Überschriften durch echte Markdown-Überschriften (###) ersetzen. In Kap. 4 die nummerierte Liste der Wortbildungsprozesse ohne Fettdruck gestalten.

### 5. Kursivierung fremdsprachiger Beispiele

Überwiegend korrekt, aber mit Lücken: In Kap. 1 sind einige spanische Beispiele nicht kursiviert (v.a. in Tabellen). In Kap. 7 fehlt gelegentlich die Kursivierung bei Einzelwörtern.

### 6. Querverweise zwischen Kapiteln

Die Querverweise sind unterschiedlich dicht.

- Gut verlinkt: Aussprache → Orthographie, Aussprache → Aussprachevariation, Aussprache → Herkunftssprachen, Fehlerlinguistik → Variation
- Schwach verlinkt: Fehlerlinguistik → Aussprache/Orthographie (keine konkreten Beispiele aus diesen Kapiteln), Kreativität → Sprachwandel (naheliegend, fehlt), Sprachwandel → Kreativität (fehlt), Sprachwandel → Fehlerlinguistik (fehlt)
- Fehlend: Kap. 4 verweist nicht auf Kap. 6, obwohl Wortbildungswandel ein natürlicher Brückenpunkt wäre. Kap. 6 verweist nicht zurück auf Kap. 4.

Empfehlung: Siehe Abschnitt II und kapitelspezifische Empfehlungen.

### 7. Abkürzungen

Der MkDocs-Leitfaden schreibt Abkürzungen ohne Leerzeichen vor (z.B., d.h., u.a.). Dies wird überwiegend eingehalten, sollte aber in einem Durchlauf systematisch geprüft werden.

### 8. Bibliographie-Format

Das Format ist weitgehend konsistent. Zwei Abweichungen:

- Kap. 7 Herkunftssprachen: Bibliographie-Einträge mit Vorname vor Nachname (*Bernd Brehmer*, *Christiane Fäcke*) statt Nachname, Vorname – weicht vom Format aller anderen Kapitel ab.
- Kap. 1 Fehlerlinguistik: Ein Literatureintrag zu Coseriu nennt 2007 als Auflage, im Text steht jedoch Coseriu (1974) – sollte auf Konsistenz geprüft werden.

### 9. Einleitungsstil (motivierende Kapitelanfänge)

Die motivierenden Einleitungen variieren in Qualität und Stil.

- Kap. 2, 3, 5.1, 5.2: starke, problemorientierte Einleitungen mit Alltagsbezug
- Kap. 1: gut, aber etwas lang und ausladend bis zum analytischen Kern
- Kap. 4: schwächste Einleitung – die Frage *¿Cómo se dice Fernweh en español?* ist ansprechend, aber der Text gleitet schnell in eine allgemeine Einführung in Wortbildung ab
- Kap. 6: funktional, aber etwas akademisch
- Kap. 7: Einleitung ist gut und anschaulich

### 10. Fehlende Strukturelemente

- Kap. 5.3 (Grammatik-Variation): Noch im Beta-Zustand. Fehlende Abschnitte: Diminutive, Leísmo, Dequeísmo. Keine Zusammenfassungsbox, kein *Wer mehr wissen will*, keine Literaturliste.
- Kap. 6 Sprachwandel: Keine Zusammenfassungsbox (`summary`).
- Einleitung: Enthält noch den Abschnitt *Work in Progress & Peer Review*, der für eine Version 1.0 überarbeitet werden muss (steht im Widerspruch zum Vorwort, das eine abgeschlossene Version 1.0 ankündigt).

---

## II. Kohärenzstärkung: Fehlerlinguistik als roter Faden

### a) Inhalte aus Kap. 2–7 als Beispiele in Fehlerlinguistik einbinden

Das Kapitel Fehlerlinguistik beansprucht, das *zentrale Werkzeug* des Toolkits zu sein und *alle folgenden Kapitel zu begleiten*. Dieser Anspruch wird bisher nicht hinreichend durch konkrete Bezüge zu den Folgekapiteln eingelöst. Folgende Beispiele aus Kap. 2–7 könnten in Kap. 1 exemplarisch herangezogen werden:

- Aus Kap. 2 (Aussprache): Die Unterscheidung zwischen zielsprachlicher Aussprache und deutschem Akzent als Beispiel für phonetische Fehler, die keine grammatischen Fehler sind; Beispiel `[ʔo.ʔai]` statt `[o.ˈai]` als diagnostisch aufschlussreicher Fehler
- Aus Kap. 3 (Orthographie): *Spelling pronunciation* als Fehlerquelle (z.B. Aussprache von `<v>` als `[v]`, Aussprache von `<h>`); die Unterscheidung `<b>/<v>` als Illustration dafür, dass historische Orthographie Fehler erzeugt
- Aus Kap. 5.1/5.2 (Variation): Das *ustedes*-Beispiel (bereits vorhanden) könnte um die *seseo*-Frage ergänzt werden: Ist es ein Fehler, wenn eine Schülerin konsequent den *seseo* verwendet?
- Aus Kap. 7 (Herkunftssprachen): Transfer aus der Erstsprache als systematische Fehlerquelle – z.B. türkischsprachige Lernende und Artikelfehler, arabischsprachige Lernende und Vokale

### b) Kapitel 2–7: explizitere Rückverweise auf Fehlerlinguistik

Die folgenden Kapitel sollten an geeigneten Stellen auf Kap. 1 verweisen:

- Kap. 2 (Aussprache): Bei der Darstellung des deutschen Akzents wäre ein Verweis sinnvoll, dass es sich bei phonetischen Abweichungen um Fehler im Sinne der Fehlerlinguistik handelt, die diagnostisch genutzt werden können.
- Kap. 3 (Orthographie): Bei der Diskussion von *spelling pronunciation* und orthographischen Fehlerquellen fehlt ein expliziter Verweis.
- Kap. 4 (Kreativität): Bei der Diskussion von Fehlern bei Wortbildung (z.B. übergeneralisierte Affixe) sollte auf die Fehlerlinguistik verwiesen werden.
- Kap. 5.1 (Plurizentrik): Verweis auf Fehlerlinguistik bei Bewertung und Korrektur ist vorhanden – gut.
- Kap. 6 (Sprachwandel): Die Passage *Die Fehler von heute gehören manchmal zur Norm von morgen* bietet einen idealen Anknüpfungspunkt, der aber bisher nicht explizit auf Kap. 1 zurückverweist.
- Kap. 7 (Herkunftssprachen): Verweis auf Fehlerlinguistik ist vorhanden – gut.

---

## III. Kapitelspezifische Überarbeitungsbedarfe

### Kap. 1 Fehlerlinguistik (Änderungsbedarf: hoch)

Bewertungsstufe: moderat bis kritisch (strukturell funktional, aber im Vergleich mit den ausgereifteren Kapiteln stilistisch und inhaltlich am weitesten vom Zielniveau entfernt)

#### Stärken
- Grundsätzlich tragfähige Argumentationsstruktur
- Gutes Einleitungsbeispiel (*En mi ciudad hay muchas gentes*)
- Kreyer-Bezug konsequent und funktional
- Tabellen zur Fehlerreaktion nützlich

#### Schwächen und Überarbeitungsbedarf

1. Stilistisch: Das Kapitel wirkt im Vergleich mit den jüngeren Kapiteln stellenweise gesprächig und weniger kontrolliert. Sätze wie *Und so weiter und so fort* oder *Willkommen in der Schule* setzen einen informelleren Ton als in den Referenzkapiteln. Das englischsprachige Blockzitat von Kreyer (S.28–29) ist relativ lang und unterbricht den Lesefluss; eine Zusammenfassung auf Deutsch mit Kurzzitat wäre passender.

2. Strukturell: Der Abschnitt *Richtig und falsch, aber auch angemessen?* mischt mehrere Phänomene (ser/estar, Varietätenabweichungen, geographische Unterschiede) in einem einzigen Abschnitt. Die Coseriu-Expand-Box ist inhaltlich wertvoll, aber sehr lang und könnte gestrafft werden.

3. Inhaltlich: Die Zusammenfassungsbox ist zu lang und wiederholt zu viel. Die Tabellen (A und B) sind nützlich, aber die Abschnittsüberschriften verwenden `####` – das ist eine Ebene tiefer als in anderen Kapiteln üblich und erzeugt Uneinheitlichkeit.

4. Fehlende Querbezüge: s.o. unter II.

5. Admonition-Prüfung: Die `context`-Box für Lernendensprache ist funktional passend. Die `expand`-Box *Beurteilen und Kritisieren* am Anfang könnte überprüft werden: Ist sie an dieser Stelle optimal platziert, oder wäre sie besser in die Diskussion des Normbegriffs eingebettet? Die `expand`-Box *Wer mehr wissen will* ist inhaltlich gut.

6. Konkrete Maßnahmen:
    - Stil an Referenzniveau angleichen (weniger gesprächig, kontrollierter)
    - Kreyer-Zitat S. 28–29 kürzen oder auf Deutsch paraphrasieren
    - Beispiele aus Kap. 2–7 exemplarisch einbinden (s.o.)
    - Zusammenfassungsbox straffen
    - Überschriftenhierarchie an Standard angleichen (#### → ###)
    - Fettdruck im Fließtext reduzieren

---

### Kap. 4 Lexikalische Kreativität (Änderungsbedarf: hoch)

Bewertungsstufe: moderat (solide Grundstruktur, aber inhaltlich und stilistisch am weitesten von der Lehrbuch-Spezifik entfernt)

#### Stärken
- Gutes Einleitungsbeispiel (*Fernweh*)
- Systematische Darstellung der Wortbildungsprozesse
- Zahlreiche DLE-Links
- Gute Expand-Boxen mit Beispielen

#### Schwächen und Überarbeitungsbedarf

1. Zu generisch: Das Kapitel liest sich streckenweise wie eine allgemeine linguistische Einführung in die Wortbildungslehre und nicht wie ein didaktisch orientiertes Toolkit für Spanischlehrkräfte. Der spezifische Bezug zur Unterrichtspraxis ist schwächer ausgeprägt als in anderen Kapiteln. Die Frage *Warum und wie kann dieses Kapitel nun sinnvoll für Lehrkräfte und Lernende sein?* als Abschnittsüberschrift wirkt defensiv und meta-kommentierend.

2. Auflistungslastigkeit: Der Abschnitt *Wortbildungsprozesse im Spanischen* beginnt mit einer nummerierten Liste der sechs Prozesse, in der jeder Punkt fett markiert ist. Die Expand-Boxen zu jedem Prozess enthalten weitere verschachtelte Listen. Diese Struktur erzeugt einen Katalog-Charakter, der dem Lehrbuchstil widerspricht.

3. Praxis-Boxen: Sechs `praxis`-Admonitions in einem einzigen Kapitel sind zu viele. Die Inhalte sind teils repetitiv (*Sammeln Sie*, *Lassen Sie Lernende*). Hier wäre eine Reduktion auf zwei bis drei, dafür gehaltvollere Boxen sinnvoll.

4. Anredewechsel: In den Praxis-Boxen wird konsequent Sie verwendet (*Sammeln Sie*, *Bitten Sie*), im Fließtext schwankt die Anrede. Das muss vereinheitlicht werden.

5. Fehlende Querverweise:
    - Zu Kap. 6 (Sprachwandel): Wortbildung und Sprachwandel hängen eng zusammen (z.B. Grammatikalisierung von *-mente*, Entstehung neuer Verbklassen). Ein Querverweis fehlt.
    - Zu Kap. 1 (Fehlerlinguistik): Typische Fehler bei der Wortbildung (z.B. übergeneralisierte Suffixe: *\*hablación* statt *habla*) wären ein natürlicher Bezugspunkt.
    - Zu Kap. 5.1 (Variation): Variation in der Wortbildung (z.B. regionale Diminutivpräferenzen: *-ito* vs. *-ico* vs. *-ingo*) wird nicht thematisiert.

6. Fehlende didaktische Rahmung: Im Vergleich zu Kap. 2 oder 5 fehlt eine konsequente didaktische Perspektive. Andere Kapitel stellen die Frage *Was bedeutet das für meinen Unterricht?* systematisch in den Abschnitten. Kap. 4 delegiert dies ausschließlich an die Praxis-Boxen.

7. Konkrete Maßnahmen:
    - Einleitung straffen; die Meta-Frage als Überschrift streichen
    - Stärker auf spanischspezifische Wortbildungsbesonderheiten fokussieren (z.B. die hohe Produktivität von Diminutiven im Vergleich zum Deutschen, regionale Variation)
    - Die bulleted Aufzählung der sechs Prozesse in Fließtext umwandeln
    - Praxis-Boxen auf 2–3 reduzieren und inhaltlich vertiefen
    - Anrede vereinheitlichen (Du statt Sie)
    - Querverweise zu Kap. 1, 5, 6 ergänzen
    - Kontrastive Perspektive zum Deutschen stärken (wie in Kap. 2, 3, 7)
    - Expand-Boxen: Fettdruck in den Überschriften innerhalb der Boxen prüfen

---

### Einleitung (Änderungsbedarf: mittel)

Bewertungsstufe: moderat

#### Überarbeitungsbedarf

1. Der Abschnitt *Work in Progress & Peer Review* beschreibt das Projekt als offenen, laufenden Prozess. Das Vorwort kündigt jedoch eine *Version 1.0* an. Hier besteht ein Widerspruch, der für die Publikation aufgelöst werden muss. Empfehlung: Entweder den Abschnitt kürzen und in die Vergangenheitsform setzen oder in das Vorwort integrieren und als eigenständigen Abschnitt in der Einleitung streichen.

2. Stilistisch: Die Einleitung hat einen persönlicheren, essayistischen Ton (*Und natürlich gilt auch hier*, *Aber Linguistik – und das ist mir ein besonderes Anliegen*). Das passt zur Autor-Perspektive, weicht aber vom Stil der Folgekapitel ab.

3. Die Tabelle *Aufbau dieses Buches* muss aktualisiert werden, wenn die Unterkapitel von 5.3 geteilt werden.

4. Expand-Box *Was ist eine Metapher*: Inhaltlich etwas dünn und nicht auf dem Niveau der Expand-Boxen in späteren Kapiteln.

---

### Kap. 2 Aussprache (Änderungsbedarf: gering)

Bewertungsstufe: geringfügig

#### Stärken
- Didaktisch-kontrastiver Ansatz konsequent durchgehalten
- Exzellente Integration der Hörbeispiele
- Gute Verweisstruktur zu anderen Kapiteln
- Zusammenfassungsbox prägnant und korrekt

#### Überarbeitungsbedarf

1. Admonition-Klasse: `regel` ist nicht im Leitfaden definiert → in `tip` ändern oder als Klasse offiziell aufnehmen.
2. `info`-Admonition (*Regionale Diversität*): Laut Leitfaden gibt es `note`, nicht `info`. Prüfen, ob `info` als Alias funktioniert oder zu `note` geändert werden muss.
3. Geringfügig: Vereinzelt sehr lange Absätze (z.B. der Einleitungsabsatz des R-Laute-Abschnitts). Könnten aufgebrochen werden.
4. Querverweis auf Fehlerlinguistik ergänzen (s.o.).

---

### Kap. 3 Orthographie (Änderungsbedarf: gering)

Bewertungsstufe: geringfügig

#### Stärken
- Klare Struktur, didaktisch sehr gut aufgebaut
- Vorbildliche Expand-Boxen
- Gute Querverweise zu Aussprache und Aussprachevariation
- Sprachvergleiche (Deutsch, Französisch, Englisch, Italienisch) sehr gelungen

#### Überarbeitungsbedarf

1. Kleinere Tippfehler: *Orthogrpahie* (Z. 163), *Orthographien* mit variierender Schreibung (Orthographie vs. Orthoepie).
2. Blockquote für die Schriftsystem-Hierarchie (Z. 18–24): Hier wird ein Blockquote für eine Auflistung verwendet. Laut Admonition-Leitfaden wäre hier kein Blockquote, sondern ggf. ein Infokasten (`note`) oder Fließtext passender.
3. Querverweis auf Fehlerlinguistik ergänzen.

---

### Kap. 5.1 Variation & Plurizentrik (Änderungsbedarf: gering)

Bewertungsstufe: geringfügig

#### Stärken
- Stilistisch auf dem Zielniveau des Lehrbuchs
- Exzellente Integration der O-Ton-Admonition
- Konsequente didaktische Rahmung
- Gute Querverweise

#### Überarbeitungsbedarf

1. Fettdruck: Ländernamen (*Mexiko*, *Argentinien*, *Kolumbien*) und einzelne Schlüsselwörter (*rezeptive Varietätenkompetenz*) sind fett gesetzt – sollte im Hinblick auf die Fettdruck-Regel geprüft werden.
2. In *Wer mehr wissen will*: Autorennamen sind fett gedruckt (**Tacke (2011)**, **Reimann 2010 ff.**). Das widerspricht dem MkDocs-Leitfaden. In allen anderen Kapiteln sind Literaturverweise im Fließtext nicht fett gesetzt.
3. Kongruenzfehler: *Lernende, die eine amerikanische Form regelmäßig nutzen, sollten nicht korrigiert, sondern in **seiner** bewussten Formwahl bestärkt werden* → *ihrer*.
4. Verweis auf *Variation im Klassenraum* (variation_klassenraum.md): Dieses Kapitel existiert noch nicht in den Projektdateien, wird aber mehrfach verlinkt. Muss vor Publikation entweder erstellt oder die Verweise entfernt werden.

---

### Kap. 5.2 Aussprachevariation (Änderungsbedarf: gering)

Bewertungsstufe: geringfügig

#### Stärken
- Hervorragende Audiobeispiele aus dem CO.RA.PAN-Korpus
- Konsequente plurizentrische Perspektive
- Didaktisch vorbildlich strukturiert

#### Überarbeitungsbedarf

1. Das Kapitel ist mit 486 Zeilen das längste. Einzelne Abschnitte könnten gestrafft werden.
2. Verweis auf *variation_klassenraum.md*: Kapitel existiert nicht (s.o.).
3. Geringfügig: Einige Bullet-Listen in der didaktischen Empfehlung am Ende könnten in Fließtext umgewandelt werden.

---

### Kap. 5.3 Variation in Grammatik und Pragmatik (Änderungsbedarf: hoch – unfertig)

Bewertungsstufe: kritisch (beta)

#### Status

Das Kapitel ist als *beta* gekennzeichnet und noch unvollständig. Die vorhandenen Abschnitte (Tempusvariation, Anrede) sind inhaltlich auf dem Niveau der anderen Variationskapitel.

#### Fehlende Elemente

1. Drei Abschnitte sind als Platzhalter vorhanden, aber leer: Diminutive, Leísmo, Dequeísmo
2. Keine Zusammenfassungsbox
3. Kein *Wer mehr wissen will*
4. Keine Literaturliste
5. Kein `summary` vorhanden

#### Vorhandene Qualität

Die Abschnitte zu Tempusvariation und Anrede sind sehr gut geschrieben, differenziert und auf dem Niveau der Referenzkapitel. Die interaktive Karte zur Tempusvariation ist ein sehr gutes Element. Der Anrede-Abschnitt ist umfassend und vermeidet die typischen Vereinfachungen.

#### Entscheidung: Teilen

Die geplante Teilung in *5.3 Variation in der Anrede* und *5.4 Variation in der Grammatik* ist sinnvoll, da der Anrede-Abschnitt inhaltlich eigenständig und umfangreich genug ist.

---

### Kap. 6 Sprachwandel (Änderungsbedarf: mittel)

Bewertungsstufe: moderat

#### Stärken
- Innovativer Ansatz (Diachrone Betrachtung von der Gegenwart aus)
- Q&A-Format macht abstrakte Inhalte zugänglich
- Gute Verknüpfung von Sprachwandel-Theorie und konkreten Beispielen

#### Überarbeitungsbedarf

1. Fehlende Zusammenfassungsbox: Kap. 6 hat keine `summary`-Admonition. Das ist obligatorisch laut Kapitelarchitektur.
2. Fehlende Querverweise: Kein Verweis auf Kap. 1 (Fehlerlinguistik), obwohl die *Fehler von heute*-Box ein natürlicher Anknüpfungspunkt wäre. Kein Verweis auf Kap. 4 (Kreativität), obwohl Grammatikalisierung und Wortbildungswandel inhaltlich eng verbunden sind.
3. Tippfehler: *ingetraler* (Z. 43) → *integraler*; *Sprachegemeinschaften* (Z. 55) → *Sprachgemeinschaften*
4. Stil: Etwas akademischer als die Referenzkapitel. Einzelne Passagen könnten zugänglicher formuliert werden.
5. Expand-Box *Sprachwandel – linguistisch betrachtet*: Gut, aber einzelne Stellen etwas dicht. Könnte um ein bis zwei konkrete spanische Beispiele ergänzt werden.
6. Der Abschnitt zur Pluralbildung und zum Kasussystem ist inhaltlich sehr dicht und anspruchsvoll – für die Zielgruppe (Lehrkräfte) möglicherweise etwas zu detailliert. Könnte ggf. in eine Expand-Box ausgelagert werden.

---

### Kap. 7 Herkunftssprachen (Änderungsbedarf: mittel)

Bewertungsstufe: moderat

#### Stärken
- Sehr relevantes Thema, guter Perspektivwechsel
- Interaktive Karte als Ressource hervorragend
- Systematische kontrastive Darstellung

#### Überarbeitungsbedarf

1. Anredewechsel: Im Empfehlungsteil wechselt die Anrede zwischen Du und implizitem Sie. Die Fettdruck-Pseudo-Überschriften (*Lehrkräfte sensibilisieren:*, *Schüler:innen sensibilisieren:*) müssen durch echte Markdown-Überschriften (###) ersetzt werden.
2. Bibliographie-Format: Vorname vor Nachname weicht vom Standard ab (s.o.).
3. Didaktische Boxen: Die `praxis`-Box muss als Typ geprüft werden (s.o.).
4. Fettdruck-Regel: Etliche Fettdrucke im Empfehlungsteil, die entfernt werden müssen.
5. Querverweis auf Kap. 5.2 (Aussprachevariation): Ein expliziter Verweis, dass sich die lautliche Variation auch über Herkunftssprachen erschließen lässt, wäre sinnvoll.
6. Stilistisch einzelne Stellen etwas listig statt flüssig erzählt.

---

## IV. Vorwort (index.md)

Das Vorwort ist gut geschrieben und angemessen für eine Version 1.0. Zwei Punkte:

1. *Version 1.0* (Z. 69): Fettdruck entfernen.
2. **Rolf Kreyer** (Z. 73): Fettdruck des Namens ist im Fließtext nicht durch den MkDocs-Leitfaden gedeckt.
3. *Studierende als (Mit-)Autor:innen* (Z. 61): Fettdruck entfernen.
4. Prüfen, ob das Vorwort und die Einleitung in ihrem Verhältnis zueinander stimmig sind (beide beschreiben den Entstehungsprozess; die Einleitung enthält zusätzlich den *Work in Progress*-Abschnitt).

---

## V. Priorisierung der Überarbeitung

| Priorität | Kapitel | Geschätzter Aufwand |
|---|---|---|
| 1 (hoch) | 5.3 Grammatik-Variation (Fertigstellung) | hoch |
| 2 (hoch) | 4 Lexikalische Kreativität (inhaltliche Neuausrichtung, Stilangleichung) | hoch |
| 3 (hoch) | 1 Fehlerlinguistik (Stilangleichung, Kohärenzstärkung, Querbezüge) | mittel–hoch |
| 4 (mittel) | 7 Herkunftssprachen (Formatierung, Anrede, Bibliographie) | mittel |
| 5 (mittel) | 6 Sprachwandel (Summary ergänzen, Querverweise, Tippfehler) | gering–mittel |
| 6 (mittel) | Einleitung (Work-in-Progress anpassen, Tabelle aktualisieren) | gering |
| 7 (gering) | 2 Aussprache (Admonition-Klassen prüfen) | gering |
| 8 (gering) | 3 Orthographie (Tippfehler, Blockquote prüfen) | gering |
| 9 (gering) | 5.1 Plurizentrik (Fettdruck, Kongruenz, fehlende Kapitelverweise) | gering |
| 10 (gering) | 5.2 Aussprachevariation (Straffung, fehlende Kapitelverweise) | gering |

---

## VI. Nächste Schritte

Empfohlen wird, die Überarbeitung Kapitel für Kapitel durchzuführen, beginnend mit den Kapiteln höchster Priorität. Für jedes Kapitel sollte der folgende Ablauf gelten:

1. Abgleich mit den hier dokumentierten kapitelspezifischen Bedarfen
2. Durchlauf der systematischen Uneinheitlichkeiten (Abschnitt I) am konkreten Kapitel
3. Stilistische Angleichung an die Referenzkapitel
4. Prüfung und ggf. Ergänzung der Querverweise
5. Prüfung und ggf. Anpassung der Admonitions
6. Abschließende Lektüre auf Tippfehler und Formatierung
