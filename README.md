# Blatu - Blasrohr Turnierverwaltung

Version 1.5.4

## Beschreibung

Blatu ist eine Desktop-Anwendung zur einfachen und effizienten Organisation, Durchführung und Auswertung von Blasrohr-Turnieren (sowie Bogen- oder anderen Schießturnieren). Sie umfasst die komplette Verwaltung von Schützen, Wettkampfklassen, Gruppen/Scheiben, Mannschaften, Startgeldern und Ergebnissen inklusive Stechschießen, mobiler Online-Eingabe, Live-Bildschirmanzeige sowie PDF- und Word-Exporten (Ergebnislisten, Startlisten, Urkunden und Schießzettel).

## Projektstruktur

```
blatu/
├── main.py                              # Haupteinstiegspunkt der Anwendung
├── config.py                            # Konfiguration, Version und Konstanten
├── web_server.py                        # Lokaler Flask-Webserver für die Online-Eingabe
├── blatu.ico                            # Anwendungs-Icon
├── models/                              # Datenmodelle
│   ├── __init__.py
│   ├── turnier.py                       # Turnier-, Klassen-, Mannschafts- und Ergebnis-Datenmodell
│   └── schuetze.py                      # Schützen-Datenmodell und Ranglistenberechnung
├── templates/                           # HTML-Templates für die mobile Online-Eingabe
│   ├── index.html                       # Schützenauswahl (1 bis 2 Schützen)
│   ├── login_multi.html                 # PIN-Anmeldung
│   └── input_multi.html                 # Schussweise Ergebniseingabe
├── ui/                                  # Benutzeroberfläche (Tkinter)
│   ├── __init__.py
│   ├── main_window.py                   # Hauptfenster mit Reiter-Steuerung
│   ├── turnier_tab.py                   # Reiter: Turnierverwaltung
│   ├── klassen_tab.py                   # Reiter: Klassenverwaltung
│   ├── schuetzen_tab.py                 # Reiter: Schützenverwaltung
│   ├── gruppen_tab.py                   # Reiter: Gruppenverwaltung
│   ├── ergebnisse_tab.py                # Reiter: Ergebniseingabe
│   ├── ergebnisse_window.py             # Fenster: Ergebnisanzeige (Einzelwertung)
│   ├── stechschiessen_window.py         # Fenster: Stechschießen bei Punkt-Gleichstand
│   ├── bildschirm_anzeige_window.py     # Fenster: Live-Bildschirmanzeige (Beamer-Modus)
│   ├── mannschaften_tab.py              # Reiter: Mannschaften (Verwaltung & Wertung)
│   ├── mannschaft_ergebnisse_window.py  # Fenster: Mannschaftswertung
│   ├── online_eingabe_tab.py            # Reiter: Online-Eingabe (Webserver-Steuerung)
│   ├── urkunden_tab.py                  # Reiter: Urkunden (Einzel- und Mannschafts-Urkunden)
│   ├── schiesszettel_tab.py             # Reiter: Schießzettel
│   ├── startgeld_tab.py                 # Reiter: Startgeld
│   ├── pdf_settings_tab.py              # Reiter: PDF Settings (Schriftgrößen)
│   └── info_tab.py                      # Reiter: Info
├── utils/                               # Hilfsfunktionen und Generatoren
│   ├── __init__.py
│   ├── data_manager.py                  # Speichern und Laden der Turnierdaten (JSON)
│   ├── gui_helper.py                    # Fenster- und Taskleisten-Icon-Helfer
│   ├── pdf_generator.py                 # PDF-Erstellung (Ergebnisse, Mannschaften, Gruppen, Vereine)
│   └── word_generator.py                # Word-Dokument-Erstellung (Urkunden & Schießzettel)
├── BENUTZERHANDBUCH.md                  # Ausführliches Benutzerhandbuch
├── LICENSE.md                           # Lizenzinformationen
└── README.md                            # Projektübersicht
```

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- `tkinter` (meist in der Standard-Python-Installation enthalten)
- `reportlab` (für den PDF-Export)
- `python-docx` (für die Erstellung von Word-Urkunden und Schießzetteln)
- `docxcompose` (für das Zusammenfügen mehrseitiger Schießzettel)
- `flask` (für den integrierten Webserver der Online-Eingabe)

Die benötigten Pakete können per `pip` installiert werden:

```bash
pip install reportlab python-docx docxcompose flask
```

## Start der Anwendung

```bash
python main.py
```

## Funktionen

- **Turnierverwaltung**: Erfassung von Turniername, Datum, Anzahl der Passen, optionaler Darstellung als 1. und 2. Wettkampfhälfte sowie Bankverbindung und Zahlungsziel für die Startgeld-Abrechnung.
- **Klassenverwaltung**: Anlegen und Verwalten von Wettkampfklassen inklusive individuellem Startgeld pro Klasse (direkt per Doppelklick bearbeitbar).
- **Schützenverwaltung**: Erfassung und Bearbeitung von Teilnehmern (Name, Vorname, Klasse, Verein, automatisch generierte oder manuell anpassbare 4-stellige PIN) sowie automatische oder manuelle Zuweisung zu Gruppen und Scheiben.
- **Gruppenverwaltung**: Übersichtliche Verwaltung zugewiesener und noch nicht zugewiesener Schützen, Festlegung von Startzeiten pro Gruppe sowie Prüfung auf Doppelbelegungen.
- **Ergebniseingabe & Stechschießen**:
  - Schnelle Erfassung der Passen-Ergebnisse sowie der Zusatzwertungen (10er, 9er).
  - **Stechschießen bei Punkt-Gleichstand**: Automatische Erkennung von Punktgleichständen (gleiche Gesamtringe, 10er und 9er innerhalb einer Klasse) und gezielte Erfassung der Stech-Ergebnisse zur eindeutigen Platzierung (`nach Stechen (...)`).
- **Mannschaftsverwaltung & Mannschaftswertung**:
  - frei einstellbare Mannschaftsgröße (Teilnehmeranzahl pro Mannschaft) und eigene Mannschaftsklassen.
  - Komfortable Zuordnung von Schützen zu Mannschaften (inkl. Warnhinweis bei Unterbelegung).
  - Auswertung wahlweise als Gesamtwertung über alle Mannschaften oder getrennt nach Mannschaftsklassen sowie optional mit oder ohne Einzelergebnisse der Mannschaftsmitglieder.
- **Online-Eingabe (Webinterface)**: Lokaler Webserver für die mobile Ergebniseingabe per Smartphone oder Tablet. Unterstützt PIN-Authentifizierung, gezielte Gruppenfreigabe, gleichzeitige Eingabe für bis zu zwei Schützen (6 Schüsse pro Passe) und Live-Synchronisation mit der Hauptanwendung.
- **Urkundenerstellung**:
  - Generierung individualisierter Word-Urkunden (`.docx`) auf Basis einer eigenen Vorlage sowohl für **Einzelschützen** als auch für **Mannschaften**.
  - Unterstützt Platzhalter wie `[Turniername]`, `[Datum]`, `[Klasse]`, `[Vorname]`, `[Name]`, `[Verein]`, `[Ergebnis]`, `[Platz]`, `[Mannschaftsname]` und `[Mannschaftsmitglieder]` (optional mit Einzelergebnis hinter jedem Mitgliedsnamen).
- **Schießzettelgenerierung**: Erstellung von gruppenweisen Schießzetteln als Word-Dateien (`.docx`) für bis zu 4 Schützen pro Seite inkl. automatischem Seitenumbruch bei größeren Gruppen.
- **Startgeldverwaltung**: Übersicht und Pflege des Bezahlstatus (`bezahlt`, `unbezahlt`, `überprüfen`) für einzelne Schützen und komplette Vereine per Doppelklick, inklusive Farbcodierung, Suchfilter und Sortierung.
- **PDF-Export & PDF Settings**:
  - Klassenspezifische **PDF-Ergebnislisten** (Einzelwertung)
  - **PDF-Mannschaftswertung** (gesamt oder nach Mannschaftsklassen, mit/ohne Einzelergebnisse)
  - **PDF-Gruppenlisten** mit Startzeiten und Scheibeneinteilung
  - Separate **PDF-Startlisten pro Verein** inkl. Startgeld-Aufstellung und Überweisungsinformationen
  - **PDF Settings**: Individuelle Anpassung aller Schriftgrößen (in `pt`) getrennt für jeden der vier PDF-Dokumenttypen.
- **Live-Bildschirmanzeige**: Für Beamer und große Monitore optimierte Live-Rangliste mit nahtlosem Endlos-Scrolling, Medaillen-Hervorhebung der Top 3, Vollbildmodus und automatischer Aktualisierung.
- **Datenverwaltung**: Vollständiges Speichern und Laden aller Turnier-, Schützen-, Mannschafts-, Ergebnis- und PDF-Einstellungen im JSON-Format.

## Verwendung

1. **Turnier einrichten**: Im Reiter *Turnierverwaltung* Turniername, Datum, Anzahl der Passen und optional Bankdaten eintragen.
2. **Klassen anlegen**: Im Reiter *Klassenverwaltung* die Wettkampfklassen definieren und bei Bedarf das Startgeld pro Klasse festlegen.
3. **Schützen erfassen**: Im Reiter *Schützenverwaltung* alle Teilnehmer anlegen (PINs werden automatisch vergeben) und automatisch oder manuell Gruppen/Scheiben zuweisen.
4. **Gruppen & Startzeiten pflegen**: Im Reiter *Gruppenverwaltung* Startzeiten vergeben sowie Gruppen-PDFs, Vereins-Startlisten oder im Reiter *Schießzettel* die Schießzettel erstellen.
5. **Mannschaften zusammenstellen (optional)**: Im Reiter *Mannschaften* die Mannschaftsgröße und ggf. Mannschaftsklassen festlegen, Mannschaften anlegen und Schützen zuordnen.
6. **Ergebnisse erfassen**: Ergebnisse manuell im Reiter *Ergebniseingabe* oder mobil über den Reiter *Online-Eingabe* eintragen. Bei Punktgleichheit kann über *🎯 Stechschießen* das Stechergebnis hinterlegt werden.
7. **Auswerten & Exportieren**: Ranglisten in der *Ergebnisanzeige*, *Mannschaftswertung* oder *🖥 Bildschirmanzeige* präsentieren, als PDF exportieren und im Reiter *Urkunden* die Siegerurkunden generieren.

## Datenspeicherung

Über die Schaltflächen **„💾 Alle Daten speichern“** und **„📂 Alle Daten laden“** am unteren Fensterrand werden sämtliche Turnierdaten (inkl. Schützen, Klassen, Mannschaften, Ergebnissen, Stechschießen, Gruppenzeiten, Startgeldstatus und PDF-Schriftgrößen) in einer übersichtlichen JSON-Datei gesichert und können jederzeit wieder geladen werden.
