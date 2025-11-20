# -*- coding: utf-8 -*-
"""
Online Eingabe Tab
Steuerung des Webservers
"""

import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from web_server import WebServer

class OnlineEingabeTab:
    """Tab für die Steuerung der Online-Eingabe"""

    def __init__(self, parent, turnier_model, schuetze_model):
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.web_server = WebServer(turnier_model, schuetze_model)

        self.frame = ttk.Frame(parent, padding="10")
        self.group_vars = {}  # Stores BooleanVars for groups

        self.create_widgets()

        # Bind visibility event to refresh groups
        self.frame.bind('<Visibility>', self.refresh_groups)

    def create_widgets(self):
        """Erstellt die UI-Elemente"""
        # Titel
        ttk.Label(
            self.frame,
            text="Online-Eingabe Steuerung",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=10)

        # Server Einstellungen
        settings_frame = ttk.LabelFrame(self.frame, text="Server Einstellungen", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), pady=10, padx=5)

        # Port
        ttk.Label(settings_frame, text="Port:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value="8080")
        self.port_entry = ttk.Entry(settings_frame, textvariable=self.port_var, width=10)
        self.port_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)

        # IP Anzeige
        ttk.Label(settings_frame, text="IP-Adresse:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ip_label = ttk.Label(settings_frame, text=self.web_server.get_ip(), font=("Arial", 10, "bold"))
        self.ip_label.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        # Status
        ttk.Label(settings_frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(settings_frame, text="Gestoppt", foreground="red", font=("Arial", 10, "bold"))
        self.status_label.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)

        # Buttons
        self.start_button = ttk.Button(settings_frame, text="Server starten", command=self.toggle_server)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=15, sticky=(tk.W, tk.E))

        self.open_browser_button = ttk.Button(settings_frame, text="Im Browser öffnen", command=self.open_browser, state="disabled")
        self.open_browser_button.grid(row=4, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))

        # Gruppen Auswahl
        groups_frame = ttk.LabelFrame(self.frame, text="Aktive Gruppen", padding="10")
        groups_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10, padx=5)
        groups_frame.rowconfigure(1, weight=1)

        # Control Buttons for Groups
        group_ctrl_frame = ttk.Frame(groups_frame)
        group_ctrl_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(group_ctrl_frame, text="Alle auswählen", command=self.select_all_groups).pack(side=tk.LEFT, padx=5)
        ttk.Button(group_ctrl_frame, text="Keine auswählen", command=self.deselect_all_groups).pack(side=tk.LEFT, padx=5)
        ttk.Button(group_ctrl_frame, text="Aktualisieren", command=self.refresh_groups).pack(side=tk.LEFT, padx=5)

        # Scrollable area for checkboxes
        canvas = tk.Canvas(groups_frame)
        scrollbar = ttk.Scrollbar(groups_frame, orient="vertical", command=canvas.yview)
        self.groups_inner_frame = ttk.Frame(canvas)

        self.groups_inner_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.groups_inner_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # Initial refresh
        self.refresh_groups()

    def refresh_groups(self, event=None):
        """Lädt die Gruppen aus dem Schützenmodell und erstellt Checkboxen"""
        # Clear existing checkboxes
        for widget in self.groups_inner_frame.winfo_children():
            widget.destroy()

        schuetzen = self.schuetze_model.get_all_schuetzen()
        groups = set()
        for s in schuetzen:
            grp = s.get('gruppe')
            if grp is not None and str(grp).strip():
                groups.add(str(grp))

        sorted_groups = sorted(list(groups))

        # Create Checkboxes
        # Store old states if possible? For now, default to unchecked or keep active_groups from server
        current_active = self.web_server.active_groups

        self.group_vars = {}
        for grp in sorted_groups:
            var = tk.BooleanVar(value=(grp in current_active))
            # Trace change to update server immediately
            var.trace_add('write', lambda *args, g=grp: self.update_server_groups())
            self.group_vars[grp] = var

            cb = ttk.Checkbutton(self.groups_inner_frame, text=f"Gruppe {grp}", variable=var)
            cb.pack(anchor=tk.W, pady=2)

        self.update_server_groups()

    def update_server_groups(self):
        """Sendet die aktuell ausgewählten Gruppen an den Server"""
        active = []
        for grp, var in self.group_vars.items():
            if var.get():
                active.append(grp)
        self.web_server.set_active_groups(active)

    def select_all_groups(self):
        for var in self.group_vars.values():
            var.set(True)

    def deselect_all_groups(self):
        for var in self.group_vars.values():
            var.set(False)

    def toggle_server(self):
        if not self.web_server.is_running:
            # Start Server
            try:
                port = int(self.port_var.get())
                self.web_server.start(port)
                self.status_label.config(text="Aktiv", foreground="green")
                self.start_button.config(text="Server stoppen")
                self.port_entry.config(state="disabled")
                self.open_browser_button.config(state="normal")

                # Update IP (might change based on network interface)
                self.ip_label.config(text=f"{self.web_server.get_ip()}:{port}")

            except ValueError:
                messagebox.showerror("Fehler", "Ungültiger Port")
        else:
            # Stop Server (Fake stop as explained in plan)
            self.web_server.stop()
            self.status_label.config(text="Gestoppt", foreground="red")
            self.start_button.config(text="Server starten")
            self.port_entry.config(state="normal")
            self.open_browser_button.config(state="disabled")
            messagebox.showinfo("Info", "Der Server wird beim Beenden der Anwendung vollständig geschlossen. Die Weboberfläche ist nun nicht mehr erreichbar.")

    def open_browser(self):
        port = self.port_var.get()
        ip = self.web_server.get_ip()
        url = f"http://{ip}:{port}"
        webbrowser.open(url)
