# -*- coding: utf-8 -*-
"""
Schützen-Datenmodell
Verwaltet Schützendaten
"""


class SchuetzeModel:
    """Verwaltet alle Schützendaten"""
    
    def __init__(self):
        self.schuetzen = []
    
    def add_schuetze(self, name, vorname, klasse, verein="", gruppe=None, scheibe=None):
        """Fügt einen neuen Schützen hinzu"""
        schuetze = {
            "name": name,
            "vorname": vorname,
            "klasse": klasse,
            "verein": verein,
            "gruppe": gruppe,
            "scheibe": scheibe
        }
        self.schuetzen.append(schuetze)
        return len(self.schuetzen) - 1
    
    def update_schuetze(self, index, name, vorname, klasse, verein="", gruppe=None, scheibe=None):
        """Aktualisiert einen bestehenden Schützen"""
        if 0 <= index < len(self.schuetzen):
            self.schuetzen[index] = {
                "name": name,
                "vorname": vorname,
                "klasse": klasse,
                "verein": verein,
                "gruppe": gruppe,
                "scheibe": scheibe
            }
            return True
        return False
    
    def remove_schuetze(self, index):
        """Entfernt einen Schützen"""
        if 0 <= index < len(self.schuetzen):
            del self.schuetzen[index]
            return True
        return False
    
    def get_schuetze(self, index):
        """Gibt einen Schützen zurück"""
        if 0 <= index < len(self.schuetzen):
            return self.schuetzen[index].copy()
        return None
    
    def get_all_schuetzen(self):
        """Gibt alle Schützen zurück"""
        return [s.copy() for s in self.schuetzen]
    
    def clear_schuetzen(self):
        """Löscht alle Schützen"""
        self.schuetzen = []
    
    def get_schuetzen_by_klasse(self, klasse):
        """Gibt alle Schützen einer Klasse zurück"""
        return [s for s in self.schuetzen if s['klasse'] == klasse]
    
    def count_schuetzen_by_klasse(self, klasse):
        """Zählt Schützen einer Klasse"""
        return len(self.get_schuetzen_by_klasse(klasse))
    
    @staticmethod
    def get_schuetze_id(schuetze):
        """Erzeugt eine eindeutige ID für einen Schützen"""
        return f"{schuetze['name']}_{schuetze['vorname']}_{schuetze['klasse']}"

    def calculate_results(self, turnier_model):
        """Berechnet und gruppiert die Ergebnisse für alle Schützen."""
        results_by_class = {}

        for schuetze in self.schuetzen:
            schuetze_id = self.get_schuetze_id(schuetze)
            ergebnis_data = turnier_model.get_ergebnis(schuetze_id)

            if ergebnis_data:
                gesamt = sum(ergebnis_data.get('passen', [0]))
            else:
                gesamt = 0

            # Erstelle eine Kopie, um das Original nicht zu verändern
            schuetze_with_result = schuetze.copy()
            schuetze_with_result['Gesamt'] = gesamt

            klasse = schuetze['klasse']
            if klasse not in results_by_class:
                results_by_class[klasse] = []

            results_by_class[klasse].append(schuetze_with_result)

        # Sortiere die Schützen in jeder Klasse nach dem Gesamtergebnis
        for klasse in results_by_class:
            results_by_class[klasse].sort(key=lambda s: s.get('Gesamt', 0), reverse=True)
            # Platzierung hinzufügen
            for i, schuetze in enumerate(results_by_class[klasse]):
                schuetze['Platz'] = i + 1

        return results_by_class
