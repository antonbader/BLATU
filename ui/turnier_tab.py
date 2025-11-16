# -*- coding: utf-8 -*-
"""
Turnierverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import MIN_PASSEN, MAX_PASSEN


class TurnierTab:
    """Tab für Turnierverwaltung"""
    
    def __init__(self, parent, turnier_model, on_change_callback):
        self.turnier_model = turnier_model
        self.on_change_callback = on_change_callback
        self.on_turnier_data_changed_callback = None
        self.frame = ttk.Frame(parent, padding="20")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame, 
            text="Turniereinstellungen", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Eingabebereich
        input_frame = ttk.LabelFrame(self.frame, text="Turnierdaten", padding="20")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Name
        ttk.Label(input_frame, text="Name des Turniers:", font=("Arial", 10)).grid(
            row=0, column=0, sticky=tk.W, pady=10
        )
        self.name_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=10, padx=10)
        
        # Datum
        ttk.Label(input_frame, text="Datum:", font=("Arial", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=10
        )
        self.datum_entry = ttk.Entry(input_frame, width=50, font=("Arial", 10))
        self.datum_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=10, padx=10)
        ttk.Label(
            input_frame, 
            text="(z.B. 15.10.2024)", 
            font=("Arial", 9), 
            foreground="gray"
        ).grid(row=2, column=1, sticky=tk.W, padx=10)
        
        # Anzahl Passen
        ttk.Label(input_frame, text="Anzahl Passen:", font=("Arial", 10)).grid(
            row=3, column=0, sticky=tk.W, pady=10
        )
        self.passen_spinbox = ttk.Spinbox(
            input_frame, 
            from_=MIN_PASSEN, 
            to=MAX_PASSEN, 
            width=48, 
            font=("Arial", 10)
        )
        self.passen_spinbox.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=10, padx=10)
        self.passen_spinbox.set(1)
        
        # Checkbox für Hälfte-Ansicht
        self.show_halves_var = tk.BooleanVar(value=False)
        self.show_halves_check = ttk.Checkbutton(
            input_frame,
            text="Ergebnisse als 1. und 2. Hälfte anzeigen (statt einzelne Passen)",
            variable=self.show_halves_var,
            command=self.on_halves_changed
        )
        self.show_halves_check.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)
        
        ttk.Label(
            input_frame,
            text="Hinweis: Bei ungerader Passenanzahl ist diese Option nicht verfügbar",
            font=("Arial", 9),
            foreground="gray"
        ).grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame, 
            text="Einstellungen speichern", 
            command=self.save_settings
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Zurücksetzen", 
            command=self.reset_settings
        ).pack(side=tk.LEFT, padx=5)
        
        # Info-Bereich
        info_frame = ttk.LabelFrame(self.frame, text="Aktuelle Einstellungen", padding="20")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=20)
        
        self.info_label = ttk.Label(
            info_frame, 
            text="", 
            font=("Arial", 11), 
            justify=tk.LEFT
        )
        self.info_label.pack(anchor=tk.W)
        
        # Grid-Konfiguration
        input_frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        
        self.refresh()
    
    def on_halves_changed(self):
        """Wird aufgerufen wenn die Checkbox geändert wird"""
        try:
            passen = int(self.passen_spinbox.get())
            if self.show_halves_var.get() and passen % 2 != 0:
                messagebox.showwarning(
                    "Ungerade Passenanzahl",
                    f"Die Hälfte-Ansicht ist nur bei gerader Passenanzahl möglich.\n"
                    f"Aktuelle Anzahl: {passen} Passen (ungerade)\n\n"
                    f"Bitte wählen Sie eine gerade Anzahl Passen."
                )
                self.show_halves_var.set(False)
        except ValueError:
            pass
    
    def save_settings(self):
        """Speichert die Turniereinstellungen"""
        name = self.name_entry.get().strip()
        datum = self.datum_entry.get().strip()
        
        try:
            passen = int(self.passen_spinbox.get())
            if passen < MIN_PASSEN or passen > MAX_PASSEN:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Eingabefehler", 
                f"Bitte eine gültige Anzahl Passen eingeben ({MIN_PASSEN}-{MAX_PASSEN})!"
            )
            return
        
        if not name:
            messagebox.showwarning("Eingabefehler", "Bitte einen Turniernamen eingeben!")
            return
        
        # Prüfen ob Hälfte-Ansicht mit ungerader Passenanzahl kombiniert wird
        show_halves = self.show_halves_var.get()
        if show_halves and passen % 2 != 0:
            messagebox.showwarning(
                "Ungerade Passenanzahl",
                f"Die Hälfte-Ansicht ist nur bei gerader Passenanzahl möglich.\n"
                f"Aktuelle Anzahl: {passen} Passen (ungerade)\n\n"
                f"Bitte wählen Sie eine gerade Anzahl Passen oder deaktivieren Sie die Hälfte-Ansicht."
            )
            return
        
        self.turnier_model.set_turnier_data(name, datum, passen, show_halves)
        self.update_info()
        self.on_change_callback()
        if self.on_turnier_data_changed_callback:
            self.on_turnier_data_changed_callback()
        messagebox.showinfo("Erfolg", "Turniereinstellungen wurden gespeichert!")
    
    def reset_settings(self):
        """Setzt die Turniereinstellungen zurück"""
        if messagebox.askyesno(
            "Bestätigung", 
            "Möchten Sie die Turniereinstellungen wirklich zurücksetzen?"
        ):
            self.turnier_model.set_turnier_data("", "", 1, False)
            self.refresh()
            if self.on_turnier_data_changed_callback:
                self.on_turnier_data_changed_callback()
            messagebox.showinfo("Erfolg", "Turniereinstellungen wurden zurückgesetzt!")
    
    def refresh(self):
        """Aktualisiert die Anzeige"""
        turnier = self.turnier_model.get_turnier_data()
        
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, turnier.get("name", ""))
        
        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, turnier.get("datum", ""))
        
        self.passen_spinbox.set(turnier.get("anzahl_passen", 1))
        self.show_halves_var.set(turnier.get("show_halves", False))
        
        self.update_info()
    
    def update_info(self):
        """Aktualisiert den Info-Text"""
        turnier = self.turnier_model.get_turnier_data()
        
        if turnier["name"]:
            info_text = f"Turnier: {turnier['name']}\n"
            if turnier['datum']:
                info_text += f"Datum: {turnier['datum']}\n"
            info_text += f"Anzahl Passen: {turnier['anzahl_passen']}\n"
            if turnier.get('show_halves', False):
                info_text += "Anzeige: 1. und 2. Hälfte"
            else:
                info_text += "Anzeige: Einzelne Passen"
        else:
            info_text = "Noch keine Turniereinstellungen vorhanden."
        
        self.info_label.config(text=info_text)
