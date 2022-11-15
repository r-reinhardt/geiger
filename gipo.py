#!/usr/bin/env python
#coding: utf8 
import time
import RPi.GPIO as GPIO
import os
from datetime import datetime
import threading

## config ##
minutes = 5 # wie lange soll gemessen werden?


# Zählweise der Pins festlegen
GPIO.setmode(GPIO.BOARD)

# Pin 11 (GPIO 27) als Eingang festlegen
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

hz = 440

def addLog(time, value):
        
    with open("index.log", "r") as f:
        logString = f.read()
        with open("index.log", "w") as f:
            logString = logString + "\n" + str(time) + " " + str(value)
            f.write(logString)

# Ereignis-Funktion für Eingang HIGH

i = 1
faktor = 0.02

def playSound():
    threading.Thread(target=os.system, args=('aplay -q geiger.wav',), daemon=True).start()

def doIfHigh(pin):
    global i
    global hz
    global timeout

    # Geräusch abspielen
    playSound()
    
    timestamp = int(time.time())

    if i == 1:
        timeout = time.time() + 60 * minutes   # 5 minuten

    if time.time() > timeout: 
        print("Impuls gemessen: " + str(i))
        sievert = str(round((i * faktor) / minutes, 3))
        addLog(timestamp, sievert)
        print("\nEs wurden in den letzten " + str(minutes) + " Minuten " + str(i) + " Impulse gemessen. (" + sievert + " uSv/h)\n")
        i = 1;
    else:
        print("Impuls gemessen: " + str(i))
        i = i + 1
        
# Ereignis deklarieren
pin = 13
GPIO.add_event_detect(pin, GPIO.RISING, callback = doIfHigh, bouncetime = 150)


while True:
    time.sleep(1)
    
# TODO: nächster Schritt Daten nach einem Jahr erneuern. 