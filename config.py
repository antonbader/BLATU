# -*- coding: utf-8 -*-
"""
Konfigurationsdatei für Blatu
Enthält Konstanten und Einstellungen
"""

# Anwendungsinformationen
APP_NAME = "Blasrohr Turnier Verwaltung"
APP_SHORT_NAME = "Blatu"
VERSION = "1.4.0"
VERSION_DATE = "19.11.2025"
AUTHOR = "Anton Bader"
EMAIL = "info@anton-bader.de"
WEBSITE = "https://www.anton-bader.de"

# Fenstereinstellungen
WINDOW_WIDTH = 950
WINDOW_HEIGHT = 750
WINDOW_TITLE = APP_NAME

# Turnier-Standardwerte
DEFAULT_TURNIER = {
    "name": "",
    "datum": "",
    "anzahl_passen": 1,
    "show_halves": False,
    "max_scheiben": 3,
    "startgeld_erheben": False,
    "iban": "",
    "kontoinhaber": "",
    "zahldatum": ""
}

# Dateifilter
FILE_TYPES_JSON = [("JSON Dateien", "*.json"), ("Alle Dateien", "*.*")]
FILE_TYPES_PDF = [("PDF Dateien", "*.pdf"), ("Alle Dateien", "*.*")]

# UI-Farben
COLOR_PRIMARY = "#2E5090"
COLOR_SECONDARY = "#4472C4"
COLOR_LINK = "#0066CC"
COLOR_GRAY = "#666666"
COLOR_LIGHT_GRAY = "#999999"

# PDF-Farben
PDF_COLOR_HEADER = "#4472C4"
PDF_COLOR_GOLD = "#FFD700"
PDF_COLOR_SILVER = "#C0C0C0"
PDF_COLOR_BRONZE = "#CD7F32"
PDF_COLOR_ROW_ALT = "#F2F2F2"

# Limits
MAX_PASSEN = 100
MIN_PASSEN = 1
MAX_PASSEN_FOR_DISPLAY = 12  # Maximale Anzahl Passen die in PDF angezeigt werden
