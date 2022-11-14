import time
import os

hours = 0.0167

# every x hours, print the current time
while True:
    time.sleep(43200)
    if os.stat('/proc/uptime').st_mtime > hours * 3600:
        os.system("cp /usr/local/ramdisk/index.log /home/pi/geigerzaehler/")
    