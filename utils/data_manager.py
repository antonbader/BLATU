# -*- coding: utf-8 -*-
"""
Datenverwaltung - Speichern und Laden von Daten
"""

import json
from tkinter import filedialog

from config import FILE_TYPES_JSON


class DataManager:
    """Verwaltet das Speichern und Laden von Daten"""
    
    def __init__(self, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
    
    def save_to_file(self):
        """Speichert alle Daten in eine JSON-Datei"""
        turnier = self.turnier_model.get_turnier_data()
        schuetzen = self.schuetze_model.get_all_schuetzen()
        klassen = self.turnier_model.get_klassen()
        
        if not schuetzen and not klassen and not turnier["name"]:
            return False, "Es sind keine Daten zum Speichern vorhanden!"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=FILE_TYPES_JSON,
            title="Alle Daten speichern"
        )
        
        if not file_path:
            return False, ""  # Benutzer hat abgebrochen
        
        try:
            data = {
                "turnier": turnier,
                "schuetzen": schuetzen,
                "klassen": klassen,
                "ergebnisse": self.turnier_model.get_all_ergebnisse(),
                "group_times": self.turnier_model.get_all_group_times()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            message = (
                f"Daten wurden gespeichert:\n"
                f"Turnier: {turnier['name'] if turnier['name'] else 'Keine Angabe'}\n"
                f"{len(schuetzen)} Schützen\n"
                f"{len(klassen)} Klassen\n"
                f"{len(self.turnier_model.get_all_ergebnisse())} Ergebnisse"
            )
            return True, message
            
        except Exception as e:
            return False, f"Fehler beim Speichern:\n{str(e)}"
    
    def load_from_file(self):
        """Lädt alle Daten aus einer JSON-Datei"""
        file_path = filedialog.askopenfilename(
            filetypes=FILE_TYPES_JSON,
            title="Alle Daten laden"
        )
        
        if not file_path:
            return False, ""  # Benutzer hat abgebrochen
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Daten zurücksetzen
            self.schuetze_model.clear_schuetzen()
            self.turnier_model.clear_klassen()
            self.turnier_model.clear_ergebnisse()
            self.turnier_model.clear_group_times()
            
            # Neue Daten laden
            if isinstance(data, dict):
                # Turnierdaten
                turnier = data.get('turnier', {"name": "", "datum": "", "anzahl_passen": 1, "max_scheiben": 3})
                self.turnier_model.set_turnier_data(
                    turnier.get('name', ''),
                    turnier.get('datum', ''),
                    turnier.get('anzahl_passen', 1),
                    turnier.get('show_halves', False),
                    turnier.get('max_scheiben', 3),
                    turnier.get('startgeld_erheben', False),
                    turnier.get('iban', ''),
                    turnier.get('kontoinhaber', ''),
                    turnier.get('zahldatum', '')
                )
                
                # Klassen
                for klasse_data in data.get('klassen', []):
                    if isinstance(klasse_data, dict):
                        # Neues Format: {'name': 'Name', 'startgeld': 1000}
                        klasse_name = klasse_data.get('name')
                        startgeld = klasse_data.get('startgeld', 0)
                        if self.turnier_model.add_klasse(klasse_name):
                             # Startgeld wird in Cent gespeichert, also direkt übergeben
                            self.turnier_model.update_klasse_startgeld(klasse_name, float(startgeld) / 100.0)
                    else:
                        # Altes Format: 'Klassenname'
                        self.turnier_model.add_klasse(klasse_data)

                # Schützen
                for schuetze in data.get('schuetzen', []):
                    new_schuetze_index = self.schuetze_model.add_schuetze(
                        schuetze.get('name'),
                        schuetze.get('vorname'),
                        schuetze.get('klasse'),
                        schuetze.get('verein', ''),
                        schuetze.get('gruppe'),
                        schuetze.get('scheibe')
                    )
                    # Lade optional den Startgeld-Status
                    status = schuetze.get('startgeld_status')
                    if status:
                        self.schuetze_model.update_schuetze_startgeld_status(new_schuetze_index, status)

                # Gruppen-Uhrzeiten
                group_times = data.get('group_times', {})
                for group, time in group_times.items():
                    # Konvertiere group zu int, da JSON keys immer strings sind
                    self.turnier_model.set_group_time(int(group), time)

                # Ergebnisse
                ergebnisse = data.get('ergebnisse', {})
                for schuetze_id, ergebnis in ergebnisse.items():
                    if isinstance(ergebnis, dict):
                        self.turnier_model.add_ergebnis(
                            schuetze_id,
                            ergebnis.get('passen', []),
                            ergebnis.get('anzahl_10er', 0),
                            ergebnis.get('anzahl_9er', 0)
                        )
            else:
                # Alte Format-Kompatibilität (nur Schützenliste)
                for schuetze in data:
                    self.schuetze_model.add_schuetze(
                        schuetze['name'],
                        schuetze['vorname'],
                        schuetze['klasse'],
                        schuetze.get('verein', '')
                    )
            
            turnier = self.turnier_model.get_turnier_data()
            schuetzen = self.schuetze_model.get_all_schuetzen()
            klassen = self.turnier_model.get_klassen()
            ergebnisse = self.turnier_model.get_all_ergebnisse()
            
            message = (
                f"Turnier: {turnier['name'] if turnier['name'] else 'Keine Angabe'}\n"
                f"{len(schuetzen)} Schützen, {len(klassen)} Klassen und "
                f"{len(ergebnisse)} Ergebnisse wurden geladen!"
            )
            return True, message
            
        except Exception as e:
            return False, f"Fehler beim Laden:\n{str(e)}"
