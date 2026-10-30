# -*- coding: utf-8 -*-
"""
PDF Settings Tab
Ermöglicht das Anpassen der Schriftgrößen getrennt für jedes PDF-Dokument
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import DEFAULT_PDF_FONT_SIZES


class PDFSettingsTab:
    """Tab für die Konfiguration der PDF-Schriftgrößen"""

    def __init__(self, parent, turnier_model):
        self.turnier_model = turnier_model
        self.frame = ttk.Frame(parent, padding="15")
        self.spinboxes = {
            "ergebnisliste": {},
            "gruppen": {},
            "vereine": {},
            "mannschaften": {}
        }
        self.create_widgets()

    def create_widgets(self):
        """Erstellt alle Widgets für die PDF-Schriftgrößen"""
        ttk.Label(
            self.frame,
            text="PDF Schriftgrößen-Einstellungen",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 5))

        ttk.Label(
            self.frame,
            text="Passen Sie hier die Schriftgrößen (in Punkt / pt) getrennt für jedes PDF-Dokument an.",
            font=("Arial", 10),
            foreground="gray"
        ).pack(pady=(0, 10))

        # Container für die vier PDF-Typen im 2x2-Raster
        cards_frame = ttk.Frame(self.frame)
        cards_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        cards_frame.columnconfigure(0, weight=1)
        cards_frame.columnconfigure(1, weight=1)
        cards_frame.rowconfigure(0, weight=1)
        cards_frame.rowconfigure(1, weight=1)

        # 1. Ergebnisliste PDF
        ergebnis_fields = [
            ("title", "Turniertitel:", DEFAULT_PDF_FONT_SIZES["ergebnisliste"]["title"]),
            ("subtitle", "Datum / Untertitel:", DEFAULT_PDF_FONT_SIZES["ergebnisliste"]["subtitle"]),
            ("heading", "Klassenüberschrift:", DEFAULT_PDF_FONT_SIZES["ergebnisliste"]["heading"]),
            ("table_header", "Tabellenkopf:", DEFAULT_PDF_FONT_SIZES["ergebnisliste"]["table_header"]),
            ("table_body", "Tabelleninhalt:", DEFAULT_PDF_FONT_SIZES["ergebnisliste"]["table_body"]),
        ]
        self._create_doc_section(
            cards_frame,
            row=0,
            col=0,
            doc_key="ergebnisliste",
            title="Ergebnisliste (PDF)",
            fields=ergebnis_fields
        )

        # 2. Gruppen-PDF
        gruppen_fields = [
            ("title", "Turniertitel:", DEFAULT_PDF_FONT_SIZES["gruppen"]["title"]),
            ("subtitle", "Datum / Untertitel:", DEFAULT_PDF_FONT_SIZES["gruppen"]["subtitle"]),
            ("heading", "Gruppenüberschrift:", DEFAULT_PDF_FONT_SIZES["gruppen"]["heading"]),
            ("table_header", "Tabellenkopf:", DEFAULT_PDF_FONT_SIZES["gruppen"]["table_header"]),
            ("table_body", "Tabelleninhalt:", DEFAULT_PDF_FONT_SIZES["gruppen"]["table_body"]),
        ]
        self._create_doc_section(
            cards_frame,
            row=0,
            col=1,
            doc_key="gruppen",
            title="Gruppen-PDF",
            fields=gruppen_fields
        )

        # 3. Startliste Vereine PDF
        vereine_fields = [
            ("title", "Turniertitel:", DEFAULT_PDF_FONT_SIZES["vereine"]["title"]),
            ("subtitle", "Datum / Untertitel:", DEFAULT_PDF_FONT_SIZES["vereine"]["subtitle"]),
            ("heading", "Vereinsüberschrift:", DEFAULT_PDF_FONT_SIZES["vereine"]["heading"]),
            ("table_header", "Tabellenkopf:", DEFAULT_PDF_FONT_SIZES["vereine"]["table_header"]),
            ("table_body", "Tabelleninhalt:", DEFAULT_PDF_FONT_SIZES["vereine"]["table_body"]),
            ("footer_text", "Startgeld- & Zahlungstext:", DEFAULT_PDF_FONT_SIZES["vereine"]["footer_text"]),
        ]
        self._create_doc_section(
            cards_frame,
            row=1,
            col=0,
            doc_key="vereine",
            title="Startliste Vereine (PDF)",
            fields=vereine_fields
        )

        # 4. Mannschaftswertung PDF
        mannschaften_fields = [
            ("title", "Turniertitel:", DEFAULT_PDF_FONT_SIZES["mannschaften"]["title"]),
            ("subtitle", "Datum / Untertitel:", DEFAULT_PDF_FONT_SIZES["mannschaften"]["subtitle"]),
            ("heading", "Klassen-/Wertungsüberschrift:", DEFAULT_PDF_FONT_SIZES["mannschaften"]["heading"]),
            ("table_header", "Tabellenkopf:", DEFAULT_PDF_FONT_SIZES["mannschaften"]["table_header"]),
            ("table_body", "Tabelleninhalt:", DEFAULT_PDF_FONT_SIZES["mannschaften"]["table_body"]),
        ]
        self._create_doc_section(
            cards_frame,
            row=1,
            col=1,
            doc_key="mannschaften",
            title="Mannschaftswertung (PDF)",
            fields=mannschaften_fields
        )

        # Buttons unten
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="💾 Einstellungen speichern",
            command=self.save_settings
        ).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        ttk.Button(
            button_frame,
            text="🔄 Standardwerte wiederherstellen",
            command=self.reset_defaults
        ).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        self.refresh()

    def _create_doc_section(self, parent, row, col, doc_key, title, fields):
        """Erstellt ein LabelFrame für einen PDF-Dokumenttyp"""
        padx = (0, 8) if col == 0 else (8, 0)
        section = ttk.LabelFrame(parent, text=title, padding="12")
        section.grid(row=row, column=col, sticky="nsew", padx=padx, pady=5)

        for row_idx, (field_key, label_text, default_val) in enumerate(fields):
            ttk.Label(section, text=label_text, font=("Arial", 10)).grid(
                row=row_idx, column=0, sticky=tk.W, pady=4, padx=(0, 10)
            )

            spinbox = ttk.Spinbox(
                section,
                from_=6,
                to=36,
                width=8,
                font=("Arial", 10),
                command=self._apply_silent
            )
            spinbox.grid(row=row_idx, column=1, sticky=tk.E, pady=4)
            spinbox.set(default_val)
            spinbox.bind("<FocusOut>", lambda e: self._apply_silent())
            spinbox.bind("<Return>", lambda e: self._apply_silent())

            ttk.Label(
                section,
                text=f"pt (Std: {default_val})",
                font=("Arial", 8),
                foreground="gray"
            ).grid(row=row_idx, column=2, sticky=tk.W, padx=(6, 0), pady=4)

            self.spinboxes[doc_key][field_key] = spinbox

        section.columnconfigure(0, weight=1)

    def _collect_values(self, strict=False):
        """Liest alle Spinbox-Werte aus."""
        result = {}
        for doc_key, fields in self.spinboxes.items():
            result[doc_key] = {}
            for field_key, spinbox in fields.items():
                raw = spinbox.get().strip()
                try:
                    val = int(raw)
                    if val < 6 or val > 48:
                        raise ValueError()
                    result[doc_key][field_key] = val
                except ValueError:
                    if strict:
                        raise ValueError(f"Ungültige Schriftgröße '{raw}' (erlaubt: 6 bis 48 pt).")
                    result[doc_key][field_key] = DEFAULT_PDF_FONT_SIZES[doc_key][field_key]
        return result

    def _apply_silent(self):
        """Übernimmt gültige Änderungen sofort im Modell."""
        try:
            values = self._collect_values(strict=False)
            self.turnier_model.set_pdf_font_sizes(values)
        except Exception:
            pass

    def save_settings(self):
        """Validiert und speichert die PDF-Schriftgrößen mit Bestätigung."""
        try:
            values = self._collect_values(strict=True)
        except ValueError as e:
            messagebox.showwarning("Eingabefehler", str(e))
            return

        self.turnier_model.set_pdf_font_sizes(values)
        messagebox.showinfo("Erfolg", "Die PDF-Schriftgrößen wurden gespeichert!")

    def reset_defaults(self):
        """Setzt alle PDF-Schriftgrößen auf die Standardwerte zurück."""
        if messagebox.askyesno(
            "Standardwerte wiederherstellen",
            "Möchten Sie alle PDF-Schriftgrößen auf die Standardwerte zurücksetzen?"
        ):
            self.turnier_model.reset_pdf_font_sizes()
            self.refresh()
            messagebox.showinfo("Erfolg", "Die Standard-Schriftgrößen wurden wiederhergestellt!")

    def refresh(self):
        """Aktualisiert die Spinboxen mit den Werten aus dem TurnierModel."""
        current_sizes = self.turnier_model.get_pdf_font_sizes()
        for doc_key, fields in self.spinboxes.items():
            doc_sizes = current_sizes.get(doc_key, DEFAULT_PDF_FONT_SIZES.get(doc_key, {}))
            for field_key, spinbox in fields.items():
                default_val = DEFAULT_PDF_FONT_SIZES[doc_key][field_key]
                spinbox.set(doc_sizes.get(field_key, default_val))
