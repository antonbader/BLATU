# -*- coding: utf-8 -*-
"""
GUI Helper Utilities
"""
import tkinter as tk
import os

def set_window_icon(window):
    """
    Setzt das Icon für das übergebene Fenster.
    Versucht 'blatu.ico' im Root-Verzeichnis zu laden.
    """
    icon_path = "blatu.ico"

    if os.path.exists(icon_path):
        try:
            window.iconbitmap(icon_path)
        except tk.TclError:
            # Kann passieren, wenn das .ico-Format beschädigt ist oder vom OS nicht unterstützt wird
            print(f"Warnung: Icon '{icon_path}' konnte nicht geladen werden.")
        except Exception as e:
            print(f"Warnung: Fehler beim Laden des Icons '{icon_path}': {e}")
