#!/bin/sh


if [ ! -d '/home/pi/temp_ulanzi' ]; then
  echo $1
  echo $#
  #sudo apt update
  #sudo apt dist-upgrade -y
  sudo apt install pip
  #pip3 install logging
  pip3 install bs4
  pip3 install lxml
  mkdir /home/pi/temp_ulanzi
  mkdir /home/pi/scripts
fi

cd /home/pi/temp_ulanzi

git clone https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector

if [  $# -eq 0 ]; then
    echo 'Instanz 0 erstellt!'
    mv Ulanzi-Solaranzeige-Connector /home/pi/scripts/Ulanzi-Solaranzeige-Connector
    sudo cp /home/pi/scripts/Ulanzi-Solaranzeige-Connector/ulanzi-connector.service /etc/systemd/system/ulanzi-connector.service
    sudo chmod 644 /etc/systemd/system/ulanzi-connector.service
    sudo systemctl daemon-reload
    sudo systemctl enable ulanzi-connector.service
    echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

else
     echo 'Instanz '$1' erstellt!'
     mv Ulanzi-Solaranzeige-Connector /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1
     cd /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1
     sed -i 's/Ulanzi-Solaranzeige-Connector/Ulanzi-Solaranzeige-Connector-'$1'/g' ulanzi-connector.service
     sed -i 's/Ulanzi-Solaranzeige-Connector\/ulanzi.log/Ulanzi-Solaranzeige-Connector-'$1'\/ulanzi-'$1'.log/g' settings.ini
     mv ulanzi-connector.service ulanzi-connector-$1.service

     sudo cp /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1/ulanzi-connector-$1.service /etc/systemd/system/ulanzi-connector-$1.service
     sudo chmod 644 /etc/systemd/system/ulanzi-connector-$1.service
     sudo systemctl daemon-reload
     sudo systemctl enable ulanzi-connector-$1.service
     echo 'Nach erfolgreicher Konfiguration und Test, den Dienst starten nicht vergessen!'

fi

echo 'Installation beendet ! Have Fun !'
