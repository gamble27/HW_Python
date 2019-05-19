# T26_31 РћС‚СЂРёРјР°РЅРЅСЏ РѕР·РЅР°С‡РµРЅРЅСЏ Р· РІС–РєС–РїРµРґС–С— Р·Р° Р·Р°РїРёС‚РѕРј.

import html.parser
from t26_01_get_url_v2 import *
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError



class WikiDefParser(html.parser.HTMLParser):
    '''РљР»Р°СЃ, С‰Рѕ СЂРѕР·Р±РёСЂР°С” СЃС‚РѕСЂС–РЅРєСѓ Р· Р’С–РєС–РїРµРґС–С— С‚Р° С„РѕСЂРјСѓС” РѕР·РЅР°С‡РµРЅРЅСЏ.

       Р’ СЏРєРѕСЃС‚С– РѕР·РЅР°С‡РµРЅРЅСЏ Р±РµСЂРµС‚СЊСЃСЏ С‚РµРєСЃС‚ Сѓ РїРµСЂС€РѕРјСѓ С‚РµР·С– <p> ... </p>
    '''
    def __init__(self, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.pieces = []        # СЃРїРёСЃРѕРє С‡Р°СЃС‚РёРЅ С‚РµРєСЃС‚Сѓ РѕР·РЅР°С‡РµРЅРЅСЏ
        self.in_p = False       # С‡Рё Р·РЅР°С…РѕРґРёРјРѕСЃСЊ РјРё СѓСЃРµСЂРµРґРёРЅС– С‚РµРіСѓ <p>
        # self.in_p РґРѕСЂС–РІРЅСЋС”
            # False РґРѕ РїРµСЂС€РѕРіРѕ С‚РµРіСѓ <p>,
            # True РІСЃРµСЂРµРґРёРЅС– РїРµСЂС€РѕРіРѕ С‚РµРіСѓ <p>,
            # None РїС–СЃР»СЏ РїРµСЂС€РѕРіРѕ С‚РµРіСѓ <p>

    def handle_starttag(self, tag, attrs):
        '''РћР±СЂРѕР±Р»СЏС” РїРѕС‡Р°С‚РєРѕРІРёР№ С‚РµРі tag (<p>).'''
        if tag == 'p' and self.in_p != None:
            self.in_p = True

    def handle_endtag(self, tag):
        '''РћР±СЂРѕР±Р»СЏС” РєС–РЅС†РµРІРёР№ С‚РµРі tag (<p>).'''
        if tag == 'p':
            self.in_p = None

    def handle_data(self, data):
        '''РћР±СЂРѕР±Р»СЏС” РґР°РЅС– data.'''
        if self.in_p:
            self.pieces.append(data)

    @property
    def getdef(self):
        '''РџРѕРІРµСЂС‚Р°С” СЂСЏРґРѕРє РѕР·РЅР°С‡РµРЅРЅСЏ.'''
        return ' '.join(self.pieces)


class WikiDef:
    '''РљР»Р°СЃ РґР»СЏ С‡РёС‚Р°РЅРЅСЏ СЃС‚Р°С‚С‚С– Р’С–РєС–РїРµРґС–С— Р·Р° Р·Р°РїРёС‚РѕРј С‚Р° РїРѕРІРµСЂРЅРµРЅРЅСЏ РѕР·РЅР°С‡РµРЅРЅСЏ.'''
    def __init__(self, p_str, lang='uk'):
        '''РљРѕРЅСЃС‚СЂСѓРєС‚РѕСЂ РІС–РґРєСЂРёРІР°С” С‚Р° Р°РЅР°Р»С–Р·СѓС” СЃС‚Р°С‚С‚СЋ.

           p_str - СЂСЏРґРѕРє Р·Р°РїРёС‚Сѓ,
           lang - РјРѕРІР° РІС–РєС–РїРµРґС–С— (РјРѕР¶Рµ Р±СѓС‚Рё С‰Рµ en, ru)'''
        self._def = ''                          # РѕР·РЅР°С‡РµРЅРЅСЏ С‚РµСЂРјС–РЅСѓ
        url = 'https://{}.wikipedia.org'.format(lang)
#        print(url)
        http_file = urlopen(url)
        enc = getencoding(http_file)            # РѕС‚СЂРёРјР°С‚Рё РєРѕРґСѓРІР°РЅРЅСЏ
#        print(enc)

        params = {'q' : p_str}
        query = urlencode(params, encoding=enc)[2:] # С„РѕСЂРјСѓРІР°РЅРЅСЏ СЂСЏРґРєР° Р·Р°РїРёС‚Сѓ

        # URL Р· Р·Р°РїРёС‚РѕРј
        url = 'https://{}.wikipedia.org/wiki/{}'.format(lang, query)
#        print(url)
        try:
            request = urlopen(url)                  # РІС–РґРїСЂР°РІРєР° Р·Р°РїРёС‚Сѓ
#            print(request.status)
            # С‡РёС‚Р°РЅРЅСЏ СЃС‚РѕСЂС–РЅРєРё РІС–РґРїРѕРІС–РґС– СЃРµСЂРІРµСЂР°
            data = str(request.read(), encoding = enc, errors='ignore')
            wdp = WikiDefParser()
            wdp.feed(data)
            self._def = wdp.getdef
        except HTTPError as e:
            print(e)

    @property
    def definition(self):
        '''Р’Р»Р°СЃС‚РёРІС–СЃС‚СЊ РїРѕРІРµСЂС‚Р°С” РѕР·РЅР°С‡РµРЅРЅСЏ.

           РЇРєС‰Рѕ РЅРµ Р·РЅР°Р№РґРµРЅРѕ СЃС‚РѕСЂС–РЅРєСѓ, С‚Рѕ РїРѕСЂРѕР¶РЅС–Р№ СЂСЏРґРѕРє.
        '''
        return self._def

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        param_str = input('To search: ')
    else:
        param_str = sys.argv[1]
    wd = WikiDef(param_str)
    print('Definition:', wd.definition)



