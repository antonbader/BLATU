# -*- coding: utf-8 -*-
"""
Mannschaften Tab
Verwaltet Mannschaftsgröße, Mannschaftsklassen, Mannschaften, Schützenzuordnung
sowie die Anzeige und den PDF-Export der Mannschaftswertung.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from models.schuetze import SchuetzeModel
from utils.pdf_generator import PDFGenerator


class MannschaftenTab:
    """Tab für Mannschaftsverwaltung und Mannschaftswertung"""

    KEINE_KLASSE_LABEL = "(Keine Klasse)"

    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model

        self.editing_index = None
        self.current_mitglieder = []  # Liste von schuetze_ids für die aktuell bearbeitete Mannschaft
        self.mannschaft_ergebnis_window = None

        self.groesse_var = tk.IntVar(value=self.turnier_model.get_mannschaft_groesse())
        self.wertung_group_by_klasse_var = tk.BooleanVar(value=False)
        self.wertung_show_einzel_var = tk.BooleanVar(value=False)

        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets des Reiters 'Mannschaften'"""
        # 1. Obere Zeile: Mannschaftsgröße & Mannschaftsklassen
        top_row = ttk.Frame(self.frame)
        top_row.pack(side=tk.TOP, fill=tk.X, pady=(0, 8))
        top_row.columnconfigure(0, weight=1)
        top_row.columnconfigure(1, weight=2)

        # 1a. Mannschaftsgröße
        size_frame = ttk.LabelFrame(top_row, text="Mannschaftsgröße", padding="8")
        size_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        ttk.Label(
            size_frame,
            text="Anzahl Teilnehmer pro Mannschaft:"
        ).grid(row=0, column=0, sticky=tk.W, pady=4, padx=(0, 8))

        self.groesse_spinbox = ttk.Spinbox(
            size_frame,
            from_=1,
            to=50,
            width=6,
            textvariable=self.groesse_var
        )
        self.groesse_spinbox.grid(row=0, column=1, sticky=tk.W, pady=4)

        ttk.Button(
            size_frame,
            text="Übernehmen",
            command=self.save_mannschaft_groesse
        ).grid(row=0, column=2, sticky=tk.W, padx=(8, 0), pady=4)

        self.groesse_info_label = ttk.Label(
            size_frame,
            text=f"Aktuell: max. {self.turnier_model.get_mannschaft_groesse()} Schützen pro Mannschaft",
            font=("Arial", 8),
            foreground="gray"
        )
        self.groesse_info_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(2, 0))

        # 1b. Mannschaftsklassen
        klassen_frame = ttk.LabelFrame(top_row, text="Mannschaftsklassen verwalten", padding="8")
        klassen_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        klassen_frame.columnconfigure(1, weight=1)
        klassen_frame.columnconfigure(3, weight=1)

        ttk.Label(klassen_frame, text="Neue Klasse:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.mk_entry = ttk.Entry(klassen_frame, width=22)
        self.mk_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        self.mk_entry.bind("<Return>", lambda e: self.add_mannschaftsklasse())

        ttk.Button(
            klassen_frame,
            text="Klasse anlegen",
            command=self.add_mannschaftsklasse
        ).grid(row=0, column=2, padx=(0, 10))

        mk_list_container = ttk.Frame(klassen_frame)
        mk_list_container.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=(5, 5))

        mk_scroll = ttk.Scrollbar(mk_list_container, orient="vertical")
        self.mk_tree = ttk.Treeview(
            mk_list_container,
            columns=("Name",),
            show="headings",
            height=3,
            yscrollcommand=mk_scroll.set
        )
        self.mk_tree.heading("Name", text="Vorhandene Mannschaftsklassen")
        self.mk_tree.column("Name", width=180)
        self.mk_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mk_scroll.config(command=self.mk_tree.yview)
        mk_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Button(
            klassen_frame,
            text="Ausgewählte Klasse löschen",
            command=self.delete_mannschaftsklasse
        ).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(4, 0))

        # 2. Untere Leiste: Mannschaftswertung & PDF-Export (immer sichtbar unten)
        wertung_frame = ttk.LabelFrame(self.frame, text="Mannschaftswertung & PDF-Export", padding="8")
        wertung_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(6, 0))

        mode_sub = ttk.Frame(wertung_frame)
        mode_sub.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(mode_sub, text="Wertung:", font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Radiobutton(
            mode_sub,
            text="Alle Mannschaften",
            variable=self.wertung_group_by_klasse_var,
            value=False,
            command=self.update_mannschaften_tree
        ).pack(side=tk.LEFT, padx=4)
        ttk.Radiobutton(
            mode_sub,
            text="Nach Mannschaftsklassen",
            variable=self.wertung_group_by_klasse_var,
            value=True,
            command=self.update_mannschaften_tree
        ).pack(side=tk.LEFT, padx=4)

        ttk.Separator(wertung_frame, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=8)

        ttk.Checkbutton(
            wertung_frame,
            text="Einzelergebnisse der Mannschaftsmitglieder einbeziehen",
            variable=self.wertung_show_einzel_var
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(
            wertung_frame,
            text="📄 PDF Mannschaftswertung erstellen",
            command=self.create_mannschaft_pdf
        ).pack(side=tk.RIGHT, padx=5, ipadx=6, ipady=3)

        ttk.Button(
            wertung_frame,
            text="🏆 Mannschaftswertung anzeigen",
            command=self.open_mannschaftswertung
        ).pack(side=tk.RIGHT, padx=5, ipadx=6, ipady=3)

        # 3. Mittlerer Hauptbereich: Links Mannschaft anlegen/bearbeiten, Rechts Liste der Mannschaften
        middle_paned = ttk.Frame(self.frame)
        middle_paned.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        middle_paned.columnconfigure(0, weight=3)
        middle_paned.columnconfigure(1, weight=2)
        middle_paned.rowconfigure(0, weight=1)

        # --- Linker Bereich: Mannschaft anlegen / bearbeiten & Schützen zuordnen ---
        editor_frame = ttk.LabelFrame(
            middle_paned,
            text="Mannschaft anlegen / bearbeiten & Schützen zuordnen",
            padding="8"
        )
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.rowconfigure(1, weight=1)

        # Name + Mannschaftsklasse
        form_row = ttk.Frame(editor_frame)
        form_row.grid(row=0, column=0, sticky="ew", pady=(0, 6))
        form_row.columnconfigure(1, weight=1)
        form_row.columnconfigure(3, weight=1)

        ttk.Label(form_row, text="Mannschaftsname:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.team_name_entry = ttk.Entry(form_row, width=24)
        self.team_name_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))

        ttk.Label(form_row, text="Mannschaftsklasse:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.team_klasse_combo = ttk.Combobox(form_row, width=20, state="readonly")
        self.team_klasse_combo.grid(row=0, column=3, sticky="ew")

        # Schützen-Auswahl (links verfügbare Schützen, Mitte Buttons, rechts Mitglieder der Mannschaft)
        selection_area = ttk.Frame(editor_frame)
        selection_area.grid(row=1, column=0, sticky="nsew")
        selection_area.columnconfigure(0, weight=3)
        selection_area.columnconfigure(1, weight=0)
        selection_area.columnconfigure(2, weight=2)
        selection_area.rowconfigure(1, weight=1)

        # Suchfeld für angelegte Schützen
        search_bar = ttk.Frame(selection_area)
        search_bar.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        ttk.Label(search_bar, text="Schütze suchen:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_available_schuetzen_tree())
        ttk.Entry(search_bar, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.mitglieder_count_label = ttk.Label(
            selection_area,
            text="Zugeordnete Schützen (0 / 3):",
            font=("Arial", 9, "bold")
        )
        self.mitglieder_count_label.grid(row=0, column=2, sticky=tk.W, pady=(0, 4))

        # Liste: Angelegte Schützen
        avail_container = ttk.Frame(selection_area)
        avail_container.grid(row=1, column=0, sticky="nsew")

        avail_scroll = ttk.Scrollbar(avail_container, orient="vertical")
        self.available_tree = ttk.Treeview(
            avail_container,
            columns=("Name", "Vorname", "Klasse", "Verein", "Mannschaft"),
            show="headings",
            selectmode="extended",
            yscrollcommand=avail_scroll.set,
            height=10
        )
        self.available_tree.heading("Name", text="Name")
        self.available_tree.heading("Vorname", text="Vorname")
        self.available_tree.heading("Klasse", text="Klasse")
        self.available_tree.heading("Verein", text="Verein")
        self.available_tree.heading("Mannschaft", text="Mannschaft")
        self.available_tree.column("Name", width=85)
        self.available_tree.column("Vorname", width=85)
        self.available_tree.column("Klasse", width=70)
        self.available_tree.column("Verein", width=85)
        self.available_tree.column("Mannschaft", width=85)
        self.available_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        avail_scroll.config(command=self.available_tree.yview)
        avail_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.available_tree.bind("<Double-1>", lambda e: self.add_selected_schuetzen_to_team())

        # Buttons dazwischen
        transfer_btns = ttk.Frame(selection_area, padding="4")
        transfer_btns.grid(row=1, column=1, sticky="ns")

        ttk.Button(
            transfer_btns,
            text="Hinzufügen ➡",
            command=self.add_selected_schuetzen_to_team
        ).pack(pady=(30, 6), fill=tk.X)

        ttk.Button(
            transfer_btns,
            text="⬅ Entfernen",
            command=self.remove_selected_schuetze_from_team
        ).pack(pady=6, fill=tk.X)

        # Liste: Zugeordnete Schützen dieser Mannschaft
        members_container = ttk.Frame(selection_area)
        members_container.grid(row=1, column=2, sticky="nsew")

        members_scroll = ttk.Scrollbar(members_container, orient="vertical")
        self.mitglieder_tree = ttk.Treeview(
            members_container,
            columns=("Schütze", "Klasse", "Ergebnis"),
            show="headings",
            yscrollcommand=members_scroll.set,
            height=10
        )
        self.mitglieder_tree.heading("Schütze", text="Schütze")
        self.mitglieder_tree.heading("Klasse", text="Klasse")
        self.mitglieder_tree.heading("Ergebnis", text="Ringe")
        self.mitglieder_tree.column("Schütze", width=130)
        self.mitglieder_tree.column("Klasse", width=70)
        self.mitglieder_tree.column("Ergebnis", width=55, anchor=tk.CENTER)
        self.mitglieder_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        members_scroll.config(command=self.mitglieder_tree.yview)
        members_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.mitglieder_tree.bind("<Double-1>", lambda e: self.remove_selected_schuetze_from_team())

        # Editor-Buttons unten
        editor_btn_frame = ttk.Frame(editor_frame)
        editor_btn_frame.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        self.save_team_btn = ttk.Button(
            editor_btn_frame,
            text="💾 Mannschaft anlegen / Schützen zuordnen",
            command=self.save_mannschaft
        )
        self.save_team_btn.pack(side=tk.LEFT, padx=(0, 8), ipadx=6, ipady=3)

        ttk.Button(
            editor_btn_frame,
            text="🔄 Neue Mannschaft (Eingabe leeren)",
            command=self.clear_team_form
        ).pack(side=tk.LEFT, padx=4, ipady=3)

        # --- Rechter Bereich: Vorhandene Mannschaften & Live-Gesamtergebnis ---
        teams_frame = ttk.LabelFrame(
            middle_paned,
            text="Angelegte Mannschaften (Übersicht & Wertung)",
            padding="8"
        )
        teams_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        teams_frame.columnconfigure(0, weight=1)
        teams_frame.rowconfigure(0, weight=1)

        teams_tree_container = ttk.Frame(teams_frame)
        teams_tree_container.grid(row=0, column=0, sticky="nsew")

        teams_scroll = ttk.Scrollbar(teams_tree_container, orient="vertical")
        self.mannschaften_tree = ttk.Treeview(
            teams_tree_container,
            columns=("Platz", "Name", "Klasse", "Schützen", "Mitglieder", "Gesamt"),
            show="headings",
            yscrollcommand=teams_scroll.set,
            height=12
        )
        self.mannschaften_tree.heading("Platz", text="Platz")
        self.mannschaften_tree.heading("Name", text="Mannschaft")
        self.mannschaften_tree.heading("Klasse", text="Mannschaftsklasse")
        self.mannschaften_tree.heading("Schützen", text="Anzahl")
        self.mannschaften_tree.heading("Mitglieder", text="Schützen")
        self.mannschaften_tree.heading("Gesamt", text="Gesamt")

        self.mannschaften_tree.column("Platz", width=45, anchor=tk.CENTER)
        self.mannschaften_tree.column("Name", width=110)
        self.mannschaften_tree.column("Klasse", width=95)
        self.mannschaften_tree.column("Schützen", width=60, anchor=tk.CENTER)
        self.mannschaften_tree.column("Mitglieder", width=140)
        self.mannschaften_tree.column("Gesamt", width=60, anchor=tk.CENTER)

        self.mannschaften_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        teams_scroll.config(command=self.mannschaften_tree.yview)
        teams_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.mannschaften_tree.bind("<<TreeviewSelect>>", self.on_mannschaft_selected)
        self.mannschaften_tree.bind("<Double-1>", lambda e: self.edit_selected_mannschaft())

        teams_btn_frame = ttk.Frame(teams_frame)
        teams_btn_frame.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        ttk.Button(
            teams_btn_frame,
            text="✏ Bearbeiten",
            command=self.edit_selected_mannschaft
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            teams_btn_frame,
            text="🗑 Mannschaft löschen",
            command=self.delete_selected_mannschaft
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            teams_btn_frame,
            text="Alle löschen",
            command=self.delete_all_mannschaften
        ).pack(side=tk.LEFT, padx=5)

        self.refresh()

    # --- Methoden für Mannschaftsgröße ---

    def save_mannschaft_groesse(self):
        """Speichert die konfigurierte Teilnehmeranzahl pro Mannschaft"""
        try:
            groesse = int(self.groesse_spinbox.get().strip())
            if groesse < 1:
                raise ValueError()
        except ValueError:
            messagebox.showwarning(
                "Eingabefehler",
                "Bitte geben Sie eine gültige Teilnehmeranzahl (mindestens 1) ein!"
            )
            return

        # Prüfen ob bestehende Mannschaften mehr Mitglieder haben
        zu_grosse = [
            m['name'] for m in self.turnier_model.get_all_mannschaften()
            if len(m.get('mitglieder', [])) > groesse
        ]
        if zu_grosse:
            messagebox.showwarning(
                "Hinweis",
                f"Folgende Mannschaften haben aktuell mehr als {groesse} Schützen:\n"
                f"{', '.join(zu_grosse)}\n\n"
                f"Bitte passen Sie diese Mannschaften bei Bedarf an."
            )

        self.turnier_model.set_mannschaft_groesse(groesse)
        self.groesse_var.set(groesse)
        self.groesse_info_label.config(text=f"Aktuell: max. {groesse} Schützen pro Mannschaft")
        self.update_mitglieder_tree()
        self.update_mannschaften_tree()
        messagebox.showinfo("Erfolg", f"Mannschaftsgröße wurde auf {groesse} Teilnehmer festgelegt!")

    # --- Methoden für Mannschaftsklassen ---

    def add_mannschaftsklasse(self):
        """Legt eine neue Mannschaftsklasse an"""
        name = self.mk_entry.get().strip()
        if not name:
            messagebox.showwarning("Eingabefehler", "Bitte einen Namen für die Mannschaftsklasse eingeben!")
            return

        if self.turnier_model.add_mannschaftsklasse(name):
            self.mk_entry.delete(0, tk.END)
            self.update_mannschaftsklassen_ui()
            self.team_klasse_combo.set(name)
            messagebox.showinfo("Erfolg", f"Mannschaftsklasse '{name}' wurde angelegt!")
        else:
            messagebox.showwarning("Duplikat", f"Die Mannschaftsklasse '{name}' existiert bereits!")

    def delete_mannschaftsklasse(self):
        """Löscht die ausgewählte Mannschaftsklasse"""
        selected = self.mk_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Mannschaftsklasse zum Löschen aus!")
            return

        klasse_name = self.mk_tree.item(selected[0], "values")[0]
        betroffene = [
            m['name'] for m in self.turnier_model.get_all_mannschaften()
            if m.get('klasse') == klasse_name
        ]
        if betroffene:
            if not messagebox.askyesno(
                "Warnung",
                f"Es sind {len(betroffene)} Mannschaft(en) dieser Mannschaftsklasse zugeordnet.\n"
                f"Möchten Sie die Mannschaftsklasse '{klasse_name}' trotzdem löschen?"
            ):
                return

        self.turnier_model.remove_mannschaftsklasse(klasse_name)
        self.update_mannschaftsklassen_ui()
        self.update_mannschaften_tree()

    def update_mannschaftsklassen_ui(self):
        """Aktualisiert Treeview und Combobox der Mannschaftsklassen"""
        for item in self.mk_tree.get_children():
            self.mk_tree.delete(item)

        klassen_names = self.turnier_model.get_mannschaftsklassen_names()
        for name in klassen_names:
            self.mk_tree.insert("", tk.END, values=(name,))

        combo_values = [self.KEINE_KLASSE_LABEL] + klassen_names
        current = self.team_klasse_combo.get()
        self.team_klasse_combo['values'] = combo_values
        if current in combo_values:
            self.team_klasse_combo.set(current)
        elif klassen_names:
            self.team_klasse_combo.set(klassen_names[0])
        else:
            self.team_klasse_combo.set(self.KEINE_KLASSE_LABEL)

    # --- Methoden für Schützenauswahl & Mannschaften ---

    def _get_current_max_groesse(self):
        """Liest die aktuelle Mannschaftsgröße (inkl. Spinbox-Wert falls gültig)"""
        try:
            val = int(self.groesse_spinbox.get().strip())
            if val >= 1:
                self.turnier_model.set_mannschaft_groesse(val)
                self.groesse_info_label.config(text=f"Aktuell: max. {val} Schützen pro Mannschaft")
                return val
        except ValueError:
            pass
        return self.turnier_model.get_mannschaft_groesse()

    def add_selected_schuetzen_to_team(self):
        """Fügt die in der Schützenliste ausgewählten Schützen zur aktuellen Mannschaftsauswahl hinzu"""
        selected = self.available_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie mindestens einen Schützen aus der Liste aus!")
            return

        max_groesse = self._get_current_max_groesse()

        for item_id in selected:
            if item_id in self.current_mitglieder:
                continue

            if len(self.current_mitglieder) >= max_groesse:
                messagebox.showwarning(
                    "Maximale Teilnehmerzahl erreicht",
                    f"Es können maximal {max_groesse} Schützen einer Mannschaft zugeordnet werden!"
                )
                break

            self.current_mitglieder.append(item_id)

        self.update_mitglieder_tree()
        self.update_available_schuetzen_tree()

    def remove_selected_schuetze_from_team(self):
        """Entfernt den ausgewählten Schützen aus der aktuellen Mannschaftsauswahl"""
        selected = self.mitglieder_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Keine Auswahl",
                "Bitte wählen Sie einen zugeordneten Schützen aus, der entfernt werden soll!"
            )
            return

        for item_id in selected:
            if item_id in self.current_mitglieder:
                self.current_mitglieder.remove(item_id)

        self.update_mitglieder_tree()
        self.update_available_schuetzen_tree()

    def save_mannschaft(self):
        """Speichert eine neue oder bearbeitete Mannschaft inklusive Schützenzuordnung"""
        name = self.team_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Eingabefehler", "Der Mannschaft muss ein Name gegeben werden!")
            return

        max_groesse = self._get_current_max_groesse()

        # Falls der Benutzer Schützen links markiert hat, ohne vorher auf "Hinzufügen ➡" zu klicken,
        # übernehmen wir diese Auswahl direkt.
        if not self.current_mitglieder and self.available_tree.selection():
            selected_ids = list(self.available_tree.selection())
            if len(selected_ids) > max_groesse:
                messagebox.showwarning(
                    "Zu viele Schützen ausgewählt",
                    f"Es können maximal {max_groesse} Schützen einer Mannschaft zugeordnet werden!"
                )
                return
            self.current_mitglieder = selected_ids
            self.update_mitglieder_tree()

        if len(self.current_mitglieder) > max_groesse:
            messagebox.showwarning(
                "Zu viele Schützen",
                f"Es können maximal {max_groesse} Schützen einer Mannschaft zugeordnet werden!\n"
                f"Aktuell ausgewählt: {len(self.current_mitglieder)}."
            )
            return

        klasse_raw = self.team_klasse_combo.get().strip()
        klasse = "" if klasse_raw == self.KEINE_KLASSE_LABEL else klasse_raw

        # Prüfung auf Duplikat-Namen vor der Warnmeldung
        all_teams = self.turnier_model.get_all_mannschaften()
        for idx, existing in enumerate(all_teams):
            if idx != self.editing_index and existing['name'].lower() == name.lower():
                messagebox.showwarning(
                    "Duplikat",
                    f"Eine Mannschaft mit dem Namen '{name}' existiert bereits!"
                )
                return

        # Warnung wenn zu wenige Schützen in der Mannschaft sind (Zuordnung trotzdem möglich!)
        if len(self.current_mitglieder) < max_groesse:
            messagebox.showwarning(
                "Warnung: Zu wenige Schützen",
                f"In der Mannschaft '{name}' sind nur {len(self.current_mitglieder)} von "
                f"{max_groesse} konfigurierten Schützen zugeordnet.\n\n"
                f"Die Schützen werden der Mannschaft trotzdem zugeordnet."
            )

        if self.editing_index is not None:
            success = self.turnier_model.update_mannschaft(
                self.editing_index,
                name,
                klasse=klasse,
                mitglieder=self.current_mitglieder
            )
            if success:
                messagebox.showinfo("Erfolg", f"Mannschaft '{name}' wurde aktualisiert!")
                self.clear_team_form()
        else:
            success = self.turnier_model.add_mannschaft(
                name,
                klasse=klasse,
                mitglieder=self.current_mitglieder
            )
            if success:
                messagebox.showinfo("Erfolg", f"Mannschaft '{name}' wurde angelegt!")
                self.clear_team_form()

        self.refresh_silent_update()

    def clear_team_form(self):
        """Setzt das Formular zum Anlegen einer neuen Mannschaft zurück"""
        self.editing_index = None
        self.current_mitglieder = []
        self.team_name_entry.delete(0, tk.END)
        klassen_names = self.turnier_model.get_mannschaftsklassen_names()
        if klassen_names:
            self.team_klasse_combo.set(klassen_names[0])
        else:
            self.team_klasse_combo.set(self.KEINE_KLASSE_LABEL)
        self.save_team_btn.config(text="💾 Mannschaft anlegen / Schützen zuordnen")
        if self.mannschaften_tree.selection():
            self.mannschaften_tree.selection_remove(self.mannschaften_tree.selection())
        self.update_mitglieder_tree()
        self.update_available_schuetzen_tree()

    def on_mannschaft_selected(self, event=None):
        """Lädt die ausgewählte Mannschaft in die Bearbeitungsansicht"""
        selected = self.mannschaften_tree.selection()
        if not selected:
            return
        try:
            index = int(selected[0])
        except ValueError:
            return
        self._load_mannschaft_into_form(index)

    def edit_selected_mannschaft(self):
        """Lädt die ausgewählte Mannschaft zum Bearbeiten"""
        selected = self.mannschaften_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Mannschaft aus!")
            return
        try:
            index = int(selected[0])
        except ValueError:
            return
        self._load_mannschaft_into_form(index)

    def _load_mannschaft_into_form(self, index):
        """Befüllt die Eingabefelder mit den Daten der Mannschaft am gegebenen Index"""
        mannschaft = self.turnier_model.get_mannschaft(index)
        if not mannschaft:
            return

        self.editing_index = index
        self.team_name_entry.delete(0, tk.END)
        self.team_name_entry.insert(0, mannschaft['name'])

        klasse = mannschaft.get('klasse', '').strip()
        if klasse:
            self.team_klasse_combo.set(klasse)
        else:
            self.team_klasse_combo.set(self.KEINE_KLASSE_LABEL)

        self.current_mitglieder = list(mannschaft.get('mitglieder', []))
        self.save_team_btn.config(text="💾 Mannschaft aktualisieren / Schützen zuordnen")
        self.update_mitglieder_tree()
        self.update_available_schuetzen_tree()

    def delete_selected_mannschaft(self):
        """Löscht die ausgewählte Mannschaft"""
        selected = self.mannschaften_tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Mannschaft zum Löschen aus!")
            return

        try:
            index = int(selected[0])
        except ValueError:
            return

        mannschaft = self.turnier_model.get_mannschaft(index)
        if not mannschaft:
            return

        if messagebox.askyesno(
            "Bestätigung",
            f"Möchten Sie die Mannschaft '{mannschaft['name']}' wirklich löschen?"
        ):
            self.turnier_model.remove_mannschaft(index)
            self.clear_team_form()
            self.refresh_silent_update()

    def delete_all_mannschaften(self):
        """Löscht alle angelegten Mannschaften"""
        if not self.turnier_model.get_all_mannschaften():
            messagebox.showinfo("Info", "Es sind keine Mannschaften vorhanden!")
            return

        if messagebox.askyesno("Bestätigung", "Möchten Sie wirklich ALLE Mannschaften löschen?"):
            self.turnier_model.clear_mannschaften()
            self.clear_team_form()
            self.refresh_silent_update()

    # --- UI-Update-Methoden ---

    def update_available_schuetzen_tree(self):
        """Aktualisiert die Liste der angelegten Schützen"""
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)

        filter_text = self.search_var.get().strip().lower()
        all_schuetzen = self.schuetze_model.get_all_schuetzen()

        for s in all_schuetzen:
            s_id = SchuetzeModel.get_schuetze_id(s)
            if filter_text:
                haystack = f"{s.get('name', '')} {s.get('vorname', '')} {s.get('klasse', '')} {s.get('verein', '')}".lower()
                if filter_text not in haystack:
                    continue

            teams = self.turnier_model.get_mannschaft_for_schuetze(s_id)
            team_str = ", ".join(teams) if teams else "-"

            self.available_tree.insert(
                "",
                tk.END,
                iid=s_id,
                values=(
                    s.get('name', ''),
                    s.get('vorname', ''),
                    s.get('klasse', ''),
                    s.get('verein', ''),
                    team_str
                )
            )

    def update_mitglieder_tree(self):
        """Aktualisiert die Liste der Schützen in der aktuell bearbeiteten Mannschaft"""
        for item in self.mitglieder_tree.get_children():
            self.mitglieder_tree.delete(item)

        max_groesse = self.turnier_model.get_mannschaft_groesse()
        all_schuetzen = self.schuetze_model.get_all_schuetzen()
        schuetzen_by_id = {SchuetzeModel.get_schuetze_id(s): s for s in all_schuetzen}

        valid_mitglieder = []
        for s_id in self.current_mitglieder:
            s = schuetzen_by_id.get(s_id)
            if not s:
                continue
            valid_mitglieder.append(s_id)
            erg = self.turnier_model.get_ergebnis(s_id)
            ringe = sum(erg.get('passen', [])) if erg else 0
            self.mitglieder_tree.insert(
                "",
                tk.END,
                iid=s_id,
                values=(
                    f"{s.get('vorname', '')} {s.get('name', '')}".strip(),
                    s.get('klasse', ''),
                    str(int(ringe))
                )
            )

        self.current_mitglieder = valid_mitglieder
        count = len(self.current_mitglieder)
        warn_suffix = " ⚠ (zu wenig)" if 0 < count < max_groesse else ""
        self.mitglieder_count_label.config(
            text=f"Zugeordnete Schützen ({count} / {max_groesse}){warn_suffix}:"
        )

    def update_mannschaften_tree(self):
        """Aktualisiert die Übersichtstabelle aller Mannschaften inklusive Platzierung und Gesamtergebnis"""
        for item in self.mannschaften_tree.get_children():
            self.mannschaften_tree.delete(item)

        max_groesse = self.turnier_model.get_mannschaft_groesse()
        all_schuetzen = self.schuetze_model.get_all_schuetzen()
        schuetzen_by_id = {SchuetzeModel.get_schuetze_id(s): s for s in all_schuetzen}

        group_by_klasse = self.wertung_group_by_klasse_var.get()
        grouped_results = self.turnier_model.calculate_mannschaft_results(
            self.schuetze_model,
            group_by_klasse=group_by_klasse
        )

        # Map von Mannschaftsname -> berechnetes Ergebnis & Platz
        calc_by_name = {}
        for _, teams in grouped_results.items():
            for t in teams:
                calc_by_name[t['name']] = t

        all_mannschaften = self.turnier_model.get_all_mannschaften()
        # Sortiere Anzeige nach Platzierung (bzw. Klasse + Platzierung)
        indexed_teams = list(enumerate(all_mannschaften))
        if group_by_klasse:
            indexed_teams.sort(
                key=lambda item: (
                    item[1].get('klasse') or "Ohne Klasse",
                    calc_by_name.get(item[1]['name'], {}).get('platz', 9999)
                )
            )
        else:
            indexed_teams.sort(
                key=lambda item: calc_by_name.get(item[1]['name'], {}).get('platz', 9999)
            )

        for orig_idx, m in indexed_teams:
            calc = calc_by_name.get(m['name'], {})
            platz = calc.get('platz', '-')
            gesamt = calc.get('gesamt', 0)

            mitglieder_ids = m.get('mitglieder', [])
            mitglieder_namen = []
            for s_id in mitglieder_ids:
                s = schuetzen_by_id.get(s_id)
                if s:
                    mitglieder_namen.append(f"{s.get('vorname', '')} {s.get('name', '')}".strip())

            anz = len(mitglieder_namen)
            anz_str = f"{anz}/{max_groesse}" if anz >= max_groesse else f"⚠ {anz}/{max_groesse}"

            self.mannschaften_tree.insert(
                "",
                tk.END,
                iid=str(orig_idx),
                values=(
                    str(platz),
                    m['name'],
                    m.get('klasse') or "-",
                    anz_str,
                    ", ".join(mitglieder_namen),
                    str(int(gesamt))
                )
            )

    # --- Mannschaftswertung & PDF ---

    def open_mannschaftswertung(self):
        """Öffnet das Fenster mit der ausführlichen Mannschaftswertung"""
        if not self.turnier_model.get_all_mannschaften():
            messagebox.showinfo("Keine Mannschaften", "Es sind noch keine Mannschaften angelegt!")
            return

        from .mannschaft_ergebnisse_window import MannschaftsErgebnisWindow
        self.mannschaft_ergebnis_window = MannschaftsErgebnisWindow(
            self.frame,
            self.turnier_model,
            self.schuetze_model,
            initial_group_by_klasse=self.wertung_group_by_klasse_var.get(),
            initial_show_einzel=self.wertung_show_einzel_var.get()
        )

    def create_mannschaft_pdf(self):
        """Erstellt direkt ein PDF der Mannschaftswertung mit den gewählten Einstellungen"""
        if not self.turnier_model.get_all_mannschaften():
            messagebox.showinfo("Keine Mannschaften", "Es sind noch keine Mannschaften angelegt!")
            return

        group_by_klasse = self.wertung_group_by_klasse_var.get()
        show_einzel = self.wertung_show_einzel_var.get()

        mannschaft_ergebnisse = self.turnier_model.calculate_mannschaft_results(
            self.schuetze_model,
            group_by_klasse=group_by_klasse
        )
        pdf_generator = PDFGenerator(self.turnier_model)
        pdf_generator.create_mannschaft_pdf(
            mannschaft_ergebnisse,
            show_einzel=show_einzel,
            group_by_klasse=group_by_klasse
        )

    def refresh(self):
        """Aktualisiert alle Elemente des Tabs"""
        groesse = self.turnier_model.get_mannschaft_groesse()
        self.groesse_var.set(groesse)
        self.groesse_info_label.config(text=f"Aktuell: max. {groesse} Schützen pro Mannschaft")
        self.update_mannschaftsklassen_ui()
        self.update_available_schuetzen_tree()
        self.update_mitglieder_tree()
        self.update_mannschaften_tree()

    def refresh_silent_update(self):
        """Aktualisiert Tabellen und ggf. offenes Wertungsfenster ohne Formular-Reset"""
        self.update_available_schuetzen_tree()
        self.update_mitglieder_tree()
        self.update_mannschaften_tree()
        if self.mannschaft_ergebnis_window and self.mannschaft_ergebnis_window.window.winfo_exists():
            self.mannschaft_ergebnis_window.refresh()
