# -*- coding: utf-8 -*-
"""
Hauptfenster der Anwendung
Koordiniert alle Tabs und verwaltet globale Daten
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from models import TurnierModel, SchuetzeModel
from utils import DataManager, PDFGenerator
from .turnier_tab import TurnierTab
from .klassen_tab import KlassenTab
from .schuetzen_tab import SchuetzenTab
from .gruppen_tab import GruppenTab
from .ergebnisse_tab import ErgebnisseTab
from .urkunden_tab import UrkundenTab
from .startgeld_tab import StartgeldTab
from .info_tab import InfoTab


class MainWindow:
    """Hauptfenster der Anwendung"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Datenmodelle initialisieren
        self.turnier_model = TurnierModel()
        self.schuetze_model = SchuetzeModel()
        self.data_manager = DataManager(self.turnier_model, self.schuetze_model)
        self.pdf_generator = PDFGenerator(self.turnier_model)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        # Haupt-Button-Frame unten
        self.create_main_buttons()
        
        # Notebook für Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Tabs erstellen - mit Callback-Verbindungen
        self.turnier_tab = TurnierTab(self.notebook, self.turnier_model, self.on_turnier_changed)
        self.klassen_tab = KlassenTab(
            self.notebook, 
            self.turnier_model, 
            self.schuetze_model,
            self.on_klassen_changed
        )
        self.schuetzen_tab = SchuetzenTab(
            self.notebook,
            self.turnier_model,
            self.schuetze_model,
            self.on_schuetzen_changed
        )
        self.gruppen_tab = GruppenTab(
            self.notebook,
            self.turnier_model,
            self.schuetze_model,
            self.pdf_generator,
            self.on_assignment_changed
        )
        self.ergebnisse_tab = ErgebnisseTab(self.notebook, self.turnier_model, self.schuetze_model)
        self.urkunden_tab = UrkundenTab(self.notebook, self.turnier_model, self.schuetze_model)
        self.startgeld_tab = StartgeldTab(self.notebook, self.turnier_model, self.schuetze_model)
        self.info_tab = InfoTab(self.notebook)

        # Connect callbacks
        self.klassen_tab.on_klassen_changed_callback = self.on_klassen_changed_for_urkunden
        self.turnier_tab.on_turnier_data_changed_callback = self.on_klassen_changed_for_urkunden
        
        # Tabs zum Notebook hinzufügen
        self.notebook.add(self.turnier_tab.frame, text="Turnierverwaltung")
        self.notebook.add(self.klassen_tab.frame, text="Klassenverwaltung")
        self.notebook.add(self.schuetzen_tab.frame, text="Schützenverwaltung")
        self.notebook.add(self.gruppen_tab.frame, text="Gruppenverwaltung")
        self.notebook.add(self.ergebnisse_tab.frame, text="Ergebniseingabe")
        self.notebook.add(self.urkunden_tab.frame, text="Urkunden")
        self.notebook.add(self.startgeld_tab.frame, text="Startgeld")
        self.notebook.add(self.info_tab.frame, text="Info")
    
    def create_main_buttons(self):
        """Erstellt die Hauptbuttons zum Speichern/Laden"""
        main_button_frame = ttk.Frame(self.root, padding="10")
        main_button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        ttk.Separator(main_button_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 10))
        
        btn_container = ttk.Frame(main_button_frame)
        btn_container.pack()
        
        ttk.Button(
            btn_container, 
            text="💾 Alle Daten speichern", 
            command=self.save_all_data
        ).pack(side=tk.LEFT, padx=10, pady=5, ipadx=20, ipady=8)
        
        ttk.Button(
            btn_container, 
            text="📂 Alle Daten laden", 
            command=self.load_all_data
        ).pack(side=tk.LEFT, padx=10, pady=5, ipadx=20, ipady=8)
    
    def save_all_data(self):
        """Speichert alle Daten in eine Datei"""
        success, message = self.data_manager.save_to_file()
        if success:
            messagebox.showinfo("Erfolg", message)
        else:
            messagebox.showerror("Fehler", message)
    
    def load_all_data(self):
        """Lädt alle Daten aus einer Datei"""
        success, message = self.data_manager.load_from_file()
        if success:
            # Alle Tabs aktualisieren
            self.turnier_tab.refresh()
            self.klassen_tab.refresh()
            self.schuetzen_tab.refresh()
            self.gruppen_tab.refresh()
            self.ergebnisse_tab.refresh()
            self.startgeld_tab.refresh()
            messagebox.showinfo("Erfolg", message)
        elif message:  # Nur Fehler anzeigen, wenn eine Datei ausgewählt wurde
            messagebox.showerror("Fehler", message)
    
    def on_turnier_changed(self):
        """Wird aufgerufen wenn sich Turnierdaten ändern"""
        # Ergebnisse-Tab muss Passen-Felder neu erstellen
        if hasattr(self, 'ergebnisse_tab'):
            self.ergebnisse_tab.refresh()
    
    def on_klassen_changed(self):
        """Wird aufgerufen wenn sich Klassen ändern"""
        if hasattr(self, 'schuetzen_tab'):
            self.schuetzen_tab.refresh()
        if hasattr(self, 'startgeld_tab'):
            self.startgeld_tab.refresh()
    
    def on_schuetzen_changed(self):
        """Wird aufgerufen wenn sich Schützenliste ändert"""
        if hasattr(self, 'ergebnisse_tab'):
            self.ergebnisse_tab.refresh()
        if hasattr(self, 'gruppen_tab'):
            self.gruppen_tab.refresh()
        if hasattr(self, 'startgeld_tab'):
            self.startgeld_tab.refresh()

    def on_assignment_changed(self):
        """Wird aufgerufen, wenn sich eine Zuweisung in der Gruppenverwaltung ändert"""
        if hasattr(self, 'schuetzen_tab'):
            self.schuetzen_tab.refresh()

    def on_klassen_changed_for_urkunden(self):
        """Callback specifically for updating the Urkunden tab."""
        if hasattr(self, 'urkunden_tab'):
            self.urkunden_tab.refresh()
