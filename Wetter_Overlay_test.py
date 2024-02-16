#!/usr/bin/env python3
import time
import configparser
import funktionen
config = configparser.ConfigParser()
try:
    config.read("settings.ini")
    print("settings.ini eingelesen")
except FileNotFoundError as e:
    print("settings.ini nicht gefunden! Bitte überprüfen!")
    raise SystemExit() from e
except configparser.Error as e:
    print(f"Fehler beim Lesen der Konfigurationsdatei: {e}")
    raise SystemExit() from e

# Werte aus ini Datei zuweisen
ulanzi_url = config["ULANZI"]["url"]

funktionen.kill_all_indicator(ulanzi_url)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "drizzle"}
funktionen.ulanzi_senden_raw(url, data)

url = ulanzi_url + "/api/notify"
data = {
        "text": "Nieselregen (drizzle)          ",
        "rainbow": bool(1),
        "duration": 15  
    }
funktionen.ulanzi_senden_raw(url, data)
time.sleep(15)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "rain"}
funktionen.ulanzi_senden_raw(url, data)

url = ulanzi_url + "/api/notify"
data = {
        "text": "Regen (rain)         ",
        "rainbow": bool(1),
        "duration": 15  
    }
funktionen.ulanzi_senden_raw(url, data)
time.sleep(15)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "storm"}
funktionen.ulanzi_senden_raw(url, data)

url = ulanzi_url + "/api/notify"
data = {
        "text": "Sturm (storm)         ",
        "rainbow": bool(1),
        "duration": 15  
    }
funktionen.ulanzi_senden_raw(url, data)
time.sleep(15)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "thunder"}
funktionen.ulanzi_senden_raw(url, data)

url = ulanzi_url + "/api/notify"
data = {
        "text": "Gewitter (thunder)          ",
        "rainbow": bool(1),
        "duration": 15  
    }
funktionen.ulanzi_senden_raw(url, data)
time.sleep(15)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "snow"}
funktionen.ulanzi_senden_raw(url, data)

url = ulanzi_url + "/api/notify"
data = {
        "text": "Schnee (snow)        ",
        "rainbow": bool(1),
        "duration": 15  
    }
funktionen.ulanzi_senden_raw(url, data)
time.sleep(15)

url = ulanzi_url + "/api/settings"
data = {"BRI": 255,
        "OVERLAY": "clear"}
funktionen.ulanzi_senden_raw(url, data)
