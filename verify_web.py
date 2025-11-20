import time
import requests
import threading
from models import SchuetzeModel, TurnierModel
from web_server import WebServer

def test_integration():
    print("Setting up models...")
    tm = TurnierModel()
    sm = SchuetzeModel()

    # Add a shooter
    print("Adding shooter...")
    idx = sm.add_schuetze("Doe", "John", "Herren", "VereinX", gruppe=1)
    s = sm.get_schuetze(idx)
    s_id = sm.get_schuetze_id(s)
    pin = s['pin']
    print(f"Shooter added: {s_id}, PIN: {pin}")

    # Start Server
    print("Starting Web Server...")
    server = WebServer(tm, sm)
    server.set_active_groups(['1']) # Enable Group 1
    server.start(port=8081)

    # Wait for server start
    time.sleep(2)

    base_url = "http://127.0.0.1:8081"

    try:
        # 1. Check Index
        print("Testing Index...")
        resp = requests.get(base_url + "/")
        assert resp.status_code == 200
        assert "John Doe" in resp.text
        print("Index OK")

        # 2. Check Login Page
        print("Testing Login Page...")
        resp = requests.get(f"{base_url}/login/{s_id}")
        assert resp.status_code == 200
        assert "PIN Eingabe" in resp.text
        print("Login Page OK")

        # 3. Perform Login
        print("Testing Login Action...")
        session = requests.Session()
        resp = session.post(f"{base_url}/login/{s_id}", data={'pin': pin})
        assert resp.status_code == 200 # Should redirect or show input, requests follows redirects by default
        assert "Ergebniseingabe" in resp.text
        print("Login Action OK")

        # 4. Submit Data
        print("Testing Data Submission...")
        # Simulate 6 shots for pass 0
        data = {
            'schuetze_id': s_id,
            'data': {
                '0': [10, 9, 9, 8, 8, 8] # Sum: 52
            }
        }
        resp = requests.post(f"{base_url}/api/save", json=data)
        assert resp.status_code == 200
        assert resp.json()['success'] == True
        print("Data Submission OK")

        # 5. Verify Model Update
        print("Verifying Model Update...")
        ergebnis = tm.get_ergebnis(s_id)
        assert ergebnis is not None
        assert ergebnis['passen'][0] == 52
        assert ergebnis['anzahl_10er'] == 1
        assert ergebnis['anzahl_9er'] == 2
        # Check raw data
        assert str(ergebnis['web_raw_data']) is not None
        print(f"Model updated correctly: {ergebnis}")

        print("ALL TESTS PASSED")

    except Exception as e:
        print(f"TEST FAILED: {e}")
    finally:
        print("Stopping server...")
        server.stop()

if __name__ == "__main__":
    test_integration()
