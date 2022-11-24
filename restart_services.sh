cd /usr/local/ramdisk/geigerzaehler && sudo cp index.log /home/pi/geigerzaehler

sudo rm -r /usr/local/ramdisk/geigerzaehler && sudo mkdir /usr/local/ramdisk/geigerzaehler

cd /home/pi/geigerzaehler && sudo cp api.py /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp backup.py /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp main.js /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp index.html /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp index.log /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp style.css /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp webserver.py /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp gpio.py /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp favicon.svg /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp geiger.wav /usr/local/ramdisk/geigerzaehler
cd /home/pi/geigerzaehler && sudo cp wiki.html /usr/local/ramdisk/geigerzaehler

sudo service geiger-gpio restart
sleep 1 && sudo service geiger-backup restart
sleep 2 && sudo service geiger-webserver restart
sleep 7 && sudo service geiger-api restart