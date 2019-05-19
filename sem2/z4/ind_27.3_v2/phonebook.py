import json
import os


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

    def apprb(self, name, phone):
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

    def searchrb(self, name):
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

    def replacerb(self, name, newphone):
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


if __name__ == "__main__":
    filename = 'refs.json'      #ім'я файлу довідника

    rb = JSONPhoneBook(filename, "friend", ["phone"])

    # while True:
    #     k = int(input('Pежим роботи [1 - 5]:'))
    #     if k == 1:                      #створити довідник
    #         rb.createrb()
    #     elif k == 2:                    #додати запис до довідника
    #         rb.apprb()
    #     elif k == 3:                    #знайти телефон у довіднику
    #         name = input('Прізвище:')
    #         phone = rb.searchrb(name)
    #         if len(phone) > 0:
    #             print('Телефон:', phone)
    #         else:
    #             print('не знайдено')
    #     elif k == 4:                    #замінити телефон у довіднику
    #         name = input('Прізвище:')
    #         phone = input('Новий телефон:')
    #         rb.replacerb(name, phone)
    #     elif k == 5:
    #         break
