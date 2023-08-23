#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.4

import logging
import time
import funktionen
from configparser import (
    ConfigParser,
    ExtendedInterpolation
)

config = ConfigParser(
    interpolation=ExtendedInterpolation()
)

try:
    config.read('settings.ini')
    print("settings.ini eingelesen")
except:
    print("settings.ini Error! Bitte überprüfen!")
    raise SystemExit()

# Werte aus ini Datei zuweisen #
solaranzeige_url = config['SOLARANZEIGE']['url']
werte = config['SOLARANZEIGE']['app_werte'].split()
ulanzi_url= config['ULANZI']['url']
start_zeit = config['ULANZI']['start_zeit']
stop_zeit = config['ULANZI']['stop_zeit']
day_mode_start = config['ULANZI']['start_daymode']
day_hell = config['ULANZI']['helligkeit_daymode']
night_mode_start = config['ULANZI']['start_nightmode']
night_hell = config['ULANZI']['helligkeit_nightmode']
trans_effect = config['ULANZI']['trans_effect']
trans_effect_time = config['ULANZI']['trans_effect_time']
app_life_time = config['ULANZI']['app_life_time']
app_show_time = config['ULANZI']['app_show_time']
text_uppercase = config.getboolean('ULANZI','text_uppercase')
text_scrollspeed = config['ULANZI']['text_scrollspeed']
night_show = config.getboolean('ULANZI','night_show')
night_show_app = config['ULANZI']['night_show_app']
version_nr = config['SCRIPT']['version_nr']
log_datei = config['SCRIPT']['log_datei']
log_level = config['SCRIPT']['log_level']

# Logging definieren
logging.basicConfig(filename=log_datei, filemode='w', level=logging.getLevelName(log_level),
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

# Definition Loop
def loop():
    wert = funktionen.db_abfrage(datenbank, measurement, datenpunkt, solaranzeige_url)
    logging.info({wert})


    ################################# Beginn Block Auswertung #################################
    ################################ "solaranzeige,PV,Leistung" ###############################

    if ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,PV,Leistung":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        data = {
            "text": str(int(float(wert[3]))) + " W", # darzustellender Wert/Text
            "lifetime": int(app_life_time),
            "icon": 27283, # darzustellendes Icon
            "rainbow": bool(1),
            "duration": app_show_time
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################


    ################################# Beginn Block Auswertung #################################
    ########################### solaranzeige,Summen,Wh_GesamtHeute ############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Summen,Wh_GesamtHeute":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])
        data = {
            "text": str(round((float((wert[3])) / 1000), 2)) + " kWh",
            "lifetime": int(app_life_time),
            "icon": 51301,
            "color": [252, 186, 3],
            "duration": app_show_time
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ######################### solaranzeige,aktuellesWetter,Temperatur #########################

    elif ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,aktuellesWetter,Temperatur":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        data = {
            "text": "Aussentemp.: "+str(round(float(wert[3])))+"°C",
            "lifetime": int(app_life_time),
            "rainbow": bool(1),
            "duration": app_show_time
        }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################# "solaranzeige,Service,RaspiTemp" ############################

    elif ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,Service,RaspiTemp":
        print(wert[3])
        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])
        if wert[3] <= str(35):
            data = {
                "text": "T:"+str(round(float(wert[3])))+"°C",
                "lifetime": int(app_life_time),
                "icon": 9718,
                "color": [0, 204, 0],
                "duration": app_show_time
            }
        elif wert[3] >= str(36) and wert[3] <= str(55):
            data = {
                "text": "T:" + str(round(float(wert[3]))) + "°C",
                "lifetime": int(app_life_time),
                "icon": 9718,
                "color": [255, 153, 0],
                "duration": app_show_time
            }
        elif wert[3] >= str(56):
            data = {
                "text": "T:" + str(round(float(wert[3]))) + "°C",
                "lifetime": int(app_life_time),
                "icon": 9718,
                "color": [255, 0, 0],
                "duration": app_show_time
            }
        funktionen.ulanzi_senden(url, data)
    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################## "solaranzeige,Batterie,Strom" ##############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Batterie,Strom":
        print(wert[3])

        url = ulanzi_url + '/api/indicator1'

        if round(float(wert[3])) == 0:
            data = {
                "color": [0, 0, 0]
            }

        else:
            data = {
                "color": [0, 255, 0],
                #"blink": 1200
                "fade": 5000
            }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################# "solaranzeige,Service,IntModus" #############################

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
    ################################ "Pylontech,Batterie,SOC" #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "Pylontech,Batterie,SOC":
        print(wert[3])

        url = ulanzi_url + "/api/custom?name="+(wert[1])+(wert[2])

        if int(wert[3]) >= 1 and int(wert[3]) <= 10:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 12832,
                "color": [154, 250, 10],
                "duration": app_show_time
            }

        elif int(wert[3]) >= 11 and int(wert[3]) <= 30:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 6359,
                "color": [154, 250, 10],
                "duration": app_show_time
            }

        elif int(wert[3]) >= 31 and int(wert[3]) <= 50:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 6360,
                "color": [154, 250, 10],
                "duration": app_show_time
            }

        elif int(wert[3]) >= 51 and int(wert[3]) <= 70:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 6361,
                "color": [154, 250, 10],
                "duration": app_show_time
            }

        elif int(wert[3]) >= 71 and int(wert[3]) <= 90:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 6362,
                "color": [154, 250, 10],
                "duration": app_show_time
            }

        elif int(wert[3]) >= 91 and int(wert[3]) <= 100:
            data = {
                "text": (wert[3]) + " %",
                "lifetime": int(app_life_time),
                "icon": 6363,
                "color": [154, 250, 10],
                "duration": app_show_time
            }
        funktionen.ulanzi_senden(url, data)

    ################################## Ende Block Auswertung ##################################

    # ab hier bitte nichts mehr ändern !!!

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
# Übergangseffekt etc. festlegen, Indikatoren zurücksetzen
funktionen.ulanz_init(ulanzi_url,text_uppercase,text_scrollspeed)
funktionen.ulanzi_effekt_set(ulanzi_url,trans_effect,trans_effect_time)
funktionen.kill_all_indicator(ulanzi_url)
funktionen.ulanzi_auto_trans(ulanzi_url,1)

# Intro senden
funktionen.intro(ulanzi_url, version_nr)
time.sleep(8)

# Helligkeit einstellen
if funktionen.mode_check(day_mode_start, night_mode_start) == "D":
    funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
else:
    funktionen.ulanzi_hell_set(ulanzi_url, night_hell)

x = True
y = True

# Loop starten
while True:
    # Helligkeit setzen Start
    mode = funktionen.mode_check(day_mode_start, night_mode_start)
    #print(mode+"-Mode")
    if y and mode == "D":
        funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
        print("** -> Day_hell gesendet")
        y = False
    elif not y and mode == "N":
        funktionen.ulanzi_hell_set(ulanzi_url, night_hell)
        print("** -> Night_hell gesendet")
        y = True
    # Helligkeit setzen Ende

    uhrzeit = time.strftime("%H:%M")
    #print(uhrzeit)

    if uhrzeit >= start_zeit and uhrzeit < stop_zeit:
        if not x:
            funktionen.ulanzi_an_aus(ulanzi_url, 1)
            funktionen.ulanzi_auto_trans(ulanzi_url,1)
            logging.info('-- Ulanzi *** an *** gesendet!')
            x = True
        zaehler = 0
        for element in werte:
            D_M_D = (werte[zaehler].split(","))
            print(time.strftime("%H:%M:%S"))
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
            if not night_show:
                funktionen.ulanzi_an_aus(ulanzi_url,0)
                logging.info('-- Ulanzi *** AUS *** gesendet!')
            funktionen.ulanzi_night_show_app_set(ulanzi_url,night_show_app)
            funktionen.ulanzi_auto_trans(ulanzi_url,0)
        x = False

        print(uhrzeit + ' Night-Show is '+str(night_show))
        time.sleep(60)
