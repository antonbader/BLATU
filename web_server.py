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

        @self.app.route('/login_multi', methods=['GET', 'POST'])
        def login_multi():
            ids = request.args.getlist('ids')
            # If coming from POST (submission of PINs), ids might be hidden or in session?
            # Actually, typical pattern: GET /login_multi?ids=1&ids=2 -> Show Form
            # POST /login_multi -> Process PINs -> Redirect to /input_multi

            if request.method == 'POST':
                # Process PINs
                # We need to know which IDs we are checking. They are keys in form like 'pin_<id>'
                valid_ids = []
                errors = []

                all_schuetzen = self.schuetze_model.get_all_schuetzen()

                # Map ID to shooter
                schuetzen_map = {}
                for s in all_schuetzen:
                    sid = self.schuetze_model.get_schuetze_id(s)
                    schuetzen_map[sid] = s

                for key, value in request.form.items():
                    if key.startswith('pin_'):
                        sid = key.replace('pin_', '')
                        if sid in schuetzen_map:
                            s = schuetzen_map[sid]
                            if s.get('pin') == value:
                                valid_ids.append(sid)
                            else:
                                errors.append(f"Falsche PIN für {s['vorname']} {s['name']}")

                if errors:
                     # Re-render with error
                     # We need to reconstruct the list of shooters for the form
                     # Extract IDs from keys again
                     target_ids = [k.replace('pin_', '') for k in request.form.keys() if k.startswith('pin_')]
                     display_schuetzen = []
                     for sid in target_ids:
                         if sid in schuetzen_map:
                             s_copy = schuetzen_map[sid].copy()
                             s_copy['id'] = sid
                             display_schuetzen.append(s_copy)
                     return render_template('login_multi.html', schuetzen=display_schuetzen, error="; ".join(errors))

                # Success
                session['logged_in_ids'] = valid_ids
                return redirect(url_for('input_multi'))

            # GET Request
            if not ids:
                return redirect(url_for('index'))

            display_schuetzen = []
            all_schuetzen = self.schuetze_model.get_all_schuetzen()
            for s in all_schuetzen:
                sid = self.schuetze_model.get_schuetze_id(s)
                if sid in ids:
                    # Check group
                    if str(s.get('gruppe', '')) in self.active_groups:
                        s_copy = s.copy()
                        s_copy['id'] = sid
                        display_schuetzen.append(s_copy)

            if not display_schuetzen:
                return "Keine gültigen Schützen ausgewählt", 400

            return render_template('login_multi.html', schuetzen=display_schuetzen)

        @self.app.route('/input_multi')
        def input_multi():
            ids = session.get('logged_in_ids', [])
            if not ids:
                return redirect(url_for('index'))

            turnier_data = self.turnier_model.get_turnier_data()
            anzahl_passen = turnier_data.get('anzahl_passen', 6)

            display_schuetzen = []
            initial_sums_map = {}

            all_schuetzen = self.schuetze_model.get_all_schuetzen()
            for s in all_schuetzen:
                sid = self.schuetze_model.get_schuetze_id(s)
                if sid in ids:
                    # Check group again just in case
                    if str(s.get('gruppe', '')) not in self.active_groups:
                        continue

                    s_copy = s.copy()
                    s_copy['id'] = sid

                    # Load data
                    ergebnis = self.turnier_model.get_ergebnis(sid)
                    raw_data = {}
                    initial_sums = {}

                    if ergebnis:
                        if 'web_raw_data' in ergebnis:
                            raw_data = {str(k): v for k, v in ergebnis['web_raw_data'].items()}
                        if 'passen' in ergebnis:
                            for i, p_sum in enumerate(ergebnis['passen']):
                                initial_sums[str(i)] = p_sum

                    s_copy['raw_data'] = raw_data
                    initial_sums_map[sid] = initial_sums
                    display_schuetzen.append(s_copy)

            return render_template('input_multi.html',
                                   schuetzen=display_schuetzen,
                                   anzahl_passen=anzahl_passen,
                                   initial_sums_map=initial_sums_map)

        @self.app.route('/api/save_multi', methods=['POST'])
        def save_data_multi():
            data = request.json
            shooters_data = data.get('shooters', [])

            if not shooters_data:
                return jsonify({'success': False, 'error': 'No data'})

            anzahl_passen = self.turnier_model.get_turnier_data().get('anzahl_passen', 6)

            for item in shooters_data:
                self._process_save_single(item['schuetze_id'], item['data'], anzahl_passen)

            return jsonify({'success': True})

        # Compatibility route for single-user index link (redirect to multi flow logic or keep separate?)
        # The single user flow is effectively a subset of multi-user flow.
        # To keep things simple, I'll rewrite /login/<id> to redirect to /login_multi?ids=<id>
        @self.app.route('/login/<schuetze_id>')
        def login_single(schuetze_id):
            return redirect(url_for('login_multi', ids=schuetze_id))

        # Helper for saving logic
        def _process_save_single(self, schuetze_id, raw_data_in, anzahl_passen):
            passen_sums = []
            total_10 = 0
            total_9 = 0
            web_raw_data = {}

            current_ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            current_passen = current_ergebnis.get('passen', []) if current_ergebnis else []

            for i in range(anzahl_passen):
                shots = raw_data_in.get(str(i)) or raw_data_in.get(i)
                passe_sum = 0
                shots_list = []
                has_input = False

                if shots:
                    for shot in shots:
                        if shot is not None:
                            val = int(shot)
                            passe_sum += val
                            shots_list.append(val)
                            has_input = True
                            if val == 10: total_10 += 1
                            elif val == 9: total_9 += 1
                        else:
                            shots_list.append(None)

                if has_input:
                    passen_sums.append(passe_sum)
                    web_raw_data[i] = shots_list
                else:
                    if i < len(current_passen):
                        passen_sums.append(current_passen[i])
                    else:
                        passen_sums.append(0)
                    if current_ergebnis and 'web_raw_data' in current_ergebnis and i in current_ergebnis['web_raw_data']:
                         web_raw_data[i] = current_ergebnis['web_raw_data'][i]

            self.turnier_model.add_web_ergebnis(
                schuetze_id,
                passen_sums,
                total_10,
                total_9,
                web_raw_data
            )

    def _process_save_single(self, schuetze_id, raw_data_in, anzahl_passen):
            passen_sums = []
            total_10 = 0
            total_9 = 0
            web_raw_data = {}

            current_ergebnis = self.turnier_model.get_ergebnis(schuetze_id)
            current_passen = current_ergebnis.get('passen', []) if current_ergebnis else []

            for i in range(anzahl_passen):
                shots = raw_data_in.get(str(i)) or raw_data_in.get(i)
                passe_sum = 0
                shots_list = []
                has_input = False

                if shots:
                    for shot in shots:
                        if shot is not None:
                            val = int(shot)
                            passe_sum += val
                            shots_list.append(val)
                            has_input = True
                            if val == 10: total_10 += 1
                            elif val == 9: total_9 += 1
                        else:
                            shots_list.append(None)

                if has_input:
                    passen_sums.append(passe_sum)
                    web_raw_data[i] = shots_list
                else:
                    if i < len(current_passen):
                        passen_sums.append(current_passen[i])
                    else:
                        passen_sums.append(0)
                    if current_ergebnis and 'web_raw_data' in current_ergebnis and i in current_ergebnis['web_raw_data']:
                         web_raw_data[i] = current_ergebnis['web_raw_data'][i]

            self.turnier_model.add_web_ergebnis(
                schuetze_id,
                passen_sums,
                total_10,
                total_9,
                web_raw_data
            )

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
