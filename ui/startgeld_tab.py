# -*- coding: utf-8 -*-
"""
Startgeld-Verwaltung Tab
"""

import tkinter as tk
from tkinter import ttk

class StartgeldTab:
    """Tab für die Startgeld-Verwaltung"""

    def __init__(self, parent, turnier_model, schuetze_model):
        self.parent = parent
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.frame = ttk.Frame(parent, padding="10")

        self.sort_column_schuetzen = "Name"
        self.sort_reverse_schuetzen = False
        self.sort_column_vereine = "Verein"
        self.sort_reverse_vereine = False

        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets für den Tab"""

        # Titel
        ttk.Label(
            self.frame,
            text="Startgeldverwaltung",
            font=("Arial", 16, "bold")
        ).pack(fill=tk.X, pady=10)

        # Suchfeld
        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="Schütze filtern:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_schuetzen())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(fill=tk.X, expand=True)

        # Hauptcontainer mit PanedWindow
        paned_window = ttk.PanedWindow(self.frame, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=10)

        # Schützenliste
        schuetzen_frame = ttk.LabelFrame(paned_window, text="Alle Schützen", padding="10")
        self.create_schuetzen_tree(schuetzen_frame)
        paned_window.add(schuetzen_frame, weight=3)

        # Vereinsliste
        vereine_frame = ttk.LabelFrame(paned_window, text="Vereine", padding="10")
        self.create_vereine_tree(vereine_frame)
        paned_window.add(vereine_frame, weight=1)

    def create_schuetzen_tree(self, parent):
        """Erstellt die Treeview für die Schützenliste"""
        columns = ("Bezahlt", "Gruppe", "Scheibe", "Name", "Vorname", "Verein", "Startgeld", "Status")
        self.schuetzen_tree = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            self.schuetzen_tree.heading(col, text=col, command=lambda c=col: self.sort_schuetzen(c))

        self.schuetzen_tree.column("Bezahlt", width=50, anchor="center", stretch=False)
        self.schuetzen_tree.column("Gruppe", width=60, anchor="center")
        self.schuetzen_tree.column("Scheibe", width=60, anchor="center")
        self.schuetzen_tree.column("Name", width=150)
        self.schuetzen_tree.column("Vorname", width=150)
        self.schuetzen_tree.column("Verein", width=180)
        self.schuetzen_tree.column("Startgeld", width=80, anchor="e")
        self.schuetzen_tree.column("Status", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.schuetzen_tree.yview)
        self.schuetzen_tree.configure(yscrollcommand=scrollbar.set)

        self.schuetzen_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.schuetzen_tree.bind("<Button-1>", self.toggle_schuetze_status)

    def create_vereine_tree(self, parent):
        """Erstellt die Treeview für die Vereinsliste"""
        columns = ("Bezahlt", "Verein", "Gesamt-Startgeld", "Status")
        self.vereine_tree = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            self.vereine_tree.heading(col, text=col, command=lambda c=col: self.sort_vereine(c))

        self.vereine_tree.column("Bezahlt", width=80, anchor="center", stretch=False)
        self.vereine_tree.column("Verein", width=300)
        self.vereine_tree.column("Gesamt-Startgeld", width=120, anchor="e")
        self.vereine_tree.column("Status", width=150, anchor="center")

        self.vereine_tree.heading("Bezahlt", text="Alles bezahlt")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.vereine_tree.yview)
        self.vereine_tree.configure(yscrollcommand=scrollbar.set)

        self.vereine_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.vereine_tree.bind("<Button-1>", self.toggle_verein_status)

    def refresh(self):
        """Aktualisiert die Daten in beiden Listen"""
        # Farb-Tags konfigurieren
        self.schuetzen_tree.tag_configure('bezahlt', background='#d4edda') # Grün
        self.schuetzen_tree.tag_configure('unbezahlt', background='#f8d7da') # Rot
        self.schuetzen_tree.tag_configure('ueberpruefen', background='#fff3cd') # Orange

        self.vereine_tree.tag_configure('bezahlt', background='#d4edda')
        self.vereine_tree.tag_configure('unbezahlt', background='#f8d7da')
        self.vereine_tree.tag_configure('gemischt', background='#fff3cd')

        self.update_schuetzen_list()
        self.update_vereine_list()

    def filter_schuetzen(self):
        """Filtert die Schützenliste basierend auf der Sucheingabe."""
        self.update_schuetzen_list() # Neuaufbau der Liste mit Filter

    def sort_schuetzen(self, column):
        """Sortiert die Schützenliste."""
        if self.sort_column_schuetzen == column:
            self.sort_reverse_schuetzen = not self.sort_reverse_schuetzen
        else:
            self.sort_column_schuetzen = column
            self.sort_reverse_schuetzen = False
        self.update_schuetzen_list()

    def sort_vereine(self, column):
        """Sortiert die Vereinsliste."""
        if self.sort_column_vereine == column:
            self.sort_reverse_vereine = not self.sort_reverse_vereine
        else:
            self.sort_column_vereine = column
            self.sort_reverse_vereine = False
        self.update_vereine_list()

    def update_schuetzen_list(self):
        """Füllt die Schützenliste mit den aktuellen, gefilterten und sortierten Daten"""
        for item in self.schuetzen_tree.get_children():
            self.schuetzen_tree.delete(item)

        search_term = self.search_var.get().lower()
        all_schuetzen = self.schuetze_model.get_all_schuetzen()

        # Filtern
        if search_term:
            filtered_schuetzen = []
            for i, s in enumerate(all_schuetzen):
                full_name = f"{s.get('vorname', '')} {s.get('name', '')}".lower()
                if search_term in full_name or search_term in s.get('verein', '').lower():
                    filtered_schuetzen.append((i, s))
            schuetzen_to_display = filtered_schuetzen
        else:
            schuetzen_to_display = list(enumerate(all_schuetzen))

        # Sortieren
        sort_key_map = {
            "Name": lambda s: s[1].get('name', '').lower(),
            "Vorname": lambda s: s[1].get('vorname', '').lower(),
            "Verein": lambda s: s[1].get('verein', '').lower(),
        }
        sort_function = sort_key_map.get(self.sort_column_schuetzen)
        if sort_function:
            schuetzen_to_display.sort(key=sort_function, reverse=self.sort_reverse_schuetzen)

        for i, schuetze in schuetzen_to_display:
            startgeld_cent = self.turnier_model.get_klasse_startgeld(schuetze.get('klasse', ''))
            status = schuetze.get('startgeld_status', 'unbezahlt')

            # Wenn Startgeld 0 ist, immer als bezahlt behandeln
            if startgeld_cent == 0:
                status = 'bezahlt'

            startgeld_euro = f"{startgeld_cent / 100.0:.2f} €"

            tag = status

            self.schuetzen_tree.insert(
                "", tk.END, iid=str(i), tags=(tag,),
                values=(
                    "Ja" if status == 'bezahlt' else "Nein",
                    schuetze.get('gruppe', ''), schuetze.get('scheibe', ''),
                    schuetze.get('name', ''), schuetze.get('vorname', ''),
                    schuetze.get('verein', ''), startgeld_euro, status.capitalize()
                )
            )

    def update_vereine_list(self):
        """Füllt die Vereinsliste und berechnet die Summen"""
        for item in self.vereine_tree.get_children():
            self.vereine_tree.delete(item)

        vereine_data = {}
        all_schuetzen = self.schuetze_model.get_all_schuetzen()
        for schuetze in all_schuetzen:
            verein = schuetze.get('verein') or 'Ohne Verein'
            if verein not in vereine_data:
                vereine_data[verein] = {'total_startgeld': 0, 'bezahlt_count': 0, 'total_schuetzen': 0, 'ueberpruefen_count': 0}

            startgeld = self.turnier_model.get_klasse_startgeld(schuetze.get('klasse', ''))
            status = schuetze.get('startgeld_status', 'unbezahlt')
            vereine_data[verein]['total_startgeld'] += startgeld
            vereine_data[verein]['total_schuetzen'] += 1

            # Wenn Startgeld 0 ist, immer als bezahlt zählen
            if status == 'bezahlt' or startgeld == 0:
                vereine_data[verein]['bezahlt_count'] += 1
            elif status == 'ueberpruefen':
                vereine_data[verein]['ueberpruefen_count'] += 1

        # Sortieren
        sorted_vereine = sorted(vereine_data.items(), key=lambda item: item[0].lower(), reverse=self.sort_reverse_vereine)

        for verein, data in sorted_vereine:
            startgeld_euro = f"{data['total_startgeld'] / 100.0:.2f} €"

            tag, status_text = self.get_verein_status_display(data)

            self.vereine_tree.insert(
                "", tk.END, iid=verein, tags=(tag,),
                values=("Ja" if tag == 'bezahlt' else "Nein", verein, startgeld_euro, status_text)
            )

    def get_verein_status_display(self, data):
        """Ermittelt Anzeigetext und Tag für den Vereinsstatus."""
        total = data['total_schuetzen']
        paid = data['bezahlt_count']
        check = data['ueberpruefen_count']

        if paid == total:
            return 'bezahlt', "Vollständig bezahlt"
        if paid == 0 and check == 0:
            return 'unbezahlt', "Nicht bezahlt"
        return 'gemischt', f"{paid} von {total} bezahlt"

    def toggle_schuetze_status(self, event):
        """Ändert den Status eines Schützen beim Klick auf die Checkbox."""
        region = self.schuetzen_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.schuetzen_tree.identify_column(event.x)
        if column == "#1": # Nur die erste Spalte (Checkbox)
            item_id = self.schuetzen_tree.identify_row(event.y)
            if not item_id: return

            schuetze_index = int(item_id)
            schuetze = self.schuetze_model.get_schuetze(schuetze_index)
            startgeld_cent = self.turnier_model.get_klasse_startgeld(schuetze.get('klasse', ''))

            # Bei Startgeld 0 keine Statusänderung zulassen
            if startgeld_cent == 0:
                return

            current_status = schuetze.get('startgeld_status', 'unbezahlt')
            new_status = 'bezahlt' if current_status != 'bezahlt' else 'unbezahlt'

            self.schuetze_model.update_schuetze_startgeld_status(schuetze_index, new_status)
            self.refresh() # Neu zeichnen

    def toggle_verein_status(self, event):
        """Ändert den Status aller Schützen eines Vereins."""
        region = self.vereine_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.vereine_tree.identify_column(event.x)
        if column == "#1": # Nur die erste Spalte (Checkbox)
            verein_name = self.vereine_tree.identify_row(event.y)
            if not verein_name: return

            # Bestimme den Zielstatus: Wenn nicht alle bezahlt sind -> alle auf bezahlt setzen
            is_fully_paid = True
            for schuetze in self.schuetze_model.get_all_schuetzen():
                if (schuetze.get('verein') or 'Ohne Verein') == verein_name:
                    if schuetze.get('startgeld_status') != 'bezahlt':
                        is_fully_paid = False
                        break

            new_status = 'unbezahlt' if is_fully_paid else 'bezahlt'

            for i, schuetze in enumerate(self.schuetze_model.get_all_schuetzen()):
                if (schuetze.get('verein') or 'Ohne Verein') == verein_name:
                    self.schuetze_model.update_schuetze_startgeld_status(i, new_status)

            self.refresh()
