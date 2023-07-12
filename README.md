12.07.2023
- Beschreibung und Beispiele an neue Version angepasst!

04.07.2023 Update auf Version 0.3
- Funktionen ausgelagert
- div. Anpassungen

Achtung Wiki noch nicht komplett angepasst -> ist in Arbeit! 👋

# Ulanzi-Solaranzeige-Connector
Connector zur Anzeige von beliebigen Daten aus 
[Solaranzeige](https://solaranzeige.de)
auf einer 
[Ulanzi (awtrix light) TC001 PixelClock(Affiliate-Link)](https://www.ulanzi.de/products/ulanzi-pixel-smart-uhr-2882?_pos=1&_psq=pixel&_ss=e&_v=1.0&ref=z6pvugfl
) !


https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector/assets/136626582/99481df8-7262-40a2-a407-776780bc073b

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
