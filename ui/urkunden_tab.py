# -*- coding: utf-8 -*-
"""
Urkunden Tab
Ermöglicht die Erstellung von Urkunden für Schützen (Einzelwertung)
sowie für Mannschaften (Mannschaftswertung).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from collections import defaultdict
from utils.word_generator import WordGenerator


class UrkundenTab:
    """Tab für die Erstellung von Urkunden (Schützen und Mannschaften)"""

    def __init__(self, parent, turnier_model, schuetze_model):
        self.frame = ttk.Frame(parent, padding="15")
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model

        # UI Variablen - Allgemein & Schützen
        self.template_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.unterordner_var = tk.BooleanVar(value=True)
        self.alle_schuetzen_var = tk.BooleanVar(value=False)
        self.klassen_platz_vars = {}

        # UI Variablen - Mannschaften
        self.alle_mannschaften_var = tk.BooleanVar(value=False)
        self.mannschaft_group_by_klasse_var = tk.BooleanVar(value=False)
        self.mitglieder_einzelergebnis_var = tk.BooleanVar(value=False)
        self.mannschaft_platz_vars = {}

        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        # --- Linke Spalte: Platzierungen für Schützen & Mannschaften ---
        left_col = ttk.Frame(top_frame)
        left_col.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="nsew")
        left_col.columnconfigure(0, weight=1)
        left_col.rowconfigure(0, weight=1)
        left_col.rowconfigure(1, weight=1)

        # 1. Schützen-Platzierungen
        klassen_frame = ttk.LabelFrame(
            left_col,
            text="Schützen-Urkunden pro Platzierung",
            padding="8"
        )
        klassen_frame.grid(row=0, column=0, pady=(0, 6), sticky="nsew")

        alle_schuetzen_check = ttk.Checkbutton(
            klassen_frame,
            text="Für alle Schützen erstellen",
            variable=self.alle_schuetzen_var,
            command=self.toggle_klassen_tree
        )
        alle_schuetzen_check.pack(anchor="w", pady=(0, 3))

        ttk.Label(
            klassen_frame,
            text="💡 Doppelklick auf eine Zahl, um die Anzahl der Plätze zu ändern.",
            font=("Arial", 8),
            foreground="gray"
        ).pack(anchor="w", pady=(0, 4))

        tree_container_s = ttk.Frame(klassen_frame)
        tree_container_s.pack(fill=tk.BOTH, expand=True)

        klassen_scrollbar = ttk.Scrollbar(tree_container_s)
        klassen_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.klassen_tree = ttk.Treeview(
            tree_container_s,
            columns=("Klasse", "Anzahl"),
            show="headings",
            height=5,
            yscrollcommand=klassen_scrollbar.set
        )
        self.klassen_tree.heading("Klasse", text="Klasse")
        self.klassen_tree.heading("Anzahl", text="Anzahl Platzierungen")
        self.klassen_tree.column("Klasse", width=160)
        self.klassen_tree.column("Anzahl", width=130, anchor="center")
        self.klassen_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.klassen_tree.bind("<Double-1>", self.edit_cell)
        klassen_scrollbar.config(command=self.klassen_tree.yview)

        # 2. Mannschafts-Platzierungen
        mannschaft_frame = ttk.LabelFrame(
            left_col,
            text="Mannschafts-Urkunden pro Platzierung",
            padding="8"
        )
        mannschaft_frame.grid(row=1, column=0, pady=(6, 0), sticky="nsew")

        mode_row = ttk.Frame(mannschaft_frame)
        mode_row.pack(fill=tk.X, pady=(0, 3))
        ttk.Label(mode_row, text="Wertung:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(
            mode_row,
            text="Alle Mannschaften",
            variable=self.mannschaft_group_by_klasse_var,
            value=False,
            command=self.populate_mannschaft_tree
        ).pack(side=tk.LEFT, padx=3)
        ttk.Radiobutton(
            mode_row,
            text="Nach Mannschaftsklassen",
            variable=self.mannschaft_group_by_klasse_var,
            value=True,
            command=self.populate_mannschaft_tree
        ).pack(side=tk.LEFT, padx=3)

        alle_mannschaften_check = ttk.Checkbutton(
            mannschaft_frame,
            text="Für alle Mannschaften erstellen",
            variable=self.alle_mannschaften_var,
            command=self.toggle_mannschaft_tree
        )
        alle_mannschaften_check.pack(anchor="w", pady=(0, 3))

        ttk.Label(
            mannschaft_frame,
            text="💡 Doppelklick auf eine Zahl, um die Anzahl der Plätze zu ändern.",
            font=("Arial", 8),
            foreground="gray"
        ).pack(anchor="w", pady=(0, 4))

        tree_container_m = ttk.Frame(mannschaft_frame)
        tree_container_m.pack(fill=tk.BOTH, expand=True)

        mannschaft_scrollbar = ttk.Scrollbar(tree_container_m)
        mannschaft_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.mannschaft_tree = ttk.Treeview(
            tree_container_m,
            columns=("Klasse", "Anzahl"),
            show="headings",
            height=5,
            yscrollcommand=mannschaft_scrollbar.set
        )
        self.mannschaft_tree.heading("Klasse", text="Mannschaftsklasse / Wertung")
        self.mannschaft_tree.heading("Anzahl", text="Anzahl Platzierungen")
        self.mannschaft_tree.column("Klasse", width=160)
        self.mannschaft_tree.column("Anzahl", width=130, anchor="center")
        self.mannschaft_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.mannschaft_tree.bind("<Double-1>", self.edit_mannschaft_cell)
        mannschaft_scrollbar.config(command=self.mannschaft_tree.yview)

        # --- Rechte Spalte: Einstellungen ---
        settings_frame = ttk.LabelFrame(top_frame, text="Einstellungen", padding="10")
        settings_frame.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="nsew")
        settings_frame.columnconfigure(0, weight=1)

        # Vorlage
        ttk.Label(settings_frame, text="Word-Vorlage:").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 4)
        )
        template_entry = ttk.Entry(settings_frame, textvariable=self.template_path_var, width=38)
        template_entry.grid(row=1, column=0, sticky="we")
        ttk.Button(
            settings_frame,
            text="Durchsuchen...",
            command=self.select_template_file
        ).grid(row=1, column=1, sticky="w", padx=(5, 0))

        # Speicherort
        ttk.Label(settings_frame, text="Speicherort:").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(10, 4)
        )
        output_dir_entry = ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=38)
        output_dir_entry.grid(row=3, column=0, sticky="we")
        ttk.Button(
            settings_frame,
            text="Durchsuchen...",
            command=self.select_output_dir
        ).grid(row=3, column=1, sticky="w", padx=(5, 0))

        unterordner_check = ttk.Checkbutton(
            settings_frame,
            text="Unterordner für jede Klasse erstellen",
            variable=self.unterordner_var
        )
        unterordner_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 5))

        ttk.Separator(settings_frame, orient="horizontal").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=8
        )

        # Auswahlfeld für Mannschaftsmitglieder-Einzelergebnis
        ttk.Label(
            settings_frame,
            text="Option für Platzhalter [Mannschaftsmitglieder]:",
            font=("Arial", 9, "bold")
        ).grid(row=6, column=0, columnspan=2, sticky="w", pady=(2, 4))

        mitglieder_erg_check = ttk.Checkbutton(
            settings_frame,
            text="Einzelergebnis der Mannschaftsmitglieder hinter dem Namen ausgeben",
            variable=self.mitglieder_einzelergebnis_var
        )
        mitglieder_erg_check.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Separator(settings_frame, orient="horizontal").grid(
            row=8, column=0, columnspan=2, sticky="ew", pady=8
        )

        # Buttons zur Erstellung
        generate_button = ttk.Button(
            settings_frame,
            text="🚀 Urkunden erstellen (Schützen)",
            command=self.generate_urkunden,
            style="Accent.TButton"
        )
        generate_button.grid(row=9, column=0, columnspan=2, pady=(4, 6), ipady=4, sticky="ew")

        generate_team_button = ttk.Button(
            settings_frame,
            text="🏆 Mannschafts-Urkunden erstellen",
            command=self.generate_mannschaft_urkunden,
            style="Accent.TButton"
        )
        generate_team_button.grid(row=10, column=0, columnspan=2, pady=(4, 4), ipady=4, sticky="ew")

        # --- Unterer Bereich: Platzhalter ---
        placeholder_frame = ttk.LabelFrame(main_frame, text="Verfügbare Platzhalter", padding="8")
        placeholder_frame.pack(fill=tk.X, expand=False, pady=(4, 5))

        placeholders = [
            "[Turniername]", "[Datum]", "[Klasse]", "[Vorname]",
            "[Name]", "[Verein]", "[Ergebnis]", "[Platz]",
            "[Mannschaftsname]", "[Mannschaftsmitglieder]"
        ]

        placeholder_text = ", ".join(placeholders)
        ttk.Label(
            placeholder_frame,
            text=placeholder_text,
            wraplength=760,
            justify="center"
        ).pack(pady=3)

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.rowconfigure(0, weight=1)

        self.refresh()

    def edit_cell(self, event):
        """Doppelklick zum Bearbeiten der Platzierungsanzahl (Schützen)."""
        self._open_cell_editor(event, self.klassen_tree, self.klassen_platz_vars)

    def edit_mannschaft_cell(self, event):
        """Doppelklick zum Bearbeiten der Platzierungsanzahl (Mannschaften)."""
        self._open_cell_editor(event, self.mannschaft_tree, self.mannschaft_platz_vars)

    def _open_cell_editor(self, event, tree, vars_dict):
        """Generischer Inline-Editor für die Spalte 'Anzahl Platzierungen'."""
        item_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)

        if not item_id or column_id != "#2":
            return

        bbox = tree.bbox(item_id, column_id)
        if not bbox:
            return
        x, y, width, height = bbox

        klasse = tree.item(item_id, "values")[0]
        var = vars_dict.get(klasse)
        if var is None:
            var = tk.StringVar(value="3")
            vars_dict[klasse] = var

        entry = ttk.Entry(tree, textvariable=var, width=10, justify="center")
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()

        def save_edit(event=None):
            if not entry.winfo_exists():
                return
            new_value = entry.get()
            try:
                if int(new_value) >= 0:
                    tree.item(item_id, values=(klasse, new_value))
                else:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Ungültige Eingabe", "Bitte geben Sie eine positive ganze Zahl ein.")
                var.set(tree.item(item_id, "values")[1])
            finally:
                if entry.winfo_exists():
                    entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def select_template_file(self):
        """Öffnet Dialog zur Auswahl der Vorlagedatei."""
        filepath = filedialog.askopenfilename(filetypes=[("Word Document", "*.docx")])
        if filepath:
            self.template_path_var.set(filepath)

    def select_output_dir(self):
        """Öffnet Dialog zur Auswahl des Speicherverzeichnisses."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)

    def populate_klassen_tree(self):
        """Füllt die Klassenliste für Schützen."""
        old_values = {k: v.get() for k, v in self.klassen_platz_vars.items()}
        for item in self.klassen_tree.get_children():
            self.klassen_tree.delete(item)

        self.klassen_platz_vars.clear()

        klassen_data = self.turnier_model.get_klassen()
        for klasse_dict in klassen_data:
            klasse_name = klasse_dict['name']
            var = tk.StringVar(value=old_values.get(klasse_name, "3"))
            self.klassen_platz_vars[klasse_name] = var
            self.klassen_tree.insert("", "end", values=(klasse_name, var.get()))

    def populate_mannschaft_tree(self):
        """Füllt die Liste für Mannschafts-Platzierungen (je nach gewähltem Wertungsmodus)."""
        old_values = {k: v.get() for k, v in self.mannschaft_platz_vars.items()}
        for item in self.mannschaft_tree.get_children():
            self.mannschaft_tree.delete(item)

        self.mannschaft_platz_vars.clear()

        if not self.mannschaft_group_by_klasse_var.get():
            group_names = ["Alle Mannschaften"]
        else:
            group_names = list(self.turnier_model.get_mannschaftsklassen_names())
            # Prüfen ob es Mannschaften ohne Klasse gibt
            has_unassigned = any(
                not (m.get('klasse') or "").strip()
                for m in self.turnier_model.get_all_mannschaften()
            )
            if has_unassigned or not group_names:
                if "Ohne Klasse" not in group_names:
                    group_names.append("Ohne Klasse")

        for g_name in group_names:
            var = tk.StringVar(value=old_values.get(g_name, "3"))
            self.mannschaft_platz_vars[g_name] = var
            self.mannschaft_tree.insert("", "end", values=(g_name, var.get()))

    def toggle_klassen_tree(self):
        """Aktiviert/Deaktiviert die Klasseneingabefelder für Schützen."""
        if self.alle_schuetzen_var.get():
            self.klassen_tree.unbind("<Double-1>")
        else:
            self.klassen_tree.bind("<Double-1>", self.edit_cell)

    def toggle_mannschaft_tree(self):
        """Aktiviert/Deaktiviert die Klasseneingabefelder für Mannschaften."""
        if self.alle_mannschaften_var.get():
            self.mannschaft_tree.unbind("<Double-1>")
        else:
            self.mannschaft_tree.bind("<Double-1>", self.edit_mannschaft_cell)

    def refresh(self):
        """Wird aufgerufen, wenn der Tab aktualisiert wird."""
        self.populate_klassen_tree()
        self.populate_mannschaft_tree()

    def _validate_paths(self):
        """Validiert Vorlagedatei und Speicherort."""
        output_dir = self.output_dir_var.get()
        template_path = self.template_path_var.get()

        if not output_dir or not template_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Speicherort und eine Vorlagedatei aus.")
            return None, None

        if not os.path.exists(template_path):
            messagebox.showerror("Fehler", "Die angegebene Vorlagedatei existiert nicht.")
            return None, None

        return template_path, output_dir

    def generate_urkunden(self):
        """Startet den Prozess zur Erstellung der Schützen-Urkunden."""
        template_path, output_dir = self._validate_paths()
        if not template_path:
            return

        try:
            ergebnisse = self.schuetze_model.calculate_results(self.turnier_model)
            turnier_data = self.turnier_model.get_turnier_data()
            turnier_name = turnier_data.get("name", "Unbenanntes Turnier")
            turnier_datum = turnier_data.get("datum", "")
        except Exception as e:
            messagebox.showerror("Fehler bei der Datenverarbeitung", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
            return

        word_generator = WordGenerator(template_path)
        erstellte_dateien = 0

        for klasse, schuetzen in ergebnisse.items():
            if not schuetzen:
                continue

            schuetzen_fuer_urkunden = []
            if self.alle_schuetzen_var.get():
                schuetzen_fuer_urkunden = schuetzen
            else:
                try:
                    max_platz = int(self.klassen_platz_vars[klasse].get())
                    if max_platz > 0:
                        schuetzen_fuer_urkunden = [s for s in schuetzen if s.get('Platz', 0) <= max_platz]
                except (KeyError, ValueError):
                    messagebox.showwarning(
                        "Fehlerhafte Eingabe",
                        f"Für die Klasse '{klasse}' ist keine gültige Anzahl an Platzierungen angegeben. Sie wird übersprungen."
                    )
                    continue

            platz_counts = defaultdict(int)
            for s in schuetzen_fuer_urkunden:
                platz_counts[s['Platz']] += 1

            platz_suffixes = defaultdict(lambda: 'a')

            for schuetze in schuetzen_fuer_urkunden:
                if schuetze.get('Gesamt', 0) == 0:
                    continue

                platz = schuetze.get('Platz', 0)
                platz_str = str(platz)

                if platz_counts[platz] > 1:
                    platz_str += platz_suffixes[platz]
                    platz_suffixes[platz] = chr(ord(platz_suffixes[platz]) + 1)

                platzhalter_data = {
                    "[Turniername]": turnier_name,
                    "[Datum]": turnier_datum,
                    "[Klasse]": klasse,
                    "[Vorname]": schuetze.get('vorname', ''),
                    "[Name]": schuetze.get('name', ''),
                    "[Verein]": schuetze.get('verein', ''),
                    "[Ergebnis]": str(schuetze.get('Gesamt', 0)),
                    "[Platz]": str(platz),
                    "[Mannschaftsname]": "",
                    "[Mannschaftsmitglieder]": ""
                }

                clean_turnier_name = re.sub(r'[^\w\-]', '', turnier_name.replace(' ', ''))
                clean_klasse = re.sub(r'[^\w\-]', '', klasse.replace(' ', ''))
                filename = f"{clean_turnier_name}_{turnier_datum}_{clean_klasse}_{platz_str}.docx"

                current_output_dir = output_dir
                if self.unterordner_var.get():
                    current_output_dir = os.path.join(output_dir, clean_klasse)
                    if not os.path.exists(current_output_dir):
                        os.makedirs(current_output_dir)

                output_path = os.path.join(current_output_dir, filename)

                success, error = word_generator.generate_certificate(output_path, platzhalter_data)
                if success:
                    erstellte_dateien += 1
                else:
                    messagebox.showerror("Fehler bei der Erstellung", f"Fehler bei Datei {filename}:\n{error}")
                    return

        if erstellte_dateien > 0:
            messagebox.showinfo("Erfolg", f"{erstellte_dateien} Urkunden wurden erfolgreich erstellt.")
        else:
            messagebox.showwarning(
                "Keine Urkunden erstellt",
                "Es wurden keine Urkunden erstellt. Überprüfen Sie die Einstellungen und ob Ergebnisse vorhanden sind."
            )

    def format_mannschaftsmitglieder(self, mitglieder, include_scores=False):
        """
        Erzeugt den mehrzeiligen String für den Platzhalter [Mannschaftsmitglieder].
        Jeder Schütze steht in einer neuen Zeile, optional mit Einzelergebnis hinter dem Namen.
        """
        lines = []
        for m in mitglieder:
            full_name = f"{m.get('vorname', '')} {m.get('name', '')}".strip()
            if not full_name:
                continue
            if include_scores:
                score = int(m.get('gesamt', 0))
                lines.append(f"{full_name} ({score})")
            else:
                lines.append(full_name)
        return "\n".join(lines)

    def generate_mannschaft_urkunden(self):
        """Startet den Prozess zur Erstellung der Mannschafts-Urkunden."""
        template_path, output_dir = self._validate_paths()
        if not template_path:
            return

        if not self.turnier_model.get_all_mannschaften():
            messagebox.showwarning("Keine Mannschaften", "Es sind noch keine Mannschaften angelegt.")
            return

        group_by_klasse = self.mannschaft_group_by_klasse_var.get()
        include_member_scores = self.mitglieder_einzelergebnis_var.get()

        try:
            mannschaft_ergebnisse = self.turnier_model.calculate_mannschaft_results(
                self.schuetze_model,
                group_by_klasse=group_by_klasse
            )
            turnier_data = self.turnier_model.get_turnier_data()
            turnier_name = turnier_data.get("name", "Unbenanntes Turnier")
            turnier_datum = turnier_data.get("datum", "")
        except Exception as e:
            messagebox.showerror("Fehler bei der Datenverarbeitung", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
            return

        word_generator = WordGenerator(template_path)
        erstellte_dateien = 0

        for group_name, teams in mannschaft_ergebnisse.items():
            if not teams:
                continue

            teams_fuer_urkunden = []
            if self.alle_mannschaften_var.get():
                teams_fuer_urkunden = teams
            else:
                try:
                    var = self.mannschaft_platz_vars.get(group_name)
                    max_platz = int(var.get()) if var is not None else 3
                    if max_platz > 0:
                        teams_fuer_urkunden = [t for t in teams if t.get('platz', 0) <= max_platz]
                except ValueError:
                    messagebox.showwarning(
                        "Fehlerhafte Eingabe",
                        f"Für '{group_name}' ist keine gültige Anzahl an Platzierungen angegeben. Sie wird übersprungen."
                    )
                    continue

            platz_counts = defaultdict(int)
            for t in teams_fuer_urkunden:
                platz_counts[t['platz']] += 1

            platz_suffixes = defaultdict(lambda: 'a')

            for team in teams_fuer_urkunden:
                if team.get('gesamt', 0) == 0:
                    continue

                platz = team.get('platz', 0)
                platz_str = str(platz)

                if platz_counts[platz] > 1:
                    platz_str += platz_suffixes[platz]
                    platz_suffixes[platz] = chr(ord(platz_suffixes[platz]) + 1)

                mitglieder = team.get('mitglieder', [])
                mitglieder_text = self.format_mannschaftsmitglieder(
                    mitglieder,
                    include_scores=include_member_scores
                )

                # Verein ermitteln (falls alle Mitglieder im selben Verein sind)
                vereine = sorted({m.get('verein', '').strip() for m in mitglieder if m.get('verein', '').strip()})
                verein_str = ", ".join(vereine) if vereine else ""

                klasse_display = team.get('klasse') or group_name

                platzhalter_data = {
                    "[Turniername]": turnier_name,
                    "[Datum]": turnier_datum,
                    "[Klasse]": klasse_display,
                    "[Vorname]": "",
                    "[Name]": team.get('name', ''),
                    "[Verein]": verein_str,
                    "[Ergebnis]": str(int(team.get('gesamt', 0))),
                    "[Platz]": str(platz),
                    "[Mannschaftsname]": team.get('name', ''),
                    "[Mannschaftsmitglieder]": mitglieder_text
                }

                clean_turnier_name = re.sub(r'[^\w\-]', '', turnier_name.replace(' ', ''))
                clean_group = re.sub(r'[^\w\-]', '', group_name.replace(' ', ''))
                clean_team = re.sub(r'[^\w\-]', '', team.get('name', '').replace(' ', ''))
                filename = f"{clean_turnier_name}_{turnier_datum}_Mannschaft_{clean_group}_{platz_str}_{clean_team}.docx"

                current_output_dir = output_dir
                if self.unterordner_var.get():
                    current_output_dir = os.path.join(output_dir, f"Mannschaften_{clean_group}")
                    if not os.path.exists(current_output_dir):
                        os.makedirs(current_output_dir)

                output_path = os.path.join(current_output_dir, filename)

                success, error = word_generator.generate_certificate(output_path, platzhalter_data)
                if success:
                    erstellte_dateien += 1
                else:
                    messagebox.showerror("Fehler bei der Erstellung", f"Fehler bei Datei {filename}:\n{error}")
                    return

        if erstellte_dateien > 0:
            messagebox.showinfo("Erfolg", f"{erstellte_dateien} Mannschafts-Urkunden wurden erfolgreich erstellt.")
        else:
            messagebox.showwarning(
                "Keine Urkunden erstellt",
                "Es wurden keine Mannschafts-Urkunden erstellt. Überprüfen Sie die Einstellungen und ob Ergebnisse vorhanden sind."
            )
