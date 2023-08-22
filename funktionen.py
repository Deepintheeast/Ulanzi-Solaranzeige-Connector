## Funktionen definieren ##
## bitte hier nichts verändern ##

import requests
import bs4 as bs
import time

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
      #logging.debug(XML)
      headers = {'Content-Type': 'application/xml'} # set what your server accepts
      data = (requests.post(solaranzeige_url+"/api/control.php", data=XML, headers=headers).text)
      #logging.debug(data)
      soup = bs.BeautifulSoup(data,"xml")
      for wert in soup.find_all('fieldname'):
        return datenbank,measurement,datenpunkt,wert.text
# Ende Funktion
# ----------------------------------
# Funktion Daten an Ulanzi senden
def ulanzi_senden(url,data):
    response = requests.post(url, json=data)
    # print('#### Status Code:')
    print('#### Status Code: ' + str(response.status_code) + ' ####')
    #requests.exceptions.ConnectionError
    #logging.info(f'{url},{data}')

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
        #"text": "Have Fun!",
        "rainbow": bool(1),
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
