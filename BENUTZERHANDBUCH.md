# Benutzerhandbuch für BLATU 1.5.4

## 1. Einleitung

Willkommen bei **BLATU** (Blasrohr Turnier Verwaltung)! Diese Software wurde entwickelt, um die Organisation, Durchführung und Auswertung von Blasrohr-Turnieren so einfach und effizient wie möglich zu gestalten. Ebenso eignet sich BLATU hervorragend für Bogen- oder andere Schießturniere.

Von der Einrichtung des Turniers über die Teilnehmer-, Gruppen-, Startgeld- und Mannschaftsverwaltung bis hin zur Ergebniseingabe (manuell oder mobil per Smartphone), dem Stechschießen bei Gleichstand, einer Live-Anzeige für Zuschauer sowie dem Export von PDF-Listen, Schießzetteln und Word-Urkunden finden Sie hier alle Werkzeuge unter einer Oberfläche.

Dieses Handbuch führt Sie schrittweise durch sämtliche Reiter und Funktionen der Anwendung.

---

## 2. Erste Schritte: Das Turnier einrichten

Alles beginnt im Reiter **„Turnierverwaltung“**. Hier legen Sie die grundlegenden Parameter für Ihren Wettkampf fest:

*   **Name des Turniers:** Geben Sie einen aussagekräftigen Namen für die Veranstaltung ein (z. B. „Vereinsmeisterschaft 2026“).
*   **Datum:** Tragen Sie das Datum des Wettkampfs ein (z. B. `15.10.2026`). Dieses erscheint später auf allen Ergebnislisten, Startlisten, Schießzetteln und Urkunden.
*   **Anzahl Passen:** Legen Sie fest, wie viele Passen (Serien) pro Schütze geschossen werden (`1` bis `100`).
*   **Ergebnisse als 1. und 2. Hälfte anzeigen (statt einzelne Passen):** Wenn Sie diese Option aktivieren, werden die Ergebnisse in den Auswertungen und PDFs nicht als einzelne Passen (`P1`, `P2`, ...), sondern als Summe der ersten und zweiten Wettkampfhälfte dargestellt.
    *   **Wichtiger Hinweis:** Diese Option ist nur verfügbar, wenn eine **gerade** Anzahl an Passen eingestellt ist.

Klicken Sie nach der Eingabe auf **„Einstellungen speichern“**. Im unteren Bereich **„Aktuelle Einstellungen“** wird Ihre aktive Konfiguration zur Kontrolle zusammengefasst.

### 2.1. Bankverbindung für Startgeld hinterlegen

Wenn Sie das Startgeld per Überweisung einsammeln möchten, können Sie die Bankdaten direkt hinterlegen. Diese werden dann automatisch auf die PDF-Startlisten für die einzelnen Vereine gedruckt.

1.  Aktivieren Sie die Checkbox **„Startgeld erheben und Bankdaten auf PDFs anzeigen“**.
2.  Füllen Sie die nun freigeschalteten Felder aus:
    *   **Kontonummer (IBAN)**
    *   **BIC**
    *   **Bankname**
    *   **Kontoinhaber**
    *   **Zu bezahlen bis:** Fälligkeitsdatum für die Überweisung (z. B. `tt.mm.jjjj`).
3.  Klicken Sie auf **„Einstellungen speichern“**.

Ist die Checkbox deaktiviert, sind die Eingabefelder ausgegraut und es werden keine Zahlungshinweise auf den Vereins-PDFs ausgegeben.

**Tipp:** Mit dem Button **„Zurücksetzen“** setzen Sie die Turniereinstellungen nach einer Sicherheitsabfrage wieder auf die Standardwerte zurück.

---

## 3. Teilnehmer und Klassen verwalten

### 3.1. Wettkampfklassen und Startgeld anlegen (Reiter „Klassenverwaltung“)

Bevor Sie Schützen erfassen, definieren Sie im Reiter **„Klassenverwaltung“** die benötigten Wettkampfklassen:

*   **Klasse anlegen:** Geben Sie im Feld **„Klassenname“** die Bezeichnung ein (z. B. „Schülerklasse A“, „Damen“, „Herren I“) und klicken Sie auf **„Klasse hinzufügen“**.
*   **Startgeld (€) festlegen:** In der Tabelle **„Vorhandene Klassen“** sehen Sie neben dem Klassennamen die Spalte **„Startgeld (€)“**.
    *   Führen Sie einen **Doppelklick** auf den Betrag in der Spalte „Startgeld (€)“ aus, um ihn direkt in der Tabelle zu bearbeiten.
    *   Tragen Sie den gewünschten Euro-Betrag ein (z. B. `12,50` oder `12.50`) und bestätigen Sie mit der `Enter`-Taste (oder klicken Sie außerhalb des Feldes).
    *   **Hinweis:** Wird das Startgeld einer Klasse nachträglich geändert, wird der Bezahlstatus bereits angelegter Schützen dieser Klasse automatisch auf **„Überprüfen“** gesetzt.
*   **Klassen löschen:** Über **„Ausgewählte Klasse löschen“** oder **„Alle Klassen löschen“** entfernen Sie nicht mehr benötigte Klassen. Befinden sich noch Schützen in einer Klasse, warnt das Programm vorab.

### 3.2. Schützen anlegen und bearbeiten (Reiter „Schützenverwaltung“)

Wechseln Sie in den Reiter **„Schützenverwaltung“**, um die Teilnehmer Ihres Turniers zu erfassen:

*   **Schütze hinzufügen:** Tragen Sie **Name**, **Vorname** und optional **Verein** ein und wählen Sie die passende **Klasse** aus der Dropdown-Liste. Klicken Sie anschließend auf **„Schütze hinzufügen“**.
*   **PIN für die Online-Eingabe:** Jedem Schützen wird automatisch eine 4-stellige **PIN** zugewiesen, falls Sie das Feld leer lassen. Über das Feld **„PIN“** und den Button **„Generieren“** können Sie die PIN auch gezielt festlegen oder neu würfeln.
*   **Schütze bearbeiten:** Doppelklicken Sie auf einen Schützen in der Liste oder markieren Sie ihn und klicken Sie unten auf **„Bearbeiten“**. Die Daten werden in die Eingabefelder geladen. Passen Sie die Angaben an und klicken Sie auf **„Schütze aktualisieren“**.
    *   *Gut zu wissen:* Wenn Sie den Namen oder die Klasse eines Schützen nachträglich korrigieren, bleiben dessen bereits eingetragene Ergebnisse und Mannschaftszuordnungen automatisch erhalten. Bei einem Klassenwechsel wird der Startgeld-Status zur Sicherheit auf „Überprüfen“ gesetzt.
*   **Schützen löschen:** Markieren Sie einen Schützen und klicken Sie auf **„Ausgewählten löschen“** oder leeren Sie die gesamte Liste über **„Alle Schützen löschen“**.
*   **Sortieren:** Ein Klick auf eine beliebige Spaltenüberschrift (`Name`, `Vorname`, `Klasse`, `Verein`, `Gruppe`, `Scheibe`, `PIN`) sortiert die Tabelle auf- bzw. absteigend.

### 3.3. Automatische Zuweisung zu Gruppen und Scheiben

Oberhalb der Schützenliste können Sie alle erfassten Schützen automatisch auf Gruppen und Scheiben verteilen:

1.  **Max. Scheiben:** Geben Sie ein, wie viele Scheiben pro Gruppe maximal zur Verfügung stehen (Standard: `3`).
2.  **Zuweisungsart:** Wählen Sie die gewünschte Strategie:
    *   **Nach Eingabe:** Zuweisung in der Reihenfolge, in der die Schützen angelegt wurden.
    *   **Zufällig:** Die Teilnehmer werden zufällig auf die Gruppen und Scheiben gemischt.
    *   **Nach Klassen:** Die Schützen werden vor der Verteilung nach ihrer Wettkampfklasse sortiert.
3.  Klicken Sie auf **„Automatisch Zuweisen“**.

### 3.4. Manuelle Zuweisung

Im Bereich **„Manuelle Zuweisung“** unterhalb der Schützenliste können Sie einem ausgewählten Schützen gezielt eine **Gruppe** und **Scheibe** zuweisen:

1.  Markieren Sie den Schützen in der Tabelle.
2.  Tragen Sie die gewünschte **Gruppe** und **Scheibe** als Zahl ein.
3.  Klicken Sie auf **„Ausgewählten Schützen zuweisen“**. Die Software prüft automatisch, ob dieser Scheibenplatz in der Gruppe bereits vergeben ist.

---

## 4. Gruppeneinteilung verwalten

Der Reiter **„Gruppenverwaltung“** bietet eine detaillierte Übersicht über alle Gruppen sowie Werkzeuge zur Zeitplanung und zum PDF-Export:

*   **Zweigeteilte Ansicht:**
    *   Links (**„Gruppenübersicht“**) sehen Sie alle bereits eingeteilten Schützen, sortiert nach Gruppe und Scheibe.
    *   Rechts (**„Nicht zugewiesene Schützen“**) sind alle Teilnehmer aufgelistet, die noch keiner Gruppe/Scheibe zugeteilt wurden.
*   **Uhrzeit für Gruppe festlegen:**
    1.  Wählen Sie in der linken Liste einen beliebigen Schützen der gewünschten Gruppe aus.
    2.  Tragen Sie im Bereich **„Uhrzeit für Gruppe festlegen“** die Startzeit ein (z. B. `10:00`).
    3.  Klicken Sie auf **„Für ausgewählte Gruppe speichern“**.
*   **Zuweisung für Schützen ändern:**
    1.  Wählen Sie einen Schützen aus der linken oder rechten Liste aus.
    2.  Geben Sie rechts unten im Bereich **„Zuweisung für Schützen ändern“** die neue **Gruppe** und **Scheibe** ein.
    3.  Klicken Sie auf **„Zuweisung ändern“** (inkl. automatischer Prüfung auf Doppelbelegung).
*   **PDF-Listen direkt erstellen:**
    *   **„Gruppen-PDF erstellen“:** Erzeugt eine übersichtliche PDF-Gesamtliste aller Gruppen mit Uhrzeiten und Scheibenzuweisungen.
    *   **„Startliste Vereine“:** Erzeugt in einem gewählten Zielordner für jeden teilnehmenden Verein eine eigene PDF-Startliste inkl. Startzeiten, Scheiben, Startgeld-Summe und (sofern aktiviert) Überweisungsdaten.

---

## 5. Ergebnisse eingeben, Stechschießen und Auswertung

Wechseln Sie in den Reiter **„Ergebniseingabe“**, um die geschossenen Ringe zu erfassen.

1.  **Schütze suchen & auswählen:** Nutzen Sie bei Bedarf das Suchfeld links oben (filtert nach Name, Vorname oder Klasse) oder sortieren Sie die Liste per Klick auf die Spaltenüberschriften. Sobald Sie einen Schützen in der Liste anklicken (oder doppelklicken / `Enter` drücken), werden seine bisherigen Ergebnisse auf der rechten Seite geladen.
2.  **Passen eingeben:** Tragen Sie für jede Passe die erreichte Ringzahl als **ganze Zahl** ein. Das **Gesamtergebnis** wird während der Eingabe sofort automatisch berechnet.
3.  **Zusatzwertung:** Geben Sie im Bereich **„Zusatzwertung“** die **Anzahl 10er** und **Anzahl 9er** ein. Diese entscheiden bei Ringgleichheit über die Platzierung.
4.  **Speichern:** Klicken Sie auf **„Ergebnisse speichern“**.
5.  **Liste aktualisieren:** Falls parallel Ergebnisse über die Online-Eingabe eingehen, aktualisiert sich die Ansicht automatisch; zusätzlich können Sie jederzeit auf **„Liste aktualisieren“** klicken.

### 5.1. Gesamtergebnisse anzeigen (Fenster „Ergebnisanzeige“)

Mit einem Klick auf **„Ergebnisanzeige“** öffnet sich ein eigenes Fenster mit den vollständigen Ranglisten aller Klassen.
*   Bei vielen Passen steht Ihnen eine horizontale Scrollbar (oder `Umschalt` + Mausrad) zur Verfügung.
*   Über die untere Leiste können Sie die Ansicht **„Aktualisieren“**, ein **„🎯 Stechschießen“** starten oder direkt per **„PDF erstellen“** die Ergebnisliste als PDF exportieren.

### 5.2. Stechschießen bei Punkt-Gleichstand (`🎯 Stechschießen`)

Haben zwei oder mehr Schützen derselben Klasse exakt dasselbe reguläre Ergebnis (**gleiche Gesamtringzahl, gleiche Anzahl 10er und gleiche Anzahl 9er**), können Sie ein Stechschießen durchführen:

1.  Klicken Sie im Reiter **„Ergebniseingabe“** oder im Fenster **„Ergebnisanzeige“** auf den Button **„🎯 Stechschießen“**.
2.  Das Programm sucht automatisch in allen Klassen nach Punkt-Gleichständen (mit Gesamtergebnis > 0). Liegt kein Gleichstand vor, erscheint ein entsprechender Hinweis.
3.  Im Dialog **„Stechschießen bei Punkt-Gleichstand“** werden alle betroffenen Gleichstands-Gruppen übersichtlich mit Klasse, Platz und regulärem Ergebnis aufgelistet:
    *   Aktivieren Sie das Häkchen **„Stechen“** bei den Schützen, die am Stechschießen teilnehmen (oder tippen Sie direkt das Ergebnis ein – das Häkchen wird dann automatisch gesetzt).
    *   Tragen Sie in der Spalte **„Ergebnis Stechschießen“** die im Stechen erzielte Ringzahl (ganze Zahl >= 0) ein.
4.  Klicken Sie auf **„💾 Ergebnisse speichern“**.

**Auswirkung des Stechschießens:**
*   Die Schützen werden innerhalb ihrer Gleichstands-Gruppe anhand des Stech-Ergebnisses sortiert.
*   In der **Ergebnisanzeige**, der **Live-Bildschirmanzeige** und auf der **PDF-Ergebnisliste** wird in der Spalte `Stechen` automatisch der Vermerk `nach Stechen (<Wert>)` ausgegeben.
*   Auch bei der **Urkundenerstellung** wird die durch das Stechschießen entschiedene Platzierung berücksichtigt.
*   *Hinweis:* Wird das reguläre Ergebnis (Passen, 10er oder 9er) eines Schützen später noch einmal geändert, setzt die Software dessen Stech-Ergebnis automatisch zurück.

---

## 6. Mannschaften verwalten und auswerten

Im Reiter **„Mannschaften“** verwalten Sie Mannschaftswettbewerbe und werten diese flexibel aus. Das Gesamtergebnis einer Mannschaft berechnet sich automatisch aus der Summe der Einzelergebnisse der ihr zugeordneten Schützen.

### 6.1. Mannschaftsgröße festlegen

Links oben im Bereich **„Mannschaftsgröße“** legen Sie fest, wie viele Schützen maximal zu einer Mannschaft gehören:
1.  Wählen Sie im Zahlenfeld **„Anzahl Teilnehmer pro Mannschaft“** den gewünschten Wert (Standard: `3`).
2.  Klicken Sie auf **„Übernehmen“**.

### 6.2. Mannschaftsklassen verwalten (optional)

Rechts oben im Bereich **„Mannschaftsklassen verwalten“** können Sie eigene Klassen für die Mannschaftswertung definieren (z. B. „Jugend-Mannschaften“, „Offene Klasse“):
*   Geben Sie unter **„Neue Klasse“** den Namen ein und klicken Sie auf **„Klasse anlegen“** (oder drücken Sie `Enter`).
*   Um eine Mannschaftsklasse zu entfernen, wählen Sie sie in der Liste rechts aus und klicken auf **„Ausgewählte Klasse löschen“**.

### 6.3. Mannschaften anlegen, bearbeiten und Schützen zuordnen

Im linken Hauptbereich **„Mannschaft anlegen / bearbeiten & Schützen zuordnen“** stellen Sie die Teams zusammen:

1.  **Mannschaftsname:** Vergeben Sie einen eindeutigen Namen für die Mannschaft.
2.  **Mannschaftsklasse:** Wählen Sie optional eine zuvor angelegte Mannschaftsklasse oder belassen Sie die Auswahl auf `(Keine Klasse)`.
3.  **Schützen auswählen:**
    *   In der linken Tabelle sehen Sie alle im Turnier angelegten Schützen (inkl. Suchfeld **„Schütze suchen“** und Anzeige, ob der Schütze bereits einer Mannschaft angehört).
    *   Markieren Sie einen oder mehrere Schützen und klicken Sie auf **„Hinzufügen ➡“** (oder führen Sie einen **Doppelklick** auf den Schützen aus), um sie der Mannschaft zuzuordnen.
    *   Mit **„⬅ Entfernen“** (oder Doppelklick in der rechten Mitgliederliste) nehmen Sie einen Schützen wieder aus der Auswahl heraus.
    *   *Hinweise zur Teilnehmerzahl:* Es können nicht mehr Schützen zugeordnet werden, als unter „Mannschaftsgröße“ festgelegt ist. Sind **weniger** Schützen als vorgesehen zugeordnet, erscheint beim Speichern ein freundlicher Warnhinweis – die Mannschaft wird aber trotzdem gespeichert.
4.  **Speichern:** Klicken Sie auf **„💾 Mannschaft anlegen / Schützen zuordnen“**.
5.  **Bestehende Mannschaft bearbeiten oder löschen:**
    *   Rechts im Bereich **„Angelegte Mannschaften (Übersicht & Wertung)“** sehen Sie alle Teams samt aktuellem Platz, Schützenanzahl und Live-Gesamtergebnis.
    *   Klicken Sie eine Mannschaft an (oder klicken Sie auf **„✏ Bearbeiten“**), um sie im Editor links zu ändern und über **„💾 Mannschaft aktualisieren / Schützen zuordnen“** zu speichern.
    *   Mit **„🔄 Neue Mannschaft (Eingabe leeren)“** wechseln Sie zurück in den Neuanlage-Modus.
    *   Über **„🗑 Mannschaft löschen“** bzw. **„Alle löschen“** entfernen Sie einzelne oder alle Mannschaften.

### 6.4. Mannschaftswertung anzeigen & PDF-Export

Am unteren Rand des Reiters **„Mannschaften“** steuern Sie im Bereich **„Mannschaftswertung & PDF-Export“** die Auswertung:

*   **Wertung:**
    *   **Alle Mannschaften:** Alle Mannschaften werden gemeinsam in einer einzigen Gesamtrangliste gewertet.
    *   **Nach Mannschaftsklassen:** Die Platzierungen werden getrennt für jede Mannschaftsklasse berechnet.
*   **Einzelergebnisse der Mannschaftsmitglieder einbeziehen:** Wenn Sie dieses Häkchen setzen, werden unterhalb jeder Mannschaft auch die einzelnen Schützen mit ihren Passen-/Hälftenergebnissen und Gesamtringen aufgeführt.
*   **„🏆 Mannschaftswertung anzeigen“:** Öffnet ein eigenes, übersichtliches Auswertungsfenster, in dem Sie jederzeit zwischen Gesamtwertung und Klassenwertung sowie dem Ein-/Ausblenden der Einzelergebnisse umschalten und das PDF erstellen können.
*   **„📄 PDF Mannschaftswertung erstellen“:** Erzeugt direkt aus dem Reiter heraus das PDF-Dokument der Mannschaftswertung.

---

## 7. Online-Eingabe (Webinterface)

Der Reiter **„Online-Eingabe“** startet einen lokalen Webserver, über den Schützen ihre Ergebnisse während des Turniers selbstständig per Smartphone oder Tablet im lokalen WLAN eintragen können.

### 7.1. Server starten und stoppen

1.  Prüfen oder ändern Sie bei Bedarf den **Port** (Standard: `8080`).
2.  Klicken Sie auf **„Server starten“**.
3.  Der Status wechselt auf **„Aktiv“** (grün) und unter **„IP-Adresse“** wird die Adresse angezeigt, die die Schützen im Browser ihres Smartphones eingeben (z. B. `192.168.178.25:8080`).
4.  Mit **„Im Browser öffnen“** können Sie die Weboberfläche direkt am PC testen.

### 7.2. Aktive Gruppen freigeben

Im rechten Bereich **„Aktive Gruppen“** steuern Sie per Häkchen, welche Schießgruppen aktuell Ergebnisse eingeben dürfen:
*   Nur Schützen aus aktivierten Gruppen werden auf der Webseite zur Auswahl angezeigt.
*   Nutzen Sie die Buttons **„Alle auswählen“**, **„Keine auswählen“** und **„Aktualisieren“**, um die Gruppenfreigabe schnell anzupassen. Änderungen wirken sofort ohne Neustart des Servers.

### 7.3. Ablauf für den Schützen am Smartphone

1.  Der Schütze ruft die angezeigte Adresse (`http://<IP>:<Port>`) im Smartphone-Browser auf.
2.  **Auswahl:** Auf der Startseite sucht und markiert er seinen Namen. Es können auch **zwei Schützen gleichzeitig** ausgewählt werden (ideal, wenn man zu zweit an einer Scheibe schreibt).
3.  **Anmeldung:** Für jeden ausgewählten Schützen wird dessen persönliche 4-stellige **PIN** abgefragt (einsehbar im Reiter „Schützenverwaltung“).
4.  **Eingabe:** Pro Passe stehen 6 Eingabefelder für die einzelnen Pfeile/Schüsse (`0` bis `10`) bereit. Die Passensumme, das Gesamtergebnis sowie die Anzahl der 10er und 9er werden automatisch ermittelt.
5.  **Speichern:** Ein Tipp auf **„Alle Speichern“** überträgt die Ergebnisse sofort an die Hauptanwendung, aktualisiert die Mannschaftswertung und die Live-Bildschirmanzeige.

---

## 8. Urkunden erstellen

Im Reiter **„Urkunden“** generieren Sie auf Basis einer Word-Vorlage (`.docx`) individuelle Urkunden sowohl für **Einzelschützen** als auch für **Mannschaften**.

### 8.1. Funktionsweise

Sie gestalten Ihre Urkunde einmalig in Microsoft Word (oder LibreOffice) als `.docx`-Datei und setzen dort Platzhalter an die gewünschten Textstellen (auch innerhalb von Tabellen). BLATU ersetzt diese Platzhalter durch die Turnier- und Ergebnisdaten und speichert für jeden geehrten Schützen bzw. jede Mannschaft eine eigene Word-Datei.

### 8.2. Platzierungen für Schützen- und Mannschafts-Urkunden festlegen

Auf der linken Seite finden Sie zwei Bereiche:

1.  **Schützen-Urkunden pro Platzierung (oben):**
    *   Standardmäßig sind für jede Wettkampfklasse `3` Platzierungen (Platz 1 bis 3) voreingestellt.
    *   Führen Sie einen **Doppelklick** auf die Zahl in der Spalte **„Anzahl Platzierungen“** aus, um für einzelne Klassen beliebig viele Plätze einzustellen (z. B. `5` bei der Jugend oder `0`, um eine Klasse auszulassen).
    *   **Für alle Schützen erstellen:** Aktivieren Sie dieses Häkchen, wenn jeder Schütze (mit einem Ergebnis > 0) unabhängig vom Platz eine Urkunde erhalten soll.
2.  **Mannschafts-Urkunden pro Platzierung (unten):**
    *   Wählen Sie zunächst unter **„Wertung“**, ob die Mannschafts-Urkunden für **„Alle Mannschaften“** (Gesamtwertung) oder getrennt **„Nach Mannschaftsklassen“** erstellt werden sollen.
    *   Auch hier können Sie die **Anzahl Platzierungen** per **Doppelklick** auf die Zahl anpassen oder das Häkchen **„Für alle Mannschaften erstellen“** setzen.

### 8.3. Einstellungen und Generierung

Auf der rechten Seite unter **„Einstellungen“** legen Sie die Dateipfade und Optionen fest:

*   **Word-Vorlage:** Wählen Sie über **„Durchsuchen...“** Ihre `.docx`-Vorlagedatei aus.
*   **Speicherort:** Wählen Sie über **„Durchsuchen...“** den Zielordner, in dem die fertigen Urkunden abgelegt werden sollen.
*   **Unterordner für jede Klasse erstellen:** Ist diese Option aktiv, legt BLATU im Zielordner automatisch übersichtliche Unterordner pro Wettkampfklasse bzw. Mannschaftsklasse an.
*   **Option für Platzhalter `[Mannschaftsmitglieder]`:**
    *   Aktivieren Sie **„Einzelergebnis der Mannschaftsmitglieder hinter dem Namen ausgeben“**, wenn bei Mannschafts-Urkunden hinter jedem Mitgliedsnamen dessen geschossene Ringe in Klammern stehen sollen, z. B. `Max Mustermann (342)`.
*   **Starten der Erstellung:**
    *   Klicken Sie auf **„🚀 Urkunden erstellen (Schützen)“**, um die Einzel-Urkunden zu generieren.
    *   Klicken Sie auf **„🏆 Mannschafts-Urkunden erstellen“**, um die Mannschafts-Urkunden zu generieren.

### 8.4. Verfügbare Platzhalter für Ihre Word-Vorlage

Verwenden Sie die Platzhalter exakt mit eckigen Klammern:

*   `[Turniername]` – Name des Turniers
*   `[Datum]` – Datum des Turniers
*   `[Klasse]` – Wettkampfklasse des Schützen bzw. Mannschaftsklasse/Wertungsgruppe
*   `[Vorname]` – Vorname des Schützen (bei Mannschafts-Urkunden leer)
*   `[Name]` – Nachname des Schützen (bzw. Mannschaftsname bei Mannschafts-Urkunden)
*   `[Verein]` – Verein des Schützen (bzw. beteiligte Vereine der Mannschaftsmitglieder)
*   `[Ergebnis]` – Gesamtergebnis des Schützen bzw. der Mannschaft
*   `[Platz]` – Erreichte Platzierung innerhalb der Klasse/Wertung
*   `[Mannschaftsname]` – Name der Mannschaft (für Mannschafts-Urkunden)
*   `[Mannschaftsmitglieder]` – Zeilenweise Auflistung aller Schützen der Mannschaft (optional mit Einzelergebnis in Klammern hinter dem Namen)

*Hinweis bei Punktgleichheit:* Teilen sich mehrere Schützen oder Mannschaften denselben Platz, erhalten selbstverständlich alle eine Urkunde; die Dateinamen werden dabei automatisch mit `a`, `b`, ... ergänzt (z. B. `..._2a.docx`, `..._2b.docx`), damit keine Datei überschrieben wird. Teilnehmer und Mannschaften mit `0` Ringen werden übersprungen.

---

## 9. Schießzettel erstellen

Der Reiter **„Schießzettel“** generiert aus einer Word-Vorlage (`.docx`) fertige Schießzettel für die gewählten Gruppen.

### 9.1. Konfiguration und Platzhalter

1.  Wählen Sie links unter **„Einstellungen“** Ihre **Word-Vorlage** (`.docx`) und den **Speicherort** aus.
2.  Eine Vorlagenseite nimmt bis zu **4 Schützen** auf. Folgende Platzhalter stehen zur Verfügung:
    *   **Allgemein:** `[Turniername]`, `[Turnierdatum]`
    *   **Schütze 1 bis 4:**
        *   `[Name_1]`, `[Vorname_1]`, `[Gruppe_1]`, `[Scheibe_1]`
        *   `[Name_2]`, `[Vorname_2]`, `[Gruppe_2]`, `[Scheibe_2]`
        *   `[Name_3]`, `[Vorname_3]`, `[Gruppe_3]`, `[Scheibe_3]`
        *   `[Name_4]`, `[Vorname_4]`, `[Gruppe_4]`, `[Scheibe_4]`

### 9.2. Generierung

1.  Markieren Sie rechts unter **„Gruppenauswahl“** die gewünschten Gruppen (oder nutzen Sie **„Alle auswählen“** / **„Keine auswählen“**).
2.  Klicken Sie unten auf **„Schießzettel generieren“**.
3.  Pro Gruppe wird eine Datei `SZ_[Turniername]_[Gruppe]_[Datum].docx` erzeugt. Hat eine Gruppe mehr als 4 Schützen, fügt BLATU automatisch weitere Seiten mit Seitenumbruch in dasselbe Dokument ein.

---

## 10. Startgeldverwaltung

Im Reiter **„Startgeld“** behalten Sie jederzeit den Überblick über bezahlte und noch offene Startgelder.

### 10.1. Aufbau der Ansicht

*   **Alle Schützen (obere Tabelle):** Zeigt für jeden Teilnehmer den Status (`Bezahlt`: Ja/Nein), Gruppe, Scheibe, Name, Vorname, Verein, das fällige Startgeld (gemäß seiner Klasse) und den aktuellen Status.
*   **Vereine (untere Tabelle):** Fasst alle Teilnehmer pro Verein zusammen und zeigt das **Gesamt-Startgeld** des Vereins sowie den Zahlungsfortschritt (z. B. `Vollständig bezahlt`, `Nicht bezahlt` oder `2 von 5 bezahlt`).

### 10.2. Bezahlstatus ändern (per Doppelklick)

*   **Einzelner Schütze:** Führen Sie einen **Doppelklick** auf die gewünschte Zeile in der oberen Tabelle **„Alle Schützen“** aus. Es öffnet sich direkt in der Zeile ein Auswahlfeld, in dem Sie zwischen **`unbezahlt`** und **`bezahlt`** wählen können.
*   **Ganzer Verein:** Führen Sie einen **Doppelklick** auf einen Verein in der unteren Tabelle **„Vereine“** aus und wählen Sie im Auswahlfeld **`bezahlt`** oder **`unbezahlt`**, um den Status sämtlicher Schützen dieses Vereins in einem Schritt zu setzen.

### 10.3. Farbcodierung, Filter und Sortierung

*   **Grün:** Vollständig bezahlt.
*   **Rot:** Noch unbezahlt.
*   **Orange:**
    *   *In der Schützenliste (`Überprüfen`):* Die Klasse des Schützen oder das Startgeld seiner Klasse wurde nachträglich geändert – bitte prüfen und per Doppelklick neu bestätigen.
    *   *In der Vereinsliste:* Teilweise bezahlt (einige, aber noch nicht alle Vereinsmitglieder haben bezahlt) oder ein Mitglied steht auf „Überprüfen“.
*   Über das Feld **„Schütze filtern“** durchsuchen Sie die Liste in Echtzeit nach Namen oder Vereinen. Ein Klick auf eine beliebige Spaltenüberschrift sortiert die jeweilige Tabelle.

---

## 11. PDF-Export und PDF-Schriftgrößen (Reiter „PDF Settings“)

### 11.1. Übersicht aller PDF-Exporte

BLATU erstellt vier verschiedene, druckfertige PDF-Dokumenttypen:

1.  **Ergebnisliste (PDF):** Über den Reiter *Ergebniseingabe* -> *Ergebnisanzeige* -> *PDF erstellen* (Querformat, klassenweise mit Gold-/Silber-/Bronze-Hervorhebung und Stechschießen-Vermerk).
2.  **Mannschaftswertung (PDF):** Über den Reiter *Mannschaften* -> *📄 PDF Mannschaftswertung erstellen* oder aus dem Fenster *Mannschaftswertung* (Querformat, gesamt oder nach Mannschaftsklassen, wahlweise mit oder ohne Einzelergebnisse der Mitglieder).
3.  **Gruppen-PDF:** Über den Reiter *Gruppenverwaltung* -> *Gruppen-PDF erstellen* (Hochformat, alle Gruppen mit Startzeiten und Scheiben).
4.  **Startliste Vereine (PDF):** Über den Reiter *Gruppenverwaltung* -> *Startliste Vereine* (Hochformat, separate PDF-Datei pro Verein inkl. Gesamtstartgeld und Bankverbindung).

### 11.2. Schriftgrößen individuell anpassen (Reiter „PDF Settings“)

Im Reiter **„PDF Settings“** können Sie die Schriftgrößen (in Punkt / `pt`, von `6` bis `48` pt) **getrennt für jedes der vier PDF-Dokumente** anpassen:

*   **Ergebnisliste (PDF):** Turniertitel, Datum / Untertitel, Klassenüberschrift, Tabellenkopf, Tabelleninhalt.
*   **Gruppen-PDF:** Turniertitel, Datum / Untertitel, Gruppenüberschrift, Tabellenkopf, Tabelleninhalt.
*   **Startliste Vereine (PDF):** Turniertitel, Datum / Untertitel, Vereinsüberschrift, Tabellenkopf, Tabelleninhalt, Startgeld- & Zahlungstext.
*   **Mannschaftswertung (PDF):** Turniertitel, Datum / Untertitel, Klassen-/Wertungsüberschrift, Tabellenkopf, Tabelleninhalt.

Änderungen an den Zahlenfeldern werden sofort übernommen und beim Speichern des Turniers in der JSON-Datei mitgesichert.
*   Mit **„💾 Einstellungen speichern“** prüfen und bestätigen Sie Ihre Eingaben explizit.
*   Mit **„🔄 Standardwerte wiederherstellen“** setzen Sie alle Schriftgrößen jederzeit wieder auf die optimal abgestimmten Standardwerte zurück.

---

## 12. Live-Anzeige für Bildschirme (Beamer-Modus)

Um Zuschauern im Vereinsheim oder in der Sporthalle die aktuellen Zwischen- und Endergebnisse auf einem großen Monitor oder Beamer zu präsentieren:

1.  Wechseln Sie in den Reiter **„Ergebniseingabe“**.
2.  Klicken Sie auf **„🖥 Bildschirmanzeige“**.

### Funktionen der Live-Anzeige

*   **Nahtloses Endlos-Scrolling:** Sobald die Tabellen höher als der Bildschirm sind, scrollt die Anzeige ruckelfrei in einer Endlosschleife durch alle Klassen.
*   **Echtzeit-Aktualisierung:** Neue Ergebnisse aus der Hauptanwendung, dem Stechschießen oder der mobilen Online-Eingabe werden automatisch übernommen.
*   **Medaillen-Hervorhebung:** Die Plätze 1 bis 3 jeder Klasse werden mit Medaillen (`🥇 1`, `🥈 2`, `🥉 3`) sowie Gold-, Silber- und Bronzehintergrund hervorgehoben.
*   **Steuerleiste am unteren Rand:**
    *   **„⏸ Pause / ▶ Weiter“:** Hält das automatische Scrollen und Aktualisieren an bzw. setzt es fort.
    *   **„🔄 Aktualisieren“:** Lädt die Anzeige sofort manuell neu.
    *   **„🖥 Vollbild“:** Schaltet in den Vollbildmodus um (mit der `ESC`-Taste oder erneutem Klick auf „🖥 Vollbild“ verlassen Sie den Vollbildmodus wieder).

---

## 13. Alle Daten speichern und laden

Am unteren Rand des Hauptfensters befinden sich in jedem Reiter sichtbar die beiden Hauptschaltflächen zur Datensicherung:

*   **„💾 Alle Daten speichern“:** Speichert den gesamten Turnierstand (Turniereinstellungen, Bankdaten, Klassen, Startgelder, Schützen inkl. PINs und Bezahlstatus, Gruppeneinteilung, Gruppen-Startzeiten, Mannschaftsgröße, Mannschaftsklassen, Mannschaften, alle Ergebnisse inkl. Online-Rohdaten und Stechschießen sowie die PDF-Schriftgrößen) in einer `.json`-Datei.
*   **„📂 Alle Daten laden“:** Lädt eine gespeicherte `.json`-Turnierdatei und stellt alle Reiter und Auswertungen vollständig wieder her.

---

## 14. Über die Software

Im Reiter **„Info“** finden Sie die aktuelle Versionsnummer, das Versionsdatum sowie die Kontakt- und Webseiten-Informationen des Entwicklers.
