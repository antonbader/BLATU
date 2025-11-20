# -*- coding: utf-8 -*-
"""
Dienstprogramm zur Erstellung von Word-Dokumenten aus Vorlagen
"""

import os
from docx import Document
from docxcompose.composer import Composer
import re

class WordGenerator:
    """Erstellt Word-Dokumente aus einer Vorlage."""

    def __init__(self, template_path):
        self.template_path = template_path

    def generate_certificate(self, output_path, data):
        """
        Erstellt eine einzelne Urkunde.
        :param output_path: Der Speicherpfad für die neue Word-Datei.
        :param data: Ein Dictionary mit den Platzhalter-Daten.
        """
        try:
            document = Document(self.template_path)
            self._replace_placeholders_in_document(document, data)
            document.save(output_path)
            return True, None
        except Exception as e:
            return False, str(e)

    def generate_schiesszettel(self, output_path, shooters_list, template_path, turnier_data):
        """
        Erstellt Schießzettel für eine Gruppe von Schützen in einer Datei.
        Verwendet docxcompose, um mehrere Seiten (eine pro 4 Schützen) zusammenzufügen.
        """
        try:
            # Sortieren nach Scheibe
            shooters_list.sort(key=lambda s: s.get('scheibe', 0))

            # Chunking in 4er Gruppen
            chunks = [shooters_list[i:i + 4] for i in range(0, len(shooters_list), 4)]

            master_doc = None
            composer = None

            for chunk in chunks:
                # Vorbereiten der Daten für diesen Chunk
                data = {}

                # Turnierdaten
                data["[Turniername]"] = turnier_data.get('name', '')
                data["[Turnierdatum]"] = turnier_data.get('datum', '')

                # Schützendaten
                for i in range(4):
                    suffix = f"_{i+1}"
                    if i < len(chunk):
                        schuetze = chunk[i]
                        data[f"[Name{suffix}]"] = str(schuetze.get('name', ''))
                        data[f"[Vorname{suffix}]"] = str(schuetze.get('vorname', ''))
                        data[f"[Gruppe{suffix}]"] = str(schuetze.get('gruppe', ''))
                        data[f"[Scheibe{suffix}]"] = str(schuetze.get('scheibe', ''))
                    else:
                        # Leere Platzhalter für fehlende Schützen
                        data[f"[Name{suffix}]"] = ""
                        data[f"[Vorname{suffix}]"] = ""
                        data[f"[Gruppe{suffix}]"] = ""
                        data[f"[Scheibe{suffix}]"] = ""

                # Dokument für diesen Chunk erstellen
                doc = Document(template_path)
                self._replace_placeholders_in_document(doc, data)

                # Mergen
                if master_doc is None:
                    master_doc = doc
                    composer = Composer(master_doc)
                else:
                    # Seiteumbruch im Master-Dokument hinzufügen, BEVOR das neue Dokument angehängt wird
                    master_doc.add_page_break()
                    composer.append(doc)

            if master_doc:
                composer.save(output_path)
                return True, None
            else:
                 # Fallback: Leeres Dokument oder Fehler, sollte nicht passieren wenn Liste nicht leer
                 return False, "Keine Schützen für Schießzettel vorhanden."

        except Exception as e:
            return False, str(e)

    def _replace_placeholders_in_document(self, document, data):
        """Ersetzt Platzhalter im gesamten Dokument (Paragraphen und Tabellen)."""
        # Paragraphs
        for p in document.paragraphs:
            for key, value in data.items():
                self._replace_placeholder_in_paragraph(p, key, str(value))

        # Tables
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for p in cell.paragraphs:
                        for key, value in data.items():
                            self._replace_placeholder_in_paragraph(p, key, str(value))

    def _replace_placeholder_in_paragraph(self, paragraph, placeholder, value):
        """Replaces a placeholder in a paragraph, handling split runs."""
        # This is a common and difficult problem in python-docx.
        # A robust solution combines the text of runs, performs replacement,
        # and then writes it back, trying to preserve formatting.

        full_text = ''.join(run.text for run in paragraph.runs)
        if placeholder in full_text:
            # Clear existing paragraph content
            for run in paragraph.runs:
                run.text = ''

            # Replace and add new content
            new_text = full_text.replace(placeholder, value)

            # Add a new run. This might lose some formatting nuances if the original
            # paragraph had mixed formatting. For simple placeholders, this is fine.
            paragraph.add_run(new_text)
