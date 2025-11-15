# -*- coding: utf-8 -*-
"""
Info Tab
"""

import tkinter as tk
from tkinter import ttk

from config import (APP_SHORT_NAME, APP_NAME, VERSION, VERSION_DATE, 
                    EMAIL, WEBSITE, COLOR_PRIMARY, COLOR_LINK)


class InfoTab:
    """Tab für Programminformationen"""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, padding="50")
        self.create_widgets()
    
    def create_widgets(self):
        """Erstellt alle Widgets"""
        # Zentrierung
        content_frame = ttk.Frame(self.frame)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Programmname
        ttk.Label(
            content_frame, 
            text=APP_SHORT_NAME, 
            font=("Arial", 24, "bold"), 
            foreground=COLOR_PRIMARY
        ).pack(pady=(0, 5))
        
        # Beschreibung
        ttk.Label(
            content_frame, 
            text=APP_NAME, 
            font=("Arial", 14)
        ).pack(pady=(0, 20))
        
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        
        # Version
        ttk.Label(
            content_frame, 
            text=f"Version {VERSION}", 
            font=("Arial", 11)
        ).pack(pady=5)
        
        ttk.Label(
            content_frame, 
            text=VERSION_DATE, 
            font=("Arial", 11)
        ).pack(pady=5)
        
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, pady=10)
             
        # Kontakt
        ttk.Label(
            content_frame, 
            text=EMAIL, 
            font=("Arial", 10), 
            foreground=COLOR_LINK
        ).pack(pady=2)
        
        ttk.Label(
            content_frame, 
            text=WEBSITE, 
            font=("Arial", 10), 
            foreground=COLOR_LINK
        ).pack(pady=2)
