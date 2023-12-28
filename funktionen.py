"""Funktionen für "Ulanzi-Solaranzeige-Connector" ab Version 0.44"""
#
# bitte ab hier nichts verändern !!!
#
import time
from datetime import datetime, timedelta
import bs4 as bs
import requests
from suntime import Sun

def url_verfuegbar(url):
    """Funktion URL auf Verfügbarkeit testen"""
    try:
        r = requests.get(url, timeout=10)
        print(f"Statuscode: {r.status_code}")
       # print(f"Header: {r.headers}")
       # print(f"Inhalt: {r.text}")
        return r.status_code == 200 or r.status_code == 403
    except requests.exceptions.ConnectionError as e:
        print(f"Verbindungsfehler: {e}")
        return False
# Ende Funktion

# ----------------------------------
def db_abfrage(datenbank, measurement, datenpunkt, solaranzeige_url):
    """Funktion zur Abfrage der Daten aus der DB über API"""
    xml_tmp = (
        '<?xml version="1.0" encoding="UTF-8" ?>'
        "<solaranzeige><version>1.0</version>"
        "<in_out>out</in_out>"
        '<database name="' + datenbank + '">'
        '<measurement name="' + measurement + '">'
        '<fieldname name="' + datenpunkt + '">'
        "</fieldname>"
        "</measurement>"
        "</database></solaranzeige>"
    )
    headers = {"Content-Type": "application/xml"}  # set what your server accepts
    data = requests.post(
        solaranzeige_url + "/api/control.php",
        data=xml_tmp,
        headers=headers,
        timeout=10
    ).text
    # soup = bs.BeautifulSoup(data,"xml")
    soup = bs.BeautifulSoup(data, "html.parser")
    for wert in soup.find_all("fieldname"):
        return datenbank, measurement, datenpunkt, wert.text
# Ende Funktion

# ----------------------------------
def ulanzi_senden_raw(url, data):
    """Funktion Daten 'raw' an Ulanzi senden"""
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        #print("Erfolgreich gesendet: Statuscode =", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Daten:", e)
# Ende Funktion

# ----------------------------------
def ulanzi_senden(url, data, app_scroll_duration, app_show_time):
    """Funktion Daten an Ulanzi senden
    inkl. setzen von 'repeat' od. 'duration' in Abhängigkeit der Länge von 'text'"""
    if 'duration' in data:
        data.pop('duration')
    if 'repeat' in data:
        data.pop('repeat')
    if 'text' in data and len(data['text']) > 6:
        data['repeat'] = app_scroll_duration
    if 'text' in data and len(data['text']) <= 6:
        data['duration'] = app_show_time
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        #print("Erfolgreich gesendet: Statuscode =", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Daten:", e)
# Ende Funktion

# ----------------------------------
def intro(ulanzi_url, version_nr):
    """Funktion intro"""
    url = ulanzi_url + "/api/settings"
    data = {"BRI": 255}
    ulanzi_senden_raw(url, data)

    url = ulanzi_url + "/api/notify"
    data = {
        "text": "Ulanzi->Solaranzeige Connector Version " + str(version_nr),
        "rainbow": bool(1),
        "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c",
        "repeat": int(2),
    }
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def ulanzi_an_aus(ulanzi_url, x):
    """Start Funktion Ulanzi An/Aus schalten"""
    url = ulanzi_url + "/api/power"
    data = {
        "power": bool(x),
    }
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def ulanzi_hell_set(ulanzi_url, h):
    """Start Helligkeit einstellen"""
    url = ulanzi_url + "/api/settings"
    if h in ["a", "A"]:
        data = {"ABRI": bool(1)}
    else:
        data = {"ABRI": bool(0), "BRI": h}
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def mode_check(start_zeit, stop_zeit):
    """Start Funktion Modecheck"""
    uhrzeit = time.strftime("%H:%M")
    x = "N"
    if uhrzeit >= start_zeit and uhrzeit < stop_zeit:
        x = "D"
    return x
# Ende Funktion

# ----------------------------------
def kill_indicator(ulanzi_url, nummer):
    """Indikatoren löschen einzeln"""
    url = ulanzi_url + "/api/indicator" + str(nummer)
    data = {}
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def kill_all_indicator(ulanzi_url):
    """Indikatoren löschen alle"""
    i = 1
    while i <= 3:
        url = ulanzi_url + "/api/indicator" + str(i)
        data = {}
        ulanzi_senden_raw(url, data)
        i += 1
# Ende Funktion

# ----------------------------------
def ulanzi_effekt_set(ulanzi_url, trans_effect, trans_effect_time):
    """Übergangseffekte setzen"""
    url = ulanzi_url + "/api/settings"
    data = {"TEFF": trans_effect, "TSPEED": trans_effect_time}
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def ulanzi_night_show_app_set(ulanzi_url, night_show_app):
    """Night_show_app setzen"""
    url = ulanzi_url + "/api/switch"
    data = {"name": night_show_app}
    ulanzi_senden_raw(url, data)
    kill_all_indicator(ulanzi_url)
# Ende Funktion

# ----------------------------------
def ulanzi_auto_trans(ulanzi_url, on_off):
    """Auto Transision on/off setzen"""
    url = ulanzi_url + "/api/settings"
    data = {"ATRANS": on_off}
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def ulanz_init(ulanzi_url, text_uppercase, text_scrollspeed):
    """Ulanzi init"""
    url = ulanzi_url + "/api/settings"
    data = {"UPPERCASE": text_uppercase, "SSPEED": text_scrollspeed}
    ulanzi_senden_raw(url, data)
# Ende Funktion

# ----------------------------------
def get_sa_su(breite, laenge, sa_korrektur=0, su_korrektur=0):
    """Funktion Abfrage Sonnenaufgang/untergang"""
    # Erzeuge das Sun-Objekt
    sun = Sun(breite, laenge)

    # Bestimme das aktuelle Datum und die aktuelle Zeit
    now = datetime.now()

    # Prüfe, ob die Sommerzeit aktiv ist
    is_dst = time.localtime().tm_isdst == 1

    # Berechne die Zeiten für Sonnenaufgang und Sonnenuntergang
    sun_auf = sun.get_local_sunrise_time(now)
    sun_unter = sun.get_local_sunset_time(now)

    # Falls Sommerzeit aktiv ist, ziehe eine Stunde von den Zeiten ab
    if is_dst:
        sun_auf -= timedelta(hours=1)
        sun_unter -= timedelta(hours=1)

    # Berücksichtige die Korrekturwerte für Sonnenaufgang und Sonnenuntergang
    sun_auf_korr = sun_auf + timedelta(minutes=sa_korrektur)
    sun_unter_korr = sun_unter + timedelta(minutes=su_korrektur)

    # Konvertiere die Zeiten in String-Format
    sun_auf_str = sun_auf.strftime("%H:%M")
    sun_auf_korr_str = sun_auf_korr.strftime("%H:%M")
    sun_unter_str = sun_unter.strftime("%H:%M")
    sun_unter_korr_str = sun_unter_korr.strftime("%H:%M")

    # Gib die Zeiten als Array von Strings zurück
    return [sun_auf_str, sun_auf_korr_str, sun_unter_str, sun_unter_korr_str]
# Ende Funktion
