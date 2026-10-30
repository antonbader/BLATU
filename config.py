# -*- coding: utf-8 -*-
"""
Konfigurationsdatei für Blatu
Enthält Konstanten und Einstellungen
"""

# Anwendungsinformationen
APP_NAME = "Blasrohr Turnier Verwaltung"
APP_SHORT_NAME = "Blatu"
VERSION = "1.6.0"
VERSION_DATE = "31.10.2026"
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
    "mannschaft_groesse": 3,
    "startgeld_erheben": False,
    "iban": "",
    "bic": "",
    "bankname": "",
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

# Standard-Schriftgrößen für PDFs
DEFAULT_PDF_FONT_SIZES = {
    "ergebnisliste": {
        "title": 18,
        "subtitle": 12,
        "heading": 14,
        "table_header": 10,
        "table_body": 9
    },
    "gruppen": {
        "title": 18,
        "subtitle": 12,
        "heading": 14,
        "table_header": 10,
        "table_body": 10
    },
    "vereine": {
        "title": 16,
        "subtitle": 12,
        "heading": 14,
        "table_header": 10,
        "table_body": 10,
        "footer_text": 10
    },
    "mannschaften": {
        "title": 18,
        "subtitle": 12,
        "heading": 14,
        "table_header": 10,
        "table_body": 9
    }
}
