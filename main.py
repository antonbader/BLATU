#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blasrohr Turnier Verwaltung (Blatu)
Version 1.4.0

Haupteinstiegspunkt der Anwendung
"""

import tkinter as tk
from ui.main_window import MainWindow


def run_app():
    """Hauptfunktion zum Starten der Anwendung"""
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
