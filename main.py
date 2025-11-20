#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blasrohr Turnier Verwaltung (Blatu)
Version 1.5.1

Haupteinstiegspunkt der Anwendung
"""

import tkinter as tk
from ui.main_window import MainWindow
from utils.gui_helper import set_window_icon, set_taskbar_icon


def run_app():
    """Hauptfunktion zum Starten der Anwendung"""
    # WICHTIG: set_taskbar_icon muss vor dem Erstellen des Fensters aufgerufen werden,
    # damit Windows die AppID korrekt zuordnet.
    set_taskbar_icon()

    root = tk.Tk()
    set_window_icon(root)
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
