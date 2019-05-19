#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-

import cgi

from html_source import *

from OOP_thing import *

# 0 - MAIN PAGE
# 1 - ADD ROUTE
# 2 - ADD PASSENGER

state = 0

routes_json = RoutesJSON('route_name', ['city_0', 'city_1', 'length', 'per_km'])

passengers_json = PassengerJSON('name', ['from', 'to', 'cost'])


def mkslct(name, values):

    select_block = '<select name="{0}">\n{1}</select>\n'

    option_block = '<option value="{0}">{0}</option>\n'

    return select_block.format(name, ''.join(option_block.format(v) for v in values))


# TODO: Проверка значений

# TODO: Почему? Да потому.


def generate_table_routes(dct):

    table_component = """<tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    </tr>"""

    v = list(dct.values())

    return ''.join([table_component.format(*v[i][:2], round(float(v[i][2]) *
                                                            float(v[i][3]), 2)) for i in range(len(v))])

def generate_table_psngrs(lst):

    table_component = """<tr>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    </tr>"""

    return ''.join([table_component.format(*lst[i]) for i in range(len(lst))])


def application(environ, start_response):

    global state

    if environ.get('PATH_INFO', '').lstrip('/') == '':

        form = cgi.FieldStorage(fp=environ['wsgi.input'],
                                environ=environ)

        if state == 1:

            tags = ['from_city', 'to_city', 'length', 'cost_per_km']

            if all(t in form for t in tags):

                routes_json.add_info([form[t].value for t in tags])

        elif state == 2:

            tags = ['pass_name', 'from_city']

            if all(t in form for t in tags):

                lst = [form[t].value for t in tags]

                from_city, to_city = routes_json.get_routes()[lst[-1]][:2]

                cost = round(float(routes_json.get_routes()[lst[-1]][3]) *
                             float(routes_json.get_routes()[lst[-1]][2]), 2)

                passengers_json.add_info([lst[0], from_city, to_city, cost])

        html = HTML_MAIN

        if 'opt' in form:

            val = form['opt'].value

            if val == 'add_route':

                state = 1

                html = HTML_ADD_ROUTE

            elif val == 'add_pass':

                state = 2

                try:

                    k = list(routes_json.get_routes().keys())

                    html = HTML_ADD_PASSENGER.format(mkslct('from_city', k))

                except FileNotFoundError:

                    html = HTML_ADD_PASSENGER.format('', '')

            elif val == 'lists_r':

                try:

                    html = HTML_ROUTES_LIST \
                        .format(generate_table_routes(routes_json.get_routes()))

                except FileNotFoundError:

                    html = HTML_ROUTES_LIST.format('')

            elif val == 'lists_p':

                try:

                    psngrs = passengers_json.get_routes()

                    lst = [Passenger() for i in range(len(psngrs))]

                    res = []

                    for i, k in enumerate(psngrs):
                        lst[i].form(k, psngrs[k])
                        res.append(lst[i].print().split('|')) # Ахахах.

                    html = HTML_PASSENGERS_LIST.format(generate_table_psngrs(res))

                except FileNotFoundError:

                    html = HTML_PASSENGERS_LIST.format('')

        else:

            state = 0

        body = html

        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    else:

        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])

        body = 'Page not found'

    return [bytes(body, encoding='utf-8')]


if __name__ == '__main__':

    from wsgiref.simple_server import make_server

    print('=== Маршруты ===')

    httpd = make_server('localhost', 1902, application)

    httpd.serve_forever()
