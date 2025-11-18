# -*- coding: utf-8 -*-
"""
Turnier-Datenmodell
Verwaltet Turnierdaten, Klassen und Ergebnisse
"""

from config import DEFAULT_TURNIER


class TurnierModel:
    """Verwaltet alle Turnierdaten"""
    
    def __init__(self):
        self.turnier = DEFAULT_TURNIER.copy()
        self.klassen = []
        self.ergebnisse = {}
        self.group_times = {}
    
    def set_turnier_data(self, name, datum, anzahl_passen, show_halves=False, max_scheiben=3):
        """Setzt die Turnierdaten"""
        self.turnier = {
            "name": name,
            "datum": datum,
            "anzahl_passen": anzahl_passen,
            "show_halves": show_halves,
            "max_scheiben": max_scheiben
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
        """Aktualisiert das Startgeld für eine Klasse"""
        for klasse in self.klassen:
            if klasse['name'] == klasse_name:
                try:
                    # Speichere als Integer in Cent
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
    
    def add_ergebnis(self, schuetze_id, passen, anzahl_10er, anzahl_9er):
        """Fügt ein Ergebnis hinzu oder aktualisiert es"""
        self.ergebnisse[schuetze_id] = {
            'passen': passen,
            'anzahl_10er': anzahl_10er,
            'anzahl_9er': anzahl_9er
        }
    
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

    def reset(self):
        """Setzt alle Daten zurück"""
        self.turnier = DEFAULT_TURNIER.copy()
        self.klassen = []
        self.ergebnisse = {}
        self.group_times = {}
