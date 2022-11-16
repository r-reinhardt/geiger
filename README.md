# Geiger Counter GUI & API

How it works:
gpio.py logs every impulse received by the geiger counter's output via the raspberry pi's GPIO pins to the index.log file.
the api.py then reads the file & provides the sievert value at the time of the given timestamp, (e.g. ./api/1668349205), or the most recent value (e.g. ./api/latest) upon GET request. The webserver.py then fetches the latest values to display them on an HTML page.

![IMG_20221116_093513_Arcide-LMC8 4-OP9P-v6 2~2](https://user-images.githubusercontent.com/105526886/202131343-e8281ee0-110f-4ab9-a1fd-2510aed85d70.jpg)
*How the Geiger Counter communicates with the Raspberry Pi*


![IMG_20221116_093313_Arcide-LMC8 4-OP9P-v6 2~2](https://user-images.githubusercontent.com/105526886/202131379-de3250d0-2ba6-4697-96a4-c232d666483e.jpg)
*A rough explanation*
