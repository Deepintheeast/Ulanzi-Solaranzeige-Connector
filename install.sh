#!/bin/sh

#apt update
#apt dist-upgrade -y
#apt install pip
#pip3 install logging
#pip3 install bs4
#pip3 install lxml

mkdir /home/pi/scripts
cd /home/pi/scripts

git clone https://github.com/Deepintheeast/Ulanzi-Solaranzeige-Connector

mv Ulanzi-Solaranzeige-Connector Ulanzi-Solaranzeige-Connector-$1
cd /home/pi/scripts/Ulanzi-Solaranzeige-Connector-$1

sed -i 's/Ulanzi-Solaranzeige-Connector/Ulanzi-Solaranzeige-Connector-$1/g' ulanzi-connector.service
mv ulanzi-connector.service ulanzi-connector-$1.service

