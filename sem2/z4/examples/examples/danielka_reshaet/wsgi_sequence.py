#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import cgi

import json

import re

import numpy as np

HTML_PAGE = """<html>
<title>Решение задачи</title>
<body>
<form method=POST action="">
<table>
<tr>
<td align=right>
<table align="center">
<tr>
<td>Введите строку:</td>
<td><input type=text name=val value=""></td>
<td><input type=submit value="Выделить и вывести в JSON формате"></td>
</tr>
</table>
<table align="center">
<tr>
<br>
<td>
%s
</td>
</tr>
</table>
</form>
</body>
</html>
"""


def rle(in_array):

    # print(in_array)

    ia = np.asarray(in_array)

    n = len(ia)

    if n:

        y = np.array(ia[1:] != ia[:-1])
        i = np.append(np.where(y), n - 1)
        z = np.diff(np.append(-1, i))
        p = np.cumsum(np.append(0, z))[:-1]

        mi = p[np.where(z == np.amax(z))][0]
        mx = np.amax(z)

        # print(mi, mx)
        # print(type(ib) for ib in [mi, mx])

        return [''.join(part) for part in (in_array[:mi], in_array[mi:mi+mx], in_array[mi+mx:])]

    return None


def to_html_form(array):
    return "<p>{}<span style='color: teal'>{}</span>{}</p>".format(*array)


def application(environ, start_response):

    if environ.get('PATH_INFO', '').lstrip('/') == '':

        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        if 'val' in form:

            body = HTML_PAGE % json.dumps({'string': to_html_form(rle([x for x in re.split('', str(form['val'].value))
                                          if x]))}, ensure_ascii=False)

        else:

            body = HTML_PAGE % ''

        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    else:

        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])

        body = 'Page not found'

    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':

    from wsgiref.simple_server import make_server

    print('server init')

    httpd = make_server('localhost', 4827, application)

    httpd.serve_forever()
