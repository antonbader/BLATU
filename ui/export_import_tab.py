# -*- coding: utf-8 -*-
"""
Export/Import Tab
Ermöglicht den Export und Import von Turnier-, Klassen- und Schützendaten als JSON-Datei.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from config import FILE_TYPES_JSON, COLOR_PRIMARY


class ExportImportTab:
    """Tab für Export und Import von Turnier- und Schützendaten"""

    def __init__(self, parent, turnier_model, schuetze_model, on_data_imported=None):
        self.parent = parent
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.on_data_imported = on_data_imported

        self.frame = ttk.Frame(parent, padding="20")
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets für den Tab"""
        # Überschrift
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(
            header_frame,
            text="Export / Import",
            font=("Arial", 16, "bold"),
            foreground=COLOR_PRIMARY
        ).pack(anchor=tk.W)

        ttk.Label(
            header_frame,
            text="Exportieren oder importieren Sie hier Turnierdaten, Klassen und Schützen im JSON-Format.",
            font=("Arial", 10),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(2, 0))

        # 1. Übersichtsbereich der aktuellen Daten
        overview_frame = ttk.LabelFrame(self.frame, text="Aktuelle Datenübersicht", padding="15")
        overview_frame.pack(fill=tk.X, pady=(0, 15))

        grid_frame = ttk.Frame(overview_frame)
        grid_frame.pack(fill=tk.X)

        ttk.Label(grid_frame, text="Turniername:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=3)
        self.lbl_turniername = ttk.Label(grid_frame, text="-", font=("Arial", 10))
        self.lbl_turniername.grid(row=0, column=1, sticky=tk.W, pady=3)

        ttk.Label(grid_frame, text="Datum:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=3)
        self.lbl_datum = ttk.Label(grid_frame, text="-", font=("Arial", 10))
        self.lbl_datum.grid(row=1, column=1, sticky=tk.W, pady=3)

        ttk.Label(grid_frame, text="Vorhandene Klassen:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=3)
        self.lbl_klassen = ttk.Label(grid_frame, text="0 Klassen", font=("Arial", 10))
        self.lbl_klassen.grid(row=2, column=1, sticky=tk.W, pady=3)

        ttk.Label(grid_frame, text="Vorhandene Schützen:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=3)
        self.lbl_schuetzen = ttk.Label(grid_frame, text="0 Schützen", font=("Arial", 10))
        self.lbl_schuetzen.grid(row=3, column=1, sticky=tk.W, pady=3)

        # 2. Export Bereich
        export_frame = ttk.LabelFrame(self.frame, text="JSON-Export", padding="15")
        export_frame.pack(fill=tk.X, pady=(0, 15))

        export_desc = (
            "Erstellt eine JSON-Datei mit folgenden Inhalten:\n"
            "  • Turniername und Datum\n"
            "  • Alle vorhandenen Wettkampfklassen\n"
            "  • Alle Schützen mit Name, Vorname, Klasse, Verein, Gruppe und Scheibe"
        )
        ttk.Label(export_frame, text=export_desc, font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 10))

        ttk.Button(
            export_frame,
            text="📤 JSON-Datei exportieren",
            command=self.export_json
        ).pack(anchor=tk.W, ipady=4, ipadx=10)

        # 3. Import Bereich
        import_frame = ttk.LabelFrame(self.frame, text="JSON-Import", padding="15")
        import_frame.pack(fill=tk.X, pady=(0, 15))

        import_desc = (
            "Importiert Turniername, Datum, Klassen sowie Schützen aus einer passenden JSON-Datei.\n"
            "Bestehende Klassen und Schützen können dabei durch die importierten Daten ersetzt werden."
        )
        ttk.Label(import_frame, text=import_desc, font=("Arial", 9)).pack(anchor=tk.W, pady=(0, 10))

        ttk.Button(
            import_frame,
            text="📥 JSON-Datei importieren",
            command=self.import_json
        ).pack(anchor=tk.W, ipady=4, ipadx=10)

        self.refresh()

    def refresh(self):
        """Aktualisiert die Datenübersicht"""
        turnier_data = self.turnier_model.get_turnier_data()
        t_name = turnier_data.get("name", "").strip() or "(Kein Turniername angegeben)"
        t_datum = turnier_data.get("datum", "").strip() or "(Kein Datum angegeben)"

        klassen = self.turnier_model.get_klassen_names()
        schuetzen = self.schuetze_model.get_all_schuetzen()

        self.lbl_turniername.config(text=t_name)
        self.lbl_datum.config(text=t_datum)

        if klassen:
            klassen_text = f"{len(klassen)} Klassen ({', '.join(klassen[:5])}{' ...' if len(klassen) > 5 else ''})"
        else:
            klassen_text = "0 Klassen vorhanden"
        self.lbl_klassen.config(text=klassen_text)

        self.lbl_schuetzen.config(text=f"{len(schuetzen)} Schütze(n) vorhanden")

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
