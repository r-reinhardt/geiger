#!/usr/bin/env python
#coding: utf8
from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve

port = 26662

app = Flask(__name__)
CORS(app)

errorMessage = '<p style="font-family: sans-serif; font-size: 15pt;"><b>error:</b> invalid input <br><b>correct usage:</b> <kbd>/all</kbd>, <kbd>/latest</kbd>, <kbd>/&lt;unix timestamp&gt;<kbd> eg.: <kbd>./api/1667985999</kbd></p>'

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
            return jsonify(log[-1])

        elif input == 'all':
            return log

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
