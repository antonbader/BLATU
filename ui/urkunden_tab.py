# -*- coding: utf-8 -*-
"""
Urkunden Tab
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
from collections import defaultdict
from utils.word_generator import WordGenerator

class UrkundenTab:
    """Tab für die Erstellung von Urkunden"""

    def __init__(self, parent, turnier_model, schuetze_model):
        self.frame = ttk.Frame(parent, padding="20")
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model

        # UI Variablen
        self.template_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.unterordner_var = tk.BooleanVar()
        self.alle_schuetzen_var = tk.BooleanVar()
        self.klassen_platz_vars = {}

        self.create_widgets()

        # Refresh tree when tab is selected
        parent.bind("<<NotebookTabChanged>>", self.on_tab_selected)

    def on_tab_selected(self, event):
        """Handle tab selection event."""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == "Urkunden":
            self.refresh()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- Linke Spalte: Klassen ---
        klassen_frame = ttk.LabelFrame(top_frame, text="Urkunden pro Platzierung", padding="10")
        klassen_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")

        alle_schuetzen_check = ttk.Checkbutton(klassen_frame, text="Für alle Schützen erstellen", variable=self.alle_schuetzen_var, command=self.toggle_klassen_tree)
        alle_schuetzen_check.pack(pady=5)

        ttk.Label(
            klassen_frame,
            text="💡 Doppelklick auf eine Zahl, um die Anzahl der Plätze zu ändern.",
            font=("Arial", 8),
            foreground="gray"
        ).pack(pady=(0, 5))

        self.klassen_tree = ttk.Treeview(klassen_frame, columns=("Klasse", "Anzahl"), show="headings", height=10)
        self.klassen_tree.heading("Klasse", text="Klasse")
        self.klassen_tree.heading("Anzahl", text="Anzahl Platzierungen")
        self.klassen_tree.column("Klasse", width=150)
        self.klassen_tree.column("Anzahl", width=120, anchor="center")
        self.klassen_tree.pack(fill=tk.BOTH, expand=True)
        self.klassen_tree.bind("<Double-1>", self.edit_cell)

        # --- Rechte Spalte: Einstellungen ---
        settings_frame = ttk.LabelFrame(top_frame, text="Einstellungen", padding="10")
        settings_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")

        # Vorlage
        ttk.Label(settings_frame, text="Word-Vorlage:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        template_entry = ttk.Entry(settings_frame, textvariable=self.template_path_var, width=40)
        template_entry.grid(row=1, column=0, sticky="we")
        ttk.Button(settings_frame, text="Durchsuchen...", command=self.select_template_file).grid(row=1, column=1, sticky="w", padx=(5, 0))

        # Speicherort
        ttk.Label(settings_frame, text="Speicherort:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 5))
        output_dir_entry = ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=40)
        output_dir_entry.grid(row=3, column=0, sticky="we")
        ttk.Button(settings_frame, text="Durchsuchen...", command=self.select_output_dir).grid(row=3, column=1, sticky="w", padx=(5, 0))

        self.unterordner_var.set(True)
        unterordner_check = ttk.Checkbutton(settings_frame, text="Unterordner für jede Klasse erstellen", variable=self.unterordner_var)
        unterordner_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

        # --- Unterer Bereich: Platzhalter ---
        placeholder_frame = ttk.LabelFrame(main_frame, text="Verfügbare Platzhalter", padding="10")
        placeholder_frame.pack(fill=tk.X, expand=False, pady=10)

        placeholders = [
            "[Turniername]", "[Datum]", "[Klasse]", "[Vorname]",
            "[Name]", "[Verein]", "[Ergebnis]", "[Platz]"
        ]

        # Display placeholders as a wrapped label
        placeholder_text = ", ".join(placeholders)
        ttk.Label(
            placeholder_frame,
            text=placeholder_text,
            wraplength=700,
            justify="center"
        ).pack(pady=5)

        # --- Unterster Bereich: Aktion ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=20)

        generate_button = ttk.Button(action_frame, text="🚀 Urkunden erstellen", command=self.generate_urkunden, style="Accent.TButton")
        generate_button.pack()

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)

    def edit_cell(self, event):
        """Handle double-click to edit cell value."""
        item_id = self.klassen_tree.identify_row(event.y)
        column_id = self.klassen_tree.identify_column(event.x)

        if not item_id or column_id != "#2":  # Only edit "Anzahl" column
            return

        # Create an Entry widget over the cell
        x, y, width, height = self.klassen_tree.bbox(item_id, column_id)

        klasse = self.klassen_tree.item(item_id, "values")[0]
        var = self.klassen_platz_vars[klasse]

        entry = ttk.Entry(self.klassen_tree, textvariable=var, width=10, justify="center")
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()

        def save_edit(event=None):
            new_value = entry.get()
            try:
                if int(new_value) >= 0:
                    self.klassen_tree.item(item_id, values=(klasse, new_value))
                else:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Ungültige Eingabe", "Bitte geben Sie eine positive ganze Zahl ein.")
                var.set(self.klassen_tree.item(item_id, "values")[1]) # Reset to old value
            finally:
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
        """Füllt die Klassenliste."""
        for item in self.klassen_tree.get_children():
            self.klassen_tree.delete(item)

        self.klassen_platz_vars.clear()

        klassen_data = self.turnier_model.get_klassen()
        for klasse_dict in klassen_data:
            klasse_name = klasse_dict['name']
            var = tk.StringVar(value="3")
            self.klassen_platz_vars[klasse_name] = var
            self.klassen_tree.insert("", "end", values=(klasse_name, var.get()))

    def toggle_klassen_tree(self):
        """Aktiviert/Deaktiviert die Klasseneingabefelder."""
        state = "disabled" if self.alle_schuetzen_var.get() else "normal"
        # Since we can't disable the cell, we just prevent editing
        if state == "disabled":
            self.klassen_tree.unbind("<Double-1>")
        else:
            self.klassen_tree.bind("<Double-1>", self.edit_cell)


    def refresh(self):
        """Wird aufgerufen, wenn der Tab sichtbar wird."""
        self.populate_klassen_tree()

    def generate_urkunden(self):
        """Startet den Prozess zur Erstellung der Urkunden."""
        # 1. Eingaben validieren
        output_dir = self.output_dir_var.get()
        template_path = self.template_path_var.get()

        if not output_dir or not template_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Speicherort und eine Vorlagedatei aus.")
            return

        if not os.path.exists(template_path):
            messagebox.showerror("Fehler", "Die angegebene Vorlagedatei existiert nicht.")
            return

        # 2. Daten vorbereiten
        try:
            ergebnisse = self.schuetze_model.calculate_results(self.turnier_model)
            turnier_data = self.turnier_model.get_turnier_data()
            turnier_name = turnier_data.get("name", "Unbenanntes Turnier")
            turnier_datum = turnier_data.get("datum", "")
        except Exception as e:
            messagebox.showerror("Fehler bei der Datenverarbeitung", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
            return

        # 3. Urkunden erstellen
        word_generator = WordGenerator(template_path)
        erstellte_dateien = 0

        for klasse, schuetzen in ergebnisse.items():
            if not schuetzen:
                continue

            # Schützen für die Urkundenerstellung auswählen
            schuetzen_fuer_urkunden = []
            if self.alle_schuetzen_var.get():
                schuetzen_fuer_urkunden = schuetzen
            else:
                try:
                    max_platz = int(self.klassen_platz_vars[klasse].get())
                    if max_platz > 0:
                        schuetzen_fuer_urkunden = [s for s in schuetzen if s.get('Platz', 0) <= max_platz]
                except (KeyError, ValueError):
                    messagebox.showwarning("Fehlerhafte Eingabe", f"Für die Klasse '{klasse}' ist keine gültige Anzahl an Platzierungen angegeben. Sie wird übersprungen.")
                    continue

            # Zähle, wie oft jeder Platz vorkommt (für Dateinamen-Suffix)
            platz_counts = defaultdict(int)
            for s in schuetzen_fuer_urkunden:
                platz_counts[s['Platz']] += 1

            platz_suffixes = defaultdict(lambda: 'a')

            for schuetze in schuetzen_fuer_urkunden:
                # Überspringe Schützen mit 0 Punkten
                if schuetze.get('Gesamt', 0) == 0:
                    continue

                platz = schuetze.get('Platz', 0)
                platz_str = str(platz)

                # Dateinamen-Suffix bei Gleichstand hinzufügen
                if platz_counts[platz] > 1:
                    platz_str += platz_suffixes[platz]
                    # Increment suffix for the next person with the same rank
                    platz_suffixes[platz] = chr(ord(platz_suffixes[platz]) + 1)

                # Platzhalterdaten zusammenstellen
                platzhalter_data = {
                    "[Turniername]": turnier_name,
                    "[Datum]": turnier_datum,
                    "[Klasse]": klasse,
                    "[Vorname]": schuetze.get('vorname', ''),
                    "[Name]": schuetze.get('name', ''),
                    "[Verein]": schuetze.get('verein', ''),
                    "[Ergebnis]": str(schuetze.get('Gesamt', 0)),
                    "[Platz]": str(platz) # Platz ohne Suffix in der Urkunde
                }

                # Dateiname erstellen
                clean_turnier_name = re.sub(r'[^\w\-]', '', turnier_name.replace(' ', ''))
                clean_klasse = re.sub(r'[^\w\-]', '', klasse.replace(' ', ''))
                filename = f"{clean_turnier_name}_{turnier_datum}_{clean_klasse}_{platz_str}.docx"

                # Speicherpfad bestimmen
                current_output_dir = output_dir
                if self.unterordner_var.get():
                    current_output_dir = os.path.join(output_dir, clean_klasse)
                    if not os.path.exists(current_output_dir):
                        os.makedirs(current_output_dir)

                output_path = os.path.join(current_output_dir, filename)

                # Urkunde generieren
                success, error = word_generator.generate_certificate(output_path, platzhalter_data)
                if success:
                    erstellte_dateien += 1
                else:
                    messagebox.showerror("Fehler bei der Erstellung", f"Fehler bei Datei {filename}:\n{error}")
                    return

        if erstellte_dateien > 0:
            messagebox.showinfo("Erfolg", f"{erstellte_dateien} Urkunden wurden erfolgreich erstellt.")
        else:
            messagebox.showwarning("Keine Urkunden erstellt", "Es wurden keine Urkunden erstellt. Überprüfen Sie die Einstellungen und ob Ergebnisse vorhanden sind.")
