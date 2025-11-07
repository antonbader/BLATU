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
        if klasse_name and klasse_name not in self.klassen:
            self.klassen.append(klasse_name)
            self.klassen.sort()
            return True
        return False
    
    def remove_klasse(self, klasse_name):
        """Entfernt eine Klasse"""
        if klasse_name in self.klassen:
            self.klassen.remove(klasse_name)
            return True
        return False
    
    def get_klassen(self):
        """Gibt alle Klassen zurück"""
        return self.klassen.copy()
    
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
