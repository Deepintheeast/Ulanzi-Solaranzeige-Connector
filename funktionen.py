## Funktionen definieren ##
## bitte hier nichts verändern ##

import requests
import bs4 as bs

# Funktion URL auf Verfügbarkeit testen
def url_verfuegbar(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
# Ende Funktion url_verfuegbar
#
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
# Ende Funktion db_abfrage
#
# Funktion Daten an Ulanzi senden
def ulanzi_senden(url,data):
    response = requests.post(url, json=data)
    #logging.info(f'{url},{data}')
# Ende Funktion ulanzi_senden
#
# Funktion intro
def intro(ulanzi_url,version_nr):
    url = ulanzi_url + '/api/notify'
    data = {
        "text": "Ulanzi->Solaranzeige Connector Version "+str(version_nr),
        #"text": "Have Fun!",
        "rainbow": bool(1),
        "repeat": 1
    }
    ulanzi_senden(url,data)
# Ende Funktion intro
#
# Start Funktion Ulanzi An/Aus schalten
def ulanzi_an_aus(ulanzi_url,x):
    url = ulanzi_url + '/api/power'
    data = {
        "power": bool(x),
    }
    ulanzi_senden(url,data)
# Ende Funktion Ulanzi An/Aus
#
