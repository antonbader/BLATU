# -*- coding: utf-8 -*-
"""
Stechschießen-Fenster
Ermöglicht bei Punkt-Gleichstand die Auswahl der Schützen und Eingabe der Stech-Ergebnisse
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.schuetze import SchuetzeModel
from utils.gui_helper import set_window_icon


class StechschiessenWindow:
    """Fenster zur Auswahl der Schützen und Eingabe der Ergebnisse beim Stechschießen"""

    def __init__(self, parent, turnier_model, schuetze_model, on_save_callback=None, tie_groups=None):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.on_save_callback = on_save_callback
        self.tie_groups = tie_groups if tie_groups is not None else self.find_tie_groups(turnier_model, schuetze_model)
        self.row_controls = []

        self.window = tk.Toplevel(parent)
        self.window.title("Stechschießen bei Punkt-Gleichstand")
        set_window_icon(self.window)
        self.window.geometry("780x550")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()

        self.create_widgets()

    @classmethod
    def open_if_ties(cls, parent, turnier_model, schuetze_model, on_save_callback=None):
        """Prüft auf Punkt-Gleichstände und öffnet das Fenster, falls vorhanden."""
        tie_groups = cls.find_tie_groups(turnier_model, schuetze_model)
        if not tie_groups:
            messagebox.showinfo(
                "Kein Punkt-Gleichstand",
                "Es liegt aktuell kein Punkt-Gleichstand (gleiche Gesamtringzahl, 10er und 9er) "
                "innerhalb einer Klasse vor."
            )
            return None
        return cls(parent, turnier_model, schuetze_model, on_save_callback=on_save_callback, tie_groups=tie_groups)

    @staticmethod
    def find_tie_groups(turnier_model, schuetze_model):
        """
        Sucht in allen Klassen nach Schützen mit identischem regulärem Ergebnis
        (Gesamt > 0, gleiche 10er, gleiche 9er).
        """
        by_class = {}
        for schuetze in schuetze_model.get_all_schuetzen():
            schuetze_id = SchuetzeModel.get_schuetze_id(schuetze)
            ergebnis = turnier_model.get_ergebnis(schuetze_id)
            if not ergebnis:
                continue

            passen = ergebnis.get('passen', [])
            gesamt = sum(passen)
            if gesamt <= 0:
                continue

            anzahl_10er = ergebnis.get('anzahl_10er', 0)
            anzahl_9er = ergebnis.get('anzahl_9er', 0)
            stechen = ergebnis.get('stechen', None)

            klasse = schuetze['klasse']
            by_class.setdefault(klasse, []).append({
                'schuetze_id': schuetze_id,
                'name': schuetze['name'],
                'vorname': schuetze['vorname'],
                'verein': schuetze.get('verein', ''),
                'klasse': klasse,
                'gesamt': gesamt,
                'anzahl_10er': anzahl_10er,
                'anzahl_9er': anzahl_9er,
                'stechen': stechen
            })

        tie_groups = []
        for klasse in sorted(by_class.keys()):
            shooters = by_class[klasse]
            # Sortiere regulär nach Gesamt, 10er, 9er
            shooters.sort(
                key=lambda s: (s['gesamt'], s['anzahl_10er'], s['anzahl_9er']),
                reverse=True
            )

            # Gruppiere nach regulärem Score-Tupel und merke regulären Platz
            idx = 0
            while idx < len(shooters):
                current = shooters[idx]
                score_key = (current['gesamt'], current['anzahl_10er'], current['anzahl_9er'])
                reg_platz = idx + 1
                group = [current]
                j = idx + 1
                while j < len(shooters):
                    other = shooters[j]
                    if (other['gesamt'], other['anzahl_10er'], other['anzahl_9er']) == score_key:
                        group.append(other)
                        j += 1
                    else:
                        break

                if len(group) >= 2:
                    tie_groups.append({
                        'klasse': klasse,
                        'platz': reg_platz,
                        'gesamt': current['gesamt'],
                        'anzahl_10er': current['anzahl_10er'],
                        'anzahl_9er': current['anzahl_9er'],
                        'shooters': group
                    })

                idx = j

        return tie_groups

    def create_widgets(self):
        """Erstellt die Benutzeroberfläche des Stechschießen-Dialogs"""
        # Untere Button-Leiste
        button_frame = ttk.Frame(self.window, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(
            button_frame,
            text="💾 Ergebnisse speichern",
            command=self.save_stechen
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=4)

        ttk.Button(
            button_frame,
            text="Abbrechen",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5, ipadx=10, ipady=4)

        # Kopfbereich
        header_frame = ttk.Frame(self.window, padding="10")
        header_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(
            header_frame,
            text="Stechschießen verwalten",
            font=("Arial", 15, "bold")
        ).pack(anchor=tk.W)

        ttk.Label(
            header_frame,
            text=(
                "Wählen Sie bei Punkt-Gleichstand die Schützen aus, die ein Stechschießen "
                "durchführen, und tragen Sie deren Ergebnis aus dem Stechschießen ein."
            ),
            font=("Arial", 9),
            foreground="#444444",
            wraplength=740
        ).pack(anchor=tk.W, pady=(4, 0))

        # Scrollbarer Hauptbereich
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_frame, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Gleichstands-Gruppen darstellen
        for group in self.tie_groups:
            self._create_group_section(scrollable_frame, group)

    def _create_group_section(self, parent, group):
        """Erstellt einen Bereich für eine Gleichstands-Gruppe"""
        title = (
            f"Klasse: {group['klasse']}  |  Gleichstand um Platz {group['platz']}  "
            f"({group['gesamt']} Ringe, {group['anzahl_10er']}x 10er, {group['anzahl_9er']}x 9er)"
        )
        group_frame = ttk.LabelFrame(parent, text=title, padding="10")
        group_frame.pack(fill=tk.X, expand=True, pady=6, padx=4)

        # Tabellenkopf
        ttk.Label(group_frame, text="Auswahl", font=("Arial", 9, "bold")).grid(
            row=0, column=0, padx=8, pady=(0, 6), sticky=tk.W
        )
        ttk.Label(group_frame, text="Schütze", font=("Arial", 9, "bold")).grid(
            row=0, column=1, padx=8, pady=(0, 6), sticky=tk.W
        )
        ttk.Label(group_frame, text="Verein", font=("Arial", 9, "bold")).grid(
            row=0, column=2, padx=8, pady=(0, 6), sticky=tk.W
        )
        ttk.Label(group_frame, text="Regulär", font=("Arial", 9, "bold")).grid(
            row=0, column=3, padx=8, pady=(0, 6), sticky=tk.W
        )
        ttk.Label(group_frame, text="Ergebnis Stechschießen", font=("Arial", 9, "bold")).grid(
            row=0, column=4, padx=8, pady=(0, 6), sticky=tk.W
        )

        for row_idx, shooter in enumerate(group['shooters'], start=1):
            has_stechen = shooter['stechen'] is not None
            selected_var = tk.BooleanVar(value=has_stechen)
            score_var = tk.StringVar(value=str(shooter['stechen']) if has_stechen else "")

            entry = ttk.Entry(group_frame, textvariable=score_var, width=12)

            def on_check_toggle(s_var=selected_var, e_var=score_var, ent=entry):
                if s_var.get():
                    ent.focus_set()
                else:
                    e_var.set("")

            def on_entry_key(_event, s_var=selected_var, e_var=score_var):
                if e_var.get().strip():
                    s_var.set(True)

            chk = ttk.Checkbutton(
                group_frame,
                text="Stechen",
                variable=selected_var,
                command=on_check_toggle
            )
            chk.grid(row=row_idx, column=0, padx=8, pady=4, sticky=tk.W)

            ttk.Label(
                group_frame,
                text=f"{shooter['vorname']} {shooter['name']}"
            ).grid(row=row_idx, column=1, padx=8, pady=4, sticky=tk.W)

            ttk.Label(
                group_frame,
                text=shooter['verein'] or "-"
            ).grid(row=row_idx, column=2, padx=8, pady=4, sticky=tk.W)

            ttk.Label(
                group_frame,
                text=f"{shooter['gesamt']} ({shooter['anzahl_10er']}x10, {shooter['anzahl_9er']}x9)"
            ).grid(row=row_idx, column=3, padx=8, pady=4, sticky=tk.W)

            entry.grid(row=row_idx, column=4, padx=8, pady=4, sticky=tk.W)
            entry.bind("<KeyRelease>", on_entry_key)

            self.row_controls.append({
                'schuetze_id': shooter['schuetze_id'],
                'name': f"{shooter['vorname']} {shooter['name']}",
                'selected_var': selected_var,
                'score_var': score_var
            })

        group_frame.columnconfigure(1, weight=1)
        group_frame.columnconfigure(2, weight=1)

    def save_stechen(self):
        """Validiert und speichert die Stechschießen-Ergebnisse"""
        updates = []

        for item in self.row_controls:
            is_selected = item['selected_var'].get()
            raw_score = item['score_var'].get().strip()

            if is_selected:
                if not raw_score:
                    messagebox.showwarning(
                        "Fehlende Eingabe",
                        f"Bitte geben Sie ein Stechschießen-Ergebnis für {item['name']} ein "
                        f"oder deaktivieren Sie die Auswahl.",
                        parent=self.window
                    )
                    return
                try:
                    score_val = int(raw_score)
                    if score_val < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showwarning(
                        "Ungültige Eingabe",
                        f"Bitte geben Sie für {item['name']} eine gültige ganze Zahl (>= 0) ein!",
                        parent=self.window
                    )
                    return
                updates.append((item['schuetze_id'], score_val))
            else:
                updates.append((item['schuetze_id'], None))

        for schuetze_id, score_val in updates:
            self.turnier_model.set_stechen(schuetze_id, score_val)

        if self.on_save_callback:
            self.on_save_callback()

        messagebox.showinfo(
            "Erfolg",
            "Die Ergebnisse des Stechschießens wurden gespeichert!",
            parent=self.window
        )
        self.window.destroy()
