#!/usr/bin/env python
#coding: utf8
import time
import RPi.GPIO as GPIO
import os
from datetime import datetime
import threading

#### config ####
minutes = 5       # wie lange soll gemessen werden?
debug = False     # falls 'True' wird ein Ton abgespielt & Konsolen Logs werden aktiviert
bouncetime = 150  # wie hoch soll die bounce time sein?
pin = 13          # welcher gpio pin soll verwendet werden?
faktor = 0.02     # mit welchem Faktor soll mikrosievert errechnet werden?
################

# Zählweise der Pins festlegen
GPIO.setmode(GPIO.BOARD)

# Pin 13 (GPIO 27) als Eingang festlegen
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# Funktion, um im Log einen Eintrag hinzu zu fügen
def addLog(time, value):
    with open("index.log", "r") as f:
        logString = f.read()
        with open("index.log", "w") as f:
            logString = logString + "\n" + str(time) + " " + str(value)
            f.write(logString)



# Ton 'geiger.wav' in neuem Thread (damit async) abspielen
def playSound():
    threading.Thread(target=os.system, args=('aplay -q geiger.wav',), daemon=True).start()

i = 1
# Wenn pin 13 auf einen puls erhält:
def onInterrupt(pin):
    global i
    global timeout
    global debug

    # falls, debug aktiviert ist, Geräusch abspielen
    if debug:
        playSound()
    
    timestamp = int(time.time())

    if i == 1:
        timeout = time.time() + 60 * minutes

    if time.time() > timeout: 
        if debug:
            print("Impuls gemessen: " + str(i))
        sievert = str(round((i * faktor) / minutes, 3))
        addLog(timestamp, sievert)
        if debug:
            print("\nEs wurden in den letzten " + str(minutes) + " Minuten " + str(i) + " Impulse gemessen. (" + sievert + " uSv/h)\n")
        i = 1;
    else:
        if debug:
            print("Impuls gemessen: " + str(i))
        i = i + 1
        
# Ereignis deklarieren
GPIO.add_event_detect(pin, GPIO.RISING, callback = onInterrupt, bouncetime = bouncetime)


while True:
    time.sleep(1)
    
# TODO: nach einem Jahr alte logs z.B. überschreiben