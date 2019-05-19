#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi


def is_factorial(number):
    if isinstance(number, int) and (number >= 0):
        for i in range(number):
            f = factorial(i)
            if f == number:
                return True
            elif f > number:
                return False
        return False
    else:
        return ValueError("Expected natural number")


def factorial(number):
    if number == 0:
        return 1
    else:
        return number*factorial(number-1)


form = cgi.FieldStorage()
field = "val_to_check"
resp = ""
if field in form:
    try:
        n = int(form[field].value)
        if is_factorial(n):
            resp = "Yeah, {} is a factorial. Congrats!".format(n)
        else:
            resp = "No, {} is not a factorial, sorry.".format(n)
    except ValueError as e:
        resp = e
# else:
#     pass

# with open("/home/olga/PyCharm/domashki/sem2/z3/coll_27.1/cgi-bin/resp.html") as f:
#     HTML = f.read()

HTML = """Content-type: text/html charset=utf-8\n\n
<html lang="ua">
<head>
    <meta charset="UTF-8">
    <title>Factorial</title>
</head>
<body>
<h1>Check whether your number is factorial</h1>
<p>{ans}</p>
</body>
</html>"""

#<p>Українська і</p>

p = HTML.format(ans=resp)
print(p)
