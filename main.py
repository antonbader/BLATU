#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blasrohr Turnier Verwaltung (Blatu)
Version 1.4.0

Haupteinstiegspunkt der Anwendung
"""

import tkinter as tk
from ui.main_window import MainWindow


def main():
    """Hauptfunktion zum Starten der Anwendung"""
    root = tk.Tk()
    app = MainWindow(root)

    # Automatisches Laden und Screenshot für die Verifizierung
    if "--screenshot" in sys.argv:
        # Lade die Testdaten direkt über den DataManager
        success, _ = app.data_manager.load_from_filepath("test_turnier.json")
        if success:
            # Definiere eine Funktion, die den Screenshot macht und die App beendet
            def take_screenshot_and_exit():
                # Stelle sicher, dass der Turnier-Tab im Vordergrund ist
                app.notebook.select(app.turnier_tab.frame)

                x = root.winfo_rootx()
                y = root.winfo_rooty()
                width = root.winfo_width()
                height = root.winfo_height()

                # Erstelle das Verzeichnis, falls es nicht existiert
                os.makedirs("/home/jules/verification", exist_ok=True)

                # Mache den Screenshot
                ImageGrab.grab(bbox=(x, y, x + width, y + height)).save("/home/jules/verification/verification.png")

                # Beende die Anwendung
                root.destroy()

            # Führe die UI-Aktualisierung und den Screenshot nach einer kurzen Verzögerung aus
            app.root.after(10, lambda: app.post_load_refresh("Testdaten geladen"))
            root.after(500, take_screenshot_and_exit) # 500ms für Stabilität
        else:
            print("Fehler beim Laden der Testdaten für den Screenshot.")
            root.destroy()
            return

    root.mainloop()


if __name__ == "__main__":
    import sys
    import os
    from PIL import ImageGrab
    main()
