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
from .online_eingabe_tab import OnlineEingabeTab
from .urkunden_tab import UrkundenTab
from .schiesszettel_tab import SchiesszettelTab
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
        
        # Tracking für Live-Updates
        self.last_update_check = 0

        self.create_widgets()
        self.start_update_loop()
    
    def start_update_loop(self):
        """Startet die Schleife zur Prüfung auf Updates"""
        self.check_for_updates()
        self.root.after(1000, self.start_update_loop)

    def check_for_updates(self):
        """Prüft ob Updates vorliegen und aktualisiert die UI"""
        if self.turnier_model.last_update_time > self.last_update_check:
            self.last_update_check = self.turnier_model.last_update_time
            # Refresh Tabs die Ergebnisse anzeigen
            if hasattr(self, 'ergebnisse_tab'):
                self.ergebnisse_tab.refresh_silent_update()
            # Weitere Tabs könnten hier folgen, aber Ergebnisse ist am wichtigsten

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
        self.online_eingabe_tab = OnlineEingabeTab(self.notebook, self.turnier_model, self.schuetze_model)
        self.urkunden_tab = UrkundenTab(self.notebook, self.turnier_model, self.schuetze_model)
        self.schiesszettel_tab = SchiesszettelTab(self.notebook, self.turnier_model, self.schuetze_model)
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
        self.notebook.add(self.online_eingabe_tab.frame, text="Online-Eingabe")
        self.notebook.add(self.urkunden_tab.frame, text="Urkunden")
        self.notebook.add(self.schiesszettel_tab.frame, text="Schießzettel")
        self.notebook.add(self.startgeld_tab.frame, text="Startgeld")
        self.notebook.add(self.info_tab.frame, text="Info")
    
        # Tab Change Listener für Schießzettel (um Gruppen zu aktualisieren)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

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
        success, message, turnier_data = self.data_manager.load_from_file()
        if success:
            # Verzögertes Aktualisieren der UI, um sicherzustellen, dass alle Daten geladen sind
            self.root.after(10, lambda: self.post_load_refresh(message, turnier_data))
        elif message:  # Nur Fehler anzeigen, wenn eine Datei ausgewählt wurde
            messagebox.showerror("Fehler", message)

    def post_load_refresh(self, success_message, turnier_data=None):
        """Führt die Aktualisierungen nach dem Laden aus."""
        # Das Turnier-Tab benötigt die expliziten Daten, um den Race-Condition zu vermeiden
        self.turnier_tab.refresh(turnier_data=turnier_data)
        self.klassen_tab.refresh()
        self.schuetzen_tab.refresh()
        self.gruppen_tab.refresh()
        self.ergebnisse_tab.refresh()
        self.startgeld_tab.refresh()
        self.schiesszettel_tab.refresh()
        # Wichtig: Urkunden-Tab nach allen anderen aktualisieren,
        # da er von den berechneten Ergebnissen abhängt.
        self.urkunden_tab.refresh()
        # messagebox.showinfo("Erfolg", success_message) # Temporarily disabled for verification
    
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
        if hasattr(self, 'schiesszettel_tab'):
            self.schiesszettel_tab.refresh()

    def on_assignment_changed(self):
        """Wird aufgerufen, wenn sich eine Zuweisung in der Gruppenverwaltung ändert"""
        if hasattr(self, 'schuetzen_tab'):
            self.schuetzen_tab.refresh()
        if hasattr(self, 'schiesszettel_tab'):
            self.schiesszettel_tab.refresh()

    def on_klassen_changed_for_urkunden(self):
        """Callback specifically for updating the Urkunden tab."""
        if hasattr(self, 'urkunden_tab'):
            self.urkunden_tab.refresh()

    def on_tab_changed(self, event):
        """Handler for tab changes to trigger refresh"""
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")

        if tab_text == "Schießzettel":
             self.schiesszettel_tab.refresh()
        elif tab_text == "Gruppenverwaltung":
            self.gruppen_tab.refresh()
