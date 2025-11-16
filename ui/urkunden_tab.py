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
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""

        main_frame = ttk.Frame(self.frame)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Linke Spalte: Einstellungen ---
        settings_frame = ttk.LabelFrame(main_frame, text="Einstellungen", padding="10")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Platzierungen
        ttk.Label(settings_frame, text="Urkunden für wie viele Platzierungen pro Klasse erstellen?").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.platzierungen_var = tk.StringVar(value="3")
        platzierungen_entry = ttk.Entry(settings_frame, textvariable=self.platzierungen_var, width=10)
        platzierungen_entry.grid(row=1, column=0, sticky="w")

        self.alle_schuetzen_var = tk.BooleanVar()
        alle_schuetzen_check = ttk.Checkbutton(settings_frame, text="Für alle Schützen erstellen", variable=self.alle_schuetzen_var)
        alle_schuetzen_check.grid(row=1, column=1, sticky="w", padx=(10, 0))

        # Speicherort
        ttk.Label(settings_frame, text="Speicherort für die Urkunden:").grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 5))

        self.output_dir_var = tk.StringVar()
        output_dir_entry = ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.grid(row=3, column=0, columnspan=2, sticky="we")

        browse_button = ttk.Button(settings_frame, text="Durchsuchen...", command=self.select_output_dir)
        browse_button.grid(row=3, column=2, sticky="w", padx=(5, 0))

        self.unterordner_var = tk.BooleanVar()
        unterordner_check = ttk.Checkbutton(settings_frame, text="Unterordner für jede Klasse erstellen", variable=self.unterordner_var)
        unterordner_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

        # --- Rechte Spalte: Platzhalter ---
        placeholder_frame = ttk.LabelFrame(main_frame, text="Platzhalter", padding="10")
        placeholder_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.placeholder_vars = {
            "[Turniername]": tk.BooleanVar(value=True),
            "[Datum]": tk.BooleanVar(value=True),
            "[Klasse]": tk.BooleanVar(value=True),
            "[Vorname]": tk.BooleanVar(value=True),
            "[Name]": tk.BooleanVar(value=True),
            "[Verein]": tk.BooleanVar(value=True),
            "[Ergebnis]": tk.BooleanVar(value=True),
            "[Platz]": tk.BooleanVar(value=True),
        }

        row = 0
        for placeholder, var in self.placeholder_vars.items():
            ttk.Checkbutton(placeholder_frame, text=placeholder, variable=var).grid(row=row, column=0, sticky="w")
            row += 1

        # --- Unterer Bereich: Aktion ---
        action_frame = ttk.Frame(main_frame, padding="10")
        action_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        generate_button = ttk.Button(action_frame, text="🚀 Urkunden erstellen", command=self.generate_urkunden, style="Accent.TButton")
        generate_button.pack(pady=10)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def select_output_dir(self):
        """Öffnet einen Dialog zur Auswahl des Speicherverzeichnisses."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)

    def generate_urkunden(self):
        """Startet den Prozess zur Erstellung der Urkunden."""
        # 1. Eingaben validieren
        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Speicherort aus.")
            return

        try:
            if not self.alle_schuetzen_var.get():
                platzierungen_anzahl = int(self.platzierungen_var.get())
                if platzierungen_anzahl <= 0:
                    raise ValueError()
        except ValueError:
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige, positive Zahl für die Platzierungen ein.")
            return

        # 2. Word-Vorlage abfragen
        template_path = filedialog.askopenfilename(
            title="Word-Vorlage auswählen",
            filetypes=[("Word Documents", "*.docx")]
        )
        if not template_path:
            return

        # 3. Daten vorbereiten
        ergebnisse = self.schuetze_model.calculate_results()
        turnier_name = self.turnier_model.get_turnier_name()
        turnier_datum = self.turnier_model.get_turnier_datum()

        # 4. Urkunden erstellen
        word_generator = WordGenerator(template_path)
        erstellte_dateien = 0

        for klasse, schuetzen in ergebnisse.items():
            schuetzen.sort(key=lambda s: s.get('Gesamt', 0), reverse=True)

            limit = len(schuetzen) if self.alle_schuetzen_var.get() else platzierungen_anzahl

            for i, schuetze in enumerate(schuetzen[:limit]):
                platz = i + 1

                # Platzhalterdaten zusammenstellen
                platzhalter_data = {
                    "[Turniername]": turnier_name,
                    "[Datum]": turnier_datum,
                    "[Klasse]": klasse,
                    "[Vorname]": schuetze.get('vorname', ''),
                    "[Name]": schuetze.get('name', ''),
                    "[Verein]": schuetze.get('verein', ''),
                    "[Ergebnis]": schuetze.get('Gesamt', 0),
                    "[Platz]": platz
                }

                # Nur ausgewählte Platzhalter verwenden
                final_data = {key: value for key, value in platzhalter_data.items() if self.placeholder_vars[key].get()}

                # Dateiname erstellen
                clean_turnier_name = re.sub(r'[^\w\-]', '', turnier_name.replace(' ', ''))
                clean_klasse = re.sub(r'[^\w\-]', '', klasse.replace(' ', ''))
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

        messagebox.showinfo("Erfolg", f"{erstellte_dateien} Urkunden wurden erfolgreich erstellt.")
