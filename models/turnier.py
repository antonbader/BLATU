# -*- coding: utf-8 -*-
"""
Turnier-Datenmodell
Verwaltet Turnierdaten, Klassen, Mannschaften und Ergebnisse
"""

import copy
from config import DEFAULT_TURNIER, DEFAULT_PDF_FONT_SIZES


class TurnierModel:
    """Verwaltet alle Turnierdaten"""
    
    def __init__(self):
        self.turnier = DEFAULT_TURNIER.copy()
        self.klassen = []
        self.mannschaft_groesse = DEFAULT_TURNIER.get("mannschaft_groesse", 3)
        self.mannschaftsklassen = []
        self.mannschaften = []
        self.ergebnisse = {}
        self.group_times = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self.last_update_time = 0
    
    def set_turnier_data(self, name, datum, anzahl_passen, *, show_halves=False, max_scheiben=3,
                         mannschaft_groesse=None, startgeld_erheben=False, iban="", bic="",
                         bankname="", kontoinhaber="", zahldatum=""):
        """Setzt die Turnierdaten und stellt eine flache Struktur sicher."""
        if mannschaft_groesse is not None:
            try:
                self.mannschaft_groesse = max(1, int(mannschaft_groesse))
            except (ValueError, TypeError):
                pass
        self.turnier = {
            'name': name,
            'datum': datum,
            'anzahl_passen': anzahl_passen,
            'show_halves': show_halves,
            'max_scheiben': max_scheiben,
            'mannschaft_groesse': self.mannschaft_groesse,
            'startgeld_erheben': startgeld_erheben,
            'iban': iban,
            'bic': bic,
            'bankname': bankname,
            'kontoinhaber': kontoinhaber,
            'zahldatum': zahldatum
        }
    
    def get_turnier_data(self):
        """Gibt die Turnierdaten zurück"""
        data = self.turnier.copy()
        data['mannschaft_groesse'] = self.mannschaft_groesse
        return data
    
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

    # --- Mannschaftsverwaltung ---

    def set_mannschaft_groesse(self, groesse):
        """Setzt die maximale Anzahl an Teilnehmern pro Mannschaft"""
        try:
            val = int(groesse)
            if val < 1:
                return False
            self.mannschaft_groesse = val
            self.turnier['mannschaft_groesse'] = val
            self._touch()
            return True
        except (ValueError, TypeError):
            return False

    def get_mannschaft_groesse(self):
        """Gibt die konfigurierte Anzahl an Teilnehmern pro Mannschaft zurück"""
        return self.mannschaft_groesse

    def add_mannschaftsklasse(self, klasse_name):
        """Fügt eine neue Mannschaftsklasse hinzu"""
        klasse_name = (klasse_name or "").strip()
        if klasse_name and not any(k['name'] == klasse_name for k in self.mannschaftsklassen):
            self.mannschaftsklassen.append({'name': klasse_name})
            self.mannschaftsklassen.sort(key=lambda k: k['name'])
            self._touch()
            return True
        return False

    def remove_mannschaftsklasse(self, klasse_name):
        """Entfernt eine Mannschaftsklasse"""
        initial_len = len(self.mannschaftsklassen)
        self.mannschaftsklassen = [k for k in self.mannschaftsklassen if k['name'] != klasse_name]
        if len(self.mannschaftsklassen) < initial_len:
            self._touch()
            return True
        return False

    def get_mannschaftsklassen(self):
        """Gibt alle Mannschaftsklassen als Liste von Dictionaries zurück"""
        return [k.copy() for k in self.mannschaftsklassen]

    def get_mannschaftsklassen_names(self):
        """Gibt eine Liste aller Mannschaftsklassennamen zurück"""
        return [k['name'] for k in self.mannschaftsklassen]

    def clear_mannschaftsklassen(self):
        """Löscht alle Mannschaftsklassen"""
        self.mannschaftsklassen = []
        self._touch()

    def add_mannschaft(self, name, klasse="", mitglieder=None):
        """Fügt eine neue Mannschaft hinzu"""
        name = (name or "").strip()
        if not name:
            return False
        if any(m['name'].lower() == name.lower() for m in self.mannschaften):
            return False
        mitglieder_list = list(mitglieder) if mitglieder else []
        self.mannschaften.append({
            'name': name,
            'klasse': (klasse or "").strip(),
            'mitglieder': mitglieder_list
        })
        self._touch()
        return True

    def update_mannschaft(self, index, name, klasse="", mitglieder=None):
        """Aktualisiert eine bestehende Mannschaft"""
        name = (name or "").strip()
        if not name or not (0 <= index < len(self.mannschaften)):
            return False
        for i, m in enumerate(self.mannschaften):
            if i != index and m['name'].lower() == name.lower():
                return False
        mitglieder_list = list(mitglieder) if mitglieder is not None else self.mannschaften[index].get('mitglieder', [])
        self.mannschaften[index] = {
            'name': name,
            'klasse': (klasse or "").strip(),
            'mitglieder': mitglieder_list
        }
        self._touch()
        return True

    def remove_mannschaft(self, index):
        """Entfernt eine Mannschaft anhand des Index"""
        if 0 <= index < len(self.mannschaften):
            del self.mannschaften[index]
            self._touch()
            return True
        return False

    def get_mannschaft(self, index):
        """Gibt eine Kopie einer Mannschaft zurück"""
        if 0 <= index < len(self.mannschaften):
            m = self.mannschaften[index]
            return {
                'name': m['name'],
                'klasse': m.get('klasse', ''),
                'mitglieder': list(m.get('mitglieder', []))
            }
        return None

    def get_all_mannschaften(self):
        """Gibt alle Mannschaften zurück"""
        return [
            {
                'name': m['name'],
                'klasse': m.get('klasse', ''),
                'mitglieder': list(m.get('mitglieder', []))
            }
            for m in self.mannschaften
        ]

    def clear_mannschaften(self):
        """Löscht alle Mannschaften"""
        self.mannschaften = []
        self._touch()

    def update_schuetze_id_in_mannschaften(self, old_id, new_id):
        """Aktualisiert die Schützen-ID in allen Mannschaften, wenn ein Schütze umbenannt wurde"""
        if old_id == new_id:
            return
        changed = False
        for m in self.mannschaften:
            mitglieder = m.get('mitglieder', [])
            if old_id in mitglieder:
                m['mitglieder'] = [new_id if mid == old_id else mid for mid in mitglieder]
                changed = True
        if changed:
            self._touch()

    def remove_schuetze_from_mannschaften(self, schuetze_id):
        """Entfernt einen gelöschten Schützen aus allen Mannschaften"""
        changed = False
        for m in self.mannschaften:
            mitglieder = m.get('mitglieder', [])
            if schuetze_id in mitglieder:
                m['mitglieder'] = [mid for mid in mitglieder if mid != schuetze_id]
                changed = True
        if changed:
            self._touch()

    def get_mannschaft_for_schuetze(self, schuetze_id):
        """Gibt die Namen aller Mannschaften zurück, denen dieser Schütze zugeordnet ist"""
        return [m['name'] for m in self.mannschaften if schuetze_id in m.get('mitglieder', [])]

    def calculate_mannschaft_results(self, schuetze_model, group_by_klasse=False):
        """
        Berechnet die Mannschaftswertung.
        Gibt ein Dictionary {gruppen_name: [mannschaft_dict, ...]} zurück.
        Wenn group_by_klasse=False, gibt es genau eine Gruppe 'Alle Mannschaften'.
        Wenn group_by_klasse=True, wird nach Mannschaftsklasse gruppiert.
        """
        from models.schuetze import SchuetzeModel

        all_schuetzen = schuetze_model.get_all_schuetzen()
        schuetzen_by_id = {SchuetzeModel.get_schuetze_id(s): s for s in all_schuetzen}
        anzahl_passen = self.turnier.get('anzahl_passen', 1)

        grouped = {}
        for m in self.mannschaften:
            mitglieder_details = []
            team_gesamt = 0
            team_10er = 0
            team_9er = 0
            team_passen = [0] * anzahl_passen

            for s_id in m.get('mitglieder', []):
                s = schuetzen_by_id.get(s_id)
                if not s:
                    continue
                erg = self.get_ergebnis(s_id)
                if erg:
                    passen = list(erg.get('passen', []))
                    s_gesamt = sum(passen)
                    s_10er = erg.get('anzahl_10er', 0)
                    s_9er = erg.get('anzahl_9er', 0)
                else:
                    passen = []
                    s_gesamt = 0
                    s_10er = 0
                    s_9er = 0

                for p_idx in range(anzahl_passen):
                    if p_idx < len(passen):
                        team_passen[p_idx] += int(passen[p_idx])

                team_gesamt += s_gesamt
                team_10er += s_10er
                team_9er += s_9er

                mitglieder_details.append({
                    'schuetze_id': s_id,
                    'name': s.get('name', ''),
                    'vorname': s.get('vorname', ''),
                    'verein': s.get('verein', ''),
                    'klasse': s.get('klasse', ''),
                    'ergebnisse': passen,
                    'gesamt': s_gesamt,
                    'anzahl_10er': s_10er,
                    'anzahl_9er': s_9er
                })

            klasse_label = m.get('klasse', '').strip() or "Ohne Klasse"
            group_key = klasse_label if group_by_klasse else "Alle Mannschaften"

            grouped.setdefault(group_key, []).append({
                'name': m['name'],
                'klasse': m.get('klasse', '').strip(),
                'mitglieder': mitglieder_details,
                'ergebnisse': team_passen,
                'gesamt': team_gesamt,
                'anzahl_10er': team_10er,
                'anzahl_9er': team_9er
            })

        # Sortieren und Platzierung berechnen
        for group_key, teams in grouped.items():
            teams.sort(
                key=lambda t: (t['gesamt'], t['anzahl_10er'], t['anzahl_9er']),
                reverse=True
            )
            platz = 1
            prev_team = None
            for idx, team in enumerate(teams):
                if prev_team and (
                    team['gesamt'] == prev_team['gesamt'] and
                    team['anzahl_10er'] == prev_team['anzahl_10er'] and
                    team['anzahl_9er'] == prev_team['anzahl_9er']
                ):
                    current_platz = platz
                else:
                    platz = idx + 1
                    current_platz = platz
                team['platz'] = current_platz
                prev_team = team

        return grouped
    
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
        self.mannschaft_groesse = DEFAULT_TURNIER.get("mannschaft_groesse", 3)
        self.mannschaftsklassen = []
        self.mannschaften = []
        self.ergebnisse = {}
        self.group_times = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self._touch()

    def _touch(self):
        """Aktualisiert den Zeitstempel der letzten Änderung"""
        import time
        self.last_update_time = time.time()
