#!/usr/bin/env python
from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = 'localhost'
PORT = 8000

print('=== Local web server ===')
HTTPServer((HOST, PORT), CGIHTTPRequestHandler).serve_forever()
