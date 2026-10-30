# -*- coding: utf-8 -*-
"""
Mannschaftswertung-Anzeige-Fenster
Zeigt die Wertung der Mannschaften (gesamt oder nach Mannschaftsklassen,
wahlweise mit oder ohne Einzelergebnisse der Mannschaftsmitglieder)
und ermöglicht den PDF-Export.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from utils.pdf_generator import PDFGenerator
from utils.gui_helper import set_window_icon


class MannschaftsErgebnisWindow:
    """Fenster zur Anzeige der Mannschaftswertung"""

    def __init__(self, parent, turnier_model, schuetze_model,
                 initial_group_by_klasse=False, initial_show_einzel=False):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.window = tk.Toplevel(parent)
        self.window.title("Mannschaftswertung")
        set_window_icon(self.window)
        self.window.geometry("1050x720")

        self.group_by_klasse_var = tk.BooleanVar(value=initial_group_by_klasse)
        self.show_einzel_anzeige_var = tk.BooleanVar(value=initial_show_einzel)
        self.show_einzel_pdf_var = tk.BooleanVar(value=initial_show_einzel)

        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        # Obere Optionsleiste für Anzeige & Wertungsmodus
        options_frame = ttk.LabelFrame(self.window, text="Optionen für die Mannschaftswertung", padding="10")
        options_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        mode_frame = ttk.Frame(options_frame)
        mode_frame.pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(mode_frame, text="Wertungsmodus:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(
            mode_frame,
            text="Alle Mannschaften (Gesamtwertung)",
            variable=self.group_by_klasse_var,
            value=False,
            command=self.refresh_tables
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            mode_frame,
            text="Nach Mannschaftsklassen unterscheiden",
            variable=self.group_by_klasse_var,
            value=True,
            command=self.refresh_tables
        ).pack(side=tk.LEFT, padx=5)

        ttk.Separator(options_frame, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Checkbutton(
            options_frame,
            text="Einzelergebnisse der Mannschaftsmitglieder in Anzeige einblenden",
            variable=self.show_einzel_anzeige_var,
            command=self._on_anzeige_einzel_toggled
        ).pack(side=tk.LEFT, padx=5)

        # Untere Button- und PDF-Leiste
        bottom_frame = ttk.Frame(self.window, padding="10")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        pdf_group = ttk.LabelFrame(bottom_frame, text="PDF Export", padding="6")
        pdf_group.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Checkbutton(
            pdf_group,
            text="Mit Einzelergebnissen der Mannschaftsmitglieder im PDF",
            variable=self.show_einzel_pdf_var
        ).pack(side=tk.LEFT, padx=(5, 10))

        ttk.Button(
            pdf_group,
            text="📄 PDF erstellen",
            command=self.create_pdf
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            bottom_frame,
            text="🔄 Aktualisieren",
            command=self.refresh_tables
        ).pack(side=tk.LEFT, padx=10)

        ttk.Button(
            bottom_frame,
            text="Schließen",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=10)

        # Hauptbereich mit Scrollbars
        self.main_frame = ttk.Frame(self.window, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame)
        self.v_scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_frame, width=event.width)

        self.canvas.bind("<Configure>", on_canvas_configure)

        self.canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.h_scrollbar.grid(row=1, column=0, sticky=(tk.E, tk.W))

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        self.refresh_tables()

    def _on_anzeige_einzel_toggled(self):
        """Synchronisiert optional die PDF-Checkbox und aktualisiert die Tabellen."""
        self.show_einzel_pdf_var.set(self.show_einzel_anzeige_var.get())
        self.refresh_tables()

    def refresh(self):
        """Externe Refresh-Methode (für Live-Updates)"""
        if self.window.winfo_exists():
            self.refresh_tables()

    def refresh_tables(self):
        """Baut den Inhalt des scrollbaren Bereichs neu auf"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        turnier = self.turnier_model.get_turnier_data()
        title_frame = ttk.Frame(self.scrollable_frame)
        title_frame.pack(fill=tk.X, pady=10)

        ttk.Label(
            title_frame,
            text=f"Mannschaftswertung: {turnier.get('name', 'Turnier') or 'Turnier'}",
            font=("Arial", 16, "bold")
        ).pack()

        if turnier.get('datum'):
            ttk.Label(
                title_frame,
                text=f"Datum: {turnier['datum']}",
                font=("Arial", 11)
            ).pack(pady=3)

        group_by_klasse = self.group_by_klasse_var.get()
        show_einzel = self.show_einzel_anzeige_var.get()

        mannschaft_ergebnisse = self.turnier_model.calculate_mannschaft_results(
            self.schuetze_model,
            group_by_klasse=group_by_klasse
        )

        if not mannschaft_ergebnisse:
            ttk.Label(
                self.scrollable_frame,
                text="Es sind noch keine Mannschaften angelegt.",
                font=("Arial", 12),
                foreground="gray"
            ).pack(pady=30)
            return

        for group_name in sorted(mannschaft_ergebnisse.keys()):
            teams = mannschaft_ergebnisse[group_name]
            self.create_group_table(
                self.scrollable_frame,
                group_name,
                teams,
                group_by_klasse=group_by_klasse,
                show_einzel=show_einzel
            )

    def create_group_table(self, parent, group_name, teams, group_by_klasse=False, show_einzel=False):
        """Erstellt eine Ergebnistabelle für eine Mannschaftsgruppe bzw. Mannschaftsklasse"""
        frame_title = f"Mannschaftsklasse: {group_name}" if group_by_klasse else "Wertung: Alle Mannschaften"
        group_frame = ttk.LabelFrame(parent, text=frame_title, padding="10")
        group_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        turnier = self.turnier_model.get_turnier_data()
        anzahl_passen = turnier.get('anzahl_passen', 1)
        show_halves = turnier.get('show_halves', False)
        max_groesse = self.turnier_model.get_mannschaft_groesse()

        tree_container = ttk.Frame(group_frame)
        tree_container.pack(fill=tk.BOTH, expand=True)

        tree_yscroll = ttk.Scrollbar(tree_container, orient="vertical")

        if not show_einzel:
            if group_by_klasse:
                columns = ["Platz", "Mannschaft", "Schützen", "Gesamt", "10er", "9er"]
            else:
                columns = ["Platz", "Mannschaft", "Mannschaftsklasse", "Schützen", "Gesamt", "10er", "9er"]
            row_count = len(teams)
        else:
            columns = ["Platz", "Mannschaft"]
            if not group_by_klasse:
                columns.append("Mannschaftsklasse")
            columns.extend(["Schütze", "Verein", "Klasse"])
            if show_halves:
                columns.extend(["1. Hälfte", "2. Hälfte"])
            else:
                columns.extend([f"P{i+1}" for i in range(anzahl_passen)])
            columns.extend(["Gesamt", "10er", "9er"])
            row_count = sum(1 + len(t.get('mitglieder', [])) for t in teams)

        tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            yscrollcommand=tree_yscroll.set,
            height=min(max(row_count + 1, 4), 18)
        )

        # Spaltenbreiten & Ausrichtung
        for col in columns:
            tree.heading(col, text=col)
            if col == "Platz":
                tree.column(col, width=55, anchor=tk.CENTER)
            elif col in ("Mannschaft", "Schütze"):
                tree.column(col, width=160, anchor=tk.W)
            elif col in ("Mannschaftsklasse", "Verein", "Klasse"):
                tree.column(col, width=120, anchor=tk.W)
            elif col == "Schützen":
                tree.column(col, width=85, anchor=tk.CENTER)
            elif col in ("1. Hälfte", "2. Hälfte", "Gesamt"):
                tree.column(col, width=75, anchor=tk.CENTER)
            else:
                tree.column(col, width=50, anchor=tk.CENTER)

        tree_yscroll.config(command=tree.yview)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_yscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Tags für optische Hervorhebung
        tree.tag_configure("team_row", background="#D9E1F2", font=("Arial", 10, "bold"))
        tree.tag_configure("member_row", background="#FFFFFF", font=("Arial", 9))
        tree.tag_configure("place_1", background="#FFF2CC")
        tree.tag_configure("place_2", background="#EDEDED")
        tree.tag_configure("place_3", background="#FCE4D6")

        for team in teams:
            platz = team.get('platz', 1)
            mitglieder = team.get('mitglieder', [])
            anz_str = f"{len(mitglieder)}/{max_groesse}"

            if not show_einzel:
                if group_by_klasse:
                    values = [
                        str(platz),
                        team['name'],
                        anz_str,
                        str(int(team['gesamt'])),
                        str(team['anzahl_10er']),
                        str(team['anzahl_9er'])
                    ]
                else:
                    values = [
                        str(platz),
                        team['name'],
                        team.get('klasse') or "-",
                        anz_str,
                        str(int(team['gesamt'])),
                        str(team['anzahl_10er']),
                        str(team['anzahl_9er'])
                    ]
                tag = f"place_{platz}" if platz in (1, 2, 3) else ""
                tree.insert("", tk.END, values=values, tags=(tag,) if tag else ())
            else:
                team_values = [str(platz), team['name']]
                if not group_by_klasse:
                    team_values.append(team.get('klasse') or "-")
                team_values.extend([f"Gesamt ({anz_str} Schützen)", "", ""])

                if show_halves:
                    half = anzahl_passen // 2
                    erste = sum(team['ergebnisse'][:half])
                    zweite = sum(team['ergebnisse'][half:])
                    team_values.extend([str(int(erste)), str(int(zweite))])
                else:
                    for i in range(anzahl_passen):
                        val = team['ergebnisse'][i] if i < len(team['ergebnisse']) else 0
                        team_values.append(str(int(val)))

                team_values.extend([
                    str(int(team['gesamt'])),
                    str(team['anzahl_10er']),
                    str(team['anzahl_9er'])
                ])
                tree.insert("", tk.END, values=team_values, tags=("team_row",))

                for member in mitglieder:
                    m_values = ["", ""]
                    if not group_by_klasse:
                        m_values.append("")
                    m_values.extend([
                        f"  ↳ {member.get('vorname', '')} {member.get('name', '')}".rstrip(),
                        member.get('verein', ''),
                        member.get('klasse', '')
                    ])

                    m_passen = member.get('ergebnisse', [])
                    if show_halves:
                        half = anzahl_passen // 2
                        m_erste = sum(m_passen[:half])
                        m_zweite = sum(m_passen[half:])
                        m_values.extend([str(int(m_erste)), str(int(m_zweite))])
                    else:
                        for i in range(anzahl_passen):
                            val = m_passen[i] if i < len(m_passen) else 0
                            m_values.append(str(int(val)))

                    m_values.extend([
                        str(int(member.get('gesamt', 0))),
                        str(member.get('anzahl_10er', 0)),
                        str(member.get('anzahl_9er', 0))
                    ])
                    tree.insert("", tk.END, values=m_values, tags=("member_row",))

    def create_pdf(self):
        """Erstellt ein PDF der Mannschaftswertung mit den gewählten Optionen"""
        group_by_klasse = self.group_by_klasse_var.get()
        show_einzel = self.show_einzel_pdf_var.get()

        mannschaft_ergebnisse = self.turnier_model.calculate_mannschaft_results(
            self.schuetze_model,
            group_by_klasse=group_by_klasse
        )
        if not mannschaft_ergebnisse:
            messagebox.showinfo("Keine Mannschaften", "Es sind noch keine Mannschaften vorhanden!")
            return

        pdf_generator = PDFGenerator(self.turnier_model)
        pdf_generator.create_mannschaft_pdf(
            mannschaft_ergebnisse,
            show_einzel=show_einzel,
            group_by_klasse=group_by_klasse
        )
