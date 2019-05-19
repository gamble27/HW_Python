#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import re

def parse_brackets(string):
    PATTERN = r"(\([^()]*\))"
    # p = re.compile(PATTERN)
    # m = p.search(string)
    # return m.group('content')
    results = re.findall(PATTERN, string)
    return [r[1:-1] for r in results]

def kick_brackets(string):
    kickstart = 0
    kickend = 0
    res = string
    ind = 0
    while ind < len(res):
        symbol = res[ind]
        if symbol == "(":
            kickstart = ind
            ind += 1
        elif symbol == ")":
            kickend = ind
            res = res[:kickstart] + res[kickend+1:]
            ind = kickstart
        else:
            ind += 1

    # res = string
    # for i in range(len(kickstart)):
    #     res

    return res

# print(parse_brackets(input()))

form = cgi.FieldStorage()
field = "check_string"
# resp = ""
if field in form:
    # resp = '<br>'.join(parse_brackets(form[field].value))
    resp = kick_brackets(form[field].value)
else:
    resp = "Internal Error"

HTML = """Content-type: text/html charset=utf-8\n\n
<html>
<head>
    <meta charset="UTF-8">
    <title>DOMASHKI</title>
</head>
<body>
<h2>Here's your content without brackets</h2>
<p>{ans}</p>
</body>
</html>"""

p = HTML.format(ans=resp)
print(p)
