# -*- coding: utf-8 -*-
"""
Bildschirmanzeige-Fenster
Automatisch aktualisierendes Fenster für externe Monitore
"""

import tkinter as tk
from tkinter import ttk

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
        
        # Scroll-Parameter
        self.scroll_position = 0.0
        self.scroll_speed = 0.3  # Pixel pro Update (langsamer Scroll)
        self.scroll_delay = 30  # Millisekunden zwischen Updates
        self.scroll_pause_top = 3000  # Pause oben in ms
        self.is_paused = False
        self.pause_counter = 0
        self.content_height = 0  # Höhe des Original-Inhalts
        
        # Auto-Update Parameter
        self.update_interval = 2000  # Alle 2 Sekunden auf Änderungen prüfen
        self.last_data_hash = None
        
        self.create_widgets()
        self.start_auto_update()
        self.start_auto_scroll()
    
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
            anchor="nw",
            width=self.canvas.winfo_width()
        )
        
        # Canvas-Größe anpassen
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        
        self.canvas.bind('<Configure>', on_canvas_configure)
        
        # Scrollregion aktualisieren
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
    
    def refresh_display(self):
        """Aktualisiert die Ergebnisanzeige"""
        # Alle vorhandenen Widgets löschen
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
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
                self.scrollable_frame,
                text="Noch keine Ergebnisse vorhanden",
                font=("Arial", 16),
                foreground="gray"
            ).pack(pady=50)
            return
        
        # Container für den Original-Inhalt
        original_content = ttk.Frame(self.scrollable_frame)
        original_content.pack(fill=tk.BOTH, expand=True)
        
        # Für jede Klasse eine Tabelle erstellen
        for idx, klasse in enumerate(sorted(klassen_ergebnisse.keys())):
            if idx > 0:
                ttk.Separator(original_content, orient='horizontal').pack(
                    fill=tk.X, pady=20
                )
            
            self.create_klassen_display(
                original_content,
                klasse,
                klassen_ergebnisse[klasse],
                show_passen_details,
                show_halves,
                anzahl_passen
            )
        
        # Warten bis das Layout fertig ist
        self.scrollable_frame.update_idletasks()
        self.content_height = original_content.winfo_reqheight()
        
        # Duplikat für nahtloses Scrolling erstellen
        duplicate_content = ttk.Frame(self.scrollable_frame)
        duplicate_content.pack(fill=tk.BOTH, expand=True)
        
        # Gleichen Inhalt nochmal erstellen
        for idx, klasse in enumerate(sorted(klassen_ergebnisse.keys())):
            if idx > 0:
                ttk.Separator(duplicate_content, orient='horizontal').pack(
                    fill=tk.X, pady=20
                )
            
            self.create_klassen_display(
                duplicate_content,
                klasse,
                klassen_ergebnisse[klasse],
                show_passen_details,
                show_halves,
                anzahl_passen
            )
        
        # Scroll-Position zurücksetzen
        self.scroll_position = 0.0
        self.canvas.yview_moveto(0)
    
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
                werte.append(f"{erste_haelfte:.1f}")
                werte.append(f"{zweite_haelfte:.1f}")
            elif show_passen_details:
                for i in range(anzahl_passen):
                    if i < len(ergebnis['ergebnisse']):
                        werte.append(f"{ergebnis['ergebnisse'][i]:.1f}")
                    else:
                        werte.append("0.0")
            
            werte.append(f"{ergebnis['gesamt']:.1f}")
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
        """Startet das automatische Scrolling"""
        def auto_scroll():
            if not self.window.winfo_exists():
                return
            
            if self.is_paused:
                self.pause_counter += self.scroll_delay
                
                # Pause beenden (nur oben)
                if self.pause_counter >= self.scroll_pause_top:
                    self.is_paused = False
                    self.pause_counter = 0
            else:
                if self.content_height > 0:
                    # Kontinuierliches Scrolling in Pixeln
                    self.scroll_position += self.scroll_speed
                    
                    # Wenn die Hälfte erreicht ist (Original-Inhalt durchgelaufen),
                    # nahtlos zum Anfang zurückspringen
                    canvas_height = self.canvas.winfo_height()
                    total_height = self.content_height * 2  # Doppelt wegen Duplikat
                    
                    if self.scroll_position >= self.content_height:
                        # Nahtlos zurück zum Anfang
                        self.scroll_position = 0.0
                        self.is_paused = True
                        self.pause_counter = 0
                    
                    # Scroll-Position als Fraction berechnen
                    if total_height > canvas_height:
                        fraction = self.scroll_position / (total_height - canvas_height)
                        self.canvas.yview_moveto(fraction)
            
            self.window.after(self.scroll_delay, auto_scroll)
        
        # Kurz warten bis Layout fertig ist
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
