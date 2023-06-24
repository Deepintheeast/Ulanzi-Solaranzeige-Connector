#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.20

# benötigte Bibliotheken importieren
import logging
import requests
import bs4 as bs
import time

# diverse Einstellungen
VERSION_NR = "0.20"

SOLARANZEIGE_URL = "http://192.x.x.x" # URL der Solaranzeige
ULANZI_URL = "http://192.x.x.x" # URL der Ulanzi Pixelclock

WERTE = ("solaranzeige,PV,Leistung","solaranzeige,Summen,Wh_GesamtHeute",)

START_ZEIT = "06:00" # Start der Darstellung der Werte auf Ulanzi-Clock
STOP_ZEIT = "22:30" # Ende der Darstellung der Werte auf Ulanzi-Clock

LOG_DATEI = "/home/pi/scripts/ulanzi.log" # Pfad und Name der Logdatei
LOG_LEVEL = "INFO"  # NOTSET =0, DEBUG =10, INFO =20, WARN =30, ERROR =40, and CRITICAL =50

# ab hier bitte nichts mehr ändern!

# Logging definieren
logging.basicConfig(filename=LOG_DATEI, level=logging.getLevelName(LOG_LEVEL),
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

## Funktionen definieren ##
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
def db_abfrage(DATENBANK,MEASUREMENT,DATENPUNKT):
      XML = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>" \
            "<solaranzeige><version>1.0</version>" \
            "<in_out>out</in_out>" \
            "<database name=\""+DATENBANK+"\">" \
            "<measurement name=\""+MEASUREMENT+"\">" \
            "<fieldname name=\""+DATENPUNKT+"\">" \
            "</fieldname>" \
            "</measurement>" \
            "</database></solaranzeige>"
      logging.debug(XML)
      headers = {'Content-Type': 'application/xml'} # set what your server accepts
      data = (requests.post(SOLARANZEIGE_URL+"/api/control.php", data=XML, headers=headers).text)
      logging.debug(data)
      soup = bs.BeautifulSoup(data,"xml")
      for wert in soup.find_all('fieldname'):
        return DATENBANK,MEASUREMENT,DATENPUNKT,wert.text
# Ende Funktion db_abfrage
#
# Funktion Ulanzi senden
def ulanzi_senden(url,data):
    response = requests.post(url, json=data)
    logging.info(f'{url},{data}')
# Ende Funktion ulanzi_senden
#
# Funktion intro
def intro():
    url = ULANZI_URL + '/api/notify'
    data = {
        "text": "Ulanzi->Solaranzeige Connector Version "+str(VERSION_NR),
        "rainbow": bool(1),
        "repeat": 1
    }
    ulanzi_senden(url,data)
# Ende Funktion intro
#
# Start Funktion Ulanzi An/Aus schalten
def ulanzi_an_aus(x):
    url = ULANZI_URL + '/api/power'
    data = {
        "power": bool(x),
    }
    ulanzi_senden(url,data)
# Ende Funktion Ulanzi An/Aus
#
# Start Funtion Loop
def loop():

    WERT = db_abfrage(DATENBANK,MEASUREMENT,DATENPUNKT)

    ################################# Beginn Block Auswertung #################################

    if ((WERT[0])+","+(WERT[1])+","+(WERT[2])) == "solaranzeige,PV,Leistung":
        print(WERT[3])

        url = ULANZI_URL + "/api/custom?name="+(WERT[1])+"_"+(WERT[2])

        data = {
            "text": str(int(float(WERT[3]))) + " W",
            "icon": 27283,
            "rainbow": bool(1),
            "duration": 3
        }
        ulanzi_senden(url,data)
    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif (WERT[0])+","+(WERT[1])+","+(WERT[2]) == "solaranzeige,Summen,Wh_GesamtHeute":
        print(WERT[3])

        url = ULANZI_URL + "/api/custom?"+(WERT[1])+"_"+(WERT[2])

        data = {
            "text": str(round((float((WERT[3])) / 1000), 2))+" kWh",
            "icon": 51301,
            "color": [252, 186, 3],
            "duration": 3
        }
        ulanzi_senden(url,data)

    ################################## Ende Block Auswertung ##################################

    else:
        print("Nope, keine Auswertung verfügbar für "+str(WERT[0])+","+str(WERT[1])+","+(WERT[2]))
# Ende Funktion Loop

## Programm starten ##
print(str(url_verfuegbar(SOLARANZEIGE_URL))+" -> Solaranzeige verfügbar")
if not (url_verfuegbar(SOLARANZEIGE_URL)):
    exit("Solaranzeige unter der eingegeben URL nicht erreichbar!")

print(str(url_verfuegbar(ULANZI_URL))+" -> Ulanzi verfügbar")
if not (url_verfuegbar(ULANZI_URL)):
    exit("Ulanzi unter der eingegeben URL nicht erreichbar!")

# Ulanzi anschalten
ulanzi_an_aus(1)

# Intro senden
intro()
time.sleep(8)

# Loop starten
while True:

    uhrzeit = time.strftime("%H:%M")
    #print(uhrzeit)

    if uhrzeit >= START_ZEIT and uhrzeit < STOP_ZEIT:
        ulanzi_an_aus(1)

        zaehler = 0
        for element in WERTE:
            D_M_D = (WERTE[zaehler].split(","))
            print(D_M_D)
            DATENBANK = (D_M_D[0])
            MEASUREMENT = (D_M_D[1])
            DATENPUNKT = (D_M_D[2])
            loop()
            time.sleep(5)
            zaehler = zaehler + 1
    else:
        ulanzi_an_aus(0)
        print(uhrzeit+"  Pause, ausserhalb \"Start - Stop\" Bereich!")
        time.sleep(60)
