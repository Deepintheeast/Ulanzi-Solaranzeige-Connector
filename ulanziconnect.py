#!/usr/bin/env python3
#
# Das Script "abonniert" Topics eines MQTT Brokers, wertet (formatiert) die Daten aus
# um sie entsprechend aufbereitet an eine Ulanzi Pixelclock zur Darstellung weiterzuschicken!
#

# benötigte Bibliotheken importieren

import paho.mqtt.client as mqtt
import requests
import json
import logging

# div. Einstellungen festlegen

MQTT_HOST = "192.168.x.x"  # IP-Adresse oder Hostname des Brokers
MQTT_PORT = 1883  # Port des Brokers
MQTT_USER = "admin"  # Benutzername (falls nötig)
MQTT_PASSWORD = "solaranzeige"  # Passwort (falls nötig)
MQTT_TOPIC = "solaranzeige/ulanzi/#"  # Topic unter dem die Daten liegen
MQTT_CLIENTNAME = "Ulanzi-Anzeige"  # Client name
ULANZI_URL = "http://192.168.x.x" # Ulanzi URL
LOG_DATEI = "/home/pi/scripts/ulanzi.log"
LOG_LEVEL = "INFO"  # NOTSET =0, DEBUG =10, INFO =20, WARN =30, ERROR =40, and CRITICAL =50

REGLER1_TOPIC = "solaranzeige/ulanzi/xxxx" # Topic Regler 1
REGLER2_TOPIC = "solaranzeige/ulanzi/xxxx" # Topic Regler 2

VERSION_NR = "0.20"

# Logging definieren
logging.basicConfig(filename=LOG_DATEI, level=logging.getLevelName(LOG_LEVEL),
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')


# Funktionen definieren
# Funktion MQTT Client erstellen und verbinden

def create_configured_client():
    client = mqtt.Client(MQTT_CLIENTNAME)
    client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
    client.connect(host=MQTT_HOST, port=MQTT_PORT)
    return client


# Funktion empfangene Topic's auswerten und weiterverarbeiten

def handle_message(client, userdata, msg):
    logging.info(msg.topic)
    if msg.topic == REGLER2_TOPIC+"/soc":
        # print("SOC: "+str(msg.payload.decode("utf-8")))
        soc = (msg.payload.decode("utf-8"))
        logging.info(soc)

        url = ULANZI_URL + '/api/custom?name=soc'

        if int(soc) >= 1 and int(soc) <= 10:
            data = {
                "text": str(soc) + " %",
                "icon": 12832,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif int(soc) >= 11 and int(soc) <= 30:
            data = {
                "text": str(soc) + " %",
                "icon": 6359,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif int(soc) >= 31 and int(soc) <= 50:
            data = {
                "text": str(soc) + " %",
                "icon": 6360,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif int(soc) >= 51 and int(soc) <= 70:
            data = {
                "text": str(soc) + " %",
                "icon": 6361,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif int(soc) >= 71 and int(soc) <= 90:
            data = {
                "text": str(soc) + " %",
                "icon": 6362,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif int(soc) >= 91 and int(soc) <= 100:
            data = {
                "text": str(soc) + " %",
                "icon": 6363,
                "color": [154, 250, 10],
                "duration": 5
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')


    elif msg.topic == REGLER1_TOPIC+"/pv_leistung":
        pv_aktuell = round(float(msg.payload.decode("utf-8")))
        logging.info(pv_aktuell)

        url = ULANZI_URL + '/api/custom?name=pvleistung'

        data = {
            "text": (str(pv_aktuell) + " W"),
            "icon": 27283,
            "rainbow": bool(1),
            "duration": 5
        }
        response = requests.post(url, json=data)
        logging.info(f'{url},{data}')

    elif msg.topic == REGLER1_TOPIC+"/wattstundengesamtheute":
        pv_gesamt = round((float(msg.payload.decode("utf-8")) / 1000), 2)
        logging.info(pv_gesamt)

        url = ULANZI_URL + '/api/custom?name=pvtaggesamt'

        data = {
            "text": (str(pv_gesamt) + " kWh"),
            "icon": 51301,
            "color": [252, 186, 3],
            "duration": 5
        }
        response = requests.post(url, json=data)
        logging.info(f'{url},{data}')

    elif msg.topic == REGLER1_TOPIC+"/batterie_strom":
        bat_strom = round(float(msg.payload.decode("utf-8")))
        logging.info(f'{bat_strom}')

        url = ULANZI_URL + '/api/indicator1'

        if bat_strom == 0:
            data = {
                "color": [0, 0, 0]
            }

            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        else:
            data = {
                "color": [0, 255, 0],
                "blink": 1200
            }

            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

    elif msg.topic == REGLER1_TOPIC+"/modus":
        modus = (msg.payload.decode("utf-8"))
        logging.info(f'{modus}')

        url = ULANZI_URL + '/api/indicator3'

        if modus == "B":  # Batteriemodus
            data = {
                "color": [0, 255, 0]
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif modus == "L":  # Line(Netz)modus
            data = {
                "color": [0, 0, 255]
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

        elif modus == "E":  # Error(Fehler)modus
            data = {
                "color": [255, 0, 0],
                "blink": 100
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

            url = ULANZI_URL + '/api/notify'
            data = {
                "text": "Achtung! Wechselrichter befindet sich im Fehlermodus! Bitte überprüfen! ",
                "color": [255, 0, 0],
                "hold": bool(1)
            }
            response = requests.post(url, json=data)
            logging.info(f'{url},{data}')

    else:
        logging.info('Parameter nicht bekannt !', msg.topic)


# Funktion Topic publish (senden)

def send_message(client, topic, payload):
    client.publish(topic, payload)


# Funktion Topic subscription (empfangen)

def setup_subscriptions(client, topic):
    client.on_message = handle_message
    client.subscribe(topic)

# Funktion Intro
def intro():
    url = ULANZI_URL + '/api/notify'
    data = {
        "text": "Ulanzi->Solaranzeige Connector Version "+str(VERSION_NR),
        "rainbow": bool(1),
        "repeat": 2
    }
    response = requests.post(url, json=data)
    logging.info(f'{url},{data}')

# Programm starten
# MQTT Verbindung herstellen und Topic subscriben

mqtt_client = create_configured_client()
setup_subscriptions(mqtt_client, MQTT_TOPIC)
intro()

# Loop starten

while True:
    mqtt_client.loop()
