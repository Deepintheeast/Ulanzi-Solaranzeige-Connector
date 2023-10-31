## Funktionen definieren ##
## bitte hier nichts verändern !!! ##

import requests
import bs4 as bs
import time
from suntime import Sun
from datetime import datetime, timedelta

# Funktion URL auf Verfügbarkeit testen
def url_verfuegbar(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
# Ende Funktion
# ----------------------------------
# Funktion zur Abfrage der Daten aus der DB über API
def db_abfrage(datenbank,measurement,datenpunkt,solaranzeige_url):
      XML = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" \
            "<solaranzeige><version>1.0</version>" \
            "<in_out>out</in_out>" \
            "<database name=\""+datenbank+"\">" \
            "<measurement name=\""+measurement+"\">" \
            "<fieldname name=\""+datenpunkt+"\">" \
            "</fieldname>" \
            "</measurement>" \
            "</database></solaranzeige>"
      headers = {'Content-Type': 'application/xml'} # set what your server accepts
      data = (requests.post(solaranzeige_url+"/api/control.php", data=XML, headers=headers).text)
      #soup = bs.BeautifulSoup(data,"xml")
      soup = bs.BeautifulSoup(data,"html.parser")
      for wert in soup.find_all('fieldname'):
        return datenbank,measurement,datenpunkt,wert.text
# Ende Funktion
# ----------------------------------
# Funktion Daten an Ulanzi senden
def ulanzi_senden(url, data):
    response = requests.post(url, json=data)
    #print('#### Status Code: ' + str(response.status_code) + ' ####')
    #requests.exceptions.ConnectionError

# Ende Funktion
# ----------------------------------
# Funktion intro
def intro(ulanzi_url,version_nr):
    url = ulanzi_url + "/api/settings"
    data = {
        "BRI": 255}
    ulanzi_senden(url, data)

    url = ulanzi_url + '/api/notify'
    data = {
        "text": "Ulanzi->Solaranzeige Connector Version "+str(version_nr),
        "rainbow": bool(1),
        "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c",
        "repeat": 1
    }
    ulanzi_senden(url,data)
# Ende Funktion
# ----------------------------------
# Start Funktion Ulanzi An/Aus schalten
def ulanzi_an_aus(ulanzi_url,x):
    url = ulanzi_url + '/api/power'
    data = {
        "power": bool(x),
    }
    ulanzi_senden(url,data)
# Ende Funktion
# ----------------------------------
# Start Helligkeit einstellen
def ulanzi_hell_set(ulanzi_url,h):
    url = ulanzi_url + "/api/settings"
    if h in ['a', 'A']:
        data = {
            "ABRI": bool(1)}
    else:
        data = {
            "ABRI": bool(0),
            "BRI":h }
    ulanzi_senden(url, data)
# Ende Funktion
# ----------------------------------
# Start Funktion Modecheck
def mode_check(start_zeit,stop_zeit):
    uhrzeit = time.strftime("%H:%M")
    x = "N"
    if uhrzeit >= start_zeit and uhrzeit < stop_zeit:
        x = "D"
    return x
# Ende Funktion
# ----------------------------------
# Indikatoren löschen einzeln
def kill_indicator(ulanzi_url,Nummer):
    url = ulanzi_url + "/api/indicator"+str(Nummer)
    data = {
        }
    ulanzi_senden(url, data)
# Ende Funktion
# ----------------------------------
# Indikatoren löschen alle
def kill_all_indicator(ulanzi_url):
    i = 1
    while i <= 3:
        url = ulanzi_url + "/api/indicator" + str(i)
        data = {
        }
        ulanzi_senden(url, data)
        i += 1
# Ende Funktion
# ----------------------------------
# Übergangseffekte setzen
def ulanzi_effekt_set(ulanzi_url,trans_effect,trans_effect_time):
    url = ulanzi_url + "/api/settings"
    data = {
     "TEFF" : trans_effect,
     "TSPEED" : trans_effect_time
    }
    ulanzi_senden(url,data)
# Ende Funktion
# ----------------------------------
# Night_show_app setzen
def ulanzi_night_show_app_set(ulanzi_url,night_show_app):
    url = ulanzi_url + "/api/switch"
    data = {
        "name": night_show_app
    }
    ulanzi_senden(url,data)
    kill_all_indicator(ulanzi_url)
# Ende Funktion
# ----------------------------------
# Auto Transision on/off setzen
def ulanzi_auto_trans(ulanzi_url,on_off):
    url = ulanzi_url+ "/api/settings"
    data = {
        "ATRANS": on_off
    }
    ulanzi_senden(url, data)
# Ende Funktion
# ----------------------------------
# Ulanzi init
def ulanz_init(ulanzi_url,text_uppercase,text_scrollspeed):
    url = ulanzi_url + "/api/settings"
    data = {
        "UPPERCASE": text_uppercase ,
        "SSPEED": text_scrollspeed
    }
    ulanzi_senden(url, data)
# Ende Funktion
# ----------------------------------
# Funktion Abfrage Sonnenaufgang/untergang
def get_sa_su(breite, laenge, sa_korrektur=0, su_korrektur=0):
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
# ----------------------------------
