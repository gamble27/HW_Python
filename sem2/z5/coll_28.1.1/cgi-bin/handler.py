#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import json

def split_and_jsonify(string):
    return json.dumps(list(set(string.split())), skipkeys=True)

HTML = """Content-type: text/html charset=utf-8\n\n
<html lang="ua">
<head>
    <meta charset="UTF-8">
    <title>DOMASHKI</title>
</head>
<body>
<h1>Here's your json</h1>
<p>{ans}</p>
</body>
</html>"""

form = cgi.FieldStorage()
field = "check_string"

try:
    cnt = split_and_jsonify(form[field].value)
except Exception as e:
    cnt = e

p = HTML.format(ans=cnt)
print(p)
