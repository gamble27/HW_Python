#t28_01_refbook_json_v1.py
#РўРµР»РµС„РѕРЅРЅРёР№ РґРѕРІС–РґРЅРёРє (json)
import json

class JSONRefBook:
    '''РљР»Р°СЃ РґР»СЏ РІРµРґРµРЅРЅСЏ С‚РµР»РµС„РѕРЅРЅРѕРіРѕ РґРѕРІС–РґРЅРёРєР° Р· РІРёРєРѕСЂРёСЃС‚Р°РЅРЅСЏРј JSON.

       РЈ С„Р°Р№Р»С– JSON Р·Р°РїРёСЃРё РґРѕРІС–РґРЅРёРєР° Р·Р±РµСЂС–РіР°СЋС‚СЊСЃСЏ Сѓ С„РѕСЂРјР°С‚С–:
       [
         {"friend": <name>,
          "phone", <phone>},
          ...
       ]
       Р¦РµР№ СЃРїРёСЃРѕРє РґР»СЏ Р·СЂСѓС‡РЅРѕСЃС‚С– РѕР±СЂРѕР±РєРё С‚СЂРµР±Р° РїРµСЂРµС‚РІРѕСЂРёС‚Рё Сѓ СЃР»РѕРІРЅРёРє.
       РљР»СЋС‡ Сѓ СЃР»РѕРІРЅРёРєСѓ - Р·РЅР°С‡РµРЅРЅСЏ "friend", Р° Р·РЅР°С‡РµРЅРЅСЏ - Р·РЅР°С‡РµРЅРЅСЏ "phone".
       РџСЂРё Р·Р°РїРёСЃС– С‚СЂРµР±Р° Р·РґС–Р№СЃРЅРёС‚Рё РѕР±РµСЂРЅРµРЅРµ РїРµСЂРµС‚РІРѕСЂРµРЅРЅСЏ.

       РџРѕР»СЏ:
       self.filename - С–Рј'СЏ С„Р°Р№Р»Сѓ РґРѕРІС–РґРЅРёРєР°
       self.key_field - РєР»СЋС‡, С‰Рѕ РІРёРєРѕСЂРёСЃС‚РѕРІСѓС”С‚СЊСЃСЏ РїСЂРё СѓС‚РІРѕСЂРµРЅРЅС– СЃР»РѕРІРЅРёРєР°
       self.fields_list - СЃРїРёСЃРѕРє С–РјРµРЅ РїРѕР»С–РІ Р· С„Р°Р№Р»Сѓ JSON
    '''
    def __init__(self, filename, key_field, fields_list):
        self.filename = filename
        self.key_field = key_field
        self.fields_list = fields_list

    def createrb(self):
        '''РЎС‚РІРѕСЂСЋС” РґРѕРІС–РґРЅРёРє С‚Р° Р·Р°РїРёСЃСѓС” Сѓ РЅСЊРѕРіРѕ n Р·Р°РїРёСЃС–РІ.'''
        n = int(input('РљС–Р»СЊРєС–СЃС‚СЊ Р·Р°РїРёСЃС–РІ: '))
        book = {}
        for i in range(n):
            name = input('РџСЂС–Р·РІРёС‰Рµ: ')
            phone = input('РўРµР»РµС„РѕРЅ: ')
            book[name] = [phone]          #РґРѕРґР°С”РјРѕ Р·Р°РїРёСЃ
        out = self._dict_to_list(book)
        with open(self.filename, 'w') as f:
            json.dump(out, f, indent=4, sort_keys=True)

    def apprb(self):
        '''Р”РѕРїРѕРІРЅСЋС” РґРѕРІС–РґРЅРёРє РѕРґРЅРёРј Р·Р°РїРёСЃРѕРј.'''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        name = input('РџСЂС–Р·РІРёС‰Рµ: ')
        phone = input('РўРµР»РµС„РѕРЅ: ')
        book[name] = [phone]              #РґРѕРґР°С”РјРѕ Р·Р°РїРёСЃ
        out = self._dict_to_list(book)
        with open(self.filename, 'w') as f:
            json.dump(out, f, indent=4, sort_keys=True)

    def searchrb(self, name):
        '''РЁСѓРєР°С” Сѓ РґРѕРІС–РґРЅРёРєСѓ С‚РµР»РµС„РѕРЅ Р·Р° С–Рј'СЏРј name.

        РЇРєС‰Рѕ РЅРµ Р·РЅР°Р№РґРµРЅРѕ, РїРѕРІРµСЂС‚Р°С” РїРѕСЂРѕР¶РЅС–Р№ СЂСЏРґРѕРє.
        '''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        if name in book:
            phone = book[name][0]
        else:
            phone = ""
        return phone

    def replacerb(self, name, newphone):
        '''Р—Р°РјС–РЅСЋС” Сѓ РґРѕРІС–РґРЅРёРєСѓ С‚РµР»РµС„РѕРЅ Р·Р° С–Рј'СЏРј name РЅР° newphone.

        РЇРєС‰Рѕ РЅРµ Р·РЅР°Р№РґРµРЅРѕ, РЅС–С‡РѕРіРѕ РЅРµ СЂРѕР±РёС‚СЊ.
        '''
        with open(self.filename, 'r') as f:
            lst = json.load(f)
            book = self._list_to_dict(lst)
        if name in book:
            book[name] = [newphone]           #Р·РјС–РЅСЋС”РјРѕ Р·Р°РїРёСЃ
        out = self._dict_to_list(book)
        with open(self.filename, 'w') as f:
            json.dump(out, f, indent=4, sort_keys=True)


    def _list_to_dict(self, lst):
        '''РџРµСЂРµС‚РІРѕСЂСЋС” СЃРїРёСЃРѕРє lst Сѓ СЃР»РѕРІРЅРёРє.'''
        dct = {}
        for d in lst:
            key = d[self.key_field]
            value = [item[1] for item in d.items()
                     if item[0] != self.key_field]
            dct[key] = value
        return dct

    def _dict_to_list(self, dct):
        '''РџРµСЂРµС‚РІРѕСЂСЋС” СЃР»РѕРІРЅРёРє dct Сѓ СЃРїРёСЃРѕРє.'''
        lst = []
        for a in dct:
            value_list = dct[a]
            d = {self.fields_list[i] : value_list[i]
                 for i in range(len(value_list))}
            d[self.key_field] = a
            lst.append(d)
        return lst



filename = 'refs.json'      #С–Рј'СЏ С„Р°Р№Р»Сѓ РґРѕРІС–РґРЅРёРєР°

rb = JSONRefBook(filename, "friend", ["phone"])

while True:
    k = int(input('Р РµР¶РёРј СЂРѕР±РѕС‚Рё [1 - 5]:'))
    if k == 1:                      #СЃС‚РІРѕСЂРёС‚Рё РґРѕРІС–РґРЅРёРє
        rb.createrb()
    elif k == 2:                    #РґРѕРґР°С‚Рё Р·Р°РїРёСЃ РґРѕ РґРѕРІС–РґРЅРёРєР°
        rb.apprb()
    elif k == 3:                    #Р·РЅР°Р№С‚Рё С‚РµР»РµС„РѕРЅ Сѓ РґРѕРІС–РґРЅРёРєСѓ
        name = input('РџСЂС–Р·РІРёС‰Рµ: ')
        phone = rb.searchrb(name)
        if len(phone) > 0:
            print('РўРµР»РµС„РѕРЅ:', phone)
        else:
            print('РЅРµ Р·РЅР°Р№РґРµРЅРѕ')
    elif k == 4:                    #Р·Р°РјС–РЅРёС‚Рё С‚РµР»РµС„РѕРЅ Сѓ РґРѕРІС–РґРЅРёРєСѓ
        name = input('РџСЂС–Р·РІРёС‰Рµ: ')
        phone = input('РќРѕРІРёР№ С‚РµР»РµС„РѕРЅ: ')
        rb.replacerb(name, phone)
    elif k == 5:
        break








