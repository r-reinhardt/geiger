#!/usr/bin/env python
#coding: utf8
import time
import RPi.GPIO as GPIO
import os
from datetime import datetime
import threading
import smtplib
from email.mime.text import MIMEText

# #### config ####
minutes = 1       # wie lange soll gemessen werden?
debug = False     # falls 'True' wird ein Ton abgespielt & Konsolen Logs werden aktiviert
bouncetime = 150  # wie hoch soll die bounce time sein?
pin = 13          # welcher gpio pin soll verwendet werden?
faktor = 0.02     # mit welchem Faktor soll mikrosievert errechnet werden?

login = False                                 # wenn man sich für den SMTP-Server anmelden muss
mail_cooldown = 900                           # wie viel Zeit zwischen Mails vergehen muss
mail_limit = 1                                # welche grenze der sievert überschreiten muss
mail_to = ['Rene.Reinhardt@sinc.de']          # empfänger der email
mail_user = 'Geiger-Raspi@sinc.de'            # username des absenders
mail_password = ''                            # passwort des absenders
mail_from = 'Geiger-Raspi'                    # name des Absenders (Steht in der Kopfzeile)
mail_smtp = 'mailrelay.sinc.de'               # smtp server des absenders
mail_port = 25                                # port des smtp servers
mail_subject = 'Mail Server Test'             # Betreff der email
mail_cc = ['Alessandro.Rinaldi@sinc.de',      # CC der Mail
           'Lukas.Blum@sinc.de'
           'Gulniza.Taaleibekova@sinc.de']    
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
            # if file is empty, add header
            if logString == '':
                logString = str(time) + " " + str(value)
            else:
                logString = logString + "\n" + str(time) + " " + str(value)
            f.write(logString)

# Ton 'geiger.wav' in neuem Thread (damit async) abspielen
def playSound():
    threading.Thread(target=os.system, args=('aplay -q geiger.wav',), daemon=True).start()

i = 1
# Wenn pin 13 auf einen puls erhält:
def onInterrupt(pin):
    global i
    global debug

    # falls, debug aktiviert ist, Geräusch abspielen
    if debug:
        playSound()
        print('Impuls gemessen: ' + str(i))

    i += 1

def sendWarning(sievert):
    global mail_limit
    global mail_to
    global mail_from
    global mail_password
    global mail_smtp
    global mail_port
    global mail_subject
    global mail_cc

    try:
        msg = MIMEText("Alarm!\nDer Sievert hat die Grenze von " + str(mail_limit) + " überschritten.\nAktueller Wert: " + sievert)
        msg['Subject'] = mail_subject
        msg['From'] = mail_from
        msg['To'] = ''.join(mail_to)
        msg['Cc'] = ', '.join(mail_cc)
        s = smtplib.SMTP(mail_smtp, mail_port)
        if login:
            s.starttls()
            s.login(mail_user, mail_password)
        else:
            s.ehlo()
        s.sendmail(mail_from, mail_to+mail_cc, msg.as_string())
        s.quit()
        print('Email gesendet.')
    except Exception as e:
        print('Etwas ist schiefglaufen beim Senden der Mail:\n' + str(e))

lastMail = 0
def timer():
    while True:
        global i
        global debug
        global lastMail
        global mail_cooldown
        global mail_limit

        time.sleep(minutes * 60)
        sievert = str(round((i * faktor) / minutes, 3))
        timestamp = int(time.time())
        addLog(timestamp, sievert)
        if debug:
            print("\nEs wurden in den letzten " + str(minutes) + " Minuten " + str(i) + " Impulse gemessen. (" + sievert + " uSv/h)\n")
        if lastMail + mail_cooldown < timestamp & float(sievert) > mail_limit:
            sendWarning(sievert)
            lastMail = timestamp
        i = 1;

# timer() funktion in neuem thread ausführen
threading.Thread(target=timer, daemon=True).start()   

# Ereignis deklarieren
GPIO.add_event_detect(pin, GPIO.RISING, callback = onInterrupt, bouncetime = bouncetime)

# TODO: nach einem Jahr alte logs z.B. überschreiben

while True:
    time.sleep(1)