# -*- coding: utf-8 -*-
"""
Schützenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox


class SchuetzenTab:
    """Tab für Schützenverwaltung"""
    
    def __init__(self, parent, turnier_model, schuetze_model, on_schuetzen_changed=None):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.on_schuetzen_changed = on_schuetzen_changed  # Callback-Funktion
        self.editing_index = None
        self.sort_column = None
        self.sort_reverse = False
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame, 
            text="Schützenverwaltung", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)
        
        # Eingabebereich
        input_frame = ttk.LabelFrame(self.frame, text="Schützen bearbeiten", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Name
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Vorname
        ttk.Label(input_frame, text="Vorname:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.vorname_entry = ttk.Entry(input_frame, width=30)
        self.vorname_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Klasse
        ttk.Label(input_frame, text="Klasse:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.klasse_combo = ttk.Combobox(input_frame, width=28, state="readonly")
        self.klasse_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Verein
        ttk.Label(input_frame, text="Verein:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.verein_entry = ttk.Entry(input_frame, width=30)
        self.verein_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Button
        self.add_button = ttk.Button(
            input_frame, 
            text="Schütze hinzufügen", 
            command=self.add_or_update_schuetze
        )
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Listenbereich
        list_frame = ttk.LabelFrame(self.frame, text="Schützenliste", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Hinweis zur Sortierung
        ttk.Label(
            list_frame, 
            text="💡 Klicken Sie auf die Spaltenüberschriften zum Sortieren", 
            font=("Arial", 9), 
            foreground="gray"
        ).pack(pady=(0, 5))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(
            list_frame, 
            columns=("Name", "Vorname", "Klasse", "Verein"), 
            show="headings", 
            yscrollcommand=scrollbar.set, 
            height=15
        )
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by_column("Name"))
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sort_by_column("Vorname"))
        self.tree.heading("Klasse", text="Klasse", command=lambda: self.sort_by_column("Klasse"))
        self.tree.heading("Verein", text="Verein", command=lambda: self.sort_by_column("Verein"))
        self.tree.column("Name", width=200)
        self.tree.column("Vorname", width=200)
        self.tree.column("Klasse", width=150)
        self.tree.column("Verein", width=200)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())
        
        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(
            button_frame, 
            text="Bearbeiten", 
            command=self.edit_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Ausgewählten löschen", 
            command=self.delete_selected
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Alle Schützen löschen", 
            command=self.delete_all
        ).pack(side=tk.LEFT, padx=5)
        
        # Grid-Konfiguration
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.refresh()
    
    def sort_by_column(self, column):
        """Sortiert die Tabelle nach der angegebenen Spalte"""
        # Wenn die gleiche Spalte nochmal geklickt wird, Sortierreihenfolge umkehren
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        self.refresh()
    
    def add_or_update_schuetze(self):
        """Fügt einen Schützen hinzu oder aktualisiert ihn"""
        name = self.name_entry.get().strip()
        vorname = self.vorname_entry.get().strip()
        klasse = self.klasse_combo.get().strip()
        verein = self.verein_entry.get().strip()
        
        if not name or not vorname or not klasse:
            messagebox.showwarning(
                "Eingabefehler", 
                "Bitte Name, Vorname und Klasse ausfüllen!"
            )
            return
        
        if self.editing_index is not None:
            # Aktualisieren
            self.schuetze_model.update_schuetze(self.editing_index, name, vorname, klasse, verein)
            messagebox.showinfo("Erfolg", f"{vorname} {name} wurde aktualisiert!")
            self.editing_index = None
            self.add_button.config(text="Schütze hinzufügen")
        else:
            # Neu hinzufügen
            self.schuetze_model.add_schuetze(name, vorname, klasse, verein)
            messagebox.showinfo("Erfolg", f"{vorname} {name} wurde hinzugefügt!")
        
        self.clear_entries()
        self.refresh()
        
        # Callback aufrufen um Ergebniseingabe zu aktualisieren
        if self.on_schuetzen_changed:
            self.on_schuetzen_changed()
    
    def edit_selected(self):
        """Lädt den ausgewählten Schützen zum Bearbeiten"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return
        
        item = selected[0]
        values = self.tree.item(item)['values']
        
        # Index finden
        schuetzen = self.schuetze_model.get_all_schuetzen()
        for i, schuetze in enumerate(schuetzen):
            if (schuetze['name'] == values[0] and 
                schuetze['vorname'] == values[1] and 
                schuetze['klasse'] == values[2] and 
                schuetze['verein'] == values[3]):
                self.editing_index = i
                break
        
        # Felder füllen
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.vorname_entry.delete(0, tk.END)
        self.vorname_entry.insert(0, values[1])
        self.klasse_combo.set(values[2])
        self.verein_entry.delete(0, tk.END)
        self.verein_entry.insert(0, values[3])
        self.add_button.config(text="Schütze aktualisieren")
    
    def delete_selected(self):
        """Löscht den ausgewählten Schützen"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return
        
        if messagebox.askyesno(
            "Bestätigung", 
            "Möchten Sie den ausgewählten Schützen wirklich löschen?"
        ):
            item = selected[0]
            values = self.tree.item(item)['values']
            
            # Index finden und löschen
            schuetzen = self.schuetze_model.get_all_schuetzen()
            for i, schuetze in enumerate(schuetzen):
                if (schuetze['name'] == values[0] and 
                    schuetze['vorname'] == values[1] and 
                    schuetze['klasse'] == values[2] and 
                    schuetze['verein'] == values[3]):
                    self.schuetze_model.remove_schuetze(i)
                    break
            
            self.clear_entries()
            self.refresh()
            messagebox.showinfo("Erfolg", "Schütze wurde gelöscht!")
            
            # Callback aufrufen um Ergebniseingabe zu aktualisieren
            if self.on_schuetzen_changed:
                self.on_schuetzen_changed()
    
    def delete_all(self):
        """Löscht alle Schützen"""
        if not self.schuetze_model.get_all_schuetzen():
            messagebox.showinfo("Info", "Es sind keine Schützen vorhanden!")
            return
        
        if messagebox.askyesno(
            "Bestätigung", 
            "Möchten Sie wirklich ALLE Schützen löschen?"
        ):
            self.schuetze_model.clear_schuetzen()
            self.refresh()
            messagebox.showinfo("Erfolg", "Alle Schützen wurden gelöscht!")
            
            # Callback aufrufen um Ergebniseingabe zu aktualisieren
            if self.on_schuetzen_changed:
                self.on_schuetzen_changed()
    
    def clear_entries(self):
        """Löscht alle Eingabefelder"""
        self.name_entry.delete(0, tk.END)
        self.vorname_entry.delete(0, tk.END)
        self.verein_entry.delete(0, tk.END)
        klassen = self.turnier_model.get_klassen()
        if klassen:
            self.klasse_combo.current(0)
        self.editing_index = None
        self.add_button.config(text="Schütze hinzufügen")
    
    def refresh(self):
        """Aktualisiert die Anzeige"""
        # Klassen-Combobox aktualisieren
        klassen = self.turnier_model.get_klassen()
        self.klasse_combo['values'] = klassen
        if klassen and not self.klasse_combo.get():
            self.klasse_combo.current(0)
        
        # Tree aktualisieren
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Schützen holen und sortieren
        schuetzen = self.schuetze_model.get_all_schuetzen()
        
        if self.sort_column:
            # Mapping der Spaltennamen zu Dictionary-Keys
            column_map = {
                "Name": "name",
                "Vorname": "vorname",
                "Klasse": "klasse",
                "Verein": "verein"
            }
            sort_key = column_map.get(self.sort_column, "name")
            schuetzen = sorted(schuetzen, key=lambda x: x[sort_key].lower(), reverse=self.sort_reverse)
        
        for schuetze in schuetzen:
            self.tree.insert("", tk.END, values=(
                schuetze['name'], 
                schuetze['vorname'], 
                schuetze['klasse'], 
                schuetze['verein']
            ))
    
    def refresh_silent(self):
        """Aktualisiert die Anzeige ohne Sortierung zurückzusetzen (für Callback)"""
        self.refresh()
