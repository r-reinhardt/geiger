import time
import os

## config ##
hours = 12
############

# every x hours, print the current time
while True:
    time.sleep(hours * 3600)
    if os.stat('/proc/uptime').st_mtime > hours * 3600:
        os.system("cp /usr/local/ramdisk/index.log /home/pi/geigerzaehler/")
    