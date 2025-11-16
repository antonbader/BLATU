# -*- coding: utf-8 -*-
"""
Bildschirmanzeige-Fenster
Automatisch aktualisierendes Fenster für externe Monitore
"""

import tkinter as tk
from tkinter import ttk
import time

from models.schuetze import SchuetzeModel
from config import MAX_PASSEN_FOR_DISPLAY


class BildschirmAnzeigeWindow:
    """Fenster zur Live-Anzeige der Ergebnisse auf externem Monitor"""
    
    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.window = tk.Toplevel(parent)
        self.window.title("Bildschirmanzeige - Live-Ergebnisse")
        self.window.geometry("1200x800")
        
        # Scroll-Parameter (time-based for smoother movement)
        # Pixels per second for scrolling (tweakable)
        self.scroll_speed_px_per_sec = 1.0
        # Milliseconds between scroll updates (smaller = smoother)
        self.scroll_interval = 10
        self.scroll_pause_top = 0  # Pause oben in ms
        self.is_paused = False
        self.pause_counter = 0
        self.content_height = 0  # Höhe desOriginal-Inhalts
        # Internal timing helpers
        self._last_scroll_time = None
        self._pixel_accumulator = 0.0
        self._debounce_job = None
    # no bottom-resume scheduling needed for seamless scrolling
        
        # Auto-Update Parameter
        self.update_interval = 2000  # Alle 2 Sekunden auf Änderungen prüfen
        self.last_data_hash = None
        
        self.create_widgets()
        self.start_auto_update()
        self.start_auto_scroll()
    
    def _on_canvas_configure(self, event):
        """Wird aufgerufen, wenn sich die Canvas-Größe ändert."""
        # Breite des scrollbaren Frames an die Canvas-Breite anpassen
        self.canvas.itemconfig(self.canvas_window, width=event.width)

        # Debounce-Mechanismus für die Neuberechnung des Scrollings
        if self._debounce_job:
            self.window.after_cancel(self._debounce_job)

        self._debounce_job = self.window.after(250, self._check_and_manage_scrolling)

    def create_widgets(self):
        """Erstellt alle Widgets"""
        # Titel-Frame (immer sichtbar oben)
        title_frame = ttk.Frame(self.window, padding="10")
        title_frame.pack(side=tk.TOP, fill=tk.X)
        
        turnier = self.turnier_model.get_turnier_data()
        
        ttk.Label(
            title_frame,
            text=f"🏆 {turnier.get('name', 'Turnier')}",
            font=("Arial", 24, "bold"),
            foreground="#2E5090"
        ).pack()
        
        if turnier.get('datum'):
            ttk.Label(
                title_frame,
                text=f"📅 {turnier['datum']}",
                font=("Arial", 14)
            ).pack(pady=5)
        
        ttk.Separator(title_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Haupt-Container mit Canvas für Scrolling
        main_container = ttk.Frame(self.window)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas für scrollbare Anzeige
        self.canvas = tk.Canvas(main_container, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbarer Frame
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )
        
        # Event-Handler für Größenänderungen des Canvas
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Scrollregion aktualisieren, wenn sich der Inhalt des Frames ändert
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Steuerungs-Frame unten
        control_frame = ttk.Frame(self.window)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Button(
            control_frame,
            text="⏸ Pause / ▶ Weiter",
            command=self.toggle_pause
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            control_frame,
            text="🔄 Aktualisieren",
            command=self.refresh_display
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            control_frame,
            text="🖥 Vollbild",
            command=self.toggle_fullscreen
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(
            control_frame,
            text="💡 Automatische Aktualisierung aktiv",
            font=("Arial", 9),
            foreground="green"
        ).pack(side=tk.LEFT, padx=20)
        
        ttk.Button(
            control_frame,
            text="❌ Schließen",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=10)
        
        # Initiale Anzeige
        self.refresh_display()

    def _populate_frame_with_tables(self, parent_frame):
        """Befüllt einen Frame mit den Ergebnistabellen."""
        # Turnierdaten holen
        turnier = self.turnier_model.get_turnier_data()
        anzahl_passen = turnier.get('anzahl_passen', 1)
        show_halves = turnier.get('show_halves', False)

        # Entscheiden ob Passen-Details angezeigt werden
        show_passen_details = anzahl_passen <= MAX_PASSEN_FOR_DISPLAY and not show_halves

        # Ergebnisse nach Klassen gruppieren
        klassen_ergebnisse = self.prepare_ergebnisse()

        if not klassen_ergebnisse:
            ttk.Label(
                parent_frame,
                text="Noch keine Ergebnisse vorhanden",
                font=("Arial", 16),
                foreground="gray"
            ).pack(pady=50)
            return

        # Für jede Klasse eine Tabelle erstellen
        for klasse in sorted(klassen_ergebnisse.keys()):
            self.create_klassen_display(
                parent_frame,
                klasse,
                klassen_ergebnisse[klasse],
                show_passen_details,
                show_halves,
                anzahl_passen
            )

    def refresh_display(self):
        """Aktualisiert die Ergebnisanzeige"""
        # Alle vorhandenen Widgets löschen
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Container für den Original-Inhalt erstellen und befüllen
        self.original_content = ttk.Frame(self.scrollable_frame)
        self.original_content.pack(fill=tk.BOTH, expand=True)
        self._populate_frame_with_tables(self.original_content)

        # Warten, bis das Layout des Original-Inhalts fertig ist
        self.scrollable_frame.update_idletasks()
        self.content_height = self.original_content.winfo_reqheight()

        # Platzhalter für das Duplikat
        self.duplicate_content = None
        self._has_duplicate = False

        # Initialen Scroll-Zustand herstellen
        self._check_and_manage_scrolling()

        # Scroll-Position zurücksetzen
        self._pixel_accumulator = 0.0
        self.canvas.yview_moveto(0)
        # Kurze Pause nach einem Refresh
        self.is_paused = True
        self.pause_counter = 0
        self._last_scroll_time = time.time()

        try:
            self.window.after(1000, self._resume_after_refresh)
        except Exception:
            pass

    def _resume_after_refresh(self):
        """Resume helper called after a refresh delay."""
        self.is_paused = False
        self.pause_counter = 0
        self._last_scroll_time = time.time()

    def _check_and_manage_scrolling(self, event=None):
        """Prüft, ob Scrolling nötig ist, und erstellt/entfernt das Duplikat."""
        canvas_height = self.canvas.winfo_height()
        needs_scrolling = self.content_height > canvas_height

        if needs_scrolling and not self._has_duplicate:
            # Duplikat für nahtloses Scrolling erstellen
            self.duplicate_content = ttk.Frame(self.scrollable_frame)
            self.duplicate_content.pack(fill=tk.BOTH, expand=True)
            self._populate_frame_with_tables(self.duplicate_content)
            self._has_duplicate = True
            # Scroll-Position zurücksetzen, um von vorne zu beginnen
            self.canvas.yview_moveto(0)
            self._pixel_accumulator = 0.0

        elif not needs_scrolling and self._has_duplicate:
            # Duplikat entfernen, wenn nicht mehr benötigt
            if self.duplicate_content:
                self.duplicate_content.destroy()
                self.duplicate_content = None
            self._has_duplicate = False
            # Scroll-Position zurücksetzen
            self.canvas.yview_moveto(0)
            self._pixel_accumulator = 0.0

    # NOTE: bottom scheduling is removed for seamless scrolling
    
    def create_klassen_display(self, parent, klasse, ergebnisse, 
                               show_passen_details, show_halves, anzahl_passen):
        """Erstellt die Anzeige für eine Klasse"""
        # Klassenüberschrift
        klassen_label = ttk.Label(
            parent,
            text=f"Klasse: {klasse}",
            font=("Arial", 20, "bold"),
            foreground="#2E5090"
        )
        klassen_label.pack(pady=(10, 15))
        
        # Tabellen-Frame
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Spalten definieren
        if show_halves:
            columns = ["Platz", "Name", "Vorname", "Verein", "1. Hälfte", "2. Hälfte", "Gesamt", "10er", "9er"]
            col_widths = [60, 150, 150, 150, 100, 100, 100, 60, 60]
        elif show_passen_details:
            columns = ["Platz", "Name", "Vorname", "Verein"]
            col_widths = [60, 150, 150, 150]
            for i in range(anzahl_passen):
                columns.append(f"P{i+1}")
                col_widths.append(70)
            columns.extend(["Gesamt", "10er", "9er"])
            col_widths.extend([100, 60, 60])
        else:
            columns = ["Platz", "Name", "Vorname", "Verein", "Gesamt", "10er", "9er"]
            col_widths = [60, 200, 200, 200, 100, 60, 60]
        
        # Treeview erstellen
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=len(ergebnisse)
        )
        
        # Spalten konfigurieren
        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=tk.CENTER)
        
        # Style für bessere Lesbarkeit
        style = ttk.Style()
        style.configure("Treeview", rowheight=35, font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))
        
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
            
            # Platzierung mit Medaillen-Emoji
            platz_anzeige = str(current_platz)
            if current_platz == 1:
                platz_anzeige = "🥇 1"
            elif current_platz == 2:
                platz_anzeige = "🥈 2"
            elif current_platz == 3:
                platz_anzeige = "🥉 3"
            
            werte = [
                platz_anzeige,
                ergebnis['name'],
                ergebnis['vorname'],
                ergebnis['verein']
            ]
            
            # Passen oder Hälften hinzufügen
            if show_halves:
                half = anzahl_passen // 2
                erste_haelfte = sum(ergebnis['ergebnisse'][:half])
                zweite_haelfte = sum(ergebnis['ergebnisse'][half:])
                werte.append(str(erste_haelfte))
                werte.append(str(zweite_haelfte))
            elif show_passen_details:
                for i in range(anzahl_passen):
                    if i < len(ergebnis['ergebnisse']):
                        werte.append(str(int(ergebnis['ergebnisse'][i])))
                    else:
                        werte.append("0")
            
            werte.append(str(int(ergebnis['gesamt'])))
            werte.append(str(ergebnis['anzahl_10er']))
            werte.append(str(ergebnis['anzahl_9er']))
            
            # Zeile einfügen mit Tag für Farbe
            tag = f"place_{current_platz}" if current_platz <= 3 else ""
            tree.insert("", tk.END, values=werte, tags=(tag,))
            
            prev_ergebnis = ergebnis
        
        # Farben für die ersten 3 Plätze
        tree.tag_configure("place_1", background="#FFD700")  # Gold
        tree.tag_configure("place_2", background="#C0C0C0")  # Silber
        tree.tag_configure("place_3", background="#CD7F32")  # Bronze
        
        tree.pack(fill=tk.BOTH, expand=True)
    
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
    
    def get_data_hash(self):
        """Erstellt einen Hash der aktuellen Daten für Änderungserkennung"""
        data = []
        for schuetze in self.schuetze_model.get_all_schuetzen():
            schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
            ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            if ergebnis:
                data.append((schuetze_id, str(ergebnis)))
        return str(sorted(data))
    
    def start_auto_update(self):
        """Startet die automatische Aktualisierung"""
        def check_for_updates():
            if self.window.winfo_exists():
                current_hash = self.get_data_hash()
                if self.last_data_hash != current_hash:
                    self.refresh_display()
                    self.last_data_hash = current_hash
                self.window.after(self.update_interval, check_for_updates)
        
        self.last_data_hash = self.get_data_hash()
        self.window.after(self.update_interval, check_for_updates)
    
    def start_auto_scroll(self):
        """Startet das automatische, nahtlose Scrolling"""
        def auto_scroll():
            if not self.window.winfo_exists():
                return

            now = time.time()
            if self._last_scroll_time is None:
                self._last_scroll_time = now

            if self.is_paused:
                self.pause_counter += self.scroll_interval
                if self.pause_counter >= self.scroll_pause_top:
                    self.is_paused = False
                    self.pause_counter = 0
                self._last_scroll_time = now
            else:
                if self.content_height > 0 and getattr(self, '_has_duplicate', False):
                    dt = now - self._last_scroll_time
                    # Pixel-Bewegung als Fließkommazahl akkumulieren
                    self._pixel_accumulator += self.scroll_speed_px_per_sec * dt

                    # Nur scrollen, wenn mindestens ein ganzer Pixel bewegt werden soll
                    if self._pixel_accumulator >= 1.0:
                        scroll_amount = int(self._pixel_accumulator)
                        try:
                            self.canvas.yview_scroll(scroll_amount, "units")
                            # Akkumulator um den gescrollten Betrag reduzieren
                            self._pixel_accumulator -= scroll_amount

                            # Nahtlosen Übergang prüfen
                            # yview() gibt Tupel (top_fraction, bottom_fraction) zurück
                            current_pos_fraction = self.canvas.yview()[0]
                            total_scroll_height = self.scrollable_frame.winfo_reqheight()

                            # Wenn die Oberkante der Ansicht den Anfang des Duplikats erreicht hat
                            if current_pos_fraction * total_scroll_height >= self.content_height:
                                # Unsichtbar an den Anfang zurückspringen
                                self.canvas.yview_moveto(0)
                                # Oben eine Pause einlegen
                                self.is_paused = True
                                self.pause_counter = 0
                                # Akkumulator zurücksetzen, um Sprünge zu vermeiden
                                self._pixel_accumulator = 0.0

                        except tk.TclError:
                            # Fehler bei Fensterzerstörung ignorieren
                            pass

                self._last_scroll_time = now

            self.window.after(self.scroll_interval, auto_scroll)

        # Warten, bis das Layout vollständig initialisiert ist
        self.window.after(500, auto_scroll)
    

    
    def toggle_pause(self):
        """Pausiert/Startet das Scrolling manuell"""
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.pause_counter = 0
    
    def toggle_fullscreen(self):
        """Schaltet Vollbildmodus um"""
        current_state = self.window.attributes('-fullscreen')
        self.window.attributes('-fullscreen', not current_state)
        
        # ESC-Taste zum Verlassen des Vollbildmodus
        if not current_state:
            self.window.bind('<Escape>', lambda e: self.window.attributes('-fullscreen', False))
