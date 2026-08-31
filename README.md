# Fördermittel-Kampagne Mathias Steinbach

Autonom aufgesetzte Kampagne für Stipendien, Bildungsfonds und bonitätsunabhängige Darlehen,
Zielhorizont Studienstart TH Köln (Präsenz), Wintersemester 2026/27.
Stand: 31.08.2026.

## Zuerst lesen

1. **`OPEN_QUESTIONS.md`** — sechs sperrende Fragen und fünf Widersprüche zwischen Belegen.
   Zwei davon (A1, A5) blockieren die beiden Programme mit dem höchsten Erwartungswert.
2. **`pipeline.md`** — 59 recherchierte Programme mit Frist, Status und Erwartungswert.
3. **`programs/01-th-koeln-deutschlandstipendium/SUBMIT_ME.md`** — die nächste Frist:
   **15.09.2026, in 15 Tagen.**

## Struktur

```
dossier/            Belege (Input, read-only) + OCR-Rohtext
assets/             cv.md (Masterlebenslauf) · narrative.md (Story-Bank)
programs/<slug>/    research.md · eligibility.md · motivation.md · review.md · SUBMIT_ME.md · anlagen/
pipeline.md         59 Programme: Typ | Summe | Frist | Status | EV | Notiz
OPEN_QUESTIONS.md   gebündelte Rückfragen
LOG.md              Einreichungsprotokoll + Nachfassfristen
```

## Was in diesem Lauf entstanden ist

- Dossier vollständig gesichtet (44 Seiten, 7 Anlagen), Fakten extrahiert
- **59 Programme** recherchiert; 19 mit dokumentierter Begründung ausgeschieden
- **11 Programmordner** angelegt, davon **4 vollständige Motivationsschreiben**
  (Deutschlandstipendium, Hans-Böckler, Cusanuswerk, Friedrich-Naumann) — jedes mit eigener
  inhaltlicher Achse, keines eine Variante eines anderen
- **7 sofort absendbare Antrags- und Anschreibenvorlagen** für Sozialleistungen
  (LVR § 112 SGB IX, SGB XII, DRV-Akteneinsicht)
- Jede Bewerbung nach der Rubrik aus §6 bewertet, mit benannter schwächster Stelle und
  Überarbeitungsprotokoll

## Zwei Dinge, die offen benannt gehören

**1. Fristen sind nicht am Original verifiziert.** §4.1 verlangt Verifikation auf der
Originalseite. In dieser Ausführungsumgebung ist der direkte Seitenabruf durch die Egress-Policy
gesperrt (`th-koeln.de`, `kfw.de`, `bva.bund.de`, `boeckler.de`, `stipendiumplus.de` u. a.
antworten mit 403 am Proxy); erreichbar war nur die Websuche. Alle Fristen stammen deshalb aus
Suchergebnis-Auszügen der Originalseiten — gut genug zum Priorisieren, nicht gut genug zum
Abgeben. **Schritt 1 jeder `SUBMIT_ME.md` ist die Bestätigung der Frist am Original.**

**2. Es wurde nichts abgeschickt.** Jedes einreichungsreife Programm braucht eine eigenhändige
Unterschrift, eine Identitätsprüfung oder einen persönlichen Zugang. Alles Inhaltliche ist
fertig; was bleibt, steht Schritt für Schritt in den `SUBMIT_ME.md`-Dateien.

## Die strategische Entscheidung dieses Laufs

Der fehlende ECTS-Stand ist der zentrale strukturelle Nachteil. Statt ihn zu umschreiben, ist die
Kampagne auf drei Kategorien konzentriert, in denen er **kein** Ausschluss ist:

1. **Erstsemester-offene Stipendien** — Deutschlandstipendium (Behinderung ist Auswahlkriterium),
   SBB-Aufstiegsstipendium (Schulnoten und Studienleistungen ausdrücklich irrelevant)
2. **Zielgruppentöpfe ohne Bewerberfeld** — LVR-Eingliederungshilfe, DRV-Teilhabeleistungen,
   SGB XII. Das sind Anspruchsprüfungen, keine Wettbewerbe; pro Stunde Aufwand liegt dort mehr
   als bei jedem Begabtenförderungswerk.
3. **Bonitätsunabhängige Finanzierung** — KfW-Studienkredit und Bildungskredit des Bundes. Von
   allen geprüften Darlehensprodukten sind das die einzigen zwei, die ohne Bürgen und ohne
   Bonitätsprüfung auskommen; DAKA und das Notlagendarlehen des Kölner Studierendenwerks
   scheitern am Bürgschaftserfordernis.

Werksbewerbungen wurden gezielt auf Runden mit **spätem Förderbeginn** gelegt (Hans-Böckler:
Juni–September 2027; Friedrich-Naumann: Sommersemester 2027). Dadurch wächst der Notenspiegel im
laufenden Verfahren nach — die Schwäche löst sich zeitlich auf, statt bekämpft werden zu müssen.
