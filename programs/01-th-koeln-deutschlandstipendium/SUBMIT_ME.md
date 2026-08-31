# SUBMIT_ME — Deutschlandstipendium TH Köln

**Status:** `READY_MANUAL` · **Frist: 15.09.2026** · **verbleibend: 15 Tage**
**Warum manuell:** Die Teilnahmeerklärung muss eigenhändig auf Papier unterschrieben werden, und
die Bewerbung läuft über ein Portal mit persönlichem Hochschul-Login. Beides kann ich nicht
übernehmen. Alles Inhaltliche ist fertig.

**Zeitbedarf für dich: rund 45 Minuten.** Bitte nicht auf die letzte Woche legen — Portale sind
kurz vor Fristende regelmäßig überlastet.

---

## Schritt 1 — Frist und Unterlagen am Original bestätigen (5 Min., **zuerst**)

Öffne https://www.th-koeln.de/studium/deutschlandstipendium_225.php und prüfe:
- [ ] Bewerbungszeitraum endet tatsächlich am **15.09.2026** (recherchierter Stand: 15.08.–15.09.2026)
- [ ] Uhrzeit des Fristendes (viele Portale schließen um 23:59, manche um 12:00)
- [ ] Liste der geforderten Unterlagen — ist außer Teilnahmeerklärung und Motivationsschreiben
      noch etwas verlangt (Lebenslauf, Foto, Immatrikulationsbescheinigung, Abiturzeugnis)?
- [ ] Link zum Bewerbungsportal

Wenn die Liste von der unten abweicht: melde es, ich passe die Unterlagen an. Diese Prüfung ist
nötig, weil der direkte Seitenabruf in meiner Ausführungsumgebung gesperrt war — meine Angaben
stammen aus Suchauszügen, nicht aus der Seite selbst.

## Schritt 2 — Teilnahmeerklärung (10 Min.)

- [ ] Formular herunterladen:
      https://www.th-koeln.de/mam/downloads/deutsch/studium/bewerbung_zulassung/stipendien/anleitung_zur_bewerbung_und_teilnahmeerklarung_deutschlandstipendium.pdf
- [ ] Ausdrucken, **handschriftlich** ausfüllen und unterschreiben (eine eingefügte Bilddatei der
      Unterschrift genügt ausdrücklich nicht)
- [ ] Als PDF scannen oder abfotografieren, gerade, vollständig, lesbar
- [ ] Ablegen unter `programs/01-th-koeln-deutschlandstipendium/anlagen/teilnahmeerklaerung.pdf`

## Schritt 3 — Motivationsschreiben (10 Min.)

- [ ] `motivation.md` öffnen, Datum aktualisieren
- [ ] Anrede prüfen: falls die Ausschreibung eine namentliche Ansprechperson nennt, diese einsetzen
- [ ] In ein PDF wandeln, eine Seite, Standardschrift 11 pt, Rand 2,5 cm
- [ ] **Vor dem Export einmal laut lesen.** Der Text ist auf Sprechrhythmus geschrieben; Stellen,
      an denen du beim Lautlesen stolperst, sind Stellen, an denen ein Gremium stolpert.
- [ ] Ablegen als `anlagen/motivationsschreiben.pdf`

## Schritt 4 — Ergänzende Anlagen bereitlegen (10 Min.)

Auch wenn sie nicht ausdrücklich verlangt sind — falls das Portal Uploadfelder anbietet, gehören
diese hinein, in dieser Reihenfolge:

1. [ ] **Lebenslauf** — aus `assets/cv.md` als PDF (Redaktionsnotiz **vorher entfernen**, die ist intern)
2. [ ] **Abiturzeugnis** — lesbare Kopie. Achtung: Der Scan im Dossier ist stellenweise
       unleserlich (C2). Bitte frisch scannen; die Note 1,4 / 770 Punkte ist das tragende
       Leistungsargument der gesamten Bewerbung und muss lesbar sein.
3. [ ] **Immatrikulationsbescheinigung WiSe 2026/27** (C1)
4. [ ] **Schwerbehindertenausweis** (Vorder- und Rückseite) — nur hochladen, wenn ein Feld für
       „besondere persönliche Umstände" existiert. Der Status ist im Motivationsschreiben genannt
       und sollte belegbar sein.
5. [ ] **NABU-Bescheinigung vom 14.02.2014** — der einzige Fremdbeleg für das Engagement
6. [ ] Bewerbungsfoto, falls gefordert (C11)

**Nicht hochladen:** Rentenbescheid, JobCenter-Bescheid, KAI-Testblatt. Der Rentenbescheid enthält
Gesundheits- und Kontodaten, die hier niemand braucht; das KAI-Blatt ist unausgefüllt (siehe
OPEN_QUESTIONS D) und würde die Bewerbung schwächen statt stärken.

## Schritt 5 — Einreichen (5 Min.)

- [ ] Im Portal einloggen, Bewerbung anlegen
- [ ] Alle PDFs hochladen, Dateinamen prüfen (`Nachname_Vorname_Dokument.pdf`)
- [ ] Vorschau kontrollieren: Ist jedes PDF vollständig und richtig herum?
- [ ] Absenden
- [ ] **Bestätigungsseite als PDF speichern oder abfotografieren** und die Bestätigungsmail
      aufbewahren — ohne Eingangsnachweis gibt es später keine Handhabe

## Schritt 6 — Protokollieren (2 Min.)

- [ ] In `LOG.md` eintragen: Datum, Uhrzeit, Kanal, Bestätigungsnummer
- [ ] In `pipeline.md` Zeile 1 den Status von `READY_MANUAL` auf `SUBMITTED` setzen
- [ ] Nachfassfrist notieren: bei ausbleibender Rückmeldung **Mitte November 2026** nachfragen

---

## Wenn etwas schiefgeht

- **Portal verlangt Angaben zum Einkommen:** Nicht raten. Es fehlt der aktuelle Stand
  (OPEN_QUESTIONS A4 — JobCenter-Folgebescheid, BAföG-Ausgang). Belegbar und aktuell ist allein
  der Rentenzahlbetrag von 317,29 € monatlich ab 01.09.2026. Alles darüber hinaus erst nach
  Klärung eintragen; eine falsche Einkommensangabe im Förderantrag ist der teuerste aller Fehler.
- **Portal verlangt einen Notenspiegel:** Bescheinigung der Hochschule beilegen, dass noch keine
  Prüfungsleistungen vorliegen, weil das Präsenzstudium erst zum WiSe 2026/27 beginnt. Nicht
  leer lassen und nicht umschreiben.
- **Frist ist entgegen meiner Recherche bereits abgelaufen:** Sofort melden. Dann rückt das
  Programm auf `DEFER` für die Runde 2027/28 (pipeline.md Nr. 26) und die freigewordene Zeit
  geht an Hans-Böckler (Frist 02.11.) und Cusanuswerk (01.11.).
