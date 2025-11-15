#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blasrohr Turnier Verwaltung (Blatu)
Version 1.3.1

Haupteinstiegspunkt der Anwendung
"""

import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Hauptfunktion zum Starten der Anwendung"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
