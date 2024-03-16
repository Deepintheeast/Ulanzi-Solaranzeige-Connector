# Achtung! Projekt wird nicht mehr weiterentwickelt! Aber ...! Voraussichtlich zu Ostern erscheint das "NachfolgeProjekt" was noch viel mehr kann!

Einige Highlight's schon mal im Vorraus:

Daten werden(können) direkt aus der Datenbank geholt werden
Aktuell unterstützt werden:
- influxdb
- sqlite
- mariadb
- postgresql

Daten können wie gewohnt "einzeln" geholt und verarbeitet werden. 
Aber auch das holen und verarbeiten von mehreren Daten als "Gruppe" ist möglich.
Damit sind Ausgaben von "kombinierten" Daten wie im folgenden Video möglich! Innerhalb dieser Gruppen sind auch "mathematische Berechnungen" zB. Summen aus einzelnen Werten bilden etc. möglich. Es besteht damit auch die Möglichkeit Infos und Daten der "Automatisierung" anzuzeigen.


https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/assets/136626582/e98a82a7-dbf1-4f82-815e-c514b2acc5c1



Es gibt wieder die Möglichkeit Astrodaten anzuzeigen und zur Steuerung zu nutzen, Mondphasen können angezeigt werden, die neuen Wetteroverlays wurden integriert etc.
Lasst Euch überraschen!

Sobald das Projekt online geht findet Ihr hier die entsprechenden Links!








https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/assets/136626582/01b3815b-6cdc-4f46-af8c-d7f69a1ce544

28.12.2023 Update auf Version 0.44

Update zur Anpassung an Solaranzeige Ver. 6.x . Alle User der 0.43 Version müssen nur die "funktionen.py" ersetzen. Alle Einstellungen/Änderungen bleiben erhalten!  

23.12.2023 Anpassungen Installscript

Das Script erkennt ob es auf Debian 11 (Solaranzeige Ver. 5.x) oder Debian 12 (Solaranzeige Ver. 6.x) aufgerufen wurde und installiert entsprechend die benötigten Pakete.

19.11.2023 Update auf Version 0.43

die Anzeigedauer der einzelnen Apps lässt sich jetzt in der "settings.ini" durch die Parameter

```
app_show_time = 3
# Länge der Anzeige "statischer" Apps im Loop in Sekunden

app_scroll_duration = 2
# Anzahl der Wiederholungen "scrollender" Apps im Loop
```

jeweils für "statische" und "scrollende" Apps separat festlegen!
Vorteil -> scrollende Apps laufen sauber bis zum Ende durch und werden nicht mehr mittendrin beendet!

Code bereinigt, vorbeugende "Fehlerbehandlungen" hinzugefügt. Diverse Anpassungen und Fixe!


31.10.2023 Update auf Version 0.42
Start/Stop nach Astro Zeit (Sonnen-Auf/Untergang)
div. kleine Fixe und Anpassungen

08.09.2023 Update auf Version 0.41
div. kleinere Anpassungen an AWTRIX light 0.85

05.09.2023 Progressbar zur Auswertung  "solarnzeige,Batterie,SOC" hinzugefügt!

24.08.203 Update auf Version 0.40

## Installation

Um die Installation möglichst einfach zu gestalten habe ich diesmal ein 
Installationsscript dazu erstellt!

Zur Installation bitte als User "pi" auf einer Konsole an Eurer "Solaranzeige-Installation" anmelden!

Als erstes müssen wir das Script runterladen:

`wget https://raw.githubusercontent.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/main/install.sh`

jetzt einfach das Script aufrufen und durchlaufen lassen:

`bash ./install.sh`

Tja, eigentlich war es das schon! 

Es sollten jetzt alle benötigten Programmdaten unter

`/home/pi/scripts/Ulanzi-Solaranzeige-Connector`

angelegt sein und auch der dazugehörige Dienst wurde schon mit erstellt (aber noch nicht gestartet)!

## Konfiguration/Einstellungen

Alle Einstellungen zum Programm wurden in eine eigene "settings.ini" Datei ausgelagert und sollten am besten mit

`mcedit /home/pi/scripts/Ulanzi-Solaranzeige-Connector/settings.ini`

bearbeitet werden! Ihr findet in der "settings.ini" entsprechende erklärende Kommentare zu den einzelnen Parametern!



Zum testen des Programmes als erstes in den Programmordner wechseln!

`cd /home/pi/scripts/Ulanzi-Solaranzeige-Connector`

und von dort aus mit

`python3 ./ulanziconnect.py` starten.

Beenden mit Strg+C!


Wenn alles passt dann erst als Dienst starten !

`sudo systemctl start ulanzi-connector.service`



## Installation 2. Instanz

Hat jemand mehr als eine Ulanzi, können zusätzliche Instanzen des Programmes, welche unabhängig voneinander laufen, installiert werden!

Das geht einfach durch wiederholten Aufruf des Scriptes mit Angabe eines Parameters als Name/Nummer etc.

Beispiel:

normaler Aufruf des Scripts mit

`bash ./install.sh`

erzeugt eine Instanz unter 

`/home/pi/scripts/Ulanzi-Solaranzeige-Connector`

ein Aufruf mit Parameter "buero" 

Aufruf des Scripts mit

`bash ./install.sh buero`

erzeugt eine Instanz unter 

`/home/pi/scripts/Ulanzi-Solaranzeige-Connector-buero`

Bitte keine Sonderzeichen, Umlaute, Leerzeichen im "Parameter" verwenden!

Das kann für quasi beliebig viele Instanzen durchgeführt werden!

Es werden auch der jeweilige Dienst unter selbem Schema eingerichtet!





# ---------------------------------------------------------------

# Achtung!

# Alle weiteren Information und das Wiki werden in den kommenden Tagen für Version 0.40 überarbeitet und angepasst!

# ---------------------------------------------------------------














09.08 2023 Update auf Version 0.32
- Anpassung an awtrix-light 0.73
- Integration "neuer Übergangseffekt -> 0-random"

06.08 2023 Update auf Version 0.31
- Anpassung an awtrix-light 0.72
- Integration "neue Übergangseffekte"

28.07.2023
- weitere Beispiele hinzugefügt
- [Beispiel Anzeige "Status Laden" über "Indikator 1"](https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/wiki#beispiel-anzeige-status-laden-%C3%BCber-indikator-1)
- [Beispiel Anzeige "Status Wechselrichter" über "Indikator 3" und Fehlermeldung über "Notifikation"](https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/wiki#beispiel-anzeige-status-wechselrichter-%C3%BCber-indikator-3-und-fehlermeldung-%C3%BCber-notifikation)
  
12.07.2023
- Beschreibung und Beispiele an neue Version angepasst!
- Beispiel ["Anzeige Aussentemperatur"](https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/wiki#beispiel-anzeige-aussentemperatur) hinzugefügt

04.07.2023 Update auf Version 0.3
- Funktionen ausgelagert
- div. Anpassungen

Achtung Wiki noch nicht komplett angepasst -> ist in Arbeit! 👋

# Ulanzi-Solaranzeige-Connector
Connector zur Anzeige von beliebigen Daten aus 
[Solaranzeige](https://solaranzeige.de)
auf einer 
["Ulanzi Pixel Clock mit Awtrix Light"(Affiliate-Link)](https://www.ulanzi.de/products/ulanzi-pixel-smart-uhr-2882?_pos=1&_psq=pixel&_ss=e&_v=1.0&ref=z6pvugfl
) !




Im Video seht Ihr der Reihe nach folgende Infos:

1. Uhrzeit und Anzeige des Wochentages durch den entsprechenden Balken unter der Schrift! 
  (das ist ein Bestandteil der Firmware des Awtrix-Light)

2. SOC der Batterie (56%), das Logo "füllt/leert" sich in Abhängigkeit des Ladezustandes von "leer" <-> "voll" in aktuell 5 Stufen.

3. Tagesertrag in kWh, hier 5,51 kWh (es fehlt heute echt etwas die Sonne! 🌤️ )

4. aktuelle PV-Leistung (2675 W) mit animiertem Logo und Schrift im "Rainbow Effekt"!

5. Temperaturanzeige, dieser Wert kommt nicht von der "Solaranzeige" sondern vom "IOBroker" und wird nicht in meinem Script erzeugt!

Zusätzlich besteht die Möglichkeit 3. Indikatoren anzusteuern. Diese sind an der rechten Seite des Display's! Hier im Video "oben" die 3 grünen blinkenden Pixel die hier anzeigen das aktuell die Batterie geladen wird. Die "unteren" 3 Pixel zeigen durch ihre Farbe in welchem Modus sich der WR befindet "grün = Batteriemode", "blau = Netzmode" und "rot blinkend = Errormode". Der 3. Indikator besteht aus zwei Pixeln zwischen Indikator 1 und 2, wird aktuell noch nicht genutzt!

Zusätzlich, wie am Ende des Video's zu sehen, wird im Fehlerfall eine entsprechende Notifikation an die Ulanzi geschickt die erst durch Be(s)tätigung  der mittleren Taste gelöscht wird! 

Weiter geht es im [Wiki.](https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/wiki)
