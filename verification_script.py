import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import MagicMock
from ui.ergebnisse_tab import ErgebnisseTab
from ui.urkunden_tab import UrkundenTab
from models.turnier import TurnierModel
from models.schuetze import SchuetzeModel

class TestUILayout(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide the window
        self.turnier_model = TurnierModel()
        self.schuetze_model = SchuetzeModel()

    def tearDown(self):
        self.root.destroy()

    def test_ergebnisse_tab_layout(self):
        tab = ErgebnisseTab(self.root, self.turnier_model, self.schuetze_model)

        # Find right frame
        # create_widgets -> self.frame
        # inside self.frame -> right_frame is grid(row=1, column=1)

        # Tkinter introspection is limited, we rely on widget hierarchy
        children = tab.frame.winfo_children()
        right_frame = None
        for child in children:
            info = child.grid_info()
            if info.get('row') == 1 and info.get('column') == 1:
                right_frame = child
                break

        self.assertIsNotNone(right_frame, "Right frame not found")

        right_children = right_frame.pack_slaves()
        # pack_slaves returns list in order of packing or stacking order.
        # But side packing logic is:
        # 1. Buttons (BOTTOM)
        # 2. Result (BOTTOM)
        # 3. Zusatz (BOTTOM)
        # 4. Info (TOP)
        # 5. Scroll Container (TOP)

        # Since pack() pushes into the allocation list:
        # If we inspect pack_info(), we can check 'side'.

        # Expected children structure based on code:
        # button_frame (BOTTOM)
        # ergebnis_frame (BOTTOM)
        # zusatz_frame (BOTTOM)
        # info_label (TOP)
        # eingabe_container (TOP)

        # Let's iterate and check sides.
        # Note: The order in pack_slaves() is usually the stacking order (z-order),
        # which corresponds to creation/pack order usually.

        found_buttons = False
        found_ergebnis = False
        found_zusatz = False
        found_container = False

        for widget in right_children:
            info = widget.pack_info()
            side = info['side']

            # Identify widgets by type or content (hard to check content directly without object ref)
            # But we know the order of creation/packing in the code.
            # 1. Buttons
            # 2. Ergebnis
            # 3. Zusatz
            # 4. Info
            # 5. Container

            # We can check widget class or contained text
            if isinstance(widget, ttk.Frame):
                # Could be button_frame, ergebnis_frame, or eingabe_frame (inside canvas, not here)
                # Check children of the frame to identify
                sub_children = widget.winfo_children()
                if any(isinstance(w, ttk.Button) and 'speichern' in w.cget('text') for w in sub_children):
                    self.assertEqual(side, 'bottom', "Buttons should be packed BOTTOM")
                    found_buttons = True
                elif any(isinstance(w, ttk.Label) and 'Gesamtergebnis' in w.cget('text') for w in sub_children):
                    self.assertEqual(side, 'bottom', "Gesamtergebnis should be packed BOTTOM")
                    found_ergebnis = True

            if isinstance(widget, ttk.LabelFrame):
                if 'Zusatzwertung' in widget.cget('text'):
                    self.assertEqual(side, 'bottom', "Zusatzwertung should be packed BOTTOM")
                    found_zusatz = True
                elif 'Ergebnisse' in widget.cget('text'):
                    self.assertEqual(side, 'top', "Ergebnisse container should be packed TOP")
                    found_container = True

        self.assertTrue(found_buttons)
        self.assertTrue(found_ergebnis)
        self.assertTrue(found_zusatz)
        self.assertTrue(found_container)

    def test_urkunden_tab_layout(self):
        tab = UrkundenTab(self.root, self.turnier_model, self.schuetze_model)

        # Check if Generate Button is inside Settings Frame
        # Settings frame is "Einstellungen"

        # Iterate through frames to find Settings frame
        main_frame = tab.frame.winfo_children()[0] # Main frame
        top_frame = main_frame.winfo_children()[0] # Top frame

        settings_frame = None
        for w in top_frame.winfo_children():
            if isinstance(w, ttk.LabelFrame) and w.cget('text') == 'Einstellungen':
                settings_frame = w
                break

        self.assertIsNotNone(settings_frame)

        # Check for button in settings frame
        button_found = False
        for w in settings_frame.winfo_children():
            if isinstance(w, ttk.Button) and 'Urkunden erstellen' in w.cget('text'):
                button_found = True
                info = w.grid_info()
                self.assertGreaterEqual(int(info['row']), 4, "Button should be at the bottom (row >= 4)")
                break

        self.assertTrue(button_found, "Generate button not found in Settings frame")

        # Check for Scrollbar in Klassen Frame
        klassen_frame = None
        for w in top_frame.winfo_children():
            if isinstance(w, ttk.LabelFrame) and 'Urkunden pro Platzierung' in w.cget('text'):
                klassen_frame = w
                break

        self.assertIsNotNone(klassen_frame)

        scrollbar_found = False
        for w in klassen_frame.winfo_children():
            if isinstance(w, ttk.Scrollbar):
                scrollbar_found = True
                break

        self.assertTrue(scrollbar_found, "Scrollbar not found in Klassen frame")

if __name__ == '__main__':
    unittest.main()
