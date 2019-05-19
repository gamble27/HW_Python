#!/usr/bin/env python
from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = 'localhost'
PORT = 8052

print('=== Local web server ===')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()

# todo: chmod +x /home/olga/PyCharm/domashki/sem2/z3/ind_27.1_v3/cgi-bin/cgi_handler.py
