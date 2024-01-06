Hier entsteht eine Sammlung "kleiner Tools" im Zusammenhang influxDB, Ulanzi etc.




## 1. - db_summen.py -

Was macht das Script?

Mit Hilfe des Scriptes kann man Werte aus verschiedenen Influxdb Datenbanken auslesen, diese "mathematisch" behandeln und das Ergebnis in eine Datenbank (zB. "Summen") zurückschreiben. Daten können dabei von beliebig vielen DB's geholt und verarbeitet werden.
Haupteinsatz im Zusammenspiel mit "Solaranzeige" ist das Bilden von Summen der Werte bei Einsatz mehrerer WR zur entsprechenden Weiterverarbeitung/Visualisierung mit "Ulanzi" etc..

Die **Installation** des Tool's ist einfach:

1. falls nicht vorhanden Ordner für Scripte im Homeverzeichnis anlegen:

`mkdir /home/pi/scripts`

2. Ordner Tools anlegen

`mkdir /home/pi/scripts/Tools`

3. Script herunterladen


`cd /home/pi/scripts/Tools/`

`wget https://raw.githubusercontent.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/main/Tools/db_summen.py`


4. Abhängigkeiten installieren

für Debian 11 Solaranzeige Ver. 5.x

`sudo pip3 install influxdb`

für Debian 12 Solaranzeige Ver. 6.x

`sudo apt install python3-influxdb`




**Konfiguration und Test.**

Es müssen folgende Einstellungen im Script vorgenommen werden:

Da wir das Script ja Über Cron (zeitgleich zum Auslesen der Regler/WR) jede Minute laufen lassen wollen müssen wir eine Verzögerung einbauen die die Ausführung unseres Scriptes solange pausiert bis die Werte der Regler(WR) ausgelesen und gespeichert sind. Das wird hier 

```
# Verzögerung in Sekunden bis alle "Regler" ausgelesen sind
time.sleep(25)
```
vorgenommen. (hier 25 Sekunden) 

Den genauen Wert bekommt man durch einen Blick ins Log mit

`tail -f /var/www/log/solaranzeige.log`
Hier kann man sehr gut erkennen nach wieviel Sekunden das Auslesen der Regler beendet ist, diesen Wert noch 3-5 Sekunden dazugeben und den Wert an Stelle der "25" eintragen.

Jetzt müssen wir nur noch festlegen welche Daten aus welcher Datenbank geholt, wie diese "mathematisch" verknüpft und wohin das "Ergebnis" geschrieben werden soll!



