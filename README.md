# Geiger Counter GUI & API

How it works:
gpio.py logs every impulse received by the geiger counter's output via the raspberry pi's GPIO pins to the index.log file.
the api.py then reads the file & provides the sievert value at the time of the given timestamp, (e.g. ./api/1668349205), or the most recent value (e.g. ./api/latest) upon GET request. The webserver.py then fetches the latest values to display them on an HTML page.
