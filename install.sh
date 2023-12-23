#!/bin/sh

# Abfrage der Debian-Version
version=$(lsb_release -rs)

sudo apt install pip
sudo apt install git

if [ ! -d '/home/pi/temp_ulanzi' ]; then
  echo $1
  echo $#
  #sudo apt update
  #sudo apt dist-upgrade -y

  if [ "$version" = "11" ]; then
    echo "Debian 11 erkannt. Führe Aktionen für Debian 11 aus..."
    pip3 install bs4
    pip3 install suntime

  elif [ "$version" = "12" ]; then
    echo "Debian 12 erkannt. Führe Aktionen für Debian 12 aus..."
    sudo apt install python3-bs4
    sudo apt install python3-suntime
    
  else
    echo "Unbekannte Debian-Version. Beende Skript."
    exit 1
  fi

  pip3 install lxml
  mkdir /home/pi/temp_ulanzi
  mkdir /home/pi/scripts
fi

cd /home/pi/temp_ulanzi

git clone https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector

if [  $# -eq 0 ]; then
    echo 'Instanz 0 erstellt!'
    mv Ulanzi-Solaranzeige-Connector /home/pi/scripts/Ulanzi-Solaranzeige-Connector
    chmod 755 /home/pi/scripts/Ulanzi-Solaranzeige-Connector/ulanziconnect.py
    sudo cp /home/pi/scripts/Ulanzi-Solaranzeige-Connector/ulanzi-connector.service /etc/systemd/system/ulanzi-connector.service
    sudo chmod 644 /etc/systemd/system/ulanzi-connector.service
    sudo systemctl daemon-reload
    sudo systemctl enable ulanzi-connector.service
    echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

else
     echo 'Instanz '$1' erstellt!'
     mv Ulanzi-Solaranzeige-Connector /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1
     cd /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1
     chmod 755 /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1/ulanziconnect.py
     sed -i 's/Ulanzi-Solaranzeige-Connector/Ulanzi-Solaranzeige-Connector-'$1'/g' ulanzi-connector.service
     mv ulanzi-connector.service ulanzi-connector-$1.service

     sudo cp /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1/ulanzi-connector-$1.service /etc/systemd/system/ulanzi-connector-$1.service
     sudo chmod 644 /etc/systemd/system/ulanzi-connector-$1.service
     sudo systemctl daemon-reload
     sudo systemctl enable ulanzi-connector-$1.service
     echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

fi

echo 'Installation beendet ! Have Fun !'
