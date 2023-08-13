#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.32

import logging
import time
import funktionen

version_nr = "0.32"
solaranzeige_url = "http://192.168.169.233"  # URL der Solaranzeige
ulanzi_url = "http://192.168.169.235"  # URL der Ulanzi Pixelclock

werte = ("solaranzeige,PV,Leistung",
         "solaranzeige,Summen,Wh_GesamtHeute",
         "Pylontech,Batterie,SOC",
         "solaranzeige,aktuellesWetter,Temperatur",
         "solaranzeige,Service,RaspiTemp",
         "solaranzeige,Batterie,Strom",
         "solaranzeige,Service,IntModus")

start_zeit = "06:00"  # Start der Darstellung der Werte auf Ulanzi-Clock
stop_zeit = "23:30"  # Ende der Darstellung der Werte auf Ulanzi-Clock

day_mode_start = "07:00" # Beginn Day-Mode
day_hell = "a" # Helligkeit im Day-Mode "0-255" oder "A" = Automatik

night_mode_start = "21:00" # Beginn Night-Mode
night_hell = "a" # Helligkeit im Night-Mode "0-255" oder "A" = Automatik

trans_effect = "0"  # Übergangseffekt  0 - Zufall, 1 - Slide, 2 - Dim, 3 - Zoom, 4 - Rotate
                    # 5 - Pixelate, 6 - Curtain, 7 - Ripple, 8 - Blink, 9 - Reload, 10 - Fade
trans_effect_time = 500  #Effekt-Zeit in mS

log_datei = "/home/pi/scripts/ulanzi.log"  # Pfad und Name der Logdatei
log_level = "DEBUG"  # NOTSET =0, DEBUG =10, INFO =20, WARN =30, ERROR =40, and CRITICAL =50

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

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        data = {
            "text": str(int(float(wert[3]))) + " W",
            #"pos": 1,
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

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])
        data = {
            "text": str(round((float((wert[3])) / 1000), 2)) + " kWh",
            #"pos": 2,
            "icon": 51301,
            "color": [252, 186, 3],
            # "lifetime": 20,
            # "pushIcon": 1,
            "duration": 4
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,aktuellesWetter,Temperatur":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        data = {
            "text": "Aussentemp.: "+str(round(float(wert[3])))+"°C",
            #"pos": 3,
            "rainbow": bool(1),
            # "lifetime": 20,
            "duration": 4
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ######################## Beginn Block Auswertung Temperatur Raspi #########################
    elif ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,Service,RaspiTemp":
        print(wert[3])
        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])
        if wert[3] <= str(35):
            data = {
                "text": "T:"+str(round(float(wert[3])))+"°C",
                "icon": 9718,
                "color": [0, 204, 0],
                "duration": 4
            }
        elif wert[3] >= str(36) and wert[3] <= str(55):
            data = {
                "text": "T:" + str(round(float(wert[3]))) + "°C",
                "icon": 9718,
                "color": [255, 153, 0],
                "duration": 4
            }
        elif wert[3] >= str(56):
            data = {
                "text": "T:" + str(round(float(wert[3]))) + "°C",
                "icon": 9718,
                "color": [255, 0, 0],
                "duration": 4
            }
        funktionen.ulanzi_senden(url, data)
    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Batterie,Strom":
        print(wert[3])

        url = ulanzi_url + '/api/indicator1'

        if round(float(wert[3])) == 0:
            data = {
                "color": [0, 0, 0]
            }
            funktionen.ulanzi_senden(url, data)

        else:
            data = {
                "color": [0, 255, 0],
                "blink": 1200
            }
            funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Service,IntModus":
        print(wert[3])

        url = ulanzi_url + '/api/indicator3'

        if (wert[3]) == "3":  # Batteriemodus
            data = {
                "color": [0, 255, 0]
            }
            funktionen.ulanzi_senden(url, data)

        elif (wert[3]) == "4":  # Line(Netz)modus
            data = {
                "color": [0, 0, 255]
            }
            funktionen.ulanzi_senden(url, data)

        elif (wert[3]) == "5":  # Error(Fehler)modus
            data = {
                "color": [255, 0, 0],
                "blink": 100
            }
            funktionen.ulanzi_senden(url, data)

            url = ulanzi_url + '/api/notify'
            data = {
                "text": "Achtung! Wechselrichter befindet sich im Fehlermodus! Bitte überprüfen! ",
                "color": [255, 0, 0],
                "hold": bool(1)
            }
            funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "Pylontech,Batterie,SOC":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        if int(wert[3]) >= 1 and int(wert[3]) <= 10:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 12832,
                "color": [154, 250, 10],
                "duration": 3
            }
            #funktionen.ulanzi_senden(url, data)

        elif int(wert[3]) >= 11 and int(wert[3]) <= 30:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 6359,
                "color": [154, 250, 10],
                "duration": 3
            }
            #funktionen.ulanzi_senden(url, data)

        elif int(wert[3]) >= 31 and int(wert[3]) <= 50:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 6360,
                "color": [154, 250, 10],
                "duration": 3
            }
            #funktionen.ulanzi_senden(url, data)

        elif int(wert[3]) >= 51 and int(wert[3]) <= 70:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 6361,
                "color": [154, 250, 10],
                "duration": 3
            }
            #funktionen.ulanzi_senden(url, data)

        elif int(wert[3]) >= 71 and int(wert[3]) <= 90:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 6362,
                "color": [154, 250, 10],
                "duration": 3
            }
            #funktionen.ulanzi_senden(url, data)

        elif int(wert[3]) >= 91 and int(wert[3]) <= 100:
            data = {
                "text": (wert[3]) + " %",
                #"pos": 4,
                "icon": 6363,
                "color": [154, 250, 10],
                "duration": 3
            }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    else:
        logging.info('  Keine passende Abfrage oder Fehler in Abfrage!?')
        print("Nope, keine Auswertung verfügbar für " + str(wert[0]) + "," + str(wert[1]) + "," + (wert[2]))


# Ende Funktion Loop


## Programm starten ##
print(str(funktionen.url_verfuegbar(solaranzeige_url)) + " -> Solaranzeige URL verfügbar")
if not (funktionen.url_verfuegbar(solaranzeige_url)):
    logging.info('Solaranzeige URL ist nicht erreichbar !!!')
    exit("Solaranzeige unter der eingegeben URL nicht erreichbar!")

print(str(funktionen.url_verfuegbar(ulanzi_url)) + " -> Ulanzi URL verfügbar")
if not (funktionen.url_verfuegbar(ulanzi_url)):
    logging.info('Ulanzi URL ist nicht erreichbar !!!')
    exit("Ulanzi unter der eingegeben URL nicht erreichbar!")

# Ulanzi anschalten
funktionen.ulanzi_an_aus(ulanzi_url, 1)

# diverse Einstellungen vornehmen (senden)
# Übergangseffekt etc. festlegen
url = ulanzi_url + "/api/settings"
data = {
     "TEFF" : trans_effect,
     "TSPEED" : trans_effect_time
    }
funktionen.ulanzi_senden(url,data)


# Intro senden
funktionen.intro(ulanzi_url, version_nr)

time.sleep(8)
x = True
# Loop starten
while True:
    # Helligkeit setzen Start
    mode = funktionen.mode_check(day_mode_start, night_mode_start)
    print(mode+"-Mode")
    if mode == "D":
        funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
        print("** -> Day_hell gesendet")
    elif mode == "N":
        funktionen.ulanzi_hell_set(ulanzi_url, night_hell)
        print("** -> Night_hell gesendet")
    # Helligkeit setzen Ende

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
            time.sleep(5)
            zaehler = zaehler + 1
    else:
        if x:
            funktionen.ulanzi_an_aus(ulanzi_url,0)
            logging.info('-- Ulanzi *** AUS *** gesendet!')
            x = False
        print(uhrzeit + "  Pause!")
        time.sleep(60)
