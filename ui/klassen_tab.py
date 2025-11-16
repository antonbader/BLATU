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
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set, 
            height=20, 
            font=("Arial", 11)
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
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
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Klasse aus!")
            return
        
        klasse = self.listbox.get(selection[0])
        
        # Prüfen ob Schützen in dieser Klasse sind
        count = self.schuetze_model.count_schuetzen_by_klasse(klasse)
        if count > 0:
            if not messagebox.askyesno(
                "Warnung", 
                f"Es gibt {count} Schütze(n) in dieser Klasse.\n"
                f"Möchten Sie die Klasse trotzdem löschen?"
            ):
                return
        
        self.turnier_model.remove_klasse(klasse)
        self.refresh()
        messagebox.showinfo("Erfolg", f"Klasse '{klasse}' wurde gelöscht!")
        
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
        self.listbox.delete(0, tk.END)
        for klasse in self.turnier_model.get_klassen():
            self.listbox.insert(tk.END, klasse)
