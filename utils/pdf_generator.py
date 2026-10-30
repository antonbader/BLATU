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
            
            # Schriftgrößen aus den PDF Settings holen
            font_cfg = self.turnier_model.get_pdf_font_sizes().get('ergebnisliste', {})
            title_size = font_cfg.get('title', 18)
            subtitle_size = font_cfg.get('subtitle', 12)
            heading_size = font_cfg.get('heading', 14)
            table_header_size = font_cfg.get('table_header', 10)
            table_body_size = font_cfg.get('table_body', 9)

            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=title_size,
                leading=max(title_size + 4, int(title_size * 1.25)),
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=subtitle_size,
                leading=max(subtitle_size + 4, int(subtitle_size * 1.25)),
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            class_style = ParagraphStyle(
                'ClassTitle',
                parent=styles['Heading2'],
                fontSize=heading_size,
                leading=max(heading_size + 4, int(heading_size * 1.25)),
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
                    key=lambda x: (
                        x['gesamt'],
                        x['anzahl_10er'],
                        x['anzahl_9er'],
                        1 if x.get('stechen') is not None else 0,
                        x.get('stechen') if x.get('stechen') is not None else -1
                    ),
                    reverse=True
                )
                
                # Tabellendaten
                table_data = []
                
                # Header
                if show_halves:
                    # Hälfte-Ansicht
                    header = ['Platz', 'Name', 'Vorname', 'Verein', '1. Hälfte', '2. Hälfte', 'Gesamt', '10er', '9er', 'Stechen']
                elif show_passen_details:
                    # Einzelne Passen
                    header = ['Platz', 'Name', 'Vorname', 'Verein']
                    for i in range(turnier['anzahl_passen']):
                        header.append(f'P{i+1}')
                    header.extend(['Gesamt', '10er', '9er', 'Stechen'])
                else:
                    # Nur Gesamt
                    header = ['Platz', 'Name', 'Vorname', 'Verein', 'Gesamt', '10er', '9er', 'Stechen']
                
                table_data.append(header)
                
                # Datenzeilen
                platz = 1
                prev_ergebnis = None
                
                for idx, ergebnis in enumerate(ergebnisse_sortiert):
                    # Platzierung
                    if prev_ergebnis and (
                        ergebnis['gesamt'] == prev_ergebnis['gesamt'] and
                        ergebnis['anzahl_10er'] == prev_ergebnis['anzahl_10er'] and
                        ergebnis['anzahl_9er'] == prev_ergebnis['anzahl_9er'] and
                        ergebnis.get('stechen') == prev_ergebnis.get('stechen')
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
                        row.append(str(erste_haelfte))
                        row.append(str(zweite_haelfte))
                    elif show_passen_details:
                        # Einzelne Passen
                        for passe in ergebnis['ergebnisse']:
                            row.append(str(int(passe)))
                    
                    row.append(str(int(ergebnis['gesamt'])))
                    row.append(str(ergebnis['anzahl_10er']))
                    row.append(str(ergebnis['anzahl_9er']))
                    stechen_val = ergebnis.get('stechen')
                    row.append(f"nach Stechen ({stechen_val})" if stechen_val is not None else "")
                    
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
                    ('FONTSIZE', (0, 0), (-1, 0), table_header_size),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), table_body_size),
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

    def create_mannschaft_pdf(self, mannschaft_ergebnisse, show_einzel=False, group_by_klasse=False):
        """Erstellt ein PDF mit dem Ergebnis der Mannschaftswertung"""
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

        if not mannschaft_ergebnisse:
            messagebox.showinfo("Keine Mannschaften", "Es sind keine Mannschaften für den PDF-Export vorhanden!")
            return

        turnier = self.turnier_model.get_turnier_data()
        max_groesse = self.turnier_model.get_mannschaft_groesse()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=FILE_TYPES_PDF,
            title="Mannschaftswertung PDF speichern",
            initialfile=f"Mannschaftswertung_{turnier.get('name', 'Turnier').replace(' ', '_')}.pdf"
        )

        if not file_path:
            return

        try:
            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=1*cm,
                leftMargin=1*cm,
                topMargin=1.5*cm,
                bottomMargin=1.5*cm
            )

            elements = []

            # Schriftgrößen aus den PDF Settings holen
            font_cfg = self.turnier_model.get_pdf_font_sizes().get('mannschaften', {})
            title_size = font_cfg.get('title', 18)
            subtitle_size = font_cfg.get('subtitle', 12)
            heading_size = font_cfg.get('heading', 14)
            table_header_size = font_cfg.get('table_header', 10)
            table_body_size = font_cfg.get('table_body', 9)

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'MannschaftTitle',
                parent=styles['Heading1'],
                fontSize=title_size,
                leading=max(title_size + 4, int(title_size * 1.25)),
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            subtitle_style = ParagraphStyle(
                'MannschaftSubtitle',
                parent=styles['Normal'],
                fontSize=subtitle_size,
                leading=max(subtitle_size + 4, int(subtitle_size * 1.25)),
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            heading_style = ParagraphStyle(
                'MannschaftHeading',
                parent=styles['Heading2'],
                fontSize=heading_size,
                leading=max(heading_size + 4, int(heading_size * 1.25)),
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            footer_style = ParagraphStyle(
                'MannschaftFooter',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            note_style = ParagraphStyle(
                'MannschaftNote',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#666666'),
                alignment=TA_CENTER,
                fontName='Helvetica-Oblique'
            )

            anzahl_passen = turnier.get('anzahl_passen', 1)
            show_halves = turnier.get('show_halves', False)
            show_passen_details = anzahl_passen <= MAX_PASSEN_FOR_DISPLAY and not show_halves

            first_group = True
            for group_name in sorted(mannschaft_ergebnisse.keys()):
                teams = mannschaft_ergebnisse[group_name]
                if not teams:
                    continue

                if not first_group:
                    elements.append(PageBreak())
                first_group = False

                elements.append(Paragraph(
                    f"Mannschaftswertung - {turnier.get('name', 'Turnier')}",
                    title_style
                ))

                if turnier.get('datum'):
                    elements.append(Paragraph(f"Datum: {turnier['datum']}", subtitle_style))
                else:
                    elements.append(Spacer(1, 0.5*cm))

                heading_text = f"Mannschaftsklasse: {group_name}" if group_by_klasse else "Wertung: Alle Mannschaften"
                elements.append(Paragraph(heading_text, heading_style))

                table_data = []
                team_row_indices = []  # (row_idx, platz)

                if not show_einzel:
                    # Nur Gesamtergebnis einer Mannschaft
                    if group_by_klasse:
                        header = ['Platz', 'Mannschaft', 'Schützen', 'Gesamt', '10er', '9er']
                    else:
                        header = ['Platz', 'Mannschaft', 'Mannschaftsklasse', 'Schützen', 'Gesamt', '10er', '9er']
                    table_data.append(header)

                    for team in teams:
                        row_idx = len(table_data)
                        platz = team.get('platz', 1)
                        team_row_indices.append((row_idx, platz))
                        anz_str = f"{len(team.get('mitglieder', []))}/{max_groesse}"
                        if group_by_klasse:
                            row = [
                                str(platz),
                                team['name'],
                                anz_str,
                                str(int(team['gesamt'])),
                                str(team['anzahl_10er']),
                                str(team['anzahl_9er'])
                            ]
                        else:
                            row = [
                                str(platz),
                                team['name'],
                                team.get('klasse') or '-',
                                anz_str,
                                str(int(team['gesamt'])),
                                str(team['anzahl_10er']),
                                str(team['anzahl_9er'])
                            ]
                        table_data.append(row)
                else:
                    # Mit Einzelergebnissen der Mannschaftsmitglieder
                    header = ['Platz', 'Mannschaft']
                    if not group_by_klasse:
                        header.append('Mannschaftsklasse')
                    header.extend(['Schütze', 'Verein', 'Klasse'])

                    if show_halves:
                        header.extend(['1. Hälfte', '2. Hälfte'])
                    elif show_passen_details:
                        for i in range(anzahl_passen):
                            header.append(f'P{i+1}')

                    header.extend(['Gesamt', '10er', '9er'])
                    table_data.append(header)

                    for team in teams:
                        row_idx = len(table_data)
                        platz = team.get('platz', 1)
                        team_row_indices.append((row_idx, platz))

                        mitglieder = team.get('mitglieder', [])
                        team_row = [str(platz), team['name']]
                        if not group_by_klasse:
                            team_row.append(team.get('klasse') or '-')
                        team_row.extend([f"Gesamtergebnis ({len(mitglieder)}/{max_groesse} Schützen)", "", ""])

                        if show_halves:
                            half = anzahl_passen // 2
                            erste = sum(team['ergebnisse'][:half])
                            zweite = sum(team['ergebnisse'][half:])
                            team_row.extend([str(int(erste)), str(int(zweite))])
                        elif show_passen_details:
                            for p_idx in range(anzahl_passen):
                                val = team['ergebnisse'][p_idx] if p_idx < len(team['ergebnisse']) else 0
                                team_row.append(str(int(val)))

                        team_row.extend([
                            str(int(team['gesamt'])),
                            str(team['anzahl_10er']),
                            str(team['anzahl_9er'])
                        ])
                        table_data.append(team_row)

                        # Einzelergebnisse der Mitglieder
                        for member in mitglieder:
                            m_row = ["", ""]
                            if not group_by_klasse:
                                m_row.append("")
                            m_row.extend([
                                f"{member.get('vorname', '')} {member.get('name', '')}".strip(),
                                member.get('verein', ''),
                                member.get('klasse', '')
                            ])

                            m_passen = member.get('ergebnisse', [])
                            if show_halves:
                                half = anzahl_passen // 2
                                m_erste = sum(m_passen[:half])
                                m_zweite = sum(m_passen[half:])
                                m_row.extend([str(int(m_erste)), str(int(m_zweite))])
                            elif show_passen_details:
                                for p_idx in range(anzahl_passen):
                                    val = m_passen[p_idx] if p_idx < len(m_passen) else 0
                                    m_row.append(str(int(val)))

                            m_row.extend([
                                str(int(member.get('gesamt', 0))),
                                str(member.get('anzahl_10er', 0)),
                                str(member.get('anzahl_9er', 0))
                            ])
                            table_data.append(m_row)

                table = Table(table_data, repeatRows=1)
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDF_COLOR_HEADER)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), table_header_size),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), table_body_size),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('TOPPADDING', (0, 1), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ])

                if not show_einzel:
                    table_style.add(
                        'ROWBACKGROUNDS', (0, 1), (-1, -1),
                        [colors.white, colors.HexColor(PDF_COLOR_ROW_ALT)]
                    )
                    for row_idx, platz in team_row_indices:
                        if platz == 1:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_GOLD))
                        elif platz == 2:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_SILVER))
                        elif platz == 3:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_BRONZE))
                else:
                    # Bei Einzelansicht: Mannschaftszeilen hervorheben
                    for row_idx, platz in team_row_indices:
                        table_style.add('FONTNAME', (0, row_idx), (-1, row_idx), 'Helvetica-Bold')
                        table_style.add('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#D9E1F2'))
                        if platz == 1:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_GOLD))
                        elif platz == 2:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_SILVER))
                        elif platz == 3:
                            table_style.add('BACKGROUND', (0, row_idx), (0, row_idx), colors.HexColor(PDF_COLOR_BRONZE))

                table.setStyle(table_style)
                elements.append(table)

                if show_einzel and not show_passen_details and not show_halves:
                    elements.append(Spacer(1, 0.3*cm))
                    elements.append(Paragraph(
                        f"Hinweis: Einzelne Passen-Ergebnisse wurden ausgeblendet ({anzahl_passen} Passen)",
                        note_style
                    ))
                elif show_einzel and show_halves:
                    elements.append(Spacer(1, 0.3*cm))
                    elements.append(Paragraph(
                        f"Hinweis: Ergebnisse als 1. und 2. Hälfte angezeigt ({anzahl_passen} Passen gesamt)",
                        note_style
                    ))

                elements.append(Spacer(1, 0.5*cm))
                elements.append(Paragraph(
                    f"Erstellt am: {self.get_current_datetime()}",
                    footer_style
                ))
                elements.append(Spacer(1, 0.5*cm))

            doc.build(elements)
            messagebox.showinfo("Erfolg", f"PDF wurde erstellt:\n{file_path}")

            if os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
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

            # Schriftgrößen aus den PDF Settings holen
            font_cfg = self.turnier_model.get_pdf_font_sizes().get('gruppen', {})
            title_size = font_cfg.get('title', 18)
            subtitle_size = font_cfg.get('subtitle', 12)
            heading_size = font_cfg.get('heading', 14)
            table_header_size = font_cfg.get('table_header', 10)
            table_body_size = font_cfg.get('table_body', 10)

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=title_size,
                leading=max(title_size + 4, int(title_size * 1.25)),
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=12,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Normal'],
                fontSize=subtitle_size,
                leading=max(subtitle_size + 4, int(subtitle_size * 1.25)),
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            )
            group_style = ParagraphStyle(
                'GroupTitle',
                parent=styles['Heading2'],
                fontSize=heading_size,
                leading=max(heading_size + 4, int(heading_size * 1.25)),
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

                table_data = [['Scheibe', 'Name', 'Vorname', 'Verein', 'Klasse']]
                for s in schuetzen_in_gruppe:
                    table_data.append([
                        s.get('scheibe', ''),
                        s.get('name', ''),
                        s.get('vorname', ''),
                        s.get('verein', ''),
                        s.get('klasse', '')
                    ])

                table = Table(table_data)
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDF_COLOR_HEADER)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), table_header_size),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), table_body_size),
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

    def generate_startliste_vereine_pdf(self, schuetzen):
        """Erstellt für jeden Verein eine PDF-Startliste"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                           Paragraph, Spacer)
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
        assigned_schuetzen = [s for s in schuetzen if s.get('gruppe') is not None]

        if not assigned_schuetzen:
            messagebox.showinfo("Info", "Es sind keine Schützen Gruppen zugewiesen. PDFs werden nicht erstellt.")
            return

        # Verzeichnis für Speicherung abfragen
        directory = filedialog.askdirectory(title="Speicherort für Vereins-PDFs auswählen")
        if not directory:
            return

        # Schützen nach Verein gruppieren
        vereine = {}
        for s in assigned_schuetzen:
            verein = s.get('verein', 'Unbekannt')
            if verein not in vereine:
                vereine[verein] = []
            vereine[verein].append(s)

        # PDF für jeden Verein erstellen
        for verein, schuetzen_im_verein in vereine.items():
            # Dateiname erstellen
            turnier_name = ''.join(c for c in turnier.get('name', 'Turnier') if c.isalnum())
            turnier_datum = ''.join(c for c in turnier.get('datum', '') if c.isalnum())
            vereins_name = ''.join(c for c in verein if c.isalnum())
            file_name = f"{turnier_name}_{turnier_datum}_{vereins_name}.pdf"
            file_path = os.path.join(directory, file_name)

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

                # Schriftgrößen aus den PDF Settings holen
                font_cfg = self.turnier_model.get_pdf_font_sizes().get('vereine', {})
                title_size = font_cfg.get('title', 16)
                subtitle_size = font_cfg.get('subtitle', 12)
                heading_size = font_cfg.get('heading', 14)
                table_header_size = font_cfg.get('table_header', 10)
                table_body_size = font_cfg.get('table_body', 10)
                footer_text_size = font_cfg.get('footer_text', 10)

                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=title_size,
                    leading=max(title_size + 4, int(title_size * 1.25)),
                    alignment=TA_CENTER,
                    spaceAfter=6
                )
                subtitle_style = ParagraphStyle(
                    'CustomSubtitle',
                    parent=styles['Normal'],
                    fontSize=subtitle_size,
                    leading=max(subtitle_size + 4, int(subtitle_size * 1.25)),
                    alignment=TA_CENTER,
                    spaceAfter=12
                )
                verein_style = ParagraphStyle(
                    'VereinTitle',
                    parent=styles['Heading2'],
                    fontSize=heading_size,
                    leading=max(heading_size + 4, int(heading_size * 1.25)),
                    alignment=TA_LEFT,
                    spaceAfter=10
                )

                # Titel und Datum
                elements.append(Paragraph(turnier.get('name', 'Turnier'), title_style))
                if turnier.get('datum'):
                    elements.append(Paragraph(f"Datum: {turnier['datum']}", subtitle_style))
                else:
                    elements.append(Spacer(1, 0.5*cm))

                elements.append(Paragraph(f"Verein: {verein}", verein_style))

                # Schützen sortieren: erst nach Gruppe, dann nach Name
                schuetzen_im_verein.sort(key=lambda s: (s.get('gruppe', 0), s.get('name', '')))

                # Tabelle erstellen und Gesamtstartgeld berechnen
                table_data = [['Name', 'Vorname', 'Klasse', 'Gruppe', 'Startzeit', 'Scheibe', 'Startgeld']]
                total_startgeld_verein = 0
                for s in schuetzen_im_verein:
                    gruppe_nr = s.get('gruppe')
                    startzeit = self.turnier_model.get_group_time(gruppe_nr) if gruppe_nr else ''
                    startgeld_cent = self.turnier_model.get_klasse_startgeld(s.get('klasse', ''))
                    total_startgeld_verein += startgeld_cent
                    startgeld_euro = f"{startgeld_cent / 100.0:.2f} €"

                    table_data.append([
                        s.get('name', ''),
                        s.get('vorname', ''),
                        s.get('klasse', ''),
                        s.get('gruppe', ''),
                        startzeit,
                        s.get('scheibe', ''),
                        startgeld_euro
                    ])

                table = Table(table_data)
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(PDF_COLOR_HEADER)),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), table_header_size),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, 0), 8),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), table_body_size),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor(PDF_COLOR_ROW_ALT)]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ])
                table.setStyle(table_style)
                elements.append(table)

                # Gesamtstartgeld anzeigen
                elements.append(Spacer(1, 0.5*cm))
                total_startgeld_euro = f"{total_startgeld_verein / 100.0:.2f} €"
                total_text = f"<b>Gesamtstartgeld für den Verein: {total_startgeld_euro}</b>"
                total_style = ParagraphStyle(
                    'TotalStartgeld',
                    parent=styles['Normal'],
                    fontSize=footer_text_size,
                    leading=max(footer_text_size + 4, int(footer_text_size * 1.25)),
                    alignment=TA_LEFT
                )
                elements.append(Paragraph(total_text, total_style))

                # Startgeld-Informationen hinzufügen, falls aktiviert und Summe > 0
                if turnier.get('startgeld_erheben') and total_startgeld_verein > 0:
                    elements.append(Spacer(1, 1*cm))

                    iban = turnier.get('iban', '')
                    bic = turnier.get('bic', '')
                    bankname = turnier.get('bankname', '')
                    kontoinhaber = turnier.get('kontoinhaber', '')
                    zahldatum = turnier.get('zahldatum', '')
                    turniername = turnier.get('name', '')

                    text = (
                        f"Bitte überweisen Sie das Startgeld bis zum {zahldatum} "
                        f"unter Angabe des Buchungszwecks \"{turniername} - {verein}\" "
                        f"auf folgendes Konto: {iban} Bank: {bankname} BIC: {bic} Kontoinhaber: {kontoinhaber}"
                    )

                    p_style = ParagraphStyle(
                        'PaymentInfo',
                        parent=styles['Normal'],
                        fontSize=footer_text_size,
                        leading=max(footer_text_size + 4, int(footer_text_size * 1.25)),
                        alignment=TA_LEFT
                    )
                    elements.append(Paragraph(text, p_style))

                doc.build(elements)

            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Erstellen des PDFs für {verein}:\n{str(e)}")
                return # Bei Fehler abbrechen

        messagebox.showinfo("Erfolg", f"Alle {len(vereine)} Vereins-PDFs wurden im Verzeichnis '{directory}' erstellt.")
