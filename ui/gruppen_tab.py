# -*- coding: utf-8 -*-
"""
Gruppenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox


class GruppenTab:
    """Tab für Gruppenverwaltung"""

    def __init__(self, parent, turnier_model, schuetze_model, pdf_generator):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.pdf_generator = pdf_generator
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame,
            text="Gruppenverwaltung",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # Listenbereich
        list_frame = ttk.LabelFrame(self.frame, text="Gruppenübersicht", padding="10")
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Gruppe", "Uhrzeit", "Scheibe", "Schütze"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.tree.heading("Gruppe", text="Gruppe")
        self.tree.heading("Uhrzeit", text="Uhrzeit")
        self.tree.heading("Scheibe", text="Scheibe")
        self.tree.heading("Schütze", text="Schütze")
        self.tree.column("Gruppe", width=100, anchor="center")
        self.tree.column("Uhrzeit", width=100, anchor="center")
        self.tree.column("Scheibe", width=100, anchor="center")
        self.tree.column("Schütze", width=400)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Uhrzeit-Eingabe
        time_frame = ttk.LabelFrame(self.frame, text="Uhrzeit für Gruppe festlegen", padding="10")
        time_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(time_frame, text="Uhrzeit (HH:MM):").grid(row=0, column=0, padx=5)
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=10)
        self.time_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            time_frame,
            text="Für ausgewählte Gruppe speichern",
            command=self.save_group_time
        ).grid(row=0, column=2, padx=10)

        # PDF-Button
        pdf_button = ttk.Button(
            self.frame,
            text="Gruppen-PDF erstellen",
            command=self.create_group_pdf
        )
        pdf_button.grid(row=3, column=0, columnspan=3, pady=20)

        # Grid-Konfiguration
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.refresh()

    def refresh(self):
        """Aktualisiert die Anzeige"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        schuetzen = self.schuetze_model.get_all_schuetzen()

        # Filtere Schützen, die einer Gruppe zugewiesen sind
        assigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is not None]

        # Sortiere nach Gruppe und dann nach Scheibe
        assigned_schuetzen.sort(key=lambda s: (s.get('gruppe', 0), s.get('scheibe', 0)))

        # Gruppiere Schützen
        groups = {}
        for s in assigned_schuetzen:
            gruppe = s.get('gruppe')
            if gruppe not in groups:
                groups[gruppe] = []
            groups[gruppe].append(s)

        for gruppe, schuetzen_in_gruppe in sorted(groups.items()):
            group_time = self.turnier_model.get_group_time(gruppe)
            for i, schuetze in enumerate(schuetzen_in_gruppe):
                display_gruppe = gruppe if i == 0 else ""
                display_time = group_time if i == 0 else ""

                self.tree.insert("", tk.END, values=(
                    display_gruppe,
                    display_time,
                    schuetze.get('scheibe', ''),
                    f"{schuetze.get('vorname', '')} {schuetze.get('name', '')}"
                ))

    def save_group_time(self):
        """Speichert die Uhrzeit für die ausgewählte Gruppe"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Eintrag in der Liste aus, um die Gruppe zu bestimmen.")
            return

        item = self.tree.item(selected[0])
        gruppe = item['values'][0]

        # Finde die tatsächliche Gruppennummer, falls die Zelle leer war
        if gruppe == "":
            current_index = self.tree.index(selected[0])
            for i in range(current_index, -1, -1):
                prev_item = self.tree.item(self.tree.get_children()[i])
                if prev_item['values'][0] != "":
                    gruppe = prev_item['values'][0]
                    break

        if gruppe == "":
             messagebox.showwarning("Fehler", "Konnte die Gruppe nicht bestimmen.")
             return

        time_str = self.time_var.get()
        # Hier könnte eine Validierung des Zeitformats (HH:MM) erfolgen

        self.turnier_model.set_group_time(gruppe, time_str)
        self.refresh()
        messagebox.showinfo("Erfolg", f"Uhrzeit für Gruppe {gruppe} wurde gespeichert.")

    def create_group_pdf(self):
        """Erstellt ein PDF mit der Gruppenübersicht"""
        schuetzen = self.schuetze_model.get_all_schuetzen()
        assigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is not None]

        if not assigned_schuetzen:
            messagebox.showinfo("Info", "Es sind keine Schützen Gruppen zugewiesen. Das PDF wird nicht erstellt.")
            return

        self.pdf_generator.generate_gruppen_pdf(assigned_schuetzen)
