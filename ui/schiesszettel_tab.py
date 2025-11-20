# -*- coding: utf-8 -*-
"""
Schießzettel Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re
from utils.word_generator import WordGenerator

class SchiesszettelTab:
    """Tab für die Generierung von Schießzetteln"""

    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.frame = ttk.Frame(parent, padding="10")

        self.template_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.selected_groups = {} # Dictionary to store BooleanVars for groups

        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame,
            text="Schießzettel generieren",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # --- Einstellungen (Links) ---
        settings_frame = ttk.LabelFrame(self.frame, text="Einstellungen", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.N, tk.W, tk.E), padx=(0, 10))

        # Vorlage
        ttk.Label(settings_frame, text="Word-Vorlage:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.template_path, width=40).grid(row=1, column=0, pady=2)
        ttk.Button(settings_frame, text="Auswählen", command=self.select_template).grid(row=1, column=1, padx=5)

        # Speicherort
        ttk.Label(settings_frame, text="Speicherort:").grid(row=2, column=0, sticky=tk.W, pady=(10, 2))
        ttk.Entry(settings_frame, textvariable=self.output_path, width=40).grid(row=3, column=0, pady=2)
        ttk.Button(settings_frame, text="Auswählen", command=self.select_output_dir).grid(row=3, column=1, padx=5)

        # Platzhalter Info
        info_frame = ttk.LabelFrame(self.frame, text="Verfügbare Platzhalter", padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=(0, 10))

        info_text = (
            "[Turniername], [Turnierdatum]\n"
            "[Name_1], [Vorname_1], [Gruppe_1], [Scheibe_1]\n"
            "[Name_2], [Vorname_2], [Gruppe_2], [Scheibe_2]\n"
            "[Name_3], [Vorname_3], [Gruppe_3], [Scheibe_3]\n"
            "[Name_4], [Vorname_4], [Gruppe_4], [Scheibe_4]"
        )
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)


        # --- Gruppenauswahl (Rechts) ---
        selection_frame = ttk.LabelFrame(self.frame, text="Gruppenauswahl", padding="10")
        selection_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Toolbar für Auswahl
        toolbar_frame = ttk.Frame(selection_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(toolbar_frame, text="Alle auswählen", command=self.select_all_groups).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar_frame, text="Keine auswählen", command=self.deselect_all_groups).pack(side=tk.LEFT)

        # Scrollbare Liste mit Checkbuttons
        canvas = tk.Canvas(selection_frame)
        scrollbar = ttk.Scrollbar(selection_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Action Button (Unten) ---
        action_frame = ttk.Frame(self.frame, padding="10")
        action_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(
            action_frame,
            text="Schießzettel generieren",
            command=self.generate_schiesszettel,
            style="Accent.TButton"  # Versucht, falls ein Theme aktiv ist, sonst normal
        ).pack(pady=10)

        # Configure Grid weights
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # Initial refresh
        self.refresh_groups()

    def refresh_groups(self):
        """Lädt die Gruppen aus dem Schützenmodell neu"""
        # Bestehende Checkboxen entfernen
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.selected_groups.clear()

        schuetzen = self.schuetze_model.get_all_schuetzen()

        # Gruppen extrahieren und sortieren
        groups = sorted(list(set(s.get('gruppe') for s in schuetzen if s.get('gruppe') is not None)))

        for group in groups:
            var = tk.BooleanVar(value=False)
            self.selected_groups[group] = var
            cb = ttk.Checkbutton(self.scrollable_frame, text=f"Gruppe {group}", variable=var)
            cb.pack(anchor=tk.W, pady=2)

    def select_template(self):
        filename = filedialog.askopenfilename(
            title="Word-Vorlage auswählen",
            filetypes=[("Word-Dokumente", "*.docx")]
        )
        if filename:
            self.template_path.set(filename)

    def select_output_dir(self):
        dirname = filedialog.askdirectory(title="Speicherort auswählen")
        if dirname:
            self.output_path.set(dirname)

    def select_all_groups(self):
        for var in self.selected_groups.values():
            var.set(True)

    def deselect_all_groups(self):
        for var in self.selected_groups.values():
            var.set(False)

    def generate_schiesszettel(self):
        template = self.template_path.get()
        output_dir = self.output_path.get()

        if not template or not os.path.exists(template):
            messagebox.showerror("Fehler", "Bitte wählen Sie eine gültige Word-Vorlage aus.")
            return

        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("Fehler", "Bitte wählen Sie einen gültigen Speicherort aus.")
            return

        selected_group_ids = [gid for gid, var in self.selected_groups.items() if var.get()]

        if not selected_group_ids:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens eine Gruppe aus.")
            return

        generator = WordGenerator(template)
        turnier_data = self.turnier_model.get_turnier_data()
        turnier_name = self._sanitize_filename(turnier_data.get('name', 'Turnier'))
        turnier_datum = self._sanitize_filename(turnier_data.get('datum', 'Datum'))

        success_count = 0
        error_msgs = []

        schuetzen = self.schuetze_model.get_all_schuetzen()

        for group_id in selected_group_ids:
            # Schützen der Gruppe filtern
            group_shooters = [s for s in schuetzen if s.get('gruppe') == group_id]
            if not group_shooters:
                continue

            # Dateiname generieren: SZ_[Turniername]_[Gruppe]_[Datum].docx
            filename = f"SZ_{turnier_name}_{group_id}_{turnier_datum}.docx"
            filepath = os.path.join(output_dir, filename)

            success, msg = generator.generate_schiesszettel(filepath, group_shooters, template, turnier_data)

            if success:
                success_count += 1
            else:
                error_msgs.append(f"Gruppe {group_id}: {msg}")

        # Abschlussmeldung
        if not error_msgs:
            messagebox.showinfo("Erfolg", f"{success_count} Schießzettel wurden erfolgreich erstellt.")
        else:
            error_text = "\n".join(error_msgs)
            messagebox.showwarning("Teilweiser Erfolg", f"{success_count} erfolgreich erstellt.\n\nFehler:\n{error_text}")

    def _sanitize_filename(self, filename):
        """Entfernt ungültige Zeichen für Dateinamen"""
        return re.sub(r'[\\/*?:"<>|]', "", str(filename)).strip().replace(" ", "")

    def refresh(self):
        """Extern aufrufbar, um die Ansicht zu aktualisieren"""
        self.refresh_groups()
