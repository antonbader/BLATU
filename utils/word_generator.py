# -*- coding: utf-8 -*-
"""
Dienstprogramm zur Erstellung von Word-Dokumenten aus Vorlagen
"""

import os
from docx import Document
import re

class WordGenerator:
    """Erstellt Word-Dokumente aus einer Vorlage."""

    def __init__(self, template_path):
        self.template_path = template_path

    def _replace_placeholder(self, paragraph, placeholder, value):
        """Ersetzt einen Platzhalter in einem Paragraphen, auch wenn er über mehrere Runs verteilt ist."""
        # Regex to find placeholder text, including the brackets
        placeholder_regex = re.compile(re.escape(placeholder))

        # We need to work with the full text of the paragraph to find the placeholder
        full_text = ''.join(run.text for run in paragraph.runs)

        if placeholder_regex.search(full_text):
            # If found, clear the existing runs and add a new one with the replaced text
            # This will lose original formatting within the paragraph, but is robust for replacement.
            # A more complex implementation would be needed to preserve mixed formatting.

            # Find the starting run
            current_len = 0
            for run in paragraph.runs:
                if placeholder in run.text:
                    # Simple case: placeholder is within a single run
                    run.text = run.text.replace(placeholder, value)
                    return # Done with this paragraph

                # Check for placeholders spanning multiple runs
                # This part is complex. The simple approach below handles most cases.

            # If we reach here, the placeholder might be split.
            # A robust but format-losing way:
            new_text = full_text.replace(placeholder, value)

            # Clear all runs in the paragraph
            for run in paragraph.runs:
                run.text = ''

            # Add a new run with the updated text
            # This takes the style of the first original run
            if paragraph.runs:
                paragraph.runs[0].text = new_text
            else:
                paragraph.add_run(new_text)


    def generate_certificate(self, output_path, data):
        """
        Erstellt eine einzelne Urkunde.
        :param output_path: Der Speicherpfad für die neue Word-Datei.
        :param data: Ein Dictionary mit den Platzhalter-Daten.
        """
        try:
            document = Document(self.template_path)

            # Paragraphs
            for p in document.paragraphs:
                for key, value in data.items():
                    # Use a more robust replacement function
                    self._replace_placeholder_in_paragraph(p, key, str(value))

            # Tables
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            for key, value in data.items():
                                self._replace_placeholder_in_paragraph(p, key, str(value))

            document.save(output_path)
            return True, None
        except Exception as e:
            return False, str(e)

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
