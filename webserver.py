#!/usr/bin/env python
#coding: utf8

import http.server
import socketserver

PORT = 25552

# falls der port bereits benutzt wird, wird er um 1 erhöht
while True:
    try:
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", PORT), Handler)
        print("serving at port", PORT)
        Handler.directory = '/home/pi/Geiger/bin'
        Handler.path = '/home/pi/Geiger/bin'
       # Handler.do_GET('/home/pi/Geiger/bin/index.html')
        Handler.extensions_map['.html'] = 'text/html'
        httpd.serve_forever()
    except OSError:
        PORT += 1