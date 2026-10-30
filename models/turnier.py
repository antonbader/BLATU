# -*- coding: utf-8 -*-
"""
Turnier-Datenmodell
Verwaltet Turnierdaten, Klassen und Ergebnisse
"""

import copy
from config import DEFAULT_TURNIER, DEFAULT_PDF_FONT_SIZES


class TurnierModel:
    """Verwaltet alle Turnierdaten"""
    
    def __init__(self):
        self.turnier = DEFAULT_TURNIER.copy()
        self.klassen = []
        self.ergebnisse = {}
        self.group_times = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self.last_update_time = 0
    
    def set_turnier_data(self, name, datum, anzahl_passen, *, show_halves=False, max_scheiben=3,
                         startgeld_erheben=False, iban="", bic="", bankname="", kontoinhaber="", zahldatum=""):
        """Setzt die Turnierdaten und stellt eine flache Struktur sicher."""
        self.turnier = {
            'name': name,
            'datum': datum,
            'anzahl_passen': anzahl_passen,
            'show_halves': show_halves,
            'max_scheiben': max_scheiben,
            'startgeld_erheben': startgeld_erheben,
            'iban': iban,
            'bic': bic,
            'bankname': bankname,
            'kontoinhaber': kontoinhaber,
            'zahldatum': zahldatum
        }
    
    def get_turnier_data(self):
        """Gibt die Turnierdaten zurück"""
        return self.turnier.copy()
    
    def add_klasse(self, klasse_name):
        """Fügt eine neue Klasse hinzu"""
        if klasse_name and not any(k['name'] == klasse_name for k in self.klassen):
            self.klassen.append({'name': klasse_name, 'startgeld': 0})
            self.klassen.sort(key=lambda k: k['name'])
            return True
        return False

    def update_klasse_startgeld(self, klasse_name, startgeld):
        """Aktualisiert das Startgeld für eine Klasse.

        Akzeptiert einen String (z.B. "15.00") aus der UI oder einen Integer
        (z.B. 1500) aus der geladenen Datei.
        """
        for klasse in self.klassen:
            if klasse['name'] == klasse_name:
                try:
                    # Wenn der Input ein String ist (aus der UI), in Cent umrechnen
                    if isinstance(startgeld, str):
                        # Ersetze Komma durch Punkt für die Umwandlung
                        startgeld_float = float(startgeld.replace(',', '.'))
                        klasse['startgeld'] = int(startgeld_float * 100)
                    # Wenn der Input bereits ein Integer ist (aus der Datei), direkt verwenden
                    elif isinstance(startgeld, int):
                        klasse['startgeld'] = startgeld
                    else:
                        # Fallback für unerwartete Typen
                        klasse['startgeld'] = int(float(startgeld) * 100)
                    return True
                except (ValueError, TypeError):
                    return False
        return False

    def get_klasse_startgeld(self, klasse_name):
        """Gibt das Startgeld für eine Klasse in Cent zurück"""
        for klasse in self.klassen:
            if klasse['name'] == klasse_name:
                return klasse.get('startgeld', 0)
        return 0

    def remove_klasse(self, klasse_name):
        """Entfernt eine Klasse"""
        initial_len = len(self.klassen)
        self.klassen = [k for k in self.klassen if k['name'] != klasse_name]
        return len(self.klassen) < initial_len

    def get_klassen(self):
        """Gibt alle Klassen als Liste von Dictionaries zurück"""
        return self.klassen.copy()

    def get_klassen_names(self):
        """Gibt eine Liste aller Klassennamen zurück"""
        return [k['name'] for k in self.klassen]

    def clear_klassen(self):
        """Löscht alle Klassen"""
        self.klassen = []
    
    def add_ergebnis(self, schuetze_id, passen, anzahl_10er, anzahl_9er, stechen=...):
        """Fügt ein Ergebnis hinzu oder aktualisiert es"""
        current = self.ergebnisse.get(schuetze_id, {})
        old_key = (
            sum(current.get('passen', [])),
            current.get('anzahl_10er', 0),
            current.get('anzahl_9er', 0)
        ) if current else None
        new_key = (sum(passen), anzahl_10er, anzahl_9er)

        current.update({
            'passen': passen,
            'anzahl_10er': anzahl_10er,
            'anzahl_9er': anzahl_9er
        })
        if stechen is not ...:
            current['stechen'] = stechen
        elif old_key is not None and old_key != new_key:
            current['stechen'] = None
        elif 'stechen' not in current:
            current['stechen'] = None
        self.ergebnisse[schuetze_id] = current
        self._touch()

    def set_stechen(self, schuetze_id, stechen_wert):
        """Setzt oder löscht das Stechschießen-Ergebnis eines Schützen"""
        if schuetze_id in self.ergebnisse:
            self.ergebnisse[schuetze_id]['stechen'] = stechen_wert
            self._touch()
            return True
        return False

    def add_web_ergebnis(self, schuetze_id, passen_sums, anzahl_10er, anzahl_9er, web_raw_data):
        """
        Fügt Ergebnisse von der Weboberfläche hinzu.
        Speichert zusätzlich die Rohdaten (Einzelschüsse).

        :param schuetze_id: ID des Schützen
        :param passen_sums: Liste der Passen-Summen (z.B. [45, 50, ...])
        :param anzahl_10er: Anzahl der 10er
        :param anzahl_9er: Anzahl der 9er
        :param web_raw_data: Dictionary mit Einzelschüssen pro Passe
                             z.B. {0: [10, 9, 9, 8, 7, 6], 1: [...]}
        """
        current = self.ergebnisse.get(schuetze_id, {})
        old_key = (
            sum(current.get('passen', [])),
            current.get('anzahl_10er', 0),
            current.get('anzahl_9er', 0)
        ) if current else None
        new_key = (sum(passen_sums), anzahl_10er, anzahl_9er)

        current.update({
            'passen': passen_sums,
            'anzahl_10er': anzahl_10er,
            'anzahl_9er': anzahl_9er,
            'web_raw_data': web_raw_data
        })
        if old_key is not None and old_key != new_key:
            current['stechen'] = None
        elif 'stechen' not in current:
            current['stechen'] = None
        self.ergebnisse[schuetze_id] = current
        self._touch()
    
    def get_ergebnis(self, schuetze_id):
        """Gibt ein Ergebnis zurück"""
        return self.ergebnisse.get(schuetze_id, None)
    
    def get_all_ergebnisse(self):
        """Gibt alle Ergebnisse zurück"""
        return self.ergebnisse.copy()
    
    def clear_ergebnisse(self):
        """Löscht alle Ergebnisse"""
        self.ergebnisse = {}
    
    def set_group_time(self, group, time):
        """Setzt die Uhrzeit für eine Gruppe"""
        self.group_times[group] = time

    def get_group_time(self, group):
        """Gibt die Uhrzeit für eine Gruppe zurück"""
        return self.group_times.get(group, "")

    def get_all_group_times(self):
        """Gibt alle Gruppen-Uhrzeiten zurück"""
        return self.group_times.copy()

    def clear_group_times(self):
        """Löscht alle Gruppen-Uhrzeiten"""
        self.group_times = {}

    def get_pdf_font_sizes(self):
        """Gibt die aktuellen PDF-Schriftgrößen zurück"""
        return copy.deepcopy(self.pdf_font_sizes)

    def set_pdf_font_sizes(self, font_sizes):
        """Aktualisiert die PDF-Schriftgrößen (merged mit Standardwerten)"""
        merged = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        if isinstance(font_sizes, dict):
            for doc_type, doc_defaults in merged.items():
                if isinstance(font_sizes.get(doc_type), dict):
                    for key in doc_defaults:
                        val = font_sizes[doc_type].get(key)
                        if val is not None:
                            try:
                                doc_defaults[key] = max(6, min(48, int(val)))
                            except (ValueError, TypeError):
                                pass
        self.pdf_font_sizes = merged

    def reset_pdf_font_sizes(self):
        """Setzt die PDF-Schriftgrößen auf die Standardwerte zurück"""
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)

    def reset(self):
        """Setzt alle Daten zurück"""
        self.turnier = DEFAULT_TURNIER.copy()
        self.klassen = []
        self.ergebnisse = {}
        self.group_times = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self._touch()

    def _touch(self):
        """Aktualisiert den Zeitstempel der letzten Änderung"""
        import time
        self.last_update_time = time.time()
