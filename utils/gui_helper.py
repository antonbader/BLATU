# -*- coding: utf-8 -*-
"""
GUI Helper Utilities
"""
import tkinter as tk
import os
import ctypes

def set_taskbar_icon():
    """
    Setzt die AppUserModelID für Windows, damit das Icon in der Taskleiste korrekt angezeigt wird.
    Dies muss vor dem Erstellen des Hauptfensters aufgerufen werden.
    """
    if os.name == 'nt':
        try:
            # Eindeutige ID für die Anwendung
            # Format: Company.Product.SubProduct.Version
            myappid = 'blatu.turnierverwaltung.main.1.5.1'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Warnung: Konnte AppUserModelID nicht setzen: {e}")

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
