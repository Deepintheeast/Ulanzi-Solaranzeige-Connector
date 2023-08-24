#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.4

import time
import funktionen
import loop
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

## Programm starten ##
print(str(funktionen.url_verfuegbar(solaranzeige_url)) + " -> Solaranzeige URL verfügbar")
if not (funktionen.url_verfuegbar(solaranzeige_url)):
    exit("Solaranzeige unter der eingegeben URL nicht erreichbar!")

print(str(funktionen.url_verfuegbar(ulanzi_url)) + " -> Ulanzi URL verfügbar")
if not (funktionen.url_verfuegbar(ulanzi_url)):
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
            x = True
        zaehler = 0
        for element in werte:
            D_M_D = (werte[zaehler].split(","))
            print(time.strftime("%H:%M:%S"))
            print(D_M_D)
            datenbank = (D_M_D[0])
            measurement = (D_M_D[1])
            datenpunkt = (D_M_D[2])
            loop.loop(datenbank, measurement, datenpunkt, solaranzeige_url,ulanzi_url,app_life_time,app_show_time)
            time.sleep(10)
            zaehler = zaehler + 1
    else:
        if x:
            if not night_show:
                funktionen.ulanzi_an_aus(ulanzi_url,0)
            funktionen.ulanzi_night_show_app_set(ulanzi_url,night_show_app)
            funktionen.ulanzi_auto_trans(ulanzi_url,0)
        x = False

        print(uhrzeit + ' Night-Show is '+str(night_show))
        time.sleep(60)
