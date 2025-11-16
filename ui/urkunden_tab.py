# -*- coding: utf-8 -*-
"""
Urkunden Tab
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re
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
        self.placeholder_vars = {}
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

        # --- Linke Spalte: Einstellungen ---
        settings_frame = ttk.LabelFrame(main_frame, text="Einstellungen", padding="10")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Vorlage
        ttk.Label(settings_frame, text="Word-Vorlage:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        template_entry = ttk.Entry(settings_frame, textvariable=self.template_path_var, width=50)
        template_entry.grid(row=1, column=0, columnspan=2, sticky="we")
        ttk.Button(settings_frame, text="Durchsuchen...", command=self.select_template_file).grid(row=1, column=2, sticky="w", padx=(5, 0))

        # Speicherort
        ttk.Label(settings_frame, text="Speicherort:").grid(row=2, column=0, sticky="w", pady=(10, 5))
        output_dir_entry = ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.grid(row=3, column=0, columnspan=2, sticky="we")
        ttk.Button(settings_frame, text="Durchsuchen...", command=self.select_output_dir).grid(row=3, column=2, sticky="w", padx=(5, 0))

        self.unterordner_var.set(True)
        unterordner_check = ttk.Checkbutton(settings_frame, text="Unterordner für jede Klasse erstellen", variable=self.unterordner_var)
        unterordner_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

        # --- Mittlere Spalte: Klassen ---
        klassen_frame = ttk.LabelFrame(main_frame, text="Anzahl pro Klasse", padding="10")
        klassen_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        alle_schuetzen_check = ttk.Checkbutton(klassen_frame, text="Für alle Schützen erstellen", variable=self.alle_schuetzen_var, command=self.toggle_klassen_tree)
        alle_schuetzen_check.pack(pady=5)

        self.klassen_tree = ttk.Treeview(klassen_frame, columns=("Klasse", "Anzahl"), show="headings", height=10)
        self.klassen_tree.heading("Klasse", text="Klasse")
        self.klassen_tree.heading("Anzahl", text="Anzahl Urkunden")
        self.klassen_tree.column("Klasse", width=150)
        self.klassen_tree.column("Anzahl", width=120, anchor="center")
        self.klassen_tree.pack(fill=tk.BOTH, expand=True)

        # --- Rechte Spalte: Platzhalter ---
        placeholder_frame = ttk.LabelFrame(main_frame, text="Platzhalter", padding="10")
        placeholder_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        placeholders = [
            "[Turniername]", "[Datum]", "[Klasse]", "[Vorname]",
            "[Name]", "[Verein]", "[Ergebnis]", "[Platz]"
        ]

        for i, p_text in enumerate(placeholders):
            var = tk.BooleanVar(value=True)
            self.placeholder_vars[p_text] = var
            ttk.Checkbutton(placeholder_frame, text=p_text, variable=var).grid(row=i, column=0, sticky="w")

        # --- Unterer Bereich: Aktion ---
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=1, column=0, columnspan=3, pady=20)

        generate_button = ttk.Button(action_frame, text="🚀 Urkunden erstellen", command=self.generate_urkunden, style="Accent.TButton")
        generate_button.pack()

        main_frame.columnconfigure(0, weight=2)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

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

        klassen = self.turnier_model.get_klassen()
        for klasse in klassen:
            var = tk.StringVar(value="3")
            self.klassen_platz_vars[klasse] = var

            # This is a bit of a hack to embed an Entry widget
            # A more robust solution would use a custom Treeview class
            item = self.klassen_tree.insert("", "end", values=(klasse, ""))
            entry = ttk.Entry(self.klassen_tree, textvariable=var, width=10, justify="center")
            self.klassen_tree.item(item, tags=(entry,))
            self.klassen_tree.window_create(item, "Anzahl", window=entry)

    def toggle_klassen_tree(self):
        """Aktiviert/Deaktiviert die Klasseneingabefelder."""
        state = "disabled" if self.alle_schuetzen_var.get() else "normal"
        for item in self.klassen_tree.get_children():
            entry_widget = self.klassen_tree.item(item, "tags")[0]
            entry_widget.config(state=state)

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
            turnier_name = self.turnier_model.get_turnier_name()
            turnier_datum = self.turnier_model.get_turnier_datum()
        except Exception as e:
            messagebox.showerror("Fehler bei der Datenverarbeitung", f"Ein unerwarteter Fehler ist aufgetreten:\n{e}")
            return

        # 4. Urkunden erstellen
        word_generator = WordGenerator(template_path)
        erstellte_dateien = 0

        for klasse, schuetzen in ergebnisse.items():
            if not schuetzen:
                continue

            limit = 0
            if self.alle_schuetzen_var.get():
                limit = len(schuetzen)
            else:
                try:
                    limit = int(self.klassen_platz_vars[klasse].get())
                except (KeyError, ValueError):
                    messagebox.showwarning("Fehlerhafte Eingabe", f"Für die Klasse '{klasse}' ist keine gültige Anzahl an Urkunden angegeben. Sie wird übersprungen.")
                    continue

            if limit <= 0:
                continue

            for schuetze in schuetzen[:limit]:
                # Platzhalterdaten zusammenstellen
                platzhalter_data = {
                    "[Turniername]": turnier_name,
                    "[Datum]": turnier_datum,
                    "[Klasse]": klasse,
                    "[Vorname]": schuetze.get('vorname', ''),
                    "[Name]": schuetze.get('name', ''),
                    "[Verein]": schuetze.get('verein', ''),
                    "[Ergebnis]": schuetze.get('Gesamt', 0),
                    "[Platz]": schuetze.get('Platz', 0)
                }

                # Nur ausgewählte Platzhalter verwenden
                final_data = {key: value for key, value in platzhalter_data.items() if self.placeholder_vars.get(key) and self.placeholder_vars[key].get()}

                # Dateiname erstellen
                clean_turnier_name = re.sub(r'[^\w\-]', '', turnier_name.replace(' ', ''))
                clean_klasse = re.sub(r'[^\w\-]', '', klasse.replace(' ', ''))
                platz = schuetze.get('Platz', 0)
                filename = f"{clean_turnier_name}_{turnier_datum}_{clean_klasse}_{platz}.docx"

                # Speicherpfad bestimmen
                current_output_dir = output_dir
                if self.unterordner_var.get():
                    current_output_dir = os.path.join(output_dir, clean_klasse)
                    if not os.path.exists(current_output_dir):
                        os.makedirs(current_output_dir)

                output_path = os.path.join(current_output_dir, filename)

                # Urkunde generieren
                success, error = word_generator.generate_certificate(output_path, final_data)
                if success:
                    erstellte_dateien += 1
                else:
                    messagebox.showerror("Fehler bei der Erstellung", f"Fehler bei Datei {filename}:\n{error}")
                    return

        if erstellte_dateien > 0:
            messagebox.showinfo("Erfolg", f"{erstellte_dateien} Urkunden wurden erfolgreich erstellt.")
        else:
            messagebox.showwarning("Keine Urkunden erstellt", "Es wurden keine Urkunden erstellt. Überprüfen Sie die Einstellungen und ob Ergebnisse vorhanden sind.")
