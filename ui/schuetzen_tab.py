# -*- coding: utf-8 -*-
"""
Schützenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random


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
        
        # Name und Vorname
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Vorname:").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.vorname_entry = ttk.Entry(input_frame, width=30)
        self.vorname_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=5, padx=5)

        # Klasse und Verein
        ttk.Label(input_frame, text="Klasse:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.klasse_combo = ttk.Combobox(input_frame, width=28, state="readonly")
        self.klasse_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(input_frame, text="Verein:").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        self.verein_entry = ttk.Entry(input_frame, width=30)
        self.verein_entry.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=5, padx=5)

        # PIN Bearbeitung
        ttk.Label(input_frame, text="PIN:").grid(row=2, column=0, sticky=tk.W, pady=5)
        pin_frame = ttk.Frame(input_frame)
        pin_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        self.pin_entry = ttk.Entry(pin_frame, width=10)
        self.pin_entry.pack(side=tk.LEFT)

        self.gen_pin_button = ttk.Button(
            pin_frame,
            text="Generieren",
            command=self.generate_random_pin,
            width=10
        )
        self.gen_pin_button.pack(side=tk.LEFT, padx=5)

        # Button
        self.add_button = ttk.Button(
            input_frame,
            text="Schütze hinzufügen",
            command=self.add_or_update_schuetze
        )
        self.add_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Grid-Konfiguration für Input-Frame
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        
        # Listenbereich
        list_frame = ttk.LabelFrame(self.frame, text="Schützenliste", padding="10")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Scheiben- und Zuweisungs-Frame
        scheiben_frame = ttk.Frame(list_frame)
        scheiben_frame.pack(fill=tk.X, pady=5)

        ttk.Label(scheiben_frame, text="Max. Scheiben:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_scheiben_var = tk.IntVar(value=self.turnier_model.get_turnier_data().get("max_scheiben", 3))
        self.max_scheiben_entry = ttk.Entry(scheiben_frame, textvariable=self.max_scheiben_var, width=5)
        self.max_scheiben_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(scheiben_frame, text="Zuweisungsart:").pack(side=tk.LEFT, padx=(10, 5))
        self.assign_strategy_var = tk.StringVar(value="Nach Eingabe")
        self.assign_strategy_combo = ttk.Combobox(
            scheiben_frame,
            textvariable=self.assign_strategy_var,
            values=["Nach Eingabe", "Zufällig", "Nach Klassen"],
            width=15,
            state="readonly"
        )
        self.assign_strategy_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            scheiben_frame,
            text="Automatisch Zuweisen",
            command=self.auto_assign_scheiben
        ).pack(side=tk.LEFT, padx=5)

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
            columns=("Name", "Vorname", "Klasse", "Verein", "Gruppe", "Scheibe", "PIN"),
            show="headings", 
            yscrollcommand=scrollbar.set, 
            height=15
        )
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by_column("Name"))
        self.tree.heading("Vorname", text="Vorname", command=lambda: self.sort_by_column("Vorname"))
        self.tree.heading("Klasse", text="Klasse", command=lambda: self.sort_by_column("Klasse"))
        self.tree.heading("Verein", text="Verein", command=lambda: self.sort_by_column("Verein"))
        self.tree.heading("Gruppe", text="Gruppe", command=lambda: self.sort_by_column("Gruppe"))
        self.tree.heading("Scheibe", text="Scheibe", command=lambda: self.sort_by_column("Scheibe"))
        self.tree.heading("PIN", text="PIN", command=lambda: self.sort_by_column("PIN"))
        self.tree.column("Name", width=150)
        self.tree.column("Vorname", width=150)
        self.tree.column("Klasse", width=120)
        self.tree.column("Verein", width=150)
        self.tree.column("Gruppe", width=70, anchor="center")
        self.tree.column("Scheibe", width=70, anchor="center")
        self.tree.column("PIN", width=70, anchor="center")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())
        
        # Manuelle Zuweisung
        manual_assign_frame = ttk.LabelFrame(self.frame, text="Manuelle Zuweisung", padding="10")
        manual_assign_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        ttk.Label(manual_assign_frame, text="Gruppe:").grid(row=0, column=0, padx=5)
        self.manual_gruppe_var = tk.StringVar()
        self.manual_gruppe_entry = ttk.Entry(manual_assign_frame, textvariable=self.manual_gruppe_var, width=5)
        self.manual_gruppe_entry.grid(row=0, column=1, padx=5)

        ttk.Label(manual_assign_frame, text="Scheibe:").grid(row=0, column=2, padx=5)
        self.manual_scheibe_var = tk.StringVar()
        self.manual_scheibe_entry = ttk.Entry(manual_assign_frame, textvariable=self.manual_scheibe_var, width=5)
        self.manual_scheibe_entry.grid(row=0, column=3, padx=5)

        ttk.Button(
            manual_assign_frame,
            text="Ausgewählten Schützen zuweisen",
            command=self.manual_assign
        ).grid(row=0, column=4, padx=10)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
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
        pin = self.pin_entry.get().strip()

        # Wenn PIN leer ist, None übergeben (dann wird sie im Model generiert/behalten)
        if not pin:
            pin = None
        
        if not name or not vorname or not klasse:
            messagebox.showwarning(
                "Eingabefehler", 
                "Bitte Name, Vorname und Klasse ausfüllen!"
            )
            return
        
        if self.editing_index is not None:
            # Aktualisieren
            schuetze = self.schuetze_model.get_schuetze(self.editing_index)
            self.schuetze_model.update_schuetze(
                self.editing_index, name, vorname, klasse, verein,
                gruppe=schuetze.get('gruppe'), scheibe=schuetze.get('scheibe'),
                pin=pin
            )
            messagebox.showinfo("Erfolg", f"{vorname} {name} wurde aktualisiert!")
            self.editing_index = None
            self.add_button.config(text="Schütze hinzufügen")
        else:
            # Neu hinzufügen
            self.schuetze_model.add_schuetze(name, vorname, klasse, verein, pin=pin)
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
        current_schuetze = None
        for i, schuetze in enumerate(schuetzen):
            if (schuetze['name'] == values[0] and 
                schuetze['vorname'] == values[1] and 
                schuetze['klasse'] == values[2] and 
                schuetze['verein'] == values[3]):
                self.editing_index = i
                current_schuetze = schuetze

                # Manuelle Zuweisungsfelder füllen
                self.manual_gruppe_var.set(schuetze.get('gruppe', ''))
                self.manual_scheibe_var.set(schuetze.get('scheibe', ''))
                break
        
        # Felder füllen
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[0])
        self.vorname_entry.delete(0, tk.END)
        self.vorname_entry.insert(0, values[1])
        self.klasse_combo.set(values[2])
        self.verein_entry.delete(0, tk.END)
        self.verein_entry.insert(0, values[3])

        self.pin_entry.delete(0, tk.END)
        if current_schuetze and 'pin' in current_schuetze:
            self.pin_entry.insert(0, current_schuetze['pin'])

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
        self.pin_entry.delete(0, tk.END)
        klassen = self.turnier_model.get_klassen_names()
        if klassen:
            self.klasse_combo.current(0)
        self.editing_index = None
        self.add_button.config(text="Schütze hinzufügen")
    
    def generate_random_pin(self):
        """Generiert eine zufällige PIN und trägt sie in das Feld ein"""
        pin = f"{random.randint(0, 9999):04d}"
        self.pin_entry.delete(0, tk.END)
        self.pin_entry.insert(0, pin)

    def refresh(self):
        """Aktualisiert die Anzeige"""
        # Klassen-Combobox aktualisieren
        klassen = self.turnier_model.get_klassen_names()
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
                "Verein": "verein",
                "Gruppe": "gruppe",
                "Scheibe": "scheibe",
                "PIN": "pin"
            }
            sort_key = column_map.get(self.sort_column, "name")

            def sort_func(x):
                val = x.get(sort_key)
                if val is None:
                    return -1 # None-Werte an den Anfang
                if isinstance(val, str):
                    return val.lower()
                return val

            schuetzen = sorted(schuetzen, key=sort_func, reverse=self.sort_reverse)

        for schuetze in schuetzen:
            self.tree.insert("", tk.END, values=(
                schuetze.get('name', ''),
                schuetze.get('vorname', ''),
                schuetze.get('klasse', ''),
                schuetze.get('verein', ''),
                schuetze.get('gruppe', ''),
                schuetze.get('scheibe', ''),
                schuetze.get('pin', '')
            ))
    
    def refresh_silent(self):
        """Aktualisiert die Anzeige ohne Sortierung zurückzusetzen (für Callback)"""
        self.refresh()

    def auto_assign_scheiben(self):
        """Automatische Zuweisung von Gruppen und Scheiben"""
        try:
            max_scheiben = self.max_scheiben_var.get()
            if max_scheiben <= 0:
                messagebox.showerror("Fehler", "Maximale Anzahl an Scheiben muss größer als 0 sein.")
                return

            schuetzen = self.schuetze_model.get_all_schuetzen()
            if not schuetzen:
                messagebox.showinfo("Info", "Keine Schützen zum Zuweisen vorhanden.")
                return

            # Zuweisungsstrategie anwenden
            strategy = self.assign_strategy_var.get()
            if strategy == "Zufällig":
                random.shuffle(schuetzen)
            elif strategy == "Nach Klassen":
                schuetzen.sort(key=lambda s: s.get('klasse', ''))

            # Bestehende Zuweisungen aufheben und neu zuweisen
            gruppe = 1
            scheibe = 1

            # Da die Reihenfolge potenziell geändert wurde, müssen wir die Schützen über ihre eindeutige ID aktualisieren
            all_schuetzen_original = self.schuetze_model.get_all_schuetzen()

            # Zuerst alle Zuweisungen aufheben
            for i in range(len(all_schuetzen_original)):
                s = self.schuetze_model.get_schuetze(i)
                self.schuetze_model.update_schuetze(i, s['name'], s['vorname'], s['klasse'], s['verein'], gruppe=None, scheibe=None)

            # Dann die neuen Zuweisungen basierend auf der sortierten/gemischten Liste setzen
            for schuetze_sorted in schuetzen:
                # Finde den Index des Schützen in der ursprünglichen Liste, um ihn zu aktualisieren
                for i, s_orig in enumerate(all_schuetzen_original):
                    if (s_orig['name'] == schuetze_sorted['name'] and
                        s_orig['vorname'] == schuetze_sorted['vorname'] and
                        s_orig['klasse'] == schuetze_sorted['klasse']):

                        self.schuetze_model.update_schuetze(
                            i, s_orig['name'], s_orig['vorname'], s_orig['klasse'], s_orig['verein'],
                            gruppe=gruppe, scheibe=scheibe
                        )
                        break

                scheibe += 1
                if scheibe > max_scheiben:
                    scheibe = 1
                    gruppe += 1

            self.refresh()
            messagebox.showinfo("Erfolg", "Schützen wurden automatisch zugewiesen.")

            # Callback aufrufen, um andere Tabs zu aktualisieren
            if self.on_schuetzen_changed:
                self.on_schuetzen_changed()

        except tk.TclError:
            messagebox.showerror("Fehler", "Ungültiger Wert für maximale Scheiben.")

    def manual_assign(self):
        """Manuelle Zuweisung von Gruppe und Scheibe"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return

        try:
            gruppe = int(self.manual_gruppe_var.get())
            scheibe = int(self.manual_scheibe_var.get())
        except ValueError:
            messagebox.showerror("Fehler", "Gruppe und Scheibe müssen Zahlen sein.")
            return

        # Prüfung auf Doppelbelegung
        schuetzen = self.schuetze_model.get_all_schuetzen()
        for i, s in enumerate(schuetzen):
            if s.get('gruppe') == gruppe and s.get('scheibe') == scheibe:
                if i != self.editing_index:
                    messagebox.showerror("Fehler", f"Scheibe {scheibe} in Gruppe {gruppe} ist bereits belegt.")
                    return

        # Index des ausgewählten Schützen finden
        item = selected[0]
        values = self.tree.item(item)['values']
        schuetzen = self.schuetze_model.get_all_schuetzen()
        selected_index = -1
        for i, schuetze in enumerate(schuetzen):
            if (schuetze['name'] == values[0] and
                schuetze['vorname'] == values[1] and
                schuetze['klasse'] == values[2] and
                schuetze['verein'] == values[3]):
                selected_index = i
                break

        if selected_index != -1:
            schuetze = self.schuetze_model.get_schuetze(selected_index)
            self.schuetze_model.update_schuetze(
                selected_index,
                schuetze['name'],
                schuetze['vorname'],
                schuetze['klasse'],
                schuetze['verein'],
                gruppe=gruppe,
                scheibe=scheibe
            )
            self.refresh()
            messagebox.showinfo("Erfolg", "Zuweisung erfolgreich.")

            if self.on_schuetzen_changed:
                self.on_schuetzen_changed()