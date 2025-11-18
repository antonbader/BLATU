# -*- coding: utf-8 -*-
"""
Klassenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox


class KlassenTab:
    """Tab für Klassenverwaltung"""
    
    def __init__(self, parent, turnier_model, schuetze_model, on_klassen_changed=None):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.on_klassen_changed = on_klassen_changed  # Callback-Funktion
        self.on_klassen_changed_callback = None
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame, 
            text="Klassenverwaltung", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Eingabebereich
        input_frame = ttk.LabelFrame(self.frame, text="Neue Klasse anlegen", padding="10")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(input_frame, text="Klassenname:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.klasse_entry = ttk.Entry(input_frame, width=40)
        self.klasse_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Button(
            input_frame, 
            text="Klasse hinzufügen", 
            command=self.add_klasse
        ).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Listenbereich
        list_frame = ttk.LabelFrame(self.frame, text="Vorhandene Klassen", padding="10")
        list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.tree = ttk.Treeview(list_frame, columns=("Klassenname", "Startgeld"), show="headings")
        self.tree.heading("Klassenname", text="Klassenname")
        self.tree.heading("Startgeld", text="Startgeld (€)")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Ausgewählte Klasse löschen", 
            command=self.delete_klasse
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Alle Klassen löschen", 
            command=self.delete_all
        ).pack(side=tk.LEFT, padx=5)
        
        # Grid-Konfiguration
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.refresh()
    
    def on_double_click(self, event):
        """Behandelt Doppelklick auf eine Zeile zum Bearbeiten des Startgelds."""
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        if column != "#2":  # Nur die Startgeld-Spalte ist editierbar
            return

        item = self.tree.identify_row(event.y)

        x, y, width, height = self.tree.bbox(item, column)

        entry = ttk.Entry(self.tree)
        entry.place(x=x, y=y, width=width, height=height)

        current_value = self.tree.item(item, "values")[1]
        entry.insert(0, current_value)
        entry.focus()

        entry.bind("<Return>", lambda e, i=item: self.save_startgeld(entry, i))
        entry.bind("<FocusOut>", lambda e, i=item: self.save_startgeld(entry, i))

    def save_startgeld(self, entry, item):
        """Speichert das geänderte Startgeld."""
        new_value_str = entry.get().replace(",", ".").strip()
        entry.destroy()

        try:
            new_value = float(new_value_str)
            if new_value < 0:
                messagebox.showerror("Fehler", "Startgeld darf nicht negativ sein.")
                return
        except ValueError:
            messagebox.showerror("Fehler", "Ungültiger Wert für Startgeld.")
            return

        klasse_name = self.tree.item(item, "values")[0]

        if self.turnier_model.update_klasse_startgeld(klasse_name, new_value):
            # Status aller Schützen dieser Klasse auf "überprüfen" setzen
            all_schuetzen = self.schuetze_model.get_all_schuetzen()
            for i, schuetze in enumerate(all_schuetzen):
                if schuetze['klasse'] == klasse_name:
                    self.schuetze_model.update_schuetze_startgeld_status(i, "überprüfen")

            messagebox.showinfo("Erfolg", f"Startgeld für {klasse_name} aktualisiert.")
            self.refresh()
            # Callback für andere Tabs
            if self.on_klassen_changed:
                self.on_klassen_changed()
            if self.on_klassen_changed_callback:
                self.on_klassen_changed_callback()
        else:
            messagebox.showerror("Fehler", "Startgeld konnte nicht aktualisiert werden.")

    def add_klasse(self):
        """Fügt eine neue Klasse hinzu"""
        klasse = self.klasse_entry.get().strip()
        
        if not klasse:
            messagebox.showwarning("Eingabefehler", "Bitte einen Klassennamen eingeben!")
            return
        
        if self.turnier_model.add_klasse(klasse):
            self.refresh()
            self.klasse_entry.delete(0, tk.END)
            messagebox.showinfo("Erfolg", f"Klasse '{klasse}' wurde hinzugefügt!")
            
            # Callback aufrufen um Schützenverwaltung zu aktualisieren
            if self.on_klassen_changed:
                self.on_klassen_changed()
            if self.on_klassen_changed_callback:
                self.on_klassen_changed_callback()
        else:
            messagebox.showwarning("Duplikat", "Diese Klasse existiert bereits!")
    
    def delete_klasse(self):
        """Löscht die ausgewählte Klasse"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Klasse aus!")
            return
        
        item = selected_item[0]
        klasse_name = self.tree.item(item, "values")[0]
        
        # Prüfen ob Schützen in dieser Klasse sind
        count = self.schuetze_model.count_schuetzen_by_klasse(klasse_name)
        if count > 0:
            if not messagebox.askyesno(
                "Warnung", 
                f"Es gibt {count} Schütze(n) in dieser Klasse.\n"
                f"Möchten Sie die Klasse trotzdem löschen?"
            ):
                return
        
        self.turnier_model.remove_klasse(klasse_name)
        self.refresh()
        messagebox.showinfo("Erfolg", f"Klasse '{klasse_name}' wurde gelöscht!")
        
        # Callback aufrufen um Schützenverwaltung zu aktualisieren
        if self.on_klassen_changed:
            self.on_klassen_changed()
        if self.on_klassen_changed_callback:
            self.on_klassen_changed_callback()
    
    def delete_all(self):
        """Löscht alle Klassen"""
        if not self.turnier_model.get_klassen():
            messagebox.showinfo("Info", "Es sind keine Klassen vorhanden!")
            return
        
        if messagebox.askyesno(
            "Bestätigung", 
            "Möchten Sie wirklich ALLE Klassen löschen?"
        ):
            self.turnier_model.clear_klassen()
            self.refresh()
            messagebox.showinfo("Erfolg", "Alle Klassen wurden gelöscht!")
            
            # Callback aufrufen um Schützenverwaltung zu aktualisieren
            if self.on_klassen_changed:
                self.on_klassen_changed()
            if self.on_klassen_changed_callback:
                self.on_klassen_changed_callback()
    
    def refresh(self):
        """Aktualisiert die Anzeige"""
        # Alte Einträge löschen
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Neue Einträge hinzufügen
        for klasse in self.turnier_model.get_klassen():
            startgeld_euro = f"{klasse.get('startgeld', 0) / 100.0:.2f}"
            self.tree.insert("", tk.END, values=(klasse['name'], startgeld_euro))
