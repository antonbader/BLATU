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

    # Icon initial setzen
    set_window_icon(root)

    MainWindow(root)

    # TRICK: Das Icon nochmals verzögert setzen.
    # Manche Windows-Konfigurationen oder Tkinter-Versionen "vergessen" das Taskleisten-Icon
    # während des initialen Fenstersaufbaus. Durch das erneute Setzen im Event-Loop
    # wird es erzwungen, sobald das Fenster wirklich da ist.
    root.after(200, lambda: set_window_icon(root))

    root.mainloop()


if __name__ == "__main__":
    run_app()
