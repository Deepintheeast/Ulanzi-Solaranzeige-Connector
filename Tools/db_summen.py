from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from datetime import datetime
import time

# Abhängigkeiten mit "pip3 install influxdb" installieren
# ab Debian 12 Bookworm  " sudo apt install python3-influxdb"

class InfluxDBHandler:
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.client = InfluxDBClient(host=self.host, port=self.port, username=self.username, password=self.password)

    def write_data(self, database, measurement, field_name, value, time_stamp):
        try:
            self.client.switch_database(database)
        except InfluxDBClientError:
            self.client.create_database(database)
            self.client.switch_database(database)

        value = round(float(value), 2)
        data = [
            {
                "measurement": measurement,
                "time": time_stamp,
                "fields": {
                    field_name: value
                }
            }
        ]
        self.client.write_points(data)

    def read_data(self, database, measurement, field_name):
        try:
            self.client.switch_database(database)
        except InfluxDBClientError:
            return None

#        query = f'SELECT {field_name} FROM "{measurement}"'
        query = f'SELECT LAST({field_name}) FROM "{measurement}"'
#       query = f'SELECT {field_name} FROM "{measurement}" ORDER BY time DESC LIMIT 1'        

        result = self.client.query(query)
        if len(result.raw['series']) > 0:
            value = result.raw['series'][0]['values'][0][1]
            value = round(float(value), 2)
            return value
        else:
            print("Keine Daten gefunden.")
            return None
        return result

# Run:

# Verzögerung in Sekunden bis alle "Regler" ausgelesen sind
time.sleep(25)

# Timestamp generieren
time_stamp_db = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Klasse initialisieren
handler = InfluxDBHandler("127.0.0.1", 8086, "", "", "WR1")


# Wertepaar 1 holen, berechnen und nach WRSummen schreiben
result = handler.read_data("WR1", "PV", "Leistung")
result_1 = round(float(result), 2)
print(result_1)
result = handler.read_data("WR2", "PV", "Leistung")
result_2 = round(float(result), 2)
print(result_2)
wert = result_1 + result_2
handler.write_data("WRSummen", "PV", "Leistung", wert, time_stamp_db)
print(wert)

# Wertepaar 2 holen, berechnen und nach WRSummen schreiben
result = handler.read_data("WR1", "Summen", "Wh_GesamtHeute")
result_1 = round(float(result), 2)
print(result_1)
result = handler.read_data("WR2", "Summen", "Wh_GesamtHeute")
result_2 = round(float(result), 2)
print(result_2)
wert = result_1 + result_2
handler.write_data("WRSummen", "Summen", "Wh_GesamtHeute", wert, time_stamp_db)
print(wert)

# Wertepaar 3 holen, berechnen und nach WRSummen schreiben
#result = handler.read_data("WR1", "AC", "Leistung")
#result_1 = round(float(result), 2)
#print(result_1)
#result = handler.read_data("WR2", "AC", "Leistung")
#result_2 = round(float(result), 2)
#print(result_2)
#wert = result_1 + result_2
#handler.write_data("WRSummen", "AC", "Leistung", wert, time_stamp_db)
#print(wert)

print("Thats all, have Fun!")

# Croneintrag zum starten des Skriptes:
# crontab -e

#   * * * * *    python3 /home/pi/scripts/db_summen.py	>/dev/null 2>&1

