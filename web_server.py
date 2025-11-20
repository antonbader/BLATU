# -*- coding: utf-8 -*-
"""
Web Server for Online Data Entry
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.serving import make_server
import threading
import socket
import logging

# Disable Flask startup banner
cli = logging.getLogger('flask.cli')
cli.setLevel(logging.ERROR)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebServer:
    def __init__(self, turnier_model, schuetze_model):
        self.app = Flask(__name__, template_folder='templates')
        self.app.secret_key = 'secret_key_change_in_production'  # Simple secret key
        self.turnier_model = turnier_model
        self.schuetze_model = schuetze_model
        self.active_groups = set()
        self.port = 8080
        self.server_thread = None
        self.server = None
        self.is_running = False

        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            schuetzen = self.schuetze_model.get_all_schuetzen()
            # Filter only active groups
            filtered_schuetzen = []
            for s in schuetzen:
                if str(s.get('gruppe', '')) in self.active_groups:
                    s_id = self.schuetze_model.get_schuetze_id(s)
                    s['id'] = s_id
                    filtered_schuetzen.append(s)

            return render_template('index.html', schuetzen=filtered_schuetzen)

        @self.app.route('/login/<schuetze_id>', methods=['GET', 'POST'])
        def login(schuetze_id):
            # Find shooter and check group permission
            all_schuetzen = self.schuetze_model.get_all_schuetzen()
            schuetze = None
            for s in all_schuetzen:
                if self.schuetze_model.get_schuetze_id(s) == schuetze_id:
                    schuetze = s
                    break

            if not schuetze:
                return "Schütze nicht gefunden", 404

            # Verify group permission
            if str(schuetze.get('gruppe', '')) not in self.active_groups:
                return "Eingabe für diese Gruppe derzeit nicht möglich", 403

            if request.method == 'POST':
                pin_input = request.form.get('pin')
                if pin_input == schuetze.get('pin'):
                    session['user_id'] = schuetze_id
                    return redirect(url_for('input_scores', schuetze_id=schuetze_id))
                else:
                    return render_template('login.html', name=f"{schuetze['vorname']} {schuetze['name']}", error="Falsche PIN")

            return render_template('login.html', name=f"{schuetze['vorname']} {schuetze['name']}")

        @self.app.route('/input/<schuetze_id>')
        def input_scores(schuetze_id):
            if 'user_id' not in session or session['user_id'] != schuetze_id:
                return redirect(url_for('login', schuetze_id=schuetze_id))

            # Find shooter
            all_schuetzen = self.schuetze_model.get_all_schuetzen()
            schuetze = None
            for s in all_schuetzen:
                if self.schuetze_model.get_schuetze_id(s) == schuetze_id:
                    schuetze = s
                    break

            if not schuetze:
                return "Schütze nicht gefunden", 404

            # Verify group permission
            if str(schuetze.get('gruppe', '')) not in self.active_groups:
                return "Eingabe für diese Gruppe derzeit nicht möglich", 403

            turnier_data = self.turnier_model.get_turnier_data()
            anzahl_passen = turnier_data.get('anzahl_passen', 6)

            # Load existing raw data
            ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            raw_data = {}
            if ergebnis and 'web_raw_data' in ergebnis:
                # Convert keys to strings for template access if needed, though Jinja handles ints usually
                # But let's ensure compatibility with JSON structure
                # Assuming stored as {0: [...], 1: [...]}
                # We convert keys to strings for safe template usage if stored as ints in JSON
                raw_data = {str(k): v for k, v in ergebnis['web_raw_data'].items()}

            return render_template('input.html',
                                   name=f"{schuetze['vorname']} {schuetze['name']}",
                                   klasse=schuetze['klasse'],
                                   verein=schuetze['verein'],
                                   schuetze_id=schuetze_id,
                                   anzahl_passen=anzahl_passen,
                                   raw_data=raw_data)

        @self.app.route('/api/save', methods=['POST'])
        def save_data():
            data = request.json
            schuetze_id = data.get('schuetze_id')
            raw_data_in = data.get('data') # {0: [10, 9..], 1: [..]}

            if not schuetze_id or not raw_data_in:
                return jsonify({'success': False, 'error': 'Missing data'})

            # Process data
            # We need to convert raw_data_in (which might have "0", "1" keys from JSON) to int keys
            # and calculate sums.

            passen_sums = []
            total_10 = 0
            total_9 = 0

            # Determine number of passes from tournament model
            anzahl_passen = self.turnier_model.get_turnier_data().get('anzahl_passen', 6)

            # Clean raw data structure for storage
            web_raw_data = {}

            for i in range(anzahl_passen):
                # Get shots for this pass (handle string/int keys)
                shots = raw_data_in.get(str(i)) or raw_data_in.get(i)

                passe_sum = 0
                shots_list = []

                if shots:
                    for shot in shots:
                        if shot is not None: # shot can be 0
                            val = int(shot)
                            passe_sum += val
                            shots_list.append(val)
                            if val == 10:
                                total_10 += 1
                            elif val == 9:
                                total_9 += 1
                        else:
                            shots_list.append(None)

                passen_sums.append(passe_sum)
                web_raw_data[i] = shots_list

            # Update Model
            self.turnier_model.add_web_ergebnis(
                schuetze_id,
                passen_sums,
                total_10,
                total_9,
                web_raw_data
            )

            return jsonify({'success': True})

    def set_active_groups(self, groups):
        """Sets the list of allowed groups (as strings)"""
        self.active_groups = set(str(g) for g in groups)

    def start(self, port=8080):
        if self.is_running:
            return

        self.port = port
        self.is_running = True

        # Run Server in a thread using werkzeug.serving.make_server for control
        self.server = make_server('0.0.0.0', port, self.app)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def stop(self):
        if self.is_running and self.server:
            self.server.shutdown()
            self.is_running = False
            self.server = None

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
