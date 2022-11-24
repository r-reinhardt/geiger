#!/usr/bin/env python
#coding: utf8

import smtplib
from email.mime.text import MIMEText
from datetime import datetime

login = False                                 # wenn man sich für den SMTP-Server anmelden muss
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

sendWarning('4')