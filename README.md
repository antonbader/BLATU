# Blatu - Blasrohr Turnierverwaltung

Version 1.5.0

## Beschreibung

Blatu ist eine Desktop-Anwendung zur Verwaltung von Blasrohr-Turnieren. Sie ermöglicht die Erfassung von Schützen, Klassen, Turnierergebnissen und erstellt professionelle PDF-Ergebnislisten.

## Projektstruktur

```
blatu/
├── main.py                 # Haupteinstiegspunkt
├── config.py              # Konfiguration und Konstanten
├── web_server.py          # Webserver für Online-Eingabe
├── models/                # Datenmodelle
│   ├── __init__.py
│   ├── turnier.py        # Turnier-Datenmodell
│   └── schuetze.py       # Schützen-Datenmodell
├── ui/                    # Benutzeroberfläche
│   ├── __init__.py
│   ├── main_window.py    # Hauptfenster
│   ├── turnier_tab.py    # Turnierverwaltung Tab
│   ├── klassen_tab.py    # Klassenverwaltung Tab
│   ├── schuetzen_tab.py  # Schützenverwaltung Tab
│   ├── startgeld_tab.py  # Startgeldverwaltung Tab
│   ├── gruppen_tab.py    # Gruppenverwaltung Tab
│   ├── ergebnisse_tab.py # Ergebniseingabe Tab
│   ├── online_eingabe_tab.py # Tab für Webserver-Steuerung
│   ├── urkunden_tab.py   # Urkundenerstellung Tab
│   ├── ergebnisse_window.py # Ergebnisanzeige Fenster
│   ├── bildschirm_anzeige_window.py # Live-Ergebnisanzeige (für Beamer)
│   └── info_tab.py       # Info Tab
├── utils/                 # Hilfsfunktionen
│   ├── __init__.py
│   ├── data_manager.py   # Speichern/Laden von Daten
│   ├── pdf_generator.py  # PDF-Erstellung
│   └── word_generator.py # Word-Dokument Erstellung
└── README.md
```

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- tkinter (meist in Python enthalten)
- reportlab (für PDF-Erstellung)
- python-docx (für Word-Urkunden)
- flask (für Online-Eingabe)

```bash
pip install reportlab python-docx flask
```

## Start der Anwendung

```bash
python main.py
```

## Funktionen

- **Turnierverwaltung**: Erfassung von Turniername, Datum und Anzahl der Passen
- **Klassenverwaltung**: Anlegen und Verwalten von Wettkampfklassen
- **Schützenverwaltung**: Erfassung von Schützendaten (Name, Vorname, Klasse, Verein, PIN)
- **Gruppenverwaltung**: Zuweisung von Schützen zu Gruppen und Scheiben, inkl. Uhrzeit-Management
- **Startgeldverwaltung**: Übersicht und Verwaltung des Bezahlstatus pro Schütze und Verein
- **Ergebniseingabe**: Eingabe von Ergebnissen mit Zusatzwertungen (10er, 9er)
- **Online-Eingabe**: Mobile Weboberfläche für die dezentrale Ergebniseingabe durch Schützen (Mehrbenutzerfähig, Live-Updates)
- **Urkundenerstellung**: Generierung von individualisierten Urkunden als Word-Dateien (.docx) basierend auf einer Vorlage.
- **Automatische Ranglistenerstellung**: Nach Punkten und Zusatzwertung
- **PDF-Export**:
    - Professionelle PDF-Ergebnislisten (klassenweise)
    - PDF-Gruppenlisten mit Startzeiten
    - Separate PDF-Startlisten für jeden Verein
- **Datenverwaltung**: Speichern und Laden kompletter Turnierdaten als JSON
- **Live-Anzeige**: Automatisches Scrollen und Aktualisieren der Ergebnisse für Zuschauer (Beamer-Modus)

## Verwendung

1. **Turnier einrichten**: Geben Sie Turniername, Datum und Anzahl Passen ein
2. **Klassen anlegen**: Definieren Sie die Wettkampfklassen (z.B. Jugend, Erwachsene, Senioren)
3. **Schützen erfassen**: Tragen Sie alle Teilnehmer mit ihren Daten ein. PINs werden automatisch generiert.
4. **Gruppen zuteilen (optional)**: Weisen Sie den Schützen Gruppen und Scheiben zu
5. **Online-Eingabe aktivieren (optional)**: Starten Sie den Webserver im Tab "Online-Eingabe" und lassen Sie Schützen ihre Ergebnisse selbst per Smartphone eintragen.
6. **Ergebnisse anzeigen**: Lassen Sie sich die Rangliste anzeigen
7. **PDF erstellen**: Exportieren Sie die Ergebnisse als professionelles PDF

## Datenspeicherung

Die Anwendung speichert alle Daten im JSON-Format. Sie können:
- Jederzeit alle Daten speichern
- Gespeicherte Turniere später wieder laden
- Mehrere Turniere verwalten (separate JSON-Dateien)
