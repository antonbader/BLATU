# -*- coding: utf-8 -*-
"""
Gruppenverwaltung Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox


class GruppenTab:
    """Tab für Gruppenverwaltung"""

    def __init__(self, parent, turnier_model, schuetze_model, pdf_generator, on_assignment_changed=None):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.pdf_generator = pdf_generator
        self.on_assignment_changed = on_assignment_changed
        self.frame = ttk.Frame(parent, padding="10")
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets"""
        ttk.Label(
            self.frame,
            text="Gruppenverwaltung",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)

        # Einstellungen für Gruppenanzahl und Anzeige leerer Plätze
        settings_frame = ttk.LabelFrame(self.frame, text="Gruppeneinstellungen & Anzeige", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(settings_frame, text="Vorgesehene Anzahl Gruppen:").pack(side=tk.LEFT, padx=(0, 5))
        self.anzahl_gruppen_var = tk.StringVar(value=str(self.turnier_model.get_anzahl_gruppen()))
        self.anzahl_gruppen_spinbox = ttk.Spinbox(
            settings_frame,
            from_=0,
            to=999,
            textvariable=self.anzahl_gruppen_var,
            width=6,
            command=self.apply_anzahl_gruppen
        )
        self.anzahl_gruppen_spinbox.pack(side=tk.LEFT, padx=5)
        self.anzahl_gruppen_spinbox.bind("<Return>", lambda e: self.apply_anzahl_gruppen())
        self.anzahl_gruppen_spinbox.bind("<FocusOut>", lambda e: self.apply_anzahl_gruppen())

        ttk.Button(
            settings_frame,
            text="Übernehmen",
            command=self.apply_anzahl_gruppen
        ).pack(side=tk.LEFT, padx=5)

        self.max_scheiben_info_label = ttk.Label(
            settings_frame,
            text=f"(Max. Scheiben pro Gruppe: {self.turnier_model.get_max_scheiben()})",
            foreground="gray"
        )
        self.max_scheiben_info_label.pack(side=tk.LEFT, padx=(10, 20))

        self.show_empty_ui_var = tk.BooleanVar(value=self.turnier_model.get_show_empty_slots_ui())
        self.show_empty_ui_check = ttk.Checkbutton(
            settings_frame,
            text="Leere Plätze in der Anzeige anzeigen",
            variable=self.show_empty_ui_var,
            command=self.on_empty_slots_option_changed
        )
        self.show_empty_ui_check.pack(side=tk.LEFT, padx=10)

        self.show_empty_pdf_var = tk.BooleanVar(value=self.turnier_model.get_show_empty_slots_pdf())
        self.show_empty_pdf_check = ttk.Checkbutton(
            settings_frame,
            text="Leere Plätze im Gruppen-PDF anzeigen",
            variable=self.show_empty_pdf_var,
            command=self.on_empty_slots_option_changed
        )
        self.show_empty_pdf_check.pack(side=tk.LEFT, padx=10)

        # Haupt-Frame für die Listen
        main_list_frame = ttk.Frame(self.frame)
        main_list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_list_frame.rowconfigure(0, weight=1)
        main_list_frame.columnconfigure(0, weight=3)  # Gruppenübersicht bekommt mehr Platz
        main_list_frame.columnconfigure(1, weight=1)

        # Listenbereich für zugewiesene Schützen
        list_frame = ttk.LabelFrame(main_list_frame, text="Gruppenübersicht", padding="10")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            list_frame,
            columns=("Gruppe", "Uhrzeit", "Scheibe", "Schütze", "Verein", "Klasse"),
            show="headings",
            yscrollcommand=scrollbar.set,
            height=18
        )
        self.tree.heading("Gruppe", text="Gruppe")
        self.tree.heading("Uhrzeit", text="Uhrzeit")
        self.tree.heading("Scheibe", text="Scheibe")
        self.tree.heading("Schütze", text="Schütze")
        self.tree.heading("Verein", text="Verein")
        self.tree.heading("Klasse", text="Klasse")
        self.tree.column("Gruppe", width=60, anchor="center")
        self.tree.column("Uhrzeit", width=80, anchor="center")
        self.tree.column("Scheibe", width=60, anchor="center")
        self.tree.column("Schütze", width=250)
        self.tree.column("Verein", width=150)
        self.tree.column("Klasse", width=120)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind("<<TreeviewSelect>>", self.on_schuetze_selected)

        # Listenbereich für nicht zugewiesene Schützen
        unassigned_frame = ttk.LabelFrame(main_list_frame, text="Nicht zugewiesene Schützen", padding="10")
        unassigned_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        unassigned_scrollbar = ttk.Scrollbar(unassigned_frame)
        unassigned_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.unassigned_tree = ttk.Treeview(
            unassigned_frame,
            columns=("Schütze", "Verein", "Klasse"),
            show="headings",
            yscrollcommand=unassigned_scrollbar.set,
            height=18
        )
        self.unassigned_tree.heading("Schütze", text="Schütze")
        self.unassigned_tree.heading("Verein", text="Verein")
        self.unassigned_tree.heading("Klasse", text="Klasse")
        self.unassigned_tree.column("Schütze", width=150)
        self.unassigned_tree.column("Verein", width=120)
        self.unassigned_tree.column("Klasse", width=100)
        self.unassigned_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        unassigned_scrollbar.config(command=self.unassigned_tree.yview)
        self.unassigned_tree.bind("<<TreeviewSelect>>", self.on_schuetze_selected)

        # Bearbeitungs-Frame
        edit_frame = ttk.Frame(self.frame)
        edit_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Uhrzeit-Eingabe
        time_frame = ttk.LabelFrame(edit_frame, text="Uhrzeit für Gruppe festlegen", padding="10")
        time_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Label(time_frame, text="Uhrzeit (HH:MM):").grid(row=0, column=0, padx=5)
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(time_frame, textvariable=self.time_var, width=10)
        self.time_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            time_frame,
            text="Für ausgewählte Gruppe speichern",
            command=self.save_group_time
        ).grid(row=0, column=2, padx=10)

        # Zuweisung ändern
        assign_frame = ttk.LabelFrame(edit_frame, text="Zuweisung für Schützen ändern", padding="10")
        assign_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

        ttk.Label(assign_frame, text="Gruppe:").grid(row=0, column=0, padx=5)
        self.gruppe_var = tk.StringVar()
        self.gruppe_entry = ttk.Entry(assign_frame, textvariable=self.gruppe_var, width=5)
        self.gruppe_entry.grid(row=0, column=1, padx=5)

        ttk.Label(assign_frame, text="Scheibe:").grid(row=0, column=2, padx=5)
        self.scheibe_var = tk.StringVar()
        self.scheibe_entry = ttk.Entry(assign_frame, textvariable=self.scheibe_var, width=5)
        self.scheibe_entry.grid(row=0, column=3, padx=5)

        ttk.Button(
            assign_frame,
            text="Zuweisung ändern",
            command=self.change_assignment
        ).grid(row=0, column=4, padx=(10, 5))

        ttk.Button(
            assign_frame,
            text="Zuweisung entfernen",
            command=self.remove_assignment
        ).grid(row=0, column=5, padx=5)

        # PDF-Buttons in einem eigenen Frame
        pdf_frame = ttk.Frame(self.frame)
        pdf_frame.grid(row=4, column=0, columnspan=3, pady=10)

        group_pdf_button = ttk.Button(
            pdf_frame,
            text="Gruppen-PDF erstellen",
            command=self.create_group_pdf
        )
        group_pdf_button.pack(side=tk.LEFT, padx=10)

        verein_pdf_button = ttk.Button(
            pdf_frame,
            text="Startliste Vereine",
            command=self.create_startliste_vereine_pdf
        )
        verein_pdf_button.pack(side=tk.LEFT, padx=10)

        # Grid-Konfiguration
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.refresh()

    def apply_anzahl_gruppen(self):
        """Übernimmt die eingegebene vorgesehene Anzahl an Gruppen"""
        raw = self.anzahl_gruppen_var.get().strip()
        if raw == "":
            val = 0
        else:
            try:
                val = int(raw)
                if val < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Fehler", "Die vorgesehene Anzahl an Gruppen muss eine Zahl >= 0 sein.")
                self.anzahl_gruppen_var.set(str(self.turnier_model.get_anzahl_gruppen()))
                return

        self.turnier_model.set_anzahl_gruppen(val)
        self.refresh()

    def on_empty_slots_option_changed(self):
        """Wird aufgerufen, wenn die Auswahl für leere Plätze (Anzeige / PDF) geändert wird"""
        self.turnier_model.set_show_empty_slots_ui(self.show_empty_ui_var.get())
        self.turnier_model.set_show_empty_slots_pdf(self.show_empty_pdf_var.get())
        self.refresh()

    def _get_group_from_tree_item(self, item_id):
        """Ermittelt die Gruppennummer für einen Eintrag in der Gruppenübersicht"""
        item = self.tree.item(item_id)
        gruppe = item['values'][0]
        if gruppe == "":
            children = self.tree.get_children()
            current_index = self.tree.index(item_id)
            for i in range(current_index, -1, -1):
                prev_item = self.tree.item(children[i])
                if prev_item['values'][0] != "":
                    gruppe = prev_item['values'][0]
                    break
        return gruppe

    def refresh(self):
        """Aktualisiert die Anzeige"""
        max_scheiben = self.turnier_model.get_max_scheiben()
        anzahl_gruppen = self.turnier_model.get_anzahl_gruppen()
        show_empty_ui = self.turnier_model.get_show_empty_slots_ui()
        show_empty_pdf = self.turnier_model.get_show_empty_slots_pdf()

        if self.anzahl_gruppen_var.get().strip() != str(anzahl_gruppen):
            self.anzahl_gruppen_var.set(str(anzahl_gruppen))
        self.show_empty_ui_var.set(show_empty_ui)
        self.show_empty_pdf_var.set(show_empty_pdf)
        self.max_scheiben_info_label.config(text=f"(Max. Scheiben pro Gruppe: {max_scheiben})")

        for item in self.tree.get_children():
            self.tree.delete(item)
        for item in self.unassigned_tree.get_children():
            self.unassigned_tree.delete(item)

        schuetzen = self.schuetze_model.get_all_schuetzen()

        assigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is not None]
        unassigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is None]

        # Zugewiesene Schützen nach Gruppe gruppieren
        assigned_schuetzen.sort(key=lambda s: (s.get('gruppe', 0), s.get('scheibe', 0)))
        groups = {}
        for s in assigned_schuetzen:
            gruppe = s.get('gruppe')
            try:
                gruppe = int(gruppe)
            except (ValueError, TypeError):
                pass
            if gruppe not in groups:
                groups[gruppe] = []
            groups[gruppe].append(s)

        # Alle darzustellenden Gruppen ermitteln:
        # Vorgesehene Gruppen (1..anzahl_gruppen) + alle Gruppen mit zugewiesenen Schützen
        planned_groups = set(range(1, anzahl_gruppen + 1))
        assigned_group_nums = {g for g in groups.keys() if isinstance(g, int)}
        all_gruppen = sorted(planned_groups | assigned_group_nums)

        for gruppe in all_gruppen:
            schuetzen_in_gruppe = groups.get(gruppe, [])
            group_time = self.turnier_model.get_group_time(gruppe)

            rows = []
            if show_empty_ui:
                by_scheibe = {}
                extra_schuetzen = []
                for s in schuetzen_in_gruppe:
                    sch_nr = s.get('scheibe')
                    try:
                        sch_nr_int = int(sch_nr)
                    except (ValueError, TypeError):
                        sch_nr_int = None

                    if sch_nr_int is not None and sch_nr_int > 0:
                        by_scheibe.setdefault(sch_nr_int, []).append(s)
                    else:
                        extra_schuetzen.append(s)

                all_scheiben = sorted(set(range(1, max_scheiben + 1)) | set(by_scheibe.keys()))
                for sch_nr in all_scheiben:
                    assigned_on_target = by_scheibe.get(sch_nr, [])
                    if assigned_on_target:
                        for s in assigned_on_target:
                            rows.append((
                                sch_nr,
                                f"{s.get('vorname', '')} {s.get('name', '')}".strip(),
                                s.get('verein', ''),
                                s.get('klasse', '')
                            ))
                    else:
                        rows.append((sch_nr, "", "", ""))

                for s in extra_schuetzen:
                    rows.append((
                        s.get('scheibe', ''),
                        f"{s.get('vorname', '')} {s.get('name', '')}".strip(),
                        s.get('verein', ''),
                        s.get('klasse', '')
                    ))
            else:
                for s in schuetzen_in_gruppe:
                    rows.append((
                        s.get('scheibe', ''),
                        f"{s.get('vorname', '')} {s.get('name', '')}".strip(),
                        s.get('verein', ''),
                        s.get('klasse', '')
                    ))
                if not rows and isinstance(gruppe, int) and gruppe <= anzahl_gruppen:
                    rows.append(("", "", "", ""))

            for i, (scheibe_val, schuetze_name, verein_val, klasse_val) in enumerate(rows):
                display_gruppe = gruppe if i == 0 else ""
                display_time = group_time if i == 0 else ""

                self.tree.insert("", tk.END, values=(
                    display_gruppe,
                    display_time,
                    scheibe_val,
                    schuetze_name,
                    verein_val,
                    klasse_val
                ))

        # Nicht zugewiesene Schützen
        for schuetze in unassigned_schuetzen:
            self.unassigned_tree.insert("", tk.END, values=(
                f"{schuetze.get('vorname', '')} {schuetze.get('name', '')}".strip(),
                schuetze.get('verein', ''),
                schuetze.get('klasse', '')
            ))

    def save_group_time(self):
        """Speichert die Uhrzeit für die ausgewählte Gruppe"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Eintrag in der Liste aus, um die Gruppe zu bestimmen.")
            return

        gruppe = self._get_group_from_tree_item(selected[0])
        if gruppe == "":
            messagebox.showwarning("Fehler", "Konnte die Gruppe nicht bestimmen.")
            return

        time_str = self.time_var.get()

        self.turnier_model.set_group_time(gruppe, time_str)
        self.refresh()
        messagebox.showinfo("Erfolg", f"Uhrzeit für Gruppe {gruppe} wurde gespeichert.")

    def create_group_pdf(self):
        """Erstellt ein PDF mit der Gruppenübersicht"""
        schuetzen = self.schuetze_model.get_all_schuetzen()
        assigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is not None]
        show_empty_pdf = self.turnier_model.get_show_empty_slots_pdf()
        anzahl_gruppen = self.turnier_model.get_anzahl_gruppen()
        max_scheiben = self.turnier_model.get_max_scheiben()

        if not assigned_schuetzen and not (show_empty_pdf and anzahl_gruppen > 0):
            messagebox.showinfo("Info", "Es sind keine Schützen Gruppen zugewiesen. Das PDF wird nicht erstellt.")
            return

        self.pdf_generator.generate_gruppen_pdf(
            assigned_schuetzen,
            show_empty_slots=show_empty_pdf,
            max_scheiben=max_scheiben,
            anzahl_gruppen=anzahl_gruppen
        )

    def create_startliste_vereine_pdf(self):
        """Erstellt die Vereins-Startlisten-PDFs"""
        schuetzen = self.schuetze_model.get_all_schuetzen()
        self.pdf_generator.generate_startliste_vereine_pdf(schuetzen)

    def on_schuetze_selected(self, event):
        """Wird aufgerufen, wenn ein Eintrag in einer der Listen ausgewählt wird"""
        widget = event.widget
        selected = widget.selection()
        if not selected:
            return

        item = widget.item(selected[0])
        values = item['values']

        if widget == self.tree:
            gruppe = self._get_group_from_tree_item(selected[0])
            scheibe = values[2]
            schuetze_name = str(values[3]).strip() if len(values) > 3 else ""

            self.gruppe_var.set(gruppe)
            self.scheibe_var.set(scheibe)
            self.time_var.set(self.turnier_model.get_group_time(gruppe))

            # Wenn ein belegter Platz ausgewählt wurde, Auswahl in der rechten Liste aufheben.
            # Bei Auswahl eines leeren Platzes bleibt ein evtl. rechts ausgewählter Schütze markiert,
            # damit man ihn direkt diesem freien Platz zuweisen kann.
            if schuetze_name and self.unassigned_tree.selection():
                self.unassigned_tree.selection_remove(self.unassigned_tree.selection())
        else:  # unassigned_tree
            # Wenn links ein belegter Platz ausgewählt war, Auswahl links aufheben und Felder leeren.
            # War links ein freier Platz ausgewählt, bleiben Gruppe & Scheibe für die schnelle Zuweisung erhalten.
            keep_free_target = False
            if self.tree.selection():
                left_item = self.tree.item(self.tree.selection()[0])
                left_vals = left_item.get('values', [])
                left_name = str(left_vals[3]).strip() if len(left_vals) > 3 else ""
                if not left_name:
                    keep_free_target = True
                self.tree.selection_remove(self.tree.selection())

            if not keep_free_target:
                self.gruppe_var.set("")
                self.scheibe_var.set("")

    def change_assignment(self):
        """Ändert die Zuweisung für den ausgewählten Schützen"""
        selected_assigned = self.tree.selection()
        selected_unassigned = self.unassigned_tree.selection()

        if not selected_assigned and not selected_unassigned:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen Schützen aus einer der Listen aus!")
            return

        # Bestimme, aus welcher Liste der Schütze kommt
        selected_tree = None
        selected_item = None
        name_index = 0
        verein_index = 1
        klasse_index = 2

        if selected_assigned:
            item_assigned = self.tree.item(selected_assigned[0])
            vals_assigned = item_assigned.get('values', [])
            assigned_name = str(vals_assigned[3]).strip() if len(vals_assigned) > 3 else ""
            if assigned_name:
                selected_tree = self.tree
                selected_item = selected_assigned[0]
                name_index = 3
                verein_index = 4
                klasse_index = 5
            elif selected_unassigned:
                selected_tree = self.unassigned_tree
                selected_item = selected_unassigned[0]
                name_index = 0
                verein_index = 1
                klasse_index = 2
            else:
                messagebox.showwarning(
                    "Leerer Platz ausgewählt",
                    "Auf dem ausgewählten Platz ist kein Schütze eingetragen.\n"
                    "Bitte wählen Sie einen Schützen aus, dem dieser Platz zugewiesen werden soll."
                )
                return
        else:
            selected_tree = self.unassigned_tree
            selected_item = selected_unassigned[0]
            name_index = 0
            verein_index = 1
            klasse_index = 2

        try:
            new_gruppe = int(self.gruppe_var.get()) if self.gruppe_var.get() else None
            new_scheibe = int(self.scheibe_var.get()) if self.scheibe_var.get() else None
        except ValueError:
            messagebox.showerror("Fehler", "Gruppe und Scheibe müssen Zahlen sein.")
            return

        if new_gruppe is None or new_scheibe is None:
            messagebox.showerror("Fehler", "Gruppe und Scheibe dürfen nicht leer sein.")
            return

        if new_gruppe <= 0 or new_scheibe <= 0:
            messagebox.showerror("Fehler", "Gruppe und Scheibe müssen größer als 0 sein.")
            return

        item = selected_tree.item(selected_item)
        values = item['values']
        schuetze_name_full = str(values[name_index]).strip()
        schuetze_verein = str(values[verein_index]).strip() if len(values) > verein_index else ""
        schuetze_klasse = str(values[klasse_index]).strip() if len(values) > klasse_index else ""

        # Finde den Schützen im Modell
        schuetzen = self.schuetze_model.get_all_schuetzen()
        schuetze_index = -1
        for i, s in enumerate(schuetzen):
            full_name = f"{s.get('vorname', '')} {s.get('name', '')}".strip()
            if (full_name == schuetze_name_full and
                str(s.get('verein', '')).strip() == schuetze_verein and
                str(s.get('klasse', '')).strip() == schuetze_klasse):
                schuetze_index = i
                break

        if schuetze_index == -1:
            for i, s in enumerate(schuetzen):
                full_name = f"{s.get('vorname', '')} {s.get('name', '')}".strip()
                if full_name == schuetze_name_full:
                    schuetze_index = i
                    break

        if schuetze_index == -1:
            messagebox.showerror("Fehler", "Ausgewählter Schütze konnte nicht gefunden werden.")
            return

        # Prüfung auf Doppelbelegung
        for i, s in enumerate(schuetzen):
            if s.get('gruppe') == new_gruppe and s.get('scheibe') == new_scheibe and i != schuetze_index:
                messagebox.showerror("Fehler", f"Scheibe {new_scheibe} in Gruppe {new_gruppe} ist bereits belegt.")
                return

        schuetze_to_update = self.schuetze_model.get_schuetze(schuetze_index)
        self.schuetze_model.update_schuetze(
            schuetze_index,
            schuetze_to_update['name'],
            schuetze_to_update['vorname'],
            schuetze_to_update['klasse'],
            schuetze_to_update['verein'],
            gruppe=new_gruppe,
            scheibe=new_scheibe
        )

        self.refresh()
        messagebox.showinfo("Erfolg", "Zuweisung wurde aktualisiert.")

        if self.on_assignment_changed:
            self.on_assignment_changed()

    def remove_assignment(self):
        """Entfernt die bestehende Gruppen- und Scheibenzuordnung für den ausgewählten Schützen"""
        selected_assigned = self.tree.selection()
        if not selected_assigned:
            if self.unassigned_tree.selection():
                messagebox.showinfo("Info", "Der ausgewählte Schütze hat aktuell keine Gruppenzuordnung.")
            else:
                messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie einen zugewiesenen Schützen in der Gruppenübersicht aus!")
            return

        selected_item = selected_assigned[0]
        item = self.tree.item(selected_item)
        values = item.get('values', [])
        schuetze_name_full = str(values[3]).strip() if len(values) > 3 else ""

        if not schuetze_name_full:
            messagebox.showwarning("Leerer Platz ausgewählt", "Auf dem ausgewählten Platz ist kein Schütze zugewiesen.")
            return

        gruppe = self._get_group_from_tree_item(selected_item)
        scheibe = values[2] if len(values) > 2 else None
        schuetze_verein = str(values[4]).strip() if len(values) > 4 else ""
        schuetze_klasse = str(values[5]).strip() if len(values) > 5 else ""

        try:
            gruppe_int = int(gruppe)
        except (ValueError, TypeError):
            gruppe_int = gruppe

        try:
            scheibe_int = int(scheibe)
        except (ValueError, TypeError):
            scheibe_int = scheibe

        schuetzen = self.schuetze_model.get_all_schuetzen()
        schuetze_index = -1

        # 1. Suche exakt über Gruppe, Scheibe und Name
        for i, s in enumerate(schuetzen):
            full_name = f"{s.get('vorname', '')} {s.get('name', '')}".strip()
            if (s.get('gruppe') == gruppe_int and
                s.get('scheibe') == scheibe_int and
                full_name == schuetze_name_full):
                schuetze_index = i
                break

        # 2. Fallback über Name, Verein und Klasse
        if schuetze_index == -1:
            for i, s in enumerate(schuetzen):
                full_name = f"{s.get('vorname', '')} {s.get('name', '')}".strip()
                if (full_name == schuetze_name_full and
                    str(s.get('verein', '')).strip() == schuetze_verein and
                    str(s.get('klasse', '')).strip() == schuetze_klasse):
                    schuetze_index = i
                    break

        if schuetze_index == -1:
            messagebox.showerror("Fehler", "Ausgewählter Schütze konnte nicht gefunden werden.")
            return

        schuetze_to_update = self.schuetze_model.get_schuetze(schuetze_index)
        self.schuetze_model.update_schuetze(
            schuetze_index,
            schuetze_to_update['name'],
            schuetze_to_update['vorname'],
            schuetze_to_update['klasse'],
            schuetze_to_update['verein'],
            gruppe=None,
            scheibe=None
        )

        self.gruppe_var.set("")
        self.scheibe_var.set("")
        self.refresh()
        messagebox.showinfo("Erfolg", f"Zuordnung für {schuetze_name_full} wurde entfernt.")

        if self.on_assignment_changed:
            self.on_assignment_changed()
