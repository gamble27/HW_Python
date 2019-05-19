from wsgiref.simple_server import make_server
import cgi

import os
import json


START_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2(1)/index.html"
ADD_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2(1)/add_contact.html"
UPDATE_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2(1)/edit_contact.html"
FIND_PAGE = "/home/olga/PyCharm/domashki/sem2/z4/ind_27.3_v2(1)/find_contact.html"

# class Contact:
#     def __init__(self, name, phone):
#         self.name = name
#         self._phone = phone
#
#     @property
#     def number(self):
#         return self._phone
#
#     def change_number(self, new_number):
#         self._phone = new_number
#
#     def __call__(self, *args, **kwargs):
#         return self.name
#
class JSONPhoneBook:
    '''Клас для ведення телефонного довідника з використанням JSON.

    У файлі JSON записи довідника зберігаються у форматі:
    [
    {"friend": <name>,
    "phone": <phone>},
    ...
    ]
    Цей список для зручності обробки треба перетворити у словник.
    Ключ у словнику - значення "friend", а значення - значення "phone".
    При записі треба здійснити обернене перетворення.

    Поля:
    self.filename - ім'я файлу довідника
    self.key_field - ключ, що використовується при утворенні словника
    self.fields_list - список імен полів з файлу JSON
    '''
    def __init__(self, filename, key_field, fields_list):
        self.filename = filename
        self.key_field = key_field
        self.fields_list = fields_list

        self._check_file()

    def _check_file(self):
        path, file = os.path.split(self.filename)

        if not os.path.exists(self.filename):
            # os.makedirs(path)


            filename = file
            with open(os.path.join(path, filename), 'wb') as temp_file:
                # temp_file.write()
                json.dump({}, fp=temp_file)
                temp_file.close()

    # def createrb(self):
    #     '''Створює довідник та записує у нього n записів.'''
    #     n = int(input('Кількість записів:'))
    #     book = {}
    #     for i in range(n):
    #         name = input('Name: ')
    #         phone = input('Phone: ')
    #         book[name] = [phone]          #додаємо запис
    #     out = self._dict_to_list(book)
    #     with open(self.filename, 'w') as f:
    #         json.dump(out, f, indent=4, sort_keys=True)

    def add_contact(self, name, phone):
        '''Доповнює довідник одним записом.'''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        # name = input('Name: ')
        # phone = input('Phone: ')
        book[name] = [phone]              #додаємо запис
        out = self._dict_to_list(book)
        with open(self.filename, 'w') as f:
            json.dump(out, f, indent=4, sort_keys=True)

    def find_contact(self, name):
        '''Шукає у довіднику телефон за ім'ям name.

        Якщо не знайдено, повертає порожній рядок.
        '''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        if name in book:
            phone = book[name][0]
        else:
            phone = "Not found"
        return phone

    def update_contact(self, name, newphone):
        '''Замінює у довіднику телефон за ім'ям name на newphone.

        Якщо не знайдено, нічого не робить.
        '''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        if name in book:
            book[name] = [newphone]           #змінюємо запис
        out = self._dict_to_list(book)
        with open(self.filename, 'w') as f:
            json.dump(out, f, indent=4, sort_keys=True)

    @property
    def contacts(self):
        cnt = []
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        for name in book:
            cnt.append(name)
        return cnt

    def _list_to_dict(self, lst):
        '''Перетворює список lst у словник.'''
        dct = {}
        for d in lst:
            key = d[self.key_field]
            value = [item[1] for item in d.items()
                     if item[0] != self.key_field]
            dct[key] = value
        return dct

    def _dict_to_list(self, dct):
        '''Перетворює словник dct у список.'''
        lst = []
        for a in dct:
            value_list = dct[a]
            d = {self.fields_list[i] : value_list[i]
                 for i in range(len(value_list))}
            d[self.key_field] = a
            lst.append(d)
        return lst

class PhoneApp:
    def __init__(self, phonebook_file, key_field="friend", fields_list=["phone"]):
        #  json stuff
        self.phonebook = JSONPhoneBook(phonebook_file, key_field, fields_list)

        #  server stuff
        self.commands = {
            "":              self.start,
            "open_add_page":           self.open_add_page,
            "open_find_page":          self.open_find_page,
            "open_update_page":        self.open_update_page,

            "add_contact":             self.add_contact,
            "update_contact":          self.update_contact,
            "find_contact":            self.find_contact,
            # "process_query": self.process,
            # "home":          self.start

        }

    def __call__(self, environ, start_response):
        command = environ.get('PATH_INFO', '').lstrip('/')

        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        error = False
        if command in self.commands:
            body = self.commands[command](form)
            if body:
                start_response(
                    '200 OK', [('Content-Type', 'text/html; charset=utf-8')]
                )
            else:
                error = True
        else:
            error = True
        if error:
            start_response(
                '404 NOT FOUND', [('Content-type', 'text/plain')]
            )
            body = 'Daaafaaaquuu! 404 is here, dude.'

        return [bytes(body, encoding='utf-8')]

    # def process(self, form):
    #     pass

    def start(self, form=None):
        with open(START_PAGE) as f:
            cnt = f.read()
        return cnt

    def open_add_page(self, form):
        with open(ADD_PAGE) as f:
            cnt = f.read()
        return cnt

    def open_find_page(self, form):
        with open(FIND_PAGE) as f:
            cnt = f.read()
        return cnt

    def open_update_page(self, form):
        with open(UPDATE_PAGE) as f:
           lines = f.readlines()

        opt_pattern = '<option value="{v}">{v}</option>\n'
        value = '<option value="Choose contact" disabled>Choose contact</option>\n'
        value += ''.join(
            [opt_pattern.format(v=contact) for contact in self.phonebook.contacts]
        )

        key = "{contact_selection}"
        for i, line in enumerate(lines):
            if key in line:
                j = line.find(key)
                lines[i] = line[:j] + value + line[j+len(key):]
        return ''.join(lines)

    def add_contact(self, form):
        name = form["name"].value
        phone = form["phone"].value

        self.phonebook.add_contact(name, phone)

        return self.start()

    def update_contact(self, form):
        name = form["name"].value
        phone = form["phone"].value

        self.phonebook.update_contact(name, phone)

        return self.start()

    def find_contact(self, form):
        name = form["name"].value
        return self.phonebook.find_contact(name)


if __name__ == "__main__":
    phone_app = PhoneApp("phones.json")
    server = make_server("localhost", 8050, phone_app)
    server.serve_forever()
