#!/usr/bin/env python
#coding: utf8
from flask import Flask, jsonify
from waitress import serve

port = 26662

app = Flask(__name__)

# cors allow only from ports 25552 and 26662
@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', 'http://172.16.14.116:25552')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
    return response

errorMessage = '<p style="font-family: Segoe UI, sans-serif; font-size: 15pt;"><b>error:</b> invalid input <br><b>correct usage:</b> <kbd>/all</kbd>, <kbd>/latest</kbd>, <kbd>/&lt;unix timestamp&gt;<kbd> eg.: <kbd>./api/1667985999</kbd></p>'

@app.route('/api/<input>', methods=['GET'])
def api(input):
    with open('./index.log', 'r') as f:
        log = f.read()

        # log zu json konvertieren
        log = log.split('\n')
        log = [i.split(' ') for i in log]
        log = [{'timestamp': i[0], 'value': i[1]} for i in log]
        

        # wenn input 'latest' ist, dann gebe nur den letzten eintrag zurück
        if input == 'latest':
            # durchschnitt der letzten 30 einträge, solange es mindestens 30 einträge gibt
            if len(log) >= 30:
                average = sum([float(i['value']) for i in log[-30:]]) / 30
                average = round(average, 2)
                return jsonify({'timestamp': log[-1]['timestamp'], 'value': average})
            else:
                return jsonify(log[-1])

        elif input == 'wiki':
            # read wiki.html
            wiki = open('./wiki.html', 'r').read()
            return wiki

        elif input == 'all':
            return jsonify(log)

        # wenn der input 10 stellig & eine nummer ist
        elif len(input) == 10 and input.isdigit():
            for i in log:
                if i['timestamp'] == input:
                    return jsonify(i)
                else:
                    # finde den nächsten timestamp
                    closest = min(log, key=lambda x: abs(int(x['timestamp']) - int(input) + 1))
                    return jsonify(closest)

        else:
            return (errorMessage, 500)

@app.route('/api/', methods=['GET'])
def empty():
    return (errorMessage, 500)



if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=port)
