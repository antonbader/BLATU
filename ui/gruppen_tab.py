# -*- coding: utf-8 -*-
"""
Gruppenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox


class GruppenTab:
    """Tab für Gruppenverwaltung"""

    def __init__(self, parent, turnier_model, schuetze_model, pdf_generator, on_assignment_changed=None):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.pdf_generator = pdf_generator
        self.on_assignment_changed = on_assignment_changed
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
            columns=("Gruppe", "Uhrzeit", "Scheibe", "Schütze", "Verein"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.tree.heading("Gruppe", text="Gruppe")
        self.tree.heading("Uhrzeit", text="Uhrzeit")
        self.tree.heading("Scheibe", text="Scheibe")
        self.tree.heading("Schütze", text="Schütze")
        self.tree.heading("Verein", text="Verein")
        self.tree.column("Gruppe", width=80, anchor="center")
        self.tree.column("Uhrzeit", width=80, anchor="center")
        self.tree.column("Scheibe", width=80, anchor="center")
        self.tree.column("Schütze", width=300)
        self.tree.column("Verein", width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<<TreeviewSelect>>", self.on_schuetze_selected)

        # Bearbeitungs-Frame
        edit_frame = ttk.Frame(self.frame)
        edit_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Uhrzeit-Eingabe
        time_frame = ttk.LabelFrame(edit_frame, text="Uhrzeit für Gruppe festlegen", padding="10")
        time_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Label(time_frame, text="Uhrzeit (HH:MM):").grid(row=0, column=0, padx=5)
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=10)
        self.time_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            time_frame,
            text="Für ausgewählte Gruppe speichern",
            command=self.save_group_time
        ).grid(row=0, column=2, padx=10)

        # Zuweisung ändern
        assign_frame = ttk.LabelFrame(edit_frame, text="Zuweisung für Schützen ändern", padding="10")
        assign_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        ttk.Label(assign_frame, text="Gruppe:").grid(row=0, column=0, padx=5)
        self.gruppe_var = tk.StringVar()
        self.gruppe_entry = ttk.Entry(assign_frame, textvariable=self.gruppe_var, width=5)
        self.gruppe_entry.grid(row=0, column=1, padx=5)

        ttk.Label(assign_frame, text="Scheibe:").grid(row=0, column=2, padx=5)
        self.scheibe_var = tk.StringVar()
        self.scheibe_entry = ttk.Entry(assign_frame, textvariable=self.scheibe_var, width=5)
        self.scheibe_entry.grid(row=0, column=3, padx=5)

        ttk.Button(
            assign_frame,
            text="Zuweisung ändern",
            command=self.change_assignment
        ).grid(row=0, column=4, padx=10)

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
                    f"{schuetze.get('vorname', '')} {schuetze.get('name', '')}",
                    schuetze.get('verein', '')
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

    def on_schuetze_selected(self, event):
        """Wird aufgerufen, wenn ein Schütze in der Liste ausgewählt wird"""
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item['values']

        # Finde die tatsächliche Gruppennummer
        gruppe = values[0]
        if gruppe == "":
            current_index = self.tree.index(selected[0])
            for i in range(current_index, -1, -1):
                prev_item = self.tree.item(self.tree.get_children()[i])
                if prev_item['values'][0] != "":
                    gruppe = prev_item['values'][0]
                    break

        scheibe = values[2]

        self.gruppe_var.set(gruppe)
        self.scheibe_var.set(scheibe)

    def change_assignment(self):
        """Ändert die Zuweisung für den ausgewählten Schützen"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return

        try:
            new_gruppe = int(self.gruppe_var.get())
            new_scheibe = int(self.scheibe_var.get())
        except ValueError:
            messagebox.showerror("Fehler", "Gruppe und Scheibe müssen Zahlen sein.")
            return

        item = self.tree.item(selected[0])
        schuetze_name_full = item['values'][3]

        # Finde den Schützen im Modell
        schuetzen = self.schuetze_model.get_all_schuetzen()
        schuetze_index = -1
        for i, s in enumerate(schuetzen):
            full_name = f"{s.get('vorname', '')} {s.get('name', '')}"
            if full_name == schuetze_name_full:
                schuetze_index = i
                break

        if schuetze_index == -1:
            messagebox.showerror("Fehler", "Ausgewählter Schütze konnte nicht gefunden werden.")
            return

        # Prüfung auf Doppelbelegung
        for i, s in enumerate(schuetzen):
            if s.get('gruppe') == new_gruppe and s.get('scheibe') == new_scheibe and i != schuetze_index:
                messagebox.showerror("Fehler", f"Scheibe {new_scheibe} in Gruppe {new_gruppe} ist bereits belegt.")
                return

        schuetze_to_update = self.schuetze_model.get_schuetze(schuetze_index)
        self.schuetze_model.update_schuetze(
            schuetze_index,
            schuetze_to_update['name'],
            schuetze_to_update['vorname'],
            schuetze_to_update['klasse'],
            schuetze_to_update['verein'],
            gruppe=new_gruppe,
            scheibe=new_scheibe
        )

        self.refresh()
        messagebox.showinfo("Erfolg", "Zuweisung wurde aktualisiert.")

        if self.on_assignment_changed:
            self.on_assignment_changed()
