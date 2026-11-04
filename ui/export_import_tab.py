# -*- coding: utf-8 -*-
"""
Export/Import Tab
Ermöglicht den Export und Import von Turnier-, Klassen- und Schützendaten (JSON)
sowie den Import von Passen- und 10er/9er-Ergebnissen aus CSV-Dateien (z. B. bgScore).
"""

import csv
import io
import json
import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import FILE_TYPES_JSON, FILE_TYPES_CSV, COLOR_PRIMARY
from models.schuetze import SchuetzeModel


class ExportImportTab:
    """Tab für Export und Import von Turnier-, Schützen- und Ergebnisdaten"""

    def __init__(self, parent, turnier_model, schuetze_model, on_data_imported=None):
        self.parent = parent
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.on_data_imported = on_data_imported

        self.frame = ttk.Frame(parent)
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets für den Tab"""
        # Scrollbarer Canvas-Container für garantierte Sichtbarkeit auf allen Displaygrößen
        canvas = tk.Canvas(self.frame, highlightthickness=0)
        v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        content_frame = ttk.Frame(canvas, padding="20")

        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set)

        def on_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", on_configure)
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Überschrift
        header_frame = ttk.Frame(content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            header_frame,
            text="Export / Import",
            font=("Arial", 16, "bold"),
            foreground=COLOR_PRIMARY
        ).pack(anchor=tk.W)

        ttk.Label(
            header_frame,
            text="Exportieren oder importieren Sie hier Turnierdaten, Klassen, Schützen (JSON) sowie Ergebnisse (CSV).",
            font=("Arial", 10),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(2, 0))

        # 1. Übersichtsbereich der aktuellen Daten (2-spaltiges Grid)
        overview_frame = ttk.LabelFrame(content_frame, text="Aktuelle Datenübersicht", padding="12")
        overview_frame.pack(fill=tk.X, pady=(0, 15))

        grid_frame = ttk.Frame(overview_frame)
        grid_frame.pack(fill=tk.X)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(3, weight=1)

        ttk.Label(grid_frame, text="Turniername:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.lbl_turniername = ttk.Label(grid_frame, text="-", font=("Arial", 9))
        self.lbl_turniername.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=2)

        ttk.Label(grid_frame, text="Vorhandene Klassen:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.lbl_klassen = ttk.Label(grid_frame, text="0 Klassen", font=("Arial", 9))
        self.lbl_klassen.grid(row=0, column=3, sticky=tk.W, pady=2)

        ttk.Label(grid_frame, text="Datum:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=2)
        self.lbl_datum = ttk.Label(grid_frame, text="-", font=("Arial", 9))
        self.lbl_datum.grid(row=1, column=1, sticky=tk.W, padx=(0, 20), pady=2)

        ttk.Label(grid_frame, text="Vorhandene Schützen:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.lbl_schuetzen = ttk.Label(grid_frame, text="0 Schützen", font=("Arial", 9))
        self.lbl_schuetzen.grid(row=1, column=3, sticky=tk.W, pady=2)

        ttk.Label(grid_frame, text="Vorhandene Ergebnisse:", font=("Arial", 9, "bold")).grid(row=2, column=2, sticky=tk.W, padx=(0, 5), pady=2)
        self.lbl_ergebnisse = ttk.Label(grid_frame, text="0 Schütze(n) mit Ergebnis", font=("Arial", 9))
        self.lbl_ergebnisse.grid(row=2, column=3, sticky=tk.W, pady=2)

        # 2-Spalten-Container für Aktionen
        cols_container = ttk.Frame(content_frame)
        cols_container.pack(fill=tk.BOTH, expand=True)
        cols_container.columnconfigure(0, weight=1)
        cols_container.columnconfigure(1, weight=1)

        # Linke Spalte: JSON Turnier- & Schützendaten (Export / Import)
        json_frame = ttk.LabelFrame(cols_container, text="Turnier- & Schützendaten (JSON)", padding="15")
        json_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(
            json_frame,
            text="Turniername, Datum, alle Klassen und alle Schützen (inkl. Gruppe und Scheibe) als JSON exportieren oder importieren.",
            font=("Arial", 9),
            wraplength=380
        ).pack(anchor=tk.W, pady=(0, 12))

        ttk.Button(
            json_frame,
            text="📤 JSON-Datei exportieren",
            command=self.export_json
        ).pack(fill=tk.X, pady=(0, 8), ipady=3)

        ttk.Separator(json_frame, orient="horizontal").pack(fill=tk.X, pady=8)

        ttk.Label(
            json_frame,
            text="Vorhandene Klassen und Schützen können durch eine passende JSON-Datei ersetzt werden.",
            font=("Arial", 9),
            foreground="gray",
            wraplength=380
        ).pack(anchor=tk.W, pady=(0, 8))

        ttk.Button(
            json_frame,
            text="📥 JSON-Datei importieren",
            command=self.import_json
        ).pack(fill=tk.X, ipady=3)

        # Rechte Spalte: CSV Ergebnisse (Import)
        csv_frame = ttk.LabelFrame(cols_container, text="Ergebnisse (CSV)", padding="15")
        csv_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        ttk.Label(
            csv_frame,
            text="Ergebnisse der einzelnen Passen sowie 10er und 9er für Schützen aus einer CSV-Datei importieren (z. B. aus der bgScore-App).\n\n"
                 "• Schützen werden nach Name, Vorname und Klasse zugeordnet.\n"
                 "• Zeilen ohne Wertungen werden automatisch übersprungen.\n"
                 "• Neue Schützen können auf Wunsch direkt mit angelegt werden.",
            font=("Arial", 9),
            wraplength=380
        ).pack(anchor=tk.W, pady=(0, 15))

        ttk.Button(
            csv_frame,
            text="🎯 Ergebnisse aus CSV importieren",
            command=self.import_ergebnisse_csv
        ).pack(fill=tk.X, ipady=5)

        ttk.Label(
            csv_frame,
            text="💡 Unterstützt bgScore-Export und Standard-CSV (Trennzeichen ';' oder ',')",
            font=("Arial", 8),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(12, 0))

        self.refresh()

    def refresh(self):
        """Aktualisiert die Datenübersicht"""
        turnier_data = self.turnier_model.get_turnier_data()
        t_name = turnier_data.get("name", "").strip() or "(Kein Turniername angegeben)"
        t_datum = turnier_data.get("datum", "").strip() or "(Kein Datum angegeben)"

        klassen = self.turnier_model.get_klassen_names()
        schuetzen = self.schuetze_model.get_all_schuetzen()
        ergebnisse = self.turnier_model.get_all_ergebnisse()

        self.lbl_turniername.config(text=t_name)
        self.lbl_datum.config(text=t_datum)

        if klassen:
            klassen_text = f"{len(klassen)} Klassen ({', '.join(klassen[:5])}{' ...' if len(klassen) > 5 else ''})"
        else:
            klassen_text = "0 Klassen vorhanden"
        self.lbl_klassen.config(text=klassen_text)

        self.lbl_schuetzen.config(text=f"{len(schuetzen)} Schütze(n) vorhanden")
        self.lbl_ergebnisse.config(text=f"{len(ergebnisse)} Schütze(n) mit Ergebnis")

    def build_export_data(self):
        """Erzeugt das Daten-Dictionary für den JSON-Export"""
        turnier_data = self.turnier_model.get_turnier_data()
        klassen = self.turnier_model.get_klassen_names()
        schuetzen = self.schuetze_model.get_all_schuetzen()

        schuetzen_list = []
        for s in schuetzen:
            gruppe = s.get("gruppe")
            if gruppe == "":
                gruppe = None

            scheibe = s.get("scheibe")
            if scheibe == "":
                scheibe = None

            schuetzen_list.append({
                "name": s.get("name", ""),
                "vorname": s.get("vorname", ""),
                "klasse": s.get("klasse", ""),
                "verein": s.get("verein", ""),
                "gruppe": gruppe,
                "scheibe": scheibe
            })

        return {
            "turniername": turnier_data.get("name", ""),
            "datum": turnier_data.get("datum", ""),
            "klassen": klassen,
            "schuetzen": schuetzen_list
        }

    def export_json(self):
        """Exportiert die Daten in eine JSON-Datei"""
        export_data = self.build_export_data()

        turniername = export_data["turniername"]
        klassen = export_data["klassen"]
        schuetzen = export_data["schuetzen"]

        if not turniername and not klassen and not schuetzen:
            messagebox.showwarning("Keine Daten", "Es sind keine Daten zum Exportieren vorhanden!")
            return

        # Dateinamen vorschlagen
        suggested_name = turniername.strip() if turniername.strip() else "Turnier"
        clean_name = "".join(c for c in suggested_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        initial_file = f"{clean_name}_Export.json" if clean_name else "Turnier_Export.json"

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=FILE_TYPES_JSON,
            title="JSON-Datei exportieren",
            initialfile=initial_file
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=4)

            messagebox.showinfo(
                "Export erfolgreich",
                f"Die Daten wurden erfolgreich exportiert!\n\n"
                f"Datei: {os.path.basename(file_path)}\n"
                f"Turniername: {export_data['turniername'] or 'Keine Angabe'}\n"
                f"Datum: {export_data['datum'] or 'Keine Angabe'}\n"
                f"Klassen: {len(klassen)}\n"
                f"Schützen: {len(schuetzen)}"
            )
        except Exception as e:
            messagebox.showerror("Fehler beim Export", f"Die Datei konnte nicht gespeichert werden:\n{str(e)}")

    def import_json(self):
        """Importiert Daten aus einer JSON-Datei"""
        file_path = filedialog.askopenfilename(
            filetypes=FILE_TYPES_JSON,
            title="JSON-Datei importieren"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                messagebox.showerror("Ungültiges Format", "Die ausgewählte Datei enthält kein gültiges JSON-Objekt.")
                return

            # Daten extrahieren (unterstützt verschiedene Formate)
            turnier_dict = data.get("turnier") if isinstance(data.get("turnier"), dict) else {}
            turniername = data.get("turniername") or data.get("Turniername") or turnier_dict.get("name", "")
            datum = data.get("datum") or data.get("Datum") or turnier_dict.get("datum", "")
            klassen = data.get("klassen") or data.get("Klassen") or []
            schuetzen = data.get("schuetzen") or data.get("Schuetzen") or data.get("Schützen") or []

            confirm_msg = (
                f"Möchten Sie die Daten aus '{os.path.basename(file_path)}' importieren?\n\n"
                f"• Turniername: {turniername or 'Keine Angabe'}\n"
                f"• Datum: {datum or 'Keine Angabe'}\n"
                f"• Klassen: {len(klassen)}\n"
                f"• Schützen: {len(schuetzen)}\n\n"
                f"Achtung: Vorhandene Klassen und Schützen werden dabei ersetzt."
            )

            if not messagebox.askyesno("Import bestätigen", confirm_msg):
                return

            # Turnierdaten aktualisieren
            current_turnier = self.turnier_model.get_turnier_data()
            self.turnier_model.set_turnier_data(
                turniername if turniername else current_turnier.get("name", ""),
                datum if datum else current_turnier.get("datum", ""),
                current_turnier.get("anzahl_passen", 1),
                show_halves=current_turnier.get("show_halves", False),
                max_scheiben=current_turnier.get("max_scheiben", 3),
                mannschaft_groesse=current_turnier.get("mannschaft_groesse", 3),
                startgeld_erheben=current_turnier.get("startgeld_erheben", False),
                iban=current_turnier.get("iban", ""),
                bic=current_turnier.get("bic", ""),
                bankname=current_turnier.get("bankname", ""),
                kontoinhaber=current_turnier.get("kontoinhaber", ""),
                zahldatum=current_turnier.get("zahldatum", "")
            )

            # Klassen ersetzen
            self.turnier_model.clear_klassen()
            for k in klassen:
                if isinstance(k, dict):
                    k_name = k.get("name")
                    if k_name and self.turnier_model.add_klasse(k_name):
                        if "startgeld" in k:
                            self.turnier_model.update_klasse_startgeld(k_name, k["startgeld"])
                elif isinstance(k, str) and k.strip():
                    self.turnier_model.add_klasse(k.strip())

            # Schützen ersetzen
            self.schuetze_model.clear_schuetzen()
            for s in schuetzen:
                if isinstance(s, dict):
                    s_name = s.get("name") or s.get("Name") or ""
                    s_vorname = s.get("vorname") or s.get("Vorname") or ""
                    s_klasse = s.get("klasse") or s.get("Klasse") or ""
                    s_verein = s.get("verein") or s.get("Verein") or ""
                    s_gruppe = s.get("gruppe") if "gruppe" in s else s.get("Gruppe")
                    s_scheibe = s.get("scheibe") if "scheibe" in s else s.get("Scheibe")
                    s_pin = s.get("pin") or s.get("PIN")

                    self.schuetze_model.add_schuetze(
                        s_name,
                        s_vorname,
                        s_klasse,
                        s_verein,
                        gruppe=s_gruppe,
                        scheibe=s_scheibe,
                        pin=s_pin
                    )

            self.refresh()

            if self.on_data_imported:
                self.on_data_imported()

            messagebox.showinfo(
                "Import erfolgreich",
                f"Die Daten wurden erfolgreich importiert!\n\n"
                f"{len(klassen)} Klassen und {len(schuetzen)} Schützen geladen."
            )
        except Exception as e:
            messagebox.showerror("Fehler beim Import", f"Fehler beim Laden der Datei:\n{str(e)}")

    @staticmethod
    def parse_ergebnisse_csv(content, existing_schuetzen, current_anzahl_passen=1):
        """
        Parst CSV-Inhalte mit Passen- und 10er/9er-Ergebnissen.
        Gibt ein Ergebnis-Dictionary zurück:
        {
            'success': bool,
            'error': str or None,
            'max_pass': int,
            'target_pass_count': int,
            'to_import': list of dict,
            'unmatched': list of dict,
            'skipped_empty': int
        }
        """
        lines = [line for line in content.splitlines() if line.strip()]
        if not lines:
            return {'success': False, 'error': 'Die CSV-Datei ist leer.'}

        # Trennzeichen ermitteln (Standard: Strichpunkt)
        first_line = lines[0]
        if ';' in first_line:
            delimiter = ';'
        elif '\t' in first_line:
            delimiter = '\t'
        elif ',' in first_line:
            delimiter = ','
        else:
            delimiter = ';'

        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        rows = [r for r in reader if any(cell.strip() for cell in r)]
        if not rows:
            return {'success': False, 'error': 'Die CSV-Datei enthält keine Daten.'}

        headers = [h.strip() for h in rows[0]]
        data_rows = rows[1:]
        if not data_rows:
            return {'success': False, 'error': 'Die CSV-Datei enthält keine Datenzeilen.'}

        col_mapping = {}
        pass_cols = []  # Liste von (pass_nr, spalten_index)

        for idx, header in enumerate(headers):
            clean = header.strip()
            clean_lower = clean.lower()

            # Passen erkennen (z. B. "Passe 1", "Passe 10", "P1", "P 1")
            pass_match = re.match(r"^(?:passe|p)\s*(\d+)$", clean, re.IGNORECASE)
            if pass_match:
                pass_num = int(pass_match.group(1))
                pass_cols.append((pass_num, idx))
                continue

            if clean_lower in ['name', 'nachname', 'familienname']:
                col_mapping['name'] = idx
            elif clean_lower in ['vorname', 'rufname']:
                col_mapping['vorname'] = idx
            elif clean_lower in ['klasse', 'wettkampfklasse', 'altersklasse']:
                col_mapping['klasse'] = idx
            elif clean_lower in ['verein', 'klub', 'club']:
                col_mapping['verein'] = idx
            elif clean_lower in ['gruppe']:
                col_mapping['gruppe'] = idx
            elif clean_lower in ['scheibe', 'standnummer', 'stand']:
                col_mapping['scheibe'] = idx
            elif clean_lower in ['10er', '10-er', '10', 'zehner', 'anzahl 10er', 'anzahl 10', 'anzahl_10er', '10s', '10 er']:
                col_mapping['10er'] = idx
            elif clean_lower in ['9er', '9-er', '9', 'neuner', 'anzahl 9er', 'anzahl 9', 'anzahl_9er', '9s', '9 er']:
                col_mapping['9er'] = idx
            elif clean_lower in ['gesamtergebnis', 'gesamt', 'total', 'ringe']:
                col_mapping['gesamt'] = idx

        if 'name' not in col_mapping or 'vorname' not in col_mapping:
            return {
                'success': False,
                'error': f"Die CSV-Datei muss mindestens die Spalten 'Name' und 'Vorname' enthalten.\n\nGefundene Spalten:\n{', '.join(headers)}"
            }

        if not pass_cols and '10er' not in col_mapping and '9er' not in col_mapping:
            return {
                'success': False,
                'error': f"In der CSV-Datei wurden weder Passen (z. B. 'Passe 1') noch Wertungsspalten ('10er'/'9er') gefunden.\n\nGefundene Spalten:\n{', '.join(headers)}"
            }

        pass_cols.sort(key=lambda x: x[0])
        max_pass_in_csv = max((p[0] for p in pass_cols), default=0)
        target_pass_count = max(current_anzahl_passen, max_pass_in_csv, 1)

        to_import = []
        unmatched = []
        skipped_empty = 0

        for row in data_rows:
            row_name = row[col_mapping['name']].strip() if col_mapping['name'] < len(row) else ""
            row_vorname = row[col_mapping['vorname']].strip() if col_mapping['vorname'] < len(row) else ""
            if not row_name and not row_vorname:
                continue

            row_klasse = row[col_mapping['klasse']].strip() if 'klasse' in col_mapping and col_mapping['klasse'] < len(row) else ""
            row_verein = row[col_mapping['verein']].strip() if 'verein' in col_mapping and col_mapping['verein'] < len(row) else ""

            row_gruppe = None
            if 'gruppe' in col_mapping and col_mapping['gruppe'] < len(row):
                g_str = row[col_mapping['gruppe']].strip()
                if g_str.isdigit():
                    row_gruppe = int(g_str)

            row_scheibe = None
            if 'scheibe' in col_mapping and col_mapping['scheibe'] < len(row):
                s_str = row[col_mapping['scheibe']].strip()
                if s_str.isdigit():
                    row_scheibe = int(s_str)

            has_result = False
            passen_dict = {}
            for pass_num, col_idx in pass_cols:
                if col_idx < len(row):
                    val_str = row[col_idx].strip()
                    if val_str != "":
                        try:
                            passen_dict[pass_num] = int(float(val_str.replace(',', '.')))
                            has_result = True
                        except ValueError:
                            passen_dict[pass_num] = 0

            anzahl_10er = 0
            if '10er' in col_mapping and col_mapping['10er'] < len(row):
                v10 = row[col_mapping['10er']].strip()
                if v10 != "":
                    try:
                        anzahl_10er = int(float(v10.replace(',', '.')))
                        has_result = True
                    except ValueError:
                        anzahl_10er = 0

            anzahl_9er = 0
            if '9er' in col_mapping and col_mapping['9er'] < len(row):
                v9 = row[col_mapping['9er']].strip()
                if v9 != "":
                    try:
                        anzahl_9er = int(float(v9.replace(',', '.')))
                        has_result = True
                    except ValueError:
                        anzahl_9er = 0

            # Wenn keine einzige Passenzahl und weder 10er noch 9er befüllt sind -> Schütze hat keine Ergebnisse
            if not has_result:
                skipped_empty += 1
                continue

            # Passen-Array aufbauen
            passen_list = [passen_dict.get(p_idx + 1, 0) for p_idx in range(target_pass_count)]
            gesamt = sum(passen_list)

            # Schütze zuordnen
            matched_schuetze = None
            # 1. Exakt nach Name, Vorname und Klasse (case-insensitive)
            for s in existing_schuetzen:
                if (s.get('name', '').strip().lower() == row_name.lower() and
                    s.get('vorname', '').strip().lower() == row_vorname.lower() and
                    s.get('klasse', '').strip().lower() == row_klasse.lower()):
                    matched_schuetze = s
                    break

            # 2. Eindeutiger Treffer nach Name und Vorname (falls Klasse variiert oder fehlt)
            if matched_schuetze is None:
                name_matches = [
                    s for s in existing_schuetzen
                    if s.get('name', '').strip().lower() == row_name.lower() and
                       s.get('vorname', '').strip().lower() == row_vorname.lower()
                ]
                if len(name_matches) == 1:
                    matched_schuetze = name_matches[0]

            # 3. Vertauschter Vor- und Nachname (falls in CSV vertauscht)
            if matched_schuetze is None:
                swapped_matches = [
                    s for s in existing_schuetzen
                    if s.get('name', '').strip().lower() == row_vorname.lower() and
                       s.get('vorname', '').strip().lower() == row_name.lower()
                ]
                if len(swapped_matches) == 1:
                    matched_schuetze = swapped_matches[0]

            item_data = {
                'name': row_name,
                'vorname': row_vorname,
                'klasse': row_klasse,
                'verein': row_verein,
                'gruppe': row_gruppe,
                'scheibe': row_scheibe,
                'passen': passen_list,
                '10er': anzahl_10er,
                '9er': anzahl_9er,
                'gesamt': gesamt
            }

            if matched_schuetze is not None:
                item_data['schuetze'] = matched_schuetze
                item_data['schuetze_id'] = SchuetzeModel.get_schuetze_id(matched_schuetze)
                to_import.append(item_data)
            else:
                unmatched.append(item_data)

        return {
            'success': True,
            'error': None,
            'max_pass': max_pass_in_csv,
            'target_pass_count': target_pass_count,
            'to_import': to_import,
            'unmatched': unmatched,
            'skipped_empty': skipped_empty
        }

    def import_ergebnisse_csv(self):
        """Importiert Ergebnisse (Passen, 10er, 9er) aus einer CSV-Datei"""
        file_path = filedialog.askopenfilename(
            filetypes=FILE_TYPES_CSV,
            title="Ergebnisse aus CSV-Datei importieren"
        )

        if not file_path:
            return

        # Datei mit verschiedenen Encodings einlesen
        content = None
        for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                with open(file_path, "r", encoding=enc) as f:
                    content = f.read()
                break
            except (UnicodeDecodeError, OSError):
                continue

        if content is None:
            messagebox.showerror(
                "Fehler beim Öffnen",
                "Die CSV-Datei konnte mit keiner gängigen Zeichencodierung geöffnet werden."
            )
            return

        existing_schuetzen = self.schuetze_model.get_all_schuetzen()
        current_turnier = self.turnier_model.get_turnier_data()
        current_anzahl_passen = current_turnier.get("anzahl_passen", 1)

        result = self.parse_ergebnisse_csv(
            content,
            existing_schuetzen,
            current_anzahl_passen=current_anzahl_passen
        )

        if not result['success']:
            messagebox.showerror("Fehler beim Einlesen", result['error'])
            return

        to_import = result['to_import']
        unmatched = result['unmatched']
        skipped_empty = result['skipped_empty']
        max_pass = result['max_pass']
        target_pass_count = result['target_pass_count']

        total_with_results = len(to_import) + len(unmatched)
        if total_with_results == 0:
            messagebox.showinfo(
                "Keine Ergebnisse",
                f"In der Datei '{os.path.basename(file_path)}' wurden keine eingetragenen Ergebnisse gefunden.\n"
                f"({skipped_empty} Zeile(n) ohne Wertungen übersprungen)"
            )
            return

        # Bestätigungsdialog
        confirm_lines = [
            f"Möchten Sie die Ergebnisse aus '{os.path.basename(file_path)}' importieren?\n",
            f"• Gefundene Passen: {max_pass}",
            f"• Schützen mit Ergebnissen: {total_with_results}",
            f"• Zugeordnete Schützen: {len(to_import)}"
        ]
        if unmatched:
            confirm_lines.append(f"• Nicht zugeordnete Schützen: {len(unmatched)}")
        if skipped_empty > 0:
            confirm_lines.append(f"• Schützen ohne Ergebnisse (übersprungen): {skipped_empty}")

        confirm_lines.append("\nBestehende Ergebnisse der zugeordneten Schützen werden dabei aktualisiert.")

        if not messagebox.askyesno("Ergebnisse importieren", "\n".join(confirm_lines)):
            return

        # Nicht zugeordnete Schützen optional neu anlegen
        if unmatched:
            unmatched_preview = [
                f"• {u['vorname']} {u['name']} (Klasse: {u['klasse'] or 'Keine Angabe'})"
                for u in unmatched[:10]
            ]
            if len(unmatched) > 10:
                unmatched_preview.append(f"... und {len(unmatched) - 10} weitere")

            add_msg = (
                f"Folgende {len(unmatched)} Schütze(n) mit Ergebnissen wurden in BLATU nicht gefunden:\n\n"
                + "\n".join(unmatched_preview) + "\n\n"
                "Möchten Sie diese Schützen automatisch neu in BLATU anlegen und ihre Ergebnisse importieren?"
            )
            if messagebox.askyesno("Neue Schützen anlegen?", add_msg):
                for u in unmatched:
                    u_klasse = u['klasse'] or "Allgemein"
                    if u_klasse not in self.turnier_model.get_klassen_names():
                        self.turnier_model.add_klasse(u_klasse)

                    self.schuetze_model.add_schuetze(
                        name=u['name'],
                        vorname=u['vorname'],
                        klasse=u_klasse,
                        verein=u['verein'],
                        gruppe=u['gruppe'],
                        scheibe=u['scheibe']
                    )

                    s_dict = {
                        'name': u['name'],
                        'vorname': u['vorname'],
                        'klasse': u_klasse
                    }
                    u['schuetze_id'] = SchuetzeModel.get_schuetze_id(s_dict)
                    to_import.append(u)

        if not to_import:
            messagebox.showwarning(
                "Keine Schützen zugeordnet",
                "Es wurden keine Schützen zugeordnet. Es wurden keine Ergebnisse importiert."
            )
            return

        # Passenanzahl im Turnier bei Bedarf anpassen
        if target_pass_count > current_turnier.get("anzahl_passen", 1):
            self.turnier_model.set_turnier_data(
                current_turnier.get("name", ""),
                current_turnier.get("datum", ""),
                target_pass_count,
                show_halves=current_turnier.get("show_halves", False),
                max_scheiben=current_turnier.get("max_scheiben", 3),
                mannschaft_groesse=current_turnier.get("mannschaft_groesse", 3),
                startgeld_erheben=current_turnier.get("startgeld_erheben", False),
                iban=current_turnier.get("iban", ""),
                bic=current_turnier.get("bic", ""),
                bankname=current_turnier.get("bankname", ""),
                kontoinhaber=current_turnier.get("kontoinhaber", ""),
                zahldatum=current_turnier.get("zahldatum", "")
            )

        # Ergebnisse im Modell speichern
        for item in to_import:
            self.turnier_model.add_ergebnis(
                item['schuetze_id'],
                item['passen'],
                item['10er'],
                item['9er']
            )

        self.refresh()

        if self.on_data_imported:
            self.on_data_imported()

        success_msg = f"Ergebnisse wurden erfolgreich importiert!\n\n• Aktualisierte Schützen: {len(to_import)}"
        if skipped_empty > 0:
            success_msg += f"\n• Zeilen ohne Ergebnisse: {skipped_empty}"

        unmatched_remaining = [u for u in unmatched if 'schuetze_id' not in u]
        if unmatched_remaining:
            success_msg += f"\n• Nicht zugeordnete Schützen (übersprungen): {len(unmatched_remaining)}"

        messagebox.showinfo("Import erfolgreich", success_msg)
