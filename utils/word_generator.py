# -*- coding: utf-8 -*-
"""
Dienstprogramm zur Erstellung von Word-Dokumenten aus Vorlagen
"""

import os
from docx import Document

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

            for p in document.paragraphs:
                for key, value in data.items():
                    if key in p.text:
                        inline = p.runs
                        # Replace strings and retain formatting
                        for i in range(len(inline)):
                            if key in inline[i].text:
                                text = inline[i].text.replace(key, str(value))
                                inline[i].text = text

            # Tabellen durchsuchen
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            for key, value in data.items():
                                if key in p.text:
                                    inline = p.runs
                                    # Replace strings and retain formatting
                                    for i in range(len(inline)):
                                        if key in inline[i].text:
                                            text = inline[i].text.replace(key, str(value))
                                            inline[i].text = text

            document.save(output_path)
            return True, None
        except Exception as e:
            return False, str(e)
