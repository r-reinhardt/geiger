import time
import os

## config ##
hours = 12
debug = False
############

# every x hours, print the current time
while True:
    if debug:
        print('sleeping for ' + str(hours) + ' hours.')
    time.sleep(hours * 3600)
    if os.stat('/proc/uptime').st_mtime > hours * 3600:
        if debug:
            print('system has been running for ' + str(hours + 3600) + '. backing up index.log.')
        os.system("sudo cp /usr/local/ramdisk/geigerzaehler/index.log /home/pi/geigerzaehler/")
        