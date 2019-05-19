import json

import os

# TODO: Наркоман, поправь if-ы в JSON классах


class Person:

    def __init__(self):

        self.name = None

        self.byear = None

    def input(self):

        self.name = input('Прізвище: ')

        self.byear = input('Рік народження: ')

    def print(self):

        print(self.name, self.byear, end=' ')


class Passenger(Person):

    def __init__(self):

        Person.__init__(self)

        del self.byear

        self.from_city = None

        self.to_city = None

        self.cost = None

    def form(self, key, lst):

        self.name = key

        self.from_city = lst[0]

        self.to_city = lst[1]

        self.cost = lst[2]

    def print(self):

        return '{}|{}-{}|{}'.format(self.name, self.from_city, self.to_city, self.cost)


class RoutesJSON:

    def __init__(self, key_field, fields_list):

        self.path = os.path.join(os.getcwd(), 'routes_json.json')

        self.key_field = key_field

        self.fields_list = fields_list

    def add_info(self, str_list):

        if not os.path.exists(self.path):

            self.generate_json_file(str_list)

        else:

            self.append_to_json_file(str_list)

    def append_to_json_file(self, str_list):

        with open(self.path, 'r') as f:

            lst = json.load(f)

            routes = self._list_to_dict(lst)

        # TODO: str 'c0-c1' --> tuple (c0, c1) or str 'line_name'

        if not (f'{str_list[0]}-{str_list[1]}' in routes):

            routes[f'{str_list[0]}-{str_list[1]}'] = str_list

        out = self._dict_to_list(routes)

        with open(self.path, 'w') as f:

            json.dump(out, f, indent=4, sort_keys=True, ensure_ascii=False)

    def generate_json_file(self, str_list):

        routes = dict()

        routes[f'{str_list[0]}-{str_list[1]}'] = str_list

        out = self._dict_to_list(routes)

        with open(self.path, 'w') as f:

            json.dump(out, f, indent=4, sort_keys=True, ensure_ascii=False)

    def get_routes(self):

        with open(self.path, 'r') as f:

            lst = json.load(f)

            routes = self._list_to_dict(lst)

        return routes

    def _list_to_dict(self, lst):

        dct = {}

        for d in lst:

            k = d[self.key_field]

            v = [i[1] for i in d.items()
                 if i[0] != self.key_field]

            dct[k] = v

        return dct

    def _dict_to_list(self, dct):

        lst = []

        for v in dct:

            v_list = dct[v]

            d = {self.fields_list[i]: v_list[i]
                 for i in range(len(v_list))}

            d[self.key_field] = v

            lst.append(d)

        return lst


class PassengerJSON(RoutesJSON):

    def __init__(self, key_field, fields_list):

        RoutesJSON.__init__(self, key_field, fields_list)

        self.path = os.path.join(os.getcwd(), 'passengers_json.json')

    def append_to_json_file(self, str_list):

        with open(self.path, 'r') as f:

            lst = json.load(f)

            passengers = self._list_to_dict(lst)

        if not str_list[0] in passengers:

            passengers[str_list[0]] = str_list[1:]

        out = self._dict_to_list(passengers)

        with open(self.path, 'w') as f:

            json.dump(out, f, indent=4, ensure_ascii=False)

    def generate_json_file(self, str_list):

        passengers = dict()

        passengers[str_list[0]] = str_list[1:]

        out = self._dict_to_list(passengers)

        with open(self.path, 'w') as f:

            json.dump(out, f, indent=4, ensure_ascii=False)
