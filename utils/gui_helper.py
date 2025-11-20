# -*- coding: utf-8 -*-
"""
GUI Helper Utilities
"""
import tkinter as tk
import os
import sys
import ctypes

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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
    Nutzt resource_path um das Icon auch in der One-File-Exe zu finden.
    """
    icon_name = "blatu.ico"
    # Versuche Pfad aufzulösen (wichtig für PyInstaller onefile)
    icon_path = resource_path(icon_name)

    # Fallback: Falls Datei nicht gefunden (z.B. Entwicklungsumgebung anders strukturiert),
    # versuche lokalen Pfad direkt
    if not os.path.exists(icon_path):
        icon_path = icon_name

    if os.path.exists(icon_path):
        try:
            if isinstance(window, tk.Tk):
                # Bei Root-Fenster als Standard für die ganze App setzen
                window.iconbitmap(default=icon_path)
            else:
                # Bei normalen Fenstern direkt setzen
                window.iconbitmap(icon_path)
        except tk.TclError:
            # Kann passieren, wenn das .ico-Format beschädigt ist oder vom OS nicht unterstützt wird
            print(f"Warnung: Icon '{icon_path}' konnte nicht geladen werden.")
        except Exception as e:
            print(f"Warnung: Fehler beim Laden des Icons '{icon_path}': {e}")
