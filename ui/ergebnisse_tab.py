# -*- coding: utf-8 -*-
"""
Ergebniseingabe Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.schuetze import SchuetzeModel
from utils.pdf_generator import PDFGenerator


class ErgebnisseTab:
    """Tab für Ergebniseingabe"""
    
    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.selected_schuetze_index = None
        self.sort_column = None
        self.sort_reverse = False
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame, 
            text="Ergebniseingabe", 
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Linker Bereich - Schützenliste
        left_frame = ttk.Frame(self.frame)
        left_frame.grid(row=1, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 5))
        
        # Suchfeld
        search_frame = ttk.LabelFrame(left_frame, text="Schütze suchen", padding="5")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(fill=tk.X, padx=5, pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_schuetzen)
        
        ttk.Label(
            search_frame, 
            text="Filter nach Name, Vorname oder Klasse", 
            font=("Arial", 8), 
            foreground="gray"
        ).pack()
        
        # Schützenliste
        list_frame = ttk.LabelFrame(left_frame, text="Schützenliste", padding="5")
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hinweis zur Sortierung
        ttk.Label(
            list_frame, 
            text="💡 Spaltenüberschrift zum Sortieren klicken", 
            font=("Arial", 8), 
            foreground="gray"
        ).pack(pady=(0, 5))
        
        list_scrollbar = ttk.Scrollbar(list_frame)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.schuetzen_tree = ttk.Treeview(
            list_frame, 
            columns=("Name", "Vorname", "Klasse", "Gesamt"), 
            show="headings", 
            yscrollcommand=list_scrollbar.set, 
            height=20
        )
        self.schuetzen_tree.heading("Name", text="Name", command=lambda: self.sort_by_column("Name"))
        self.schuetzen_tree.heading("Vorname", text="Vorname", command=lambda: self.sort_by_column("Vorname"))
        self.schuetzen_tree.heading("Klasse", text="Klasse", command=lambda: self.sort_by_column("Klasse"))
        self.schuetzen_tree.heading("Gesamt", text="Gesamt", command=lambda: self.sort_by_column("Gesamt"))
        self.schuetzen_tree.column("Name", width=120)
        self.schuetzen_tree.column("Vorname", width=120)
        self.schuetzen_tree.column("Klasse", width=100)
        self.schuetzen_tree.column("Gesamt", width=80)
        self.schuetzen_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        list_scrollbar.config(command=self.schuetzen_tree.yview)
        self.schuetzen_tree.bind("<<TreeviewSelect>>", self.on_schuetze_selected)
        self.schuetzen_tree.bind("<Double-1>", lambda e: self.load_ergebnisse())
        
        # Rechter Bereich - Eingabe
        right_frame = ttk.Frame(self.frame)
        right_frame.grid(row=1, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(5, 0))
        
        self.info_label = ttk.Label(
            right_frame, 
            text="Bitte wählen Sie einen Schützen aus", 
            font=("Arial", 11, "bold")
        )
        self.info_label.pack(pady=10)
        
        # Scrollbarer Bereich für Passen
        eingabe_container = ttk.LabelFrame(right_frame, text="Ergebnisse", padding="10")
        eingabe_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        eingabe_canvas = tk.Canvas(eingabe_container, height=200)
        eingabe_scrollbar = ttk.Scrollbar(
            eingabe_container, 
            orient="vertical", 
            command=eingabe_canvas.yview
        )
        self.eingabe_frame = ttk.Frame(eingabe_canvas)
        
        self.eingabe_frame.bind(
            "<Configure>", 
            lambda e: eingabe_canvas.configure(scrollregion=eingabe_canvas.bbox("all"))
        )
        
        eingabe_canvas.create_window((0, 0), window=self.eingabe_frame, anchor="nw")
        eingabe_canvas.configure(yscrollcommand=eingabe_scrollbar.set)
        
        eingabe_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        eingabe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.passen_entries = []
        self.create_passen_fields()
        
        # Zusatzwertung
        zusatz_frame = ttk.LabelFrame(right_frame, text="Zusatzwertung", padding="10")
        zusatz_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(zusatz_frame, text="Anzahl 10er:").grid(
            row=0, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.anzahl_10er_entry = ttk.Entry(zusatz_frame, width=15)
        self.anzahl_10er_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        self.anzahl_10er_entry.insert(0, "0")
        
        ttk.Label(zusatz_frame, text="Anzahl 9er:").grid(
            row=1, column=0, sticky=tk.W, pady=5, padx=5
        )
        self.anzahl_9er_entry = ttk.Entry(zusatz_frame, width=15)
        self.anzahl_9er_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        self.anzahl_9er_entry.insert(0, "0")
        
        # Gesamtergebnis
        ergebnis_frame = ttk.Frame(right_frame)
        ergebnis_frame.pack(pady=10)
        
        ttk.Label(
            ergebnis_frame, 
            text="Gesamtergebnis:", 
            font=("Arial", 12, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        self.gesamt_label = ttk.Label(
            ergebnis_frame, 
            text="0", 
            font=("Arial", 12, "bold")
        )
        self.gesamt_label.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame, 
            text="Ergebnisse speichern", 
            command=self.save_ergebnisse
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        ttk.Button(
            button_frame, 
            text="Ergebnisanzeige", 
            command=self.show_ergebnisanzeige
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        ttk.Button(
            button_frame, 
            text="🖥 Bildschirmanzeige", 
            command=self.show_bildschirmanzeige
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Grid-Konfiguration
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        self.refresh()
    
    def sort_by_column(self, column):
        """Sortiert die Tabelle nach der angegebenen Spalte"""
        # Wenn die gleiche Spalte nochmal geklickt wird, Sortierreihenfolge umkehren
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        self.update_schuetzen_tree(self.search_entry.get())
    
    def create_passen_fields(self):
        """Erstellt Eingabefelder für Passen"""
        for widget in self.eingabe_frame.winfo_children():
            widget.destroy()
        
        self.passen_entries = []
        turnier = self.turnier_model.get_turnier_data()
        anzahl_passen = turnier.get("anzahl_passen", 1)
        
        for i in range(anzahl_passen):
            ttk.Label(self.eingabe_frame, text=f"Passe {i+1}:").grid(
                row=i, column=0, sticky=tk.W, pady=5
            )
            entry = ttk.Entry(self.eingabe_frame, width=20)
            entry.grid(row=i, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
            entry.bind("<KeyRelease>", self.calculate_gesamt)
            self.passen_entries.append(entry)
    
    def update_schuetzen_tree(self, filter_text=""):
        """Aktualisiert die Schützenliste"""
        for item in self.schuetzen_tree.get_children():
            self.schuetzen_tree.delete(item)
        
        filter_text = filter_text.lower()
        
        # Schützen holen und filtern
        schuetzen_list = []
        for schuetze in self.schuetze_model.get_all_schuetzen():
            if filter_text:
                if (filter_text not in schuetze['name'].lower() and
                    filter_text not in schuetze['vorname'].lower() and
                    filter_text not in schuetze['klasse'].lower()):
                    continue
            
            schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
            gesamt = 0
            gesamt_str = ""
            ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            if ergebnis:
                passen = ergebnis.get('passen', [])
                gesamt = sum(passen)
                gesamt_str = f"{gesamt:.1f}"
            
            schuetzen_list.append({
                'name': schuetze['name'],
                'vorname': schuetze['vorname'],
                'klasse': schuetze['klasse'],
                'gesamt': gesamt,
                'gesamt_str': gesamt_str
            })
        
        # Sortieren wenn eine Spalte ausgewählt ist
        if self.sort_column:
            column_map = {
                "Name": "name",
                "Vorname": "vorname",
                "Klasse": "klasse",
                "Gesamt": "gesamt"
            }
            sort_key = column_map.get(self.sort_column, "name")
            
            if sort_key == "gesamt":
                # Numerische Sortierung für Gesamt
                schuetzen_list = sorted(schuetzen_list, key=lambda x: x[sort_key], reverse=self.sort_reverse)
            else:
                # Alphabetische Sortierung für Text
                schuetzen_list = sorted(schuetzen_list, key=lambda x: x[sort_key].lower(), reverse=self.sort_reverse)
        
        # In Tree einfügen
        for schuetze in schuetzen_list:
            self.schuetzen_tree.insert("", tk.END, values=(
                schuetze['name'], 
                schuetze['vorname'], 
                schuetze['klasse'], 
                schuetze['gesamt_str']
            ))
    
    def filter_schuetzen(self, event=None):
        """Filtert die Schützenliste"""
        filter_text = self.search_entry.get()
        self.update_schuetzen_tree(filter_text)
    
    def on_schuetze_selected(self, event):
        """Wird aufgerufen wenn ein Schütze ausgewählt wird"""
        selection = self.schuetzen_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.schuetzen_tree.item(item)['values']
        
        # Index finden
        schuetzen = self.schuetze_model.get_all_schuetzen()
        for i, schuetze in enumerate(schuetzen):
            if (schuetze['name'] == values[0] and 
                schuetze['vorname'] == values[1] and 
                schuetze['klasse'] == values[2]):
                self.selected_schuetze_index = i
                self.info_label.config(
                    text=f"Ausgewählt: {schuetze['vorname']} {schuetze['name']} ({schuetze['klasse']})"
                )
                break
    
    def load_ergebnisse(self):
        """Lädt die Ergebnisse des ausgewählten Schützen"""
        if self.selected_schuetze_index is None:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return
        
        schuetze = self.schuetze_model.get_schuetze(self.selected_schuetze_index)
        schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
        
        # Felder leeren
        for entry in self.passen_entries:
            entry.delete(0, tk.END)
        
        self.anzahl_10er_entry.delete(0, tk.END)
        self.anzahl_10er_entry.insert(0, "0")
        self.anzahl_9er_entry.delete(0, tk.END)
        self.anzahl_9er_entry.insert(0, "0")
        
        # Ergebnisse laden
        ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
        if ergebnis:
            passen = ergebnis.get('passen', [])
            anzahl_10er = ergebnis.get('anzahl_10er', 0)
            anzahl_9er = ergebnis.get('anzahl_9er', 0)
            
            for i, entry in enumerate(self.passen_entries):
                if i < len(passen):
                    entry.insert(0, str(passen[i]))
            
            self.anzahl_10er_entry.delete(0, tk.END)
            self.anzahl_10er_entry.insert(0, str(anzahl_10er))
            self.anzahl_9er_entry.delete(0, tk.END)
            self.anzahl_9er_entry.insert(0, str(anzahl_9er))
        
        self.calculate_gesamt()
    
    def calculate_gesamt(self, event=None):
        """Berechnet das Gesamtergebnis"""
        gesamt = 0
        for entry in self.passen_entries:
            try:
                wert = entry.get().strip()
                if wert:
                    gesamt += float(wert)
            except ValueError:
                pass
        self.gesamt_label.config(text=f"{gesamt:.1f}")
    
    def save_ergebnisse(self):
        """Speichert die Ergebnisse"""
        if self.selected_schuetze_index is None:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus!")
            return
        
        schuetze = self.schuetze_model.get_schuetze(self.selected_schuetze_index)
        schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
        
        # Passen-Ergebnisse sammeln
        ergebnisse = []
        for entry in self.passen_entries:
            try:
                wert = entry.get().strip()
                ergebnisse.append(float(wert) if wert else 0)
            except ValueError:
                messagebox.showwarning("Eingabefehler", "Bitte nur Zahlen eingeben!")
                return
        
        # Zusatzwertung
        try:
            anzahl_10er = int(self.anzahl_10er_entry.get().strip() or 0)
            anzahl_9er = int(self.anzahl_9er_entry.get().strip() or 0)
        except ValueError:
            messagebox.showwarning(
                "Eingabefehler", 
                "Bitte nur ganze Zahlen für 10er und 9er eingeben!"
            )
            return
        
        self.turnier_model.add_ergebnis(schuetze_id, ergebnisse, anzahl_10er, anzahl_9er)
        self.update_schuetzen_tree(self.search_entry.get())
        messagebox.showinfo(
            "Erfolg", 
            f"Ergebnisse für {schuetze['vorname']} {schuetze['name']} wurden gespeichert!"
        )
    
    def show_ergebnisanzeige(self):
        """Zeigt das Ergebnisfenster"""
        if not self.turnier_model.get_all_ergebnisse():
            messagebox.showinfo("Keine Ergebnisse", "Es sind noch keine Ergebnisse vorhanden!")
            return
        
        from .ergebnisse_window import ErgebnisWindow
        ErgebnisWindow(self.frame, self.turnier_model, self.schuetze_model)
    
    def show_bildschirmanzeige(self):
        """Zeigt die Bildschirmanzeige für externe Monitore"""
        if not self.turnier_model.get_all_ergebnisse():
            messagebox.showinfo("Keine Ergebnisse", "Es sind noch keine Ergebnisse vorhanden!")
            return
        
        from .bildschirm_anzeige_window import BildschirmAnzeigeWindow
        BildschirmAnzeigeWindow(self.frame, self.turnier_model, self.schuetze_model)
    
    def refresh(self):
        """Aktualisiert die Anzeige"""
        self.create_passen_fields()
        self.update_schuetzen_tree()
        self.selected_schuetze_index = None
        self.info_label.config(text="Bitte wählen Sie einen Schützen aus")
