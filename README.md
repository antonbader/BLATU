# Blatu - Blasrohr Turnierverwaltung

Version 1.4.0

## Beschreibung

Blatu ist eine Desktop-Anwendung zur Verwaltung von Blasrohr-Turnieren. Sie ermöglicht die Erfassung von Schützen, Klassen, Turnierergebnissen und erstellt professionelle PDF-Ergebnislisten.

## Projektstruktur

```
blatu/
├── main.py                 # Haupteinstiegspunkt
├── config.py              # Konfiguration und Konstanten
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


## Start der Anwendung

```bash
python main.py
```

## Funktionen

- **Turnierverwaltung**: Erfassung von Turniername, Datum und Anzahl der Passen
- **Klassenverwaltung**: Anlegen und Verwalten von Wettkampfklassen
- **Schützenverwaltung**: Erfassung von Schützendaten (Name, Vorname, Klasse, Verein)
- **Gruppenverwaltung**: Zuweisung von Schützen zu Gruppen und Scheiben, inkl. Uhrzeit-Management
- **Startgeldverwaltung**: Übersicht und Verwaltung des Bezahlstatus pro Schütze und Verein
- **Ergebniseingabe**: Eingabe von Ergebnissen mit Zusatzwertungen (10er, 9er)
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
3. **Schützen erfassen**: Tragen Sie alle Teilnehmer mit ihren Daten ein
4. **Gruppen zuteilen (optional)**: Weisen Sie den Schützen Gruppen und Scheiben zu
5. **Ergebnisse eingeben**: Erfassen Sie die Schießergebnisse für jeden Schützen
6. **Ergebnisse anzeigen**: Lassen Sie sich die Rangliste anzeigen
7. **PDF erstellen**: Exportieren Sie die Ergebnisse als professionelles PDF

## Datenspeicherung

Die Anwendung speichert alle Daten im JSON-Format. Sie können:
- Jederzeit alle Daten speichern
- Gespeicherte Turniere später wieder laden
- Mehrere Turniere verwalten (separate JSON-Dateien)
