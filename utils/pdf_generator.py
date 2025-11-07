# -*- coding: utf-8 -*-
"""
PDF-Generator für Ergebnislisten
"""

from datetime import datetime
from tkinter import filedialog, messagebox
import os

from config import (FILE_TYPES_PDF, MAX_PASSEN_FOR_DISPLAY,
                    PDF_COLOR_HEADER, PDF_COLOR_GOLD, PDF_COLOR_SILVER, 
                    PDF_COLOR_BRONZE, PDF_COLOR_ROW_ALT)


class PDFGenerator:
    """Generiert PDF-Ergebnislisten"""
    
    def __init__(self, turnier_model):
        self.turnier_model = turnier_model
    
    def create_pdf(self, klassen_ergebnisse):
        """Erstellt ein PDF mit allen Ergebnissen"""
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, 
                                           Paragraph, Spacer, PageBreak)
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER
        except ImportError:
            messagebox.showerror(
                "Fehler", 
                "Die reportlab-Bibliothek ist nicht installiert.\n\n"
                "Bitte installieren Sie sie mit:\npip install reportlab"
            )
            return
        
        turnier = self.turnier_model.get_turnier_data()
        
        # Dateiname Dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=FILE_TYPES_PDF,
            title="PDF speichern",
            initialfile=f"Ergebnisse_{turnier.get('name', 'Turnier').replace(' ', '_')}.pdf"
        )
        
        if not file_path:
            return
        
        try:
            # PDF erstellen
            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=1*cm,
                leftMargin=1*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )
            
            elements = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            class_style = ParagraphStyle(
                'ClassTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            note_style = ParagraphStyle(
                'Note',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#666666'),
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )
            
            # Passen-Details anzeigen? (Wird überschrieben wenn show_halves aktiv ist)
            show_halves = turnier.get('show_halves', False)
            show_passen_details = turnier['anzahl_passen'] <= MAX_PASSEN_FOR_DISPLAY and not show_halves
            
            first_class = True
            
            # Für jede Klasse
            for klasse in sorted(klassen_ergebnisse.keys()):
                if not first_class:
                    elements.append(PageBreak())
                first_class = False
                
                # Titel
                elements.append(Paragraph(turnier.get('name', 'Turnier'), title_style))
                
                # Datum
                if turnier.get('datum'):
                    elements.append(Paragraph(f"Datum: {turnier['datum']}", subtitle_style))
                else:
                    elements.append(Spacer(1, 0.5*cm))
                
                # Klassenname
                elements.append(Paragraph(f"Klasse: {klasse}", class_style))
                
                # Ergebnisse sortieren
                ergebnisse_sortiert = sorted(
                    klassen_ergebnisse[klasse],
                    key=lambda x: (x['gesamt'], x['anzahl_10er'], x['anzahl_9er']),
                    reverse=True
                )
                
                # Tabellendaten
                table_data = []
                
                # Header
                if show_halves:
                    # Hälfte-Ansicht
                    header = ['Platz', 'Name', 'Vorname', 'Verein', '1. Hälfte', '2. Hälfte', 'Gesamt', '10er', '9er']
                elif show_passen_details:
                    # Einzelne Passen
                    header = ['Platz', 'Name', 'Vorname', 'Verein']
                    for i in range(turnier['anzahl_passen']):
                        header.append(f'P{i+1}')
                    header.extend(['Gesamt', '10er', '9er'])
                else:
                    # Nur Gesamt
                    header = ['Platz', 'Name', 'Vorname', 'Verein', 'Gesamt', '10er', '9er']
                
                table_data.append(header)
                
                # Datenzeilen
                platz = 1
                prev_ergebnis = None
                
                for idx, ergebnis in enumerate(ergebnisse_sortiert):
                    # Platzierung
                    if prev_ergebnis and (
                        ergebnis['gesamt'] == prev_ergebnis['gesamt'] and
                        ergebnis['anzahl_10er'] == prev_ergebnis['anzahl_10er'] and
                        ergebnis['anzahl_9er'] == prev_ergebnis['anzahl_9er']
                    ):
                        current_platz = platz
                    else:
                        platz = idx + 1
                        current_platz = platz
                    
                    row = [
                        str(current_platz),
                        ergebnis['name'],
                        ergebnis['vorname'],
                        ergebnis['verein']
                    ]
                    
                    # Passen oder Hälften hinzufügen
                    if show_halves:
                        # Hälften berechnen
                        half = turnier['anzahl_passen'] // 2
                        erste_haelfte = sum(ergebnis['ergebnisse'][:half])
                        zweite_haelfte = sum(ergebnis['ergebnisse'][half:])
                        row.append(f"{erste_haelfte:.1f}")
                        row.append(f"{zweite_haelfte:.1f}")
                    elif show_passen_details:
                        # Einzelne Passen
                        for passe in ergebnis['ergebnisse']:
                            row.append(f"{passe:.1f}")
                    
                    row.append(f"{ergebnis['gesamt']:.1f}")
                    row.append(str(ergebnis['anzahl_10er']))
                    row.append(str(ergebnis['anzahl_9er']))
                    
                    table_data.append(row)
                    prev_ergebnis = ergebnis
                
                # Tabelle erstellen
                table = Table(table_data)
                
                # Tabellen-Style
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDF_COLOR_HEADER)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), 
                     [colors.white, colors.HexColor(PDF_COLOR_ROW_ALT)]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ])
                
                # Platz-Farben
                if len(ergebnisse_sortiert) >= 1:
                    table_style.add('BACKGROUND', (0, 1), (0, 1), 
                                   colors.HexColor(PDF_COLOR_GOLD))
                if len(ergebnisse_sortiert) >= 2:
                    table_style.add('BACKGROUND', (0, 2), (0, 2), 
                                   colors.HexColor(PDF_COLOR_SILVER))
                if len(ergebnisse_sortiert) >= 3:
                    table_style.add('BACKGROUND', (0, 3), (0, 3), 
                                   colors.HexColor(PDF_COLOR_BRONZE))
                
                table.setStyle(table_style)
                elements.append(table)
                
                # Hinweis wenn Passen ausgeblendet
                if not show_passen_details and not show_halves:
                    elements.append(Spacer(1, 0.3*cm))
                    elements.append(Paragraph(
                        f"Hinweis: Einzelne Passen-Ergebnisse wurden ausgeblendet "
                        f"({turnier['anzahl_passen']} Passen)",
                        note_style
                    ))
                elif show_halves:
                    elements.append(Spacer(1, 0.3*cm))
                    elements.append(Paragraph(
                        f"Hinweis: Ergebnisse als 1. und 2. Hälfte angezeigt "
                        f"({turnier['anzahl_passen']} Passen gesamt)",
                        note_style
                    ))
                
                elements.append(Spacer(1, 0.5*cm))
                elements.append(Paragraph(
                    f"Erstellt am: {self.get_current_datetime()}",
                    footer_style
                ))
                elements.append(Spacer(1, 0.5*cm))
            
            # PDF bauen
            doc.build(elements)
            
            messagebox.showinfo("Erfolg", f"PDF wurde erstellt:\n{file_path}")
            
            # PDF öffnen
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux/Mac
                import subprocess
                subprocess.call(('xdg-open', file_path))
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des PDFs:\n{str(e)}")
    
    def get_current_datetime(self):
        """Gibt aktuelles Datum und Zeit formatiert zurück"""
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def generate_gruppen_pdf(self, schuetzen):
        """Erstellt ein PDF mit der Gruppenübersicht"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                           Paragraph, Spacer, PageBreak)
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.enums import TA_CENTER, TA_LEFT
        except ImportError:
            messagebox.showerror(
                "Fehler",
                "Die reportlab-Bibliothek ist nicht installiert.\n\n"
                "Bitte installieren Sie sie mit:\npip install reportlab"
            )
            return

        turnier = self.turnier_model.get_turnier_data()

        # Dateiname Dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=FILE_TYPES_PDF,
            title="Gruppen-PDF speichern",
            initialfile=f"Gruppen_{turnier.get('name', 'Turnier').replace(' ', '_')}.pdf"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=A4,
                rightMargin=1.5*cm,
                leftMargin=1.5*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )

            elements = []

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            group_style = ParagraphStyle(
                'GroupTitle',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )

            # Titel
            elements.append(Paragraph(f"Gruppeneinteilung für {turnier.get('name', 'Turnier')}", title_style))
            if turnier.get('datum'):
                elements.append(Paragraph(f"Datum: {turnier['datum']}", subtitle_style))
            else:
                elements.append(Spacer(1, 0.5*cm))

            # Gruppen zusammenstellen
            groups = {}
            for s in schuetzen:
                gruppe = s.get('gruppe')
                if gruppe is not None:
                    if gruppe not in groups:
                        groups[gruppe] = []
                    groups[gruppe].append(s)

            # Für jede Gruppe eine Tabelle erstellen
            for gruppe_nr in sorted(groups.keys()):
                group_time = self.turnier_model.get_group_time(gruppe_nr)
                time_str = f" - Uhrzeit: {group_time}" if group_time else ""

                elements.append(Paragraph(f"Gruppe {gruppe_nr}{time_str}", group_style))

                schuetzen_in_gruppe = sorted(groups[gruppe_nr], key=lambda x: x.get('scheibe', 0))

                table_data = [['Scheibe', 'Name', 'Vorname', 'Verein']]
                for s in schuetzen_in_gruppe:
                    table_data.append([
                        s.get('scheibe', ''),
                        s.get('name', ''),
                        s.get('vorname', ''),
                        s.get('verein', '')
                    ])

                table = Table(table_data)
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDF_COLOR_HEADER)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(PDF_COLOR_ROW_ALT)]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ])
                table.setStyle(table_style)
                elements.append(table)
                elements.append(Spacer(1, 1*cm))

            doc.build(elements)
            messagebox.showinfo("Erfolg", f"Gruppen-PDF wurde erstellt:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des Gruppen-PDFs:\n{str(e)}")