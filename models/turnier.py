# -*- coding: utf-8 -*-
"""
Turnier-Datenmodell
Verwaltet Turnierdaten, Klassen, Mannschaften und Ergebnisse
"""

import copy
from datetime import datetime, timedelta
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
        self.group_dates = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self.last_update_time = 0
    
    def set_turnier_data(self, name, datum, anzahl_passen, *, enddatum=None, mehrtaegig=None,
                         show_halves=False, max_scheiben=None,
                         anzahl_gruppen=None, show_empty_slots_ui=None, show_empty_slots_pdf=None,
                         mannschaft_groesse=None, startgeld_erheben=False, iban="", bic="",
                         bankname="", kontoinhaber="", zahldatum=""):
        """Setzt die Turnierdaten und stellt eine flache Struktur sicher."""
        if mannschaft_groesse is not None:
            try:
                self.mannschaft_groesse = max(1, int(mannschaft_groesse))
            except (ValueError, TypeError):
                pass
        if max_scheiben is None:
            max_scheiben = self.turnier.get('max_scheiben', 3)
        if anzahl_gruppen is None:
            anzahl_gruppen = self.turnier.get('anzahl_gruppen', 0)
        if show_empty_slots_ui is None:
            show_empty_slots_ui = self.turnier.get('show_empty_slots_ui', True)
        if show_empty_slots_pdf is None:
            show_empty_slots_pdf = self.turnier.get('show_empty_slots_pdf', True)

        raw_datum = (datum or "").strip()
        if enddatum is None and mehrtaegig is None:
            if " - " in raw_datum:
                parts = [p.strip() for p in raw_datum.split(" - ", 1)]
                startdatum_val = parts[0]
                enddatum_val = parts[1] if len(parts) > 1 else ""
                mehrtaegig_val = bool(enddatum_val and enddatum_val != startdatum_val)
            elif raw_datum == self.turnier.get('datum', '') and self.turnier.get('mehrtaegig', False):
                startdatum_val = self.turnier.get('startdatum', raw_datum)
                enddatum_val = self.turnier.get('enddatum', '')
                mehrtaegig_val = True
            else:
                startdatum_val = raw_datum
                enddatum_val = ""
                mehrtaegig_val = False
        else:
            startdatum_val = raw_datum
            enddatum_val = (enddatum or "").strip()
            if mehrtaegig is None:
                mehrtaegig_val = bool(enddatum_val and enddatum_val != startdatum_val)
            else:
                mehrtaegig_val = bool(mehrtaegig)
            if not mehrtaegig_val:
                enddatum_val = ""

        if mehrtaegig_val and startdatum_val and enddatum_val and startdatum_val != enddatum_val:
            display_datum = f"{startdatum_val} - {enddatum_val}"
        else:
            display_datum = startdatum_val

        self.turnier = {
            'name': name,
            'datum': display_datum,
            'startdatum': startdatum_val,
            'enddatum': enddatum_val,
            'mehrtaegig': mehrtaegig_val,
            'anzahl_passen': anzahl_passen,
            'show_halves': show_halves,
            'max_scheiben': max_scheiben,
            'anzahl_gruppen': anzahl_gruppen,
            'show_empty_slots_ui': show_empty_slots_ui,
            'show_empty_slots_pdf': show_empty_slots_pdf,
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
        """Aktualisiert die Schützen-ID in allen Mannschaften und Ergebnissen, wenn ein Schütze bearbeitet wurde"""
        if old_id == new_id:
            return
        changed = False
        for m in self.mannschaften:
            mitglieder = m.get('mitglieder', [])
            if old_id in mitglieder:
                m['mitglieder'] = [new_id if mid == old_id else mid for mid in mitglieder]
                changed = True
        if old_id in self.ergebnisse:
            old_erg = self.ergebnisse.pop(old_id)
            if new_id not in self.ergebnisse:
                self.ergebnisse[new_id] = old_erg
            changed = True
        if changed:
            self._touch()

    def remove_ergebnis(self, schuetze_id):
        """Entfernt das Ergebnis eines gelöschten Schützen"""
        if schuetze_id in self.ergebnisse:
            del self.ergebnisse[schuetze_id]
            self._touch()
            return True
        return False

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
    
    def add_ergebnis(self, schuetze_id, passen, anzahl_10er, anzahl_9er, stechen=..., web_raw_data=...):
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
        if web_raw_data is not ... and web_raw_data is not None:
            current['web_raw_data'] = web_raw_data
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
        self._touch()
    
    def is_mehrtaegig(self):
        """Gibt zurück, ob das Turnier über mehrere Tage geht."""
        if self.turnier.get('mehrtaegig', False):
            return True
        tage = self.get_turnier_tage()
        if len(tage) > 1:
            return True
        unique_group_dates = {str(d).strip() for d in self.group_dates.values() if d and str(d).strip()}
        return len(unique_group_dates) > 1

    def get_turnier_tage(self):
        """Gibt eine geordnete Liste der Turniertage (als Datums-Strings) zurück."""
        startdatum = (self.turnier.get('startdatum') or "").strip()
        raw_datum = (self.turnier.get('datum') or "").strip()
        enddatum = (self.turnier.get('enddatum') or "").strip()

        if not startdatum and raw_datum:
            if " - " in raw_datum:
                parts = [p.strip() for p in raw_datum.split(" - ", 1)]
                startdatum = parts[0]
                if not enddatum and len(parts) > 1:
                    enddatum = parts[1]
            else:
                startdatum = raw_datum

        mehrtaegig = self.turnier.get('mehrtaegig', False) or bool(enddatum and enddatum != startdatum)
        if not mehrtaegig or not enddatum or enddatum == startdatum:
            return [startdatum] if startdatum else []

        if not startdatum:
            return [enddatum] if enddatum else []

        for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d.%m.%y"):
            try:
                start_dt = datetime.strptime(startdatum, fmt)
                end_dt = datetime.strptime(enddatum, fmt)
                if end_dt >= start_dt and (end_dt - start_dt).days <= 366:
                    out_fmt = "%d.%m.%Y" if fmt == "%d.%m.%y" else fmt
                    days = []
                    curr = start_dt
                    while curr <= end_dt:
                        days.append(curr.strftime(out_fmt))
                        curr += timedelta(days=1)
                    return days
            except ValueError:
                continue

        return [startdatum, enddatum]

    def set_group_time(self, group, time):
        """Setzt die Uhrzeit für eine Gruppe"""
        try:
            group = int(group)
        except (ValueError, TypeError):
            pass
        self.group_times[group] = time

    def get_group_time(self, group):
        """Gibt die Uhrzeit für eine Gruppe zurück"""
        if group in self.group_times:
            return self.group_times[group]
        try:
            return self.group_times.get(int(group), "")
        except (ValueError, TypeError):
            return ""

    def set_group_date(self, group, date_str):
        """Setzt das Datum für eine Gruppe"""
        try:
            group = int(group)
        except (ValueError, TypeError):
            pass
        date_str = (date_str or "").strip()
        if date_str:
            self.group_dates[group] = date_str
        else:
            self.group_dates.pop(group, None)

    def get_group_date(self, group):
        """Gibt das Datum für eine Gruppe zurück (manuell gesetzt oder abgeleitet aus Turniertagen)"""
        if group is None or group == "":
            return ""
        if group in self.group_dates and self.group_dates[group]:
            return self.group_dates[group]
        try:
            g_int = int(group)
            if g_int in self.group_dates and self.group_dates[g_int]:
                return self.group_dates[g_int]
        except (ValueError, TypeError):
            g_int = None

        tage = self.get_turnier_tage()
        if len(tage) == 1:
            return tage[0]
        elif len(tage) > 1 and g_int is not None and g_int > 0:
            anzahl_pro_tag = self.get_anzahl_gruppen()
            if anzahl_pro_tag > 0:
                day_idx = (g_int - 1) // anzahl_pro_tag
                if 0 <= day_idx < len(tage):
                    return tage[day_idx]
                return tage[-1]
        return ""

    def get_schuetze_tag(self, schuetze):
        """Gibt den zugeordneten Tag (Datum) eines Schützen anhand seiner Gruppe zurück"""
        if not schuetze:
            return ""
        gruppe = schuetze.get('gruppe')
        if gruppe is None or gruppe == "":
            return ""
        return self.get_group_date(gruppe)

    def set_anzahl_gruppen(self, anzahl):
        """Setzt die vorgesehene Anzahl an Gruppen (pro Tag)"""
        try:
            val = max(0, int(anzahl))
            self.turnier['anzahl_gruppen'] = val
            return True
        except (ValueError, TypeError):
            return False

    def get_anzahl_gruppen(self):
        """Gibt die vorgesehene Anzahl an Gruppen pro Tag zurück"""
        try:
            return max(0, int(self.turnier.get('anzahl_gruppen', 0)))
        except (ValueError, TypeError):
            return 0

    def get_gesamt_anzahl_gruppen(self):
        """Gibt die gesamte vorgesehene Anzahl an Gruppen über alle Turniertage zurück"""
        anzahl_pro_tag = self.get_anzahl_gruppen()
        anzahl_tage = max(1, len(self.get_turnier_tage()))
        return anzahl_pro_tag * anzahl_tage

    def set_max_scheiben(self, max_scheiben):
        """Setzt die maximale Anzahl an Scheiben pro Gruppe"""
        try:
            val = max(1, int(max_scheiben))
            self.turnier['max_scheiben'] = val
            return True
        except (ValueError, TypeError):
            return False

    def get_max_scheiben(self):
        """Gibt die maximale Anzahl an Scheiben pro Gruppe zurück"""
        try:
            return max(1, int(self.turnier.get('max_scheiben', 3)))
        except (ValueError, TypeError):
            return 3

    def set_show_empty_slots_ui(self, show):
        """Setzt, ob leere Plätze in der Gruppenverwaltung angezeigt werden"""
        self.turnier['show_empty_slots_ui'] = bool(show)

    def get_show_empty_slots_ui(self):
        """Gibt zurück, ob leere Plätze in der Gruppenverwaltung angezeigt werden"""
        return bool(self.turnier.get('show_empty_slots_ui', True))

    def set_show_empty_slots_pdf(self, show):
        """Setzt, ob leere Plätze im Gruppen-PDF angezeigt werden"""
        self.turnier['show_empty_slots_pdf'] = bool(show)

    def get_show_empty_slots_pdf(self):
        """Gibt zurück, ob leere Plätze im Gruppen-PDF angezeigt werden"""
        return bool(self.turnier.get('show_empty_slots_pdf', True))

    def get_all_group_times(self):
        """Gibt alle Gruppen-Uhrzeiten zurück"""
        return self.group_times.copy()

    def clear_group_times(self):
        """Löscht alle Gruppen-Uhrzeiten"""
        self.group_times = {}

    def get_all_group_dates(self):
        """Gibt alle explizit gesetzten Gruppen-Daten zurück"""
        return self.group_dates.copy()

    def clear_group_dates(self):
        """Löscht alle explizit gesetzten Gruppen-Daten"""
        self.group_dates = {}

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
        self.group_dates = {}
        self.pdf_font_sizes = copy.deepcopy(DEFAULT_PDF_FONT_SIZES)
        self._touch()

    def _touch(self):
        """Aktualisiert den Zeitstempel der letzten Änderung"""
        import time
        self.last_update_time = time.time()
