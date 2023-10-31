#!/usr/bin/env python3
#
# Ulanzi->Solaranzeige Connector V0.42

import time
import funktionen
import loop
import threading
from datetime import datetime

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

start_astro = config.getboolean('ASTRO','start_astro')
sa_korrektur = config.getint('ASTRO','sa_korrektur')
su_korrektur = config.getint('ASTRO','su_korrektur')
standort_breite = config.getfloat('ASTRO','standort_breite')
standort_laenge = config.getfloat('ASTRO','standort_laenge')
show_sa_su = config.getboolean('ASTRO','show_sa_su')

# Funktion zur Anzeige Sonnen-Auf/Untergang als Thread im Hintergrund
def sa_su_show():
    while True:
        aktuelle_uhrzeit = datetime.now().strftime("%H:%M")
        url = ulanzi_url + '/api/notify'
        if str(aktuelle_uhrzeit) == str(astro_zeiten[0]):
            print('   Sonnenaufgang')
            data = {
                "text": 'Achtung! Sonnenaufgang heute '+(astro_zeiten[0])+' Uhr -> Jetzt!',
                "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c",
                "rainbow": bool(1),
                "repeat": 2
            }
            funktionen.ulanzi_senden(url, data)
        if str(aktuelle_uhrzeit) == str(astro_zeiten[2]):
            print('   Sonnenuntergang')
            data = {
                "text": 'Achtung! Sonnenuntergang heute '+(astro_zeiten[2])+' Uhr -> Jetzt!',
                "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c",
                "rainbow": bool(1),
                "repeat": 2
            }
            funktionen.ulanzi_senden(url, data)
        time.sleep(60)  # Alle 60 Sekunden überprüfen

## Programm starten ##
# Holen der Sonnenaufgangs- und Sonnenuntergangszeiten mit angewendeten Korrekturen
astro_zeiten = funktionen.get_sa_su(standort_breite, standort_laenge, sa_korrektur, su_korrektur)
print(astro_zeiten)

# Thread für "Anzeige Sonnen-Auf/Untergang" erzeugen und starten
if show_sa_su:
    # Erstelle einen Hintergrund-Thread für Anzeige Sonnen-Auf/Untergang
    hintergrund_thread = threading.Thread(target=sa_su_show)
    # Starte den Hintergrund-Thread
    hintergrund_thread.daemon = True  # Beendet den Thread, wenn das Hauptprogramm beendet wird
    hintergrund_thread.start()

# Testen ob Solaranzeige URL verfügbar
print(str(funktionen.url_verfuegbar(solaranzeige_url)) + " -> Solaranzeige URL verfügbar")
if not (funktionen.url_verfuegbar(solaranzeige_url)):
    exit("Solaranzeige unter der eingegeben URL nicht erreichbar!")
# Testen ob Ulanzi URL verfügbar
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

# Helligkeit einstellen
if funktionen.mode_check(day_mode_start, night_mode_start) == "D":
    if not start_astro:
      funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
else:
    if not start_astro:
      funktionen.ulanzi_hell_set(ulanzi_url, night_hell)

x = True
y = True
z = True

# Loop starten
while True:
    # Helligkeit setzen Start
    mode = funktionen.mode_check(day_mode_start, night_mode_start)
    #print(mode+"-Mode")
    if y and mode == "D":
        funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
        print(" ** -> Day_hell gesendet")
        y = False
    elif not y and mode == "N":
        funktionen.ulanzi_hell_set(ulanzi_url, night_hell)
        print(" ** -> Night_hell gesendet")
        y = True
    # Helligkeit setzen Ende

    uhrzeit = time.strftime("%H:%M")
    #print(uhrzeit)

    if start_astro and z:
        start_zeit = astro_zeiten[1]
        stop_zeit = astro_zeiten[3]
        print(" ** -> Astro-Zeiten geladen!")
        z = False

    if uhrzeit >= start_zeit and uhrzeit < stop_zeit:
        if not x:
            if start_astro:
                funktionen.ulanzi_hell_set(ulanzi_url, day_hell)
                print(" ** -> Day-hell gesetzt!")
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
            if start_astro:
                funktionen.ulanzi_hell_set(ulanzi_url, night_hell)
                print("** -> Night-hell gesetzt!")
        x = False

        print(uhrzeit + ' ** -> Night-Show ist '+str(night_show))
        time.sleep(60)
        if uhrzeit >= "01:23" and uhrzeit < "01:24":
            astro_zeiten = funktionen.get_sa_su(float(standort_breite), float(standort_laenge), int(sa_korrektur),
                                                int(su_korrektur))
            print(astro_zeiten)
            z = True

