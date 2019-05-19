#t28_21_refbook_xml.py
#РўРµР»РµС„РѕРЅРЅРёР№ РґРѕРІС–РґРЅРёРє (xml)
import xml.etree.ElementTree as et

class XMLRefBook:
    '''РљР»Р°СЃ РґР»СЏ РІРµРґРµРЅРЅСЏ С‚РµР»РµС„РѕРЅРЅРѕРіРѕ РґРѕРІС–РґРЅРёРєР° Р· РІРёРєРѕСЂРёСЃС‚Р°РЅРЅСЏРј XML.

       РЈ С„Р°Р№Р»С– XML Р·Р°РїРёСЃРё РґРѕРІС–РґРЅРёРєР° Р·Р±РµСЂС–РіР°СЋС‚СЊСЃСЏ Сѓ С„РѕСЂРјР°С‚С–:
       <refbook>
           <friend name="С–Рј'СЏ"> С‚РµР»РµС„РѕРЅ <friend>
          ...
       </refbook>

       РџРѕР»СЏ:
       self.filename - С–Рј'СЏ С„Р°Р№Р»Сѓ РґРѕРІС–РґРЅРёРєР°
    '''
    def __init__(self, filename):
        self.filename = filename


    def createrb(self):
        '''РЎС‚РІРѕСЂСЋС” РґРѕРІС–РґРЅРёРє С‚Р° Р·Р°РїРёСЃСѓС” Сѓ РЅСЊРѕРіРѕ n Р·Р°РїРёСЃС–РІ.'''
        n = int(input('РљС–Р»СЊРєС–СЃС‚СЊ Р·Р°РїРёСЃС–РІ: '))
        book = et.Element('refbook')        # СЃС‚РІРѕСЂРёС‚Рё РєРѕСЂРµРЅРµРІРёР№ РІСѓР·РѕР» РґРµСЂРµРІР°
        for i in range(n):
            friend = et.Element('friend')   # СЃС‚РІРѕСЂРёС‚Рё РІСѓР·РѕР» РґРµСЂРµРІР°
            name = input('РџСЂС–Р·РІРёС‰Рµ: ')
            friend.set('name', name)        # РІСЃС‚Р°РЅРѕРІРёС‚Рё Р·РЅР°С‡РµРЅРЅСЏ Р°С‚СЂРёР±СѓС‚Р°
            phone = input('РўРµР»РµС„РѕРЅ: ')
            friend.text = phone             # Р·РјС–РЅРёС‚Рё С‚РµРєСЃС‚ РІСѓР·Р»Р°
            book.append(friend)             # РґРѕРґР°С‚Рё СЃРёРЅР° (РІСѓР·РѕР»)
        e = et.ElementTree(book)            # СЃС‚РІРѕСЂРёС‚Рё РґРѕРєСѓРјРµРЅС‚
        e.write(self.filename)              # Р·Р±РµСЂРµРіС‚Рё С„Р°Р№Р»

    def apprb(self):
        '''Р”РѕРїРѕРІРЅСЋС” РґРѕРІС–РґРЅРёРє РѕРґРЅРёРј Р·Р°РїРёСЃРѕРј.'''
        # Р·Р°РІР°РЅС‚Р°Р¶РёС‚Рё С‚Р° РїСЂРѕР°РЅР°Р»С–Р·СѓРІР°С‚Рё РґРѕРєСѓРјРµРЅС‚
        e = et.parse(self.filename)
        book = e.getroot()
        friend = et.Element('friend')       # СЃС‚РІРѕСЂРёС‚Рё РІСѓР·РѕР» РґРµСЂРµРІР°
        name = input('РџСЂС–Р·РІРёС‰Рµ: ')
        friend.set('name', name)            # РІСЃС‚Р°РЅРѕРІРёС‚Рё Р·РЅР°С‡РµРЅРЅСЏ Р°С‚СЂРёР±СѓС‚Р°
        phone = input('РўРµР»РµС„РѕРЅ: ')
        friend.text = phone                 # Р·РјС–РЅРёС‚Рё С‚РµРєСЃС‚ РІСѓР·Р»Р°
        book.append(friend)                 # РґРѕРґР°С‚Рё СЃРёРЅР° (РІСѓР·РѕР»)
        e.write(self.filename)              # Р·Р±РµСЂРµРіС‚Рё С„Р°Р№Р»

    def searchrb(self, name):
        '''РЁСѓРєР°С” Сѓ РґРѕРІС–РґРЅРёРєСѓ С‚РµР»РµС„РѕРЅ Р·Р° С–Рј'СЏРј name.

        РЇРєС‰Рѕ РЅРµ Р·РЅР°Р№РґРµРЅРѕ, РїРѕРІРµСЂС‚Р°С” РїРѕСЂРѕР¶РЅС–Р№ СЂСЏРґРѕРє.
        '''
        # Р·Р°РІР°РЅС‚Р°Р¶РёС‚Рё С‚Р° РїСЂРѕР°РЅР°Р»С–Р·СѓРІР°С‚Рё РґРѕРєСѓРјРµРЅС‚
        e = et.parse(self.filename)
        phone = ""
        # Р·РЅР°Р№С‚Рё РІСЃС– РІСѓР·Р»Рё "friend"
        for friend in e.iterfind('friend'):
            if friend.get('name') == name:
                phone = friend.text
                break
        return phone

    def replacerb(self, name, newphone):
        '''Р—Р°РјС–РЅСЋС” Сѓ РґРѕРІС–РґРЅРёРєСѓ С‚РµР»РµС„РѕРЅ Р·Р° С–Рј'СЏРј name РЅР° newphone.

        РЇРєС‰Рѕ РЅРµ Р·РЅР°Р№РґРµРЅРѕ, РЅС–С‡РѕРіРѕ РЅРµ СЂРѕР±РёС‚СЊ.
        '''
        # Р·Р°РІР°РЅС‚Р°Р¶РёС‚Рё С‚Р° РїСЂРѕР°РЅР°Р»С–Р·СѓРІР°С‚Рё РґРѕРєСѓРјРµРЅС‚
        e = et.parse(self.filename)
        phone = ""
        # Р·РЅР°Р№С‚Рё РІСЃС– РІСѓР·Р»Рё "friend"
        for friend in e.iterfind('friend'):
            if friend.get('name') == name:
                friend.text = newphone
                break
        e.write(self.filename)




filename = 'refs.xml'      #С–Рј'СЏ С„Р°Р№Р»Сѓ РґРѕРІС–РґРЅРёРєР°

rb = XMLRefBook(filename)

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
