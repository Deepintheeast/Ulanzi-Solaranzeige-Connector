#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.3

import logging
import time
import funktionen

version_nr = "0.30"
solaranzeige_url = "http://192.168.x.x"  # URL der Solaranzeige
ulanzi_url = "http://192.168.x.x"  # URL der Ulanzi Pixelclock

werte = ("solaranzeige,PV,Leistung",
         "solaranzeige,Summen,Wh_GesamtHeute")

start_zeit = "06:00"  # Start der Darstellung der Werte auf Ulanzi-Clock
stop_zeit = "22:30"  # Ende der Darstellung der Werte auf Ulanzi-Clock

log_datei = "/home/pi/scripts/ulanzi.log"  # Pfad und Name der Logdatei
log_level = "INFO"  # NOTSET =0, DEBUG =10, INFO =20, WARN =30, ERROR =40, and CRITICAL =50

# Logging definieren
logging.basicConfig(filename=log_datei, filemode='w', level=logging.getLevelName(log_level),
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# Definition Loop
def loop():
    wert = funktionen.db_abfrage(datenbank, measurement, datenpunkt, solaranzeige_url)
    logging.info({wert})

    ################################# Beginn Block Auswertung #################################

    if ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,PV,Leistung":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + "_" + (wert[2])

        data = {
            "text": str(int(float(wert[3]))) + " W",
            "icon": 27283,
            "rainbow": bool(1),
            # "lifetime": 20,
            "duration": 3
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Summen,Wh_GesamtHeute":
        print(wert[3])

        url = ulanzi_url + "/api/custom?" + (wert[1]) + "_" + (wert[2])

        data = {
            "text": str(round((float((wert[3])) / 1000), 2)) + " kWh",
            "icon": 51301,
            "color": [252, 186, 3],
            # "lifetime": 20,
            # "pushIcon": 1,
            "duration": 4
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################


    else:
        logging.info('  Keine passende Abfrage oder Fehler in Abfrage!?')
        print("Nope, keine Auswertung verfügbar für " + str(wert[0]) + "," + str(wert[1]) + "," + (wert[2]))


# Ende Funktion Loop


## Programm starten ##
print(str(funktionen.url_verfuegbar(solaranzeige_url)) + " -> Solaranzeige verfügbar")
if not (funktionen.url_verfuegbar(solaranzeige_url)):
    logging.info('Solaranzeige ist nicht erreichbar !!!')
    exit("Solaranzeige unter der eingegeben URL nicht erreichbar!")

print(str(funktionen.url_verfuegbar(ulanzi_url)) + " -> Ulanzi verfügbar")
if not (funktionen.url_verfuegbar(ulanzi_url)):
    logging.info('Ulanzi ist nicht erreichbar !!!')
    exit("Ulanzi unter der eingegeben URL nicht erreichbar!")

# Ulanzi anschalten
funktionen.ulanzi_an_aus(ulanzi_url, 1)
# Intro senden
funktionen.intro(ulanzi_url, version_nr)

time.sleep(8)
x = True
# Loop starten
while True:

    uhrzeit = time.strftime("%H:%M")
    # print(uhrzeit)

    if uhrzeit >= start_zeit and uhrzeit < stop_zeit:
        if not x:
            funktionen.ulanzi_an_aus(ulanzi_url, 1)
            logging.info('-- Ulanzi *** an *** gesendet!')
            x = True
        zaehler = 0
        for element in werte:
            D_M_D = (werte[zaehler].split(","))
            print(D_M_D)
            datenbank = (D_M_D[0])
            measurement = (D_M_D[1])
            datenpunkt = (D_M_D[2])
            loop()
            logging.info(f'DB Abfrage mit ** {datenbank} , {measurement} , {datenpunkt} ** gestartet !')
            time.sleep(10)
            zaehler = zaehler + 1
    else:
        if x:
            funktionen.ulanzi_an_aus(ulanzi_url, 0)
            logging.info('-- Ulanzi *** AUS *** gesendet!')
            x = False
        print(uhrzeit + "  Pause!")
        time.sleep(60)
