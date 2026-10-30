# Benutzerhandbuch für BLATU 1.5.3

## 1. Einleitung

Willkommen bei BLATU! Diese Software wurde entwickelt, um die Organisation und Durchführung von Blasrohr-Turnieren so einfach und effizient wie möglich zu gestalten. Die Software kann aber auch für Bogen- oder andere Schießturniere verwendet werden. Von der Einrichtung des Turniers über die Verwaltung der Teilnehmer und die Eingabe der Ergebnisse bis hin zur Erstellung professioneller PDF-Dokumente und einer Live-Anzeige für Zuschauer – hier finden Sie alle Werkzeuge, die Sie benötigen.

Dieses Handbuch führt Sie schrittweise durch alle Funktionen der Anwendung.

---

## 2. Erste Schritte: Das Turnier einrichten

Alles beginnt mit der Konfiguration Ihres Turniers. Wechseln Sie dazu in den Reiter **"Turnier"**.


Hier legen Sie die grundlegenden Parameter für Ihren Wettkampf fest:

*   **Name des Turniers:** Geben Sie einen aussagekräftigen Namen für die Veranstaltung ein (z. B. "Vereinsmeisterschaft 2024").
*   **Datum:** Tragen Sie das Datum des Wettkampfs ein. Dies erscheint später auf den Ergebnislisten.
*   **Anzahl Passen:** Legen Sie fest, wie viele Passen (Serien) pro Schütze geschossen werden.
*   **Ergebnisse als 1. und 2. Hälfte anzeigen:** Wenn Sie diese Option aktivieren, werden die Ergebnisse in den Auswertungen und PDFs nicht als einzelne Passen, sondern als Summe der ersten und zweiten Wettkampfhälfte dargestellt. **Wichtiger Hinweis:** Diese Option ist nur verfügbar, wenn eine gerade Anzahl an Passen eingestellt ist.

Nachdem Sie alle Daten eingegeben haben, klicken Sie auf **"Einstellungen speichern"**. Ihre Konfiguration wird nun im rechten Infobereich angezeigt.

### 2.1. Bankverbindung für Startgeld hinterlegen

Wenn Sie das Startgeld per Überweisung einsammeln möchten, können Sie die notwendigen Bankdaten direkt im Turnier hinterlegen. Diese Informationen werden dann automatisch auf die Startlisten-PDFs für die Vereine gedruckt.

1.  Aktivieren Sie die Checkbox **"Startgeld erheben und Bankdaten auf PDFs anzeigen"**.
2.  Füllen Sie die nun aktivierten Felder aus:
    *   **Kontonummer (IBAN)**
    *   **BIC**
    *   **Bankname**
    *   **Kontoinhaber**
    *   **Zu bezahlen bis:** Geben Sie hier das Fälligkeitsdatum für die Zahlung an.
3.  Speichern Sie die Einstellungen.

Wenn die Checkbox deaktiviert ist, sind die Felder ausgegraut und die Informationen werden nicht auf den PDFs angedruckt.

**Tipp:** Mit dem Button **"Zurücksetzen"** können Sie alle Eingaben in diesem Reiter auf die Standardwerte zurücksetzen.

---

## 3. Teilnehmer und Klassen verwalten

### 3.1. Wettkampfklassen anlegen

Bevor Sie Schützen anlegen, sollten Sie die benötigten Wettkampfklassen definieren. Wechseln Sie dazu in den Reiter **"Klassen"**.

*   Geben Sie im Feld **"Klassenname"** den Namen der Klasse ein (z. B. "Schülerklasse A", "Herren I").
*   Klicken Sie auf **"Klasse hinzufügen"**.

Die Klasse erscheint nun in der Liste. Diese Liste enthält nun auch eine Spalte **"Startgeld (€)"**.

*   **Startgeld bearbeiten:** Machen Sie einen Doppelklick auf den Betrag in der Spalte "Startgeld", um diesen direkt in der Tabelle zu bearbeiten. Geben Sie den Wert ein und bestätigen Sie mit der `Enter`-Taste. Das Startgeld wird mit zwei Nachkommastellen gespeichert.

Sie können Klassen jederzeit löschen, indem Sie eine Klasse auswählen und auf **"Ausgewählte Klasse löschen"** klicken.

### 3.2. Schützen anlegen und bearbeiten

Wechseln Sie in den Reiter **"Schützen"**, um Teilnehmer zu verwalten.

*   **Schütze hinzufügen:** Füllen Sie die Felder "Name", "Vorname", "Verein" aus und wählen Sie die passende "Klasse" aus der Dropdown-Liste aus. Klicken Sie anschließend auf **"Schütze hinzufügen"**. Der neue Teilnehmer erscheint in der Schützenliste.
*   **PIN:** Jedem Schützen wird automatisch eine 4-stellige PIN zugewiesen. Diese PIN wird für die **Online-Eingabe** benötigt. Sie können die PIN einsehen und ändern, indem Sie einen Schützen auswählen.
*   **Schütze bearbeiten:** Um die Daten eines Schützen zu ändern, doppelklicken Sie auf seinen Eintrag in der Liste oder wählen Sie ihn aus und klicken auf **"Bearbeiten"**. Die Daten werden in die Eingabefelder geladen. Nach der Änderung klicken Sie auf **"Schütze aktualisieren"**.
*   **Schütze löschen:** Wählen Sie einen oder mehrere Schützen aus und klicken Sie auf **"Ausgewählten löschen"**. Mit **"Alle Schützen löschen"** leeren Sie die komplette Liste.

### 3.3. Automatische Zuweisung zu Gruppen und Scheiben

Sie können Gruppen und Scheibenplätze automatisch zuweisen lassen.

1.  **Max. Scheiben:** Geben Sie an, wie viele Scheiben pro Gruppe maximal zur Verfügung stehen.
2.  **Zuweisungsart:** Wählen Sie eine Strategie:
    *   **Nach Eingabe:** Die Zuweisung erfolgt in der Reihenfolge, in der die Schützen erfasst wurden.
    *   **Zufällig:** Die Reihenfolge wird zufällig gemischt.
    *   **Nach Klassen:** Die Schützen werden vor der Zuweisung nach ihrer Klasse sortiert.
3.  Klicken Sie auf **"Automatisch Zuweisen"**.

### 3.4. Manuelle Zuweisung

Sie können einen Schützen auch manuell einer Gruppe und Scheibe zuweisen.

1.  Wählen Sie den gewünschten Schützen in der Liste aus.
2.  Geben Sie die Ziel-**Gruppe** und **-Scheibe** in die Felder im Bereich "Manuelle Zuweisung" ein.
3.  Klicken Sie auf **"Ausgewählten Schützen zuweisen"**.

**Tipp:** Sie können die Schützenliste sortieren, indem Sie auf die jeweilige Spaltenüberschrift (z. B. "Name", "Verein") klicken.

---

## 4. Gruppeneinteilung verwalten

Der Reiter **"Gruppen"** bietet eine detaillierte Übersicht und weitere Werkzeuge zur Verwaltung der Gruppeneinteilung.

*   **Zwei Listen:** Auf der linken Seite sehen Sie alle Schützen, die bereits einer Gruppe und Scheibe zugewiesen sind. Rechts finden Sie alle noch nicht zugewiesenen Schützen.
*   **Uhrzeit für Gruppe festlegen:**
    1.  Wählen Sie einen Schützen aus einer Gruppe in der linken Liste aus.
    2.  Geben Sie im Bereich "Uhrzeit für Gruppe festlegen" eine Startzeit ein (z. B. "10:00").
    3.  Klicken Sie auf **"Für ausgewählte Gruppe speichern"**. Die Uhrzeit wird nun für die gesamte Gruppe angezeigt.
*   **Zuweisung ändern:**
    1.  Wählen Sie einen Schützen aus einer der beiden Listen.
    2.  Geben Sie im Bereich "Zuweisung für Schützen ändern" die neue **Gruppe** und **Scheibe** ein.
    3.  Klicken Sie auf **"Zuweisung ändern"**. Das Programm prüft dabei automatisch, ob der Platz bereits belegt ist.

---

## 5. Ergebnisse eingeben und auswerten

Wechseln Sie zum Reiter **"Ergebnisse"**, um die Wettkampfergebnisse zu erfassen.

1.  **Schütze auswählen:** Wählen Sie den gewünschten Schützen aus der Liste auf der linken Seite aus. Sie können die Liste über das Suchfeld filtern.
2.  **Ergebnisse laden:** Doppelklicken Sie auf den Schützen oder wählen Sie ihn aus und drücken Sie die Eingabetaste. Seine Daten und die Eingabefelder für die Passen werden auf der rechten Seite geladen.
3.  **Ergebnisse eingeben:** Tragen Sie die Ergebnisse für jede Passe in die entsprechenden Felder ein. **Bitte beachten Sie, dass nur ganze Zahlen (ohne Kommastellen) als Ergebnisse akzeptiert werden.** Das Gesamtergebnis wird automatisch berechnet und unten angezeigt.
4.  **Zusatzwertung:** Geben Sie die **Anzahl der 10er und 9er** ein. Diese Werte werden zur Ermittlung der Platzierung bei Ergebnisgleichheit herangezogen.
5.  **Speichern:** Klicken Sie auf **"Ergebnisse speichern"**. Das Gesamtergebnis des Schützen wird nun in der Liste links angezeigt.
6.  **Aktualisieren:** Mit dem Button **"Liste aktualisieren"** können Sie die angezeigten Daten neu laden, falls parallel Ergebnisse über die Online-Eingabe erfasst wurden.

### 5.1. Gesamtergebnisse anzeigen

Klicken Sie auf den Button **"Ergebnisanzeige"**. Ein neues Fenster öffnet sich, das die vollständigen Ranglisten anzeigt, sortiert nach Klassen und Platzierungen. Auch hier gibt es einen **"Aktualisieren"**-Button für Live-Updates.

---

## 6. Online-Eingabe (Webinterface)

Der Reiter **"Online-Eingabe"** ermöglicht es Ihnen, einen lokalen Webserver zu starten, über den Schützen ihre Ergebnisse selbstständig mit einem Smartphone oder Tablet eingeben können.

### 6.1. Server starten

1.  Wählen Sie einen **Port** (Standard: 8080).
2.  Klicken Sie auf **"Server starten"**.
3.  Die Statusanzeige wechselt auf grün ("Aktiv") und die IP-Adresse, unter der die Webseite erreichbar ist, wird angezeigt (z. B. `192.168.1.100:8080`).

### 6.2. Gruppen freigeben

Um Missbrauch zu verhindern, können Sie festlegen, welche Gruppen aktuell Ergebnisse eingeben dürfen.
*   Wählen Sie im rechten Bereich die gewünschten Gruppen aus.
*   Nur Schützen, die diesen Gruppen zugewiesen sind, können sich anmelden.

### 6.3. Verwendung durch den Schützen

1.  Der Schütze öffnet die IP-Adresse in seinem Browser.
2.  Auf der Startseite wählt er seinen Namen aus der Liste (oder zwei Namen, um Ergebnisse für zwei Personen gleichzeitig einzugeben). Zur Orientierung werden Gruppe und Scheibe angezeigt.
3.  **Login:** Der Schütze muss seine persönliche **PIN** eingeben (diese finden Sie in der "Schützenverwaltung").
4.  **Eingabe:** Für jede Passe stehen 6 Eingabefelder zur Verfügung. Die Summen und 10er/9er werden automatisch berechnet.
5.  Nach Abschluss klickt der Schütze auf **"Speichern"**. Die Daten werden sofort an die Hauptanwendung übertragen und in der Live-Anzeige aktualisiert.

---

## 7. Startgeldverwaltung

Der Reiter **"Startgeld"** ist die zentrale Anlaufstelle, um den Überblick über die bezahlten Startgelder zu behalten.

### 7.1. Die Oberfläche

Der Reiter ist in zwei Hauptbereiche unterteilt:

1.  **Alle Schützen (obere Liste):** Hier sehen Sie jeden einzelnen Teilnehmer mit seinem Namen, Verein, dem fälligen Startgeld (basierend auf seiner Klasse) und dem Bezahlstatus.
2.  **Vereine (untere Liste):** Diese Liste fasst die Informationen pro Verein zusammen. Sie sehen das gesamte fällige Startgeld pro Verein und den Gesamt-Bezahlstatus.

### 7.2. Bezahlstatus ändern

Sie können den Status ganz einfach per Mausklick ändern:

*   **Einzelner Schütze:** Klicken Sie auf die Checkbox in der ersten Spalte der Schützenliste, um den Status eines Teilnehmers zwischen "bezahlt" (grün) und "unbezahlt" (rot) zu wechseln.
*   **Ganzer Verein:** Klicken Sie auf die Checkbox in der ersten Spalte der Vereinsliste, um den Status für **alle** Schützen dieses Vereins gleichzeitig zu ändern. Wenn noch nicht alle Mitglieder bezahlt haben, werden alle auf "bezahlt" gesetzt. Sind bereits alle als bezahlt markiert, werden alle auf "unbezahlt" zurückgesetzt.

### 7.3. Farbcodierung und Status

Die Software nutzt Farben, um den Status schnell erfassbar zu machen:

*   **Grün:** Der Schütze oder der gesamte Verein hat das Startgeld bezahlt.
*   **Rot:** Das Startgeld wurde noch nicht bezahlt.
*   **Orange:**
    *   **Beim Verein:** Einige, aber nicht alle Mitglieder des Vereins haben bezahlt.
    *   **Beim Schützen (Status "Überprüfen"):** Dieser Status wird automatisch gesetzt, wenn sich etwas an den Rahmenbedingungen ändert (z. B. der Schütze wird einer neuen Klasse zugewiesen oder das Startgeld der Klasse wird geändert). Dies dient als Hinweis, dass der ursprünglich erfasste Bezahlstatus eventuell nicht mehr korrekt ist und manuell bestätigt werden muss.

### 7.4. Schützen filtern und sortieren

*   **Filtern:** Nutzen Sie das Suchfeld oben, um die Schützenliste in Echtzeit zu filtern. Geben Sie einfach einen Teil des Namens oder Vereins ein.
*   **Sortieren:** Klicken Sie auf eine Spaltenüberschrift in einer der beiden Listen, um die Daten nach dieser Spalte zu sortieren. Ein erneuter Klick kehrt die Sortierreihenfolge um.

---

## 8. PDF-Export

Die Software kann professionelle PDF-Dokumente für die Veröffentlichung erstellen.

*   **Ergebnisliste als PDF:** Klicken Sie im Fenster "Ergebnisanzeige" auf den Button **"PDF erstellen"**. Sie werden aufgefordert, einen Speicherort für die PDF-Datei zu wählen. Das Layout (einzelne Passen oder Hälften) richtet sich nach der Einstellung im Reiter "Turnier".
*   **Gruppen-PDF erstellen:** Im Reiter **"Gruppen"** finden Sie den Button **"Gruppen-PDF erstellen"**. Dieses PDF enthält eine übersichtliche Liste aller Gruppen mit den zugewiesenen Schützen und den festgelegten Startzeiten.
*   **Startlisten pro Verein als PDF:** Im Reiter **"Gruppen"** können Sie über den Button **"Startlisten pro Verein (PDF)"** für jeden teilnehmenden Verein eine eigene PDF-Startliste erstellen. Diese Funktion ist ideal, um den Vereinen ihre individuellen Startzeiten und Scheibenzuweisungen zukommen zu lassen.

---

## 9. Live-Anzeige für Bildschirme

Für die Zuschauer oder zur Anzeige auf einem Beamer können Sie eine Live-Ansicht der Ergebnisse starten.

1.  Wechseln Sie in den Reiter **"Ergebnisse"**.
2.  Klicken Sie auf den Button **"🖥 Bildschirmanzeige"**.

Ein neues, für große Bildschirme optimiertes Fenster öffnet sich.

### Highlights der Live-Anzeige:

*   **Nahtloses Scrollen:** Die Ergebnisliste läuft in einer Endlosschleife von unten nach oben durch, sodass alle Teilnehmer ohne Unterbrechung sichtbar sind.
*   **Automatische Aktualisierung:** Die Anzeige aktualisiert sich automatisch, sobald neue Ergebnisse (ob manuell oder per Web eingegeben) gespeichert werden.
*   **Visuelle Hervorhebung:** Die ersten drei Plätze jeder Klasse werden mit Medaillen-Emojis (🥇, 🥈, 🥉) und farblicher Hinterlegung deutlich hervorgehoben.
*   **Dynamisches Layout:** Die Anzeige passt sich intelligent an die Turnierkonfiguration an. Bei wenigen Passen werden die Einzelergebnisse angezeigt, bei vielen Passen wird auf eine kompakte Gesamtansicht umgeschaltet.
*   **Einfache Steuerung:** Am unteren Rand des Fensters finden Sie Steuerelemente, um das Scrollen zu pausieren, die Ansicht manuell zu aktualisieren oder in den Vollbildmodus zu wechseln (und ihn mit der `ESC`-Taste wieder zu verlassen).

---

## 10. Urkunden erstellen

Die Software bietet eine leistungsstarke Funktion, um individuelle Urkunden für Ihre Teilnehmer zu erstellen. Wechseln Sie dazu in den Reiter **"Urkunden"**.

### 10.1. Funktionsweise

Die Urkundenerstellung basiert auf einer von Ihnen bereitgestellten Word-Vorlage (`.docx`). In dieser Vorlage definieren Sie mit Platzhaltern, wo die Daten der Schützen (Name, Platz, Ergebnis etc.) eingefügt werden sollen. Die Software ersetzt diese Platzhalter automatisch und erstellt für jeden ausgewählten Schützen eine separate Word-Datei.

### 10.2. Konfiguration

Im oberen Bereich des Reiters finden Sie alle notwendigen Einstellungen:

*   **Urkunden pro Platzierung:** Hier legen Sie fest, für wie viele Platzierungen pro Klasse Urkunden erstellt werden sollen.
    *   **Beispiel:** Wenn Sie "3" eintragen, werden Urkunden für alle Schützen auf den Plätzen 1, 2 und 3 erstellt.
    *   **Besonderheit bei Punktgleichheit:** Befinden sich mehrere Schützen auf einem Platz (z. B. zwei Schützen auf Platz 2), erhalten alle eine Urkunde. Die Software ist intelligent und stellt sicher, dass alle relevanten Ränge berücksichtigt werden.
    *   **Bearbeiten:** Machen Sie einen Doppelklick auf die Zahl in der Spalte "Anzahl Platzierungen", um den Wert für die jeweilige Klasse zu ändern.
    *   **Für alle Schützen erstellen:** Aktivieren Sie diese Option, um die Platzierungs-Logik zu ignorieren und für jeden Teilnehmer (der ein Ergebnis hat) eine Urkunde zu erstellen.

*   **Einstellungen:**
    *   **Word-Vorlage:** Wählen Sie über den "Durchsuchen..."-Button die `.docx`-Datei aus, die als Vorlage dienen soll.
    *   **Speicherort:** Wählen Sie den Ordner, in dem die erstellten Urkunden-Dateien gespeichert werden sollen.
    *   **Unterordner für jede Klasse erstellen:** Wenn diese Option aktiviert ist, erstellt die Software im Ziel-Speicherort für jede Wettkampfklasse einen eigenen Unterordner (z. B. "Herren_I", "Jugend"), in den die jeweiligen Urkunden sortiert werden.

### 10.3. Verfügbare Platzhalter

Ihre Word-Vorlage kann die folgenden Platzhalter enthalten. Achten Sie darauf, die eckigen Klammern exakt wie angegeben zu verwenden.

*   `[Turniername]` - Der Name des Turniers.
*   `[Datum]` - Das Datum des Turniers.
*   `[Klasse]` - Die Wettkampfklasse des Schützen.
*   `[Vorname]` - Der Vorname des Schützen.
*   `[Name]` - Der Nachname des Schützen.
*   `[Verein]` - Der Verein des Schützen.
*   `[Ergebnis]` - Das Gesamtergebnis des Schützen.
*   `[Platz]` - Die Platzierung des Schützen bzw. der Mannschaft innerhalb der jeweiligen Klasse.
*   `[Mannschaftsname]` - Der Name der Mannschaft (bei Mannschafts-Urkunden).
*   `[Mannschaftsmitglieder]` - Die Mitglieder der Mannschaft, zeilenweise aufgelistet (optional mit Einzelergebnis).

### 10.4. Erstellungsprozess

Wenn Sie alle Einstellungen vorgenommen haben, klicken Sie auf den Button **"🚀 Urkunden erstellen"**. Die Software führt nun folgende Schritte aus:

1.  Sie berechnet die finalen Platzierungen (inkl. korrekter Sortierung bei Punktgleichheit).
2.  Sie wählt die zu ehrenden Schützen basierend auf Ihren Platzierungs-Vorgaben aus. Schützen mit einem Ergebnis von 0 werden ignoriert.
3.  Für jeden ausgewählten Schützen wird eine neue Word-Datei basierend auf Ihrer Vorlage erstellt und die Platzhalter werden ersetzt.
4.  Die Dateien werden im Ziel-Speicherort abgelegt. Bei Punktgleichheit wird der Dateiname automatisch angepasst (z. B. `..._Platz_2a.docx`, `..._Platz_2b.docx`), um Dateikonflikte zu vermeiden.

Nach Abschluss des Vorgangs erhalten Sie eine Erfolgsmeldung.

---

## 11. Schießzettel erstellen

Der Reiter **"Schießzettel"** ermöglicht die automatische Erstellung von Schießzetteln (Scorecards) für die Schützen, basierend auf der aktuellen Gruppeneinteilung.

### 11.1. Vorbereitung

Sie benötigen eine Word-Vorlage (`.docx`), die das Layout Ihres Schießzettels definiert. Die Software füllt diese Vorlage mit den Daten der Schützen.

### 11.2. Konfiguration

1.  **Word-Vorlage:** Wählen Sie über "Auswählen" Ihre `.docx`-Vorlage aus.
2.  **Speicherort:** Bestimmen Sie den Ordner, in dem die generierten Dateien gespeichert werden sollen.

### 11.3. Platzhalter für die Vorlage

Die Software unterstützt Vorlagen, die bis zu 4 Schützen pro Seite/Zettel aufnehmen können. Verwenden Sie folgende Platzhalter in Ihrem Word-Dokument:

*   Allgemeine Daten:
    *   `[Turniername]`
    *   `[Turnierdatum]`

*   Daten für die Schützen (1 bis 4):
    *   `[Name_1]`, `[Vorname_1]`, `[Gruppe_1]`, `[Scheibe_1]`
    *   `[Name_2]`, `[Vorname_2]`, `[Gruppe_2]`, `[Scheibe_2]`
    *   `[Name_3]`, `[Vorname_3]`, `[Gruppe_3]`, `[Scheibe_3]`
    *   `[Name_4]`, `[Vorname_4]`, `[Gruppe_4]`, `[Scheibe_4]`

### 11.4. Generierung

1.  Wählen Sie im rechten Bereich **"Gruppenauswahl"** die Gruppen aus, für die Sie Schießzettel erstellen möchten. Nutzen Sie die Buttons "Alle auswählen" oder "Keine auswählen" für eine schnelle Selektion.
2.  Klicken Sie auf **"Schießzettel generieren"**.
3.  Die Software erstellt nun für jede ausgewählte Gruppe eine Word-Datei im angegebenen Speicherort (Dateiname: `SZ_[Turniername]_[Gruppe]_[Datum].docx`). Wenn eine Gruppe mehr als 4 Schützen hat, werden automatisch weitere Seiten angefügt.

---

## 12. Über die Software

Im Reiter **"Info"** finden Sie die aktuelle Versionsnummer der Software sowie Kontaktinformationen.
