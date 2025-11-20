# -*- coding: utf-8 -*-
"""
Ergebnisanzeige-Fenster
"""

import tkinter as tk
from tkinter import ttk

from models.schuetze import SchuetzeModel
from utils.pdf_generator import PDFGenerator


class ErgebnisWindow:
    """Fenster zur Anzeige der Ergebnisse"""
    
    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.window = tk.Toplevel(parent)
        self.window.title("Ergebnisanzeige")
        self.window.geometry("1000x700")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        # Buttons unten (immer sichtbar)
        button_frame = ttk.Frame(self.window)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame, 
            text="PDF erstellen", 
            command=self.create_pdf
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame, 
            text="Schließen", 
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=10)
        
        # Haupt-Frame mit Scrollbars
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas mit vertikaler UND horizontaler Scrollbar
        canvas = tk.Canvas(main_frame)
        v_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=canvas.xview)
        
        scrollable_frame = ttk.Frame(canvas)
        
        # Canvas-Konfiguration für beide Scrollrichtungen
        scrollable_frame.bind(
            "<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Canvas breiter machen wenn Fenster größer wird
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame, width=canvas_width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Titel
        turnier = self.turnier_model.get_turnier_data()
        title_frame = ttk.Frame(scrollable_frame)
        title_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            title_frame, 
            text=f"Ergebnisse: {turnier.get('name', 'Turnier')}", 
            font=("Arial", 16, "bold")
        ).pack()
        
        if turnier.get('datum'):
            ttk.Label(
                title_frame, 
                text=f"Datum: {turnier['datum']}", 
                font=("Arial", 11)
            ).pack(pady=5)
        
        # Hinweis bei vielen Passen
        if turnier.get('anzahl_passen', 1) > 10:
            ttk.Label(
                title_frame,
                text=f"💡 Hinweis: Verwenden Sie die horizontale Scrollbar unten zum Scrollen durch alle {turnier['anzahl_passen']} Passen",
                font=("Arial", 9),
                foreground="#0066CC"
            ).pack(pady=5)
        
        # Ergebnisse nach Klassen gruppieren
        klassen_ergebnisse = self.prepare_ergebnisse()
        
        # Für jede Klasse eine Tabelle
        for klasse in sorted(klassen_ergebnisse.keys()):
            self.create_klassen_table(scrollable_frame, klasse, klassen_ergebnisse[klasse])
        
        # Grid-Layout für Canvas und Scrollbars
        canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.E, tk.W))
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Mausrad-Unterstützung
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        def on_shift_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)
    
    def prepare_ergebnisse(self):
        """Bereitet die Ergebnisse für die Anzeige vor"""
        klassen_ergebnisse = {}
        
        for schuetze in self.schuetze_model.get_all_schuetzen():
            schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
            ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            
            if ergebnis:
                klasse = schuetze['klasse']
                if klasse not in klassen_ergebnisse:
                    klassen_ergebnisse[klasse] = []
                
                passen = ergebnis.get('passen', [])
                anzahl_10er = ergebnis.get('anzahl_10er', 0)
                anzahl_9er = ergebnis.get('anzahl_9er', 0)
                gesamt = sum(passen)
                
                klassen_ergebnisse[klasse].append({
                    'name': schuetze['name'],
                    'vorname': schuetze['vorname'],
                    'verein': schuetze.get('verein', ''),
                    'ergebnisse': passen,
                    'gesamt': gesamt,
                    'anzahl_10er': anzahl_10er,
                    'anzahl_9er': anzahl_9er
                })
        
        # Sortieren nach Gesamt, 10er, 9er
        for klasse in klassen_ergebnisse:
            klassen_ergebnisse[klasse].sort(
                key=lambda x: (x['gesamt'], x['anzahl_10er'], x['anzahl_9er']), 
                reverse=True
            )
        
        return klassen_ergebnisse
    
    def create_klassen_table(self, parent, klasse, ergebnisse):
        """Erstellt eine Tabelle für eine Klasse"""
        klassen_frame = ttk.LabelFrame(parent, text=f"Klasse: {klasse}", padding="10")
        klassen_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Turnierdaten holen
        turnier = self.turnier_model.get_turnier_data()
        anzahl_passen = turnier['anzahl_passen']
        show_halves = turnier.get('show_halves', False)
        
        # Container mit fester Mindestbreite für viele Passen
        tree_container = ttk.Frame(klassen_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)
        
        # Vertikale Scrollbar für die Tabelle
        tree_yscroll = ttk.Scrollbar(tree_container, orient="vertical")
        
        # Spalten definieren - abhängig von show_halves
        columns = ["Platz", "Name", "Vorname", "Verein"]
        if show_halves:
            columns += ["1. Hälfte", "2. Hälfte"]
        else:
            columns += [f"P{i+1}" for i in range(anzahl_passen)]
        columns += ["Gesamt", "10er", "9er"]
        
        # Treeview erstellen - KEINE horizontale Scrollbar hier!
        tree = ttk.Treeview(
            tree_container, 
            columns=columns, 
            show="headings", 
            yscrollcommand=tree_yscroll.set,
            height=min(len(ergebnisse) + 1, 15)
        )
        
        # Spalten konfigurieren - OHNE stretch=False, damit sie nebeneinander angezeigt werden
        tree.heading("Platz", text="Platz")
        tree.column("Platz", width=50, anchor=tk.CENTER)
        
        tree.heading("Name", text="Name")
        tree.column("Name", width=100)
        
        tree.heading("Vorname", text="Vorname")
        tree.column("Vorname", width=100)
        
        tree.heading("Verein", text="Verein")
        tree.column("Verein", width=120)
        
        # Passen-Spalten oder Hälfte-Spalten
        if show_halves:
            tree.heading("1. Hälfte", text="1. Hälfte")
            tree.column("1. Hälfte", width=80, anchor=tk.CENTER)
            tree.heading("2. Hälfte", text="2. Hälfte")
            tree.column("2. Hälfte", width=80, anchor=tk.CENTER)
        else:
            for i in range(anzahl_passen):
                col_name = f"P{i+1}"
                tree.heading(col_name, text=col_name)
                tree.column(col_name, width=50, anchor=tk.CENTER)
        
        tree.heading("Gesamt", text="Gesamt")
        tree.column("Gesamt", width=70, anchor=tk.CENTER)
        
        tree.heading("10er", text="10er")
        tree.column("10er", width=50, anchor=tk.CENTER)
        
        tree.heading("9er", text="9er")
        tree.column("9er", width=50, anchor=tk.CENTER)
        
        # Scrollbar konfigurieren
        tree_yscroll.config(command=tree.yview)
        
        # Pack-Layout
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Daten einfügen
        platz = 1
        prev_ergebnis = None
        
        for idx, ergebnis in enumerate(ergebnisse):
            # Platzierung mit Punktgleichstand
            if prev_ergebnis and (
                ergebnis['gesamt'] == prev_ergebnis['gesamt'] and 
                ergebnis['anzahl_10er'] == prev_ergebnis['anzahl_10er'] and 
                ergebnis['anzahl_9er'] == prev_ergebnis['anzahl_9er']
            ):
                current_platz = platz
            else:
                platz = idx + 1
                current_platz = platz
            
            werte = [
                str(current_platz), 
                ergebnis['name'], 
                ergebnis['vorname'], 
                ergebnis['verein']
            ]
            
            # Alle Passen hinzufügen oder Hälften berechnen
            if show_halves:
                # Hälften berechnen
                half = anzahl_passen // 2
                erste_haelfte = sum(ergebnis['ergebnisse'][:half])
                zweite_haelfte = sum(ergebnis['ergebnisse'][half:])
                werte.append(str(erste_haelfte))
                werte.append(str(zweite_haelfte))
            else:
                # Einzelne Passen
                for i in range(anzahl_passen):
                    if i < len(ergebnis['ergebnisse']):
                        werte.append(str(int(ergebnis['ergebnisse'][i])))
                    else:
                        werte.append("0")
            
            werte.append(str(int(ergebnis['gesamt'])))
            werte.append(str(ergebnis['anzahl_10er']))
            werte.append(str(ergebnis['anzahl_9er']))
            
            tree.insert("", tk.END, values=werte)
            prev_ergebnis = ergebnis
    
    def create_pdf(self):
        """Erstellt ein PDF"""
        klassen_ergebnisse = self.prepare_ergebnisse()
        pdf_generator = PDFGenerator(self.turnier_model)
        pdf_generator.create_pdf(klassen_ergebnisse)

    def refresh(self):
        """Aktualisiert die Anzeige"""
        # Canvas-Inhalt löschen
        for widget in self.window.winfo_children():
             if isinstance(widget, ttk.Frame) and widget.winfo_manager() == "pack":
                 # Dies ist der main_frame oder button_frame.
                 # Wir wollen nur den main_frame neu bauen, oder alles?
                 # Einfacher: Alles neu bauen.
                 widget.destroy()

        # Create widgets again (skip window creation)
        # Da create_widgets button_frame und main_frame erstellt, müssen wir diese vorher löschen.
        # Aber self.window bleibt.
        self.create_widgets()
