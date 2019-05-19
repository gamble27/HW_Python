#t28_41_population_xml.py
#РћС†С–РЅРєР° Р·РјС–РЅ РЅР°СЃРµР»РµРЅРЅСЏ РєСЂР°С—РЅ Р·Р° РїРµСЂС–РѕРґ Р·Р° РґР°РЅРёРјРё РЎРІС–С‚РѕРІРѕРіРѕ Р‘Р°РЅРєСѓ. XML

import xml.etree.ElementTree as et
import zlib
from urllib.request import urlopen
from urllib.parse import urlencode

def get_page(url_params):
    """Р¤СѓРЅРєС†С–СЏ С‡РёС‚Р°С” РѕРґРЅСѓ СЃС‚РѕСЂС–РЅРєСѓ РґРѕРєСѓРјРµРЅС‚Сѓ Р· url_params.

       РџРѕРІРµСЂС‚Р°С” СЂСЏРґРѕРє - СЃС‚РѕСЂС–РЅРєСѓ РґРѕРєСѓРјРµРЅС‚Сѓ.
    """
    request = urlopen(url_params) # РІС–РґРїСЂР°РІРєР° Р·Р°РїРёС‚Сѓ
#    print(request.status, request.headers)
    # РѕС‚СЂРёРјР°С‚Рё РІС–РґРїРѕРІС–РґСЊ СЃРµСЂРІРµСЂР°
    if request.getheader("Content-Encoding"): # СЏРєС‰Рѕ РґР°РЅС– Р·Р°Р°СЂС…С–РІРѕРІР°РЅРѕ
        data_zipped = request.read()
        data = zlib.decompress(data_zipped, zlib.MAX_WBITS | 16) # magic :)
    else:
        data = request.read()
    data = data.decode('utf-8')
    request.close()
#    print("data=", data)
    return data


def multipage_reader(url, page_proc_func, **params):
    """Р¤СѓРЅРєС†С–СЏ С‡РёС‚Р°С” Р±Р°РіР°С‚РѕСЃС‚РѕСЂС–РЅРєРѕРІРёР№ РґРѕРєСѓРјРµРЅС‚ Р· url Р· РїР°СЂР°РјРµС‚СЂР°РјРё params.

       page_proc_func - С„СѓРЅРєС†С–СЏ, СЏРєР° РѕР±СЂРѕР±Р»СЏС” РѕРґРЅСѓ СЃС‚РѕСЂС–РЅРєСѓ xml.
       РљРѕР¶РЅР° СЃС‚РѕСЂС–РЅРєР° РґРѕРєСѓРјРµРЅС‚Сѓ РїРѕРІРёРЅРЅР° РјР°С‚Рё Р·Р°РіРѕР»РѕРІРѕРє - РµР»РµРјРµРЅС‚ XML -
       С‚Р° СЃРїРёСЃРѕРє РµР»РµРјРµРЅС‚С–РІ-Р·РЅР°С‡РµРЅСЊ.
       Р—Р°РіРѕР»РѕРІРѕРє, Р·РѕРєСЂРµРјР°, РїРѕРІРёРЅРµРЅ РјС–СЃС‚РёС‚Рё Р°С‚СЂРёР±СѓС‚ - РєС–Р»СЊРєС–СЃС‚СЊ СЃС‚РѕСЂС–РЅРѕРє ("pages").
    """
    if params:
        query = urlencode(params, encoding='utf-8') # С„РѕСЂРјСѓРІР°РЅРЅСЏ СЂСЏРґРєР° РїР°СЂР°РјРµС‚СЂС–РІ
        url_params = url + '?' + query
    else:
        params = {}
        url_params = url
    data = get_page(url_params)             # РѕС‚СЂРёРјР°С‚Рё СЃС‚РѕСЂС–РЅРєСѓ Р· РґР°РЅРёРјРё
    response = et.fromstring(data)          # РїРµСЂРµС‚РІРѕСЂРёС‚Рё РґР°РЅС– Сѓ XML
    page_proc_func(response)                # РѕР±СЂРѕР±РёС‚Рё РїРµСЂС€Сѓ СЃС‚РѕСЂС–РЅРєСѓ
    page_num = int(response.get("pages"))   # РѕР±С‡РёСЃР»РёС‚Рё РєС–Р»СЊРєС–СЃС‚СЊ СЃС‚РѕСЂС–РЅРѕРє
    print('url {} page {} of {}'.format(url, 1, page_num))
    for page in range(2, page_num + 1):
        params["page"] = str(page)
        query = urlencode(params, encoding='utf-8') # С„РѕСЂРјСѓРІР°РЅРЅСЏ СЂСЏРґРєР° РїР°СЂР°РјРµС‚СЂС–РІ
        url_params = url + '?' + query
        data = get_page(url_params)                 # РѕС‚СЂРёРјР°С‚Рё СЃС‚РѕСЂС–РЅРєСѓ Р· РґР°РЅРёРјРё
        response = et.fromstring(data)              # РїРµСЂРµС‚РІРѕСЂРёС‚Рё РґР°РЅС– Сѓ XML
        page_proc_func(response)                    # РѕР±СЂРѕР±РёС‚Рё СЃС‚РѕСЂС–РЅРєСѓ
        print('url {} page {} of {}'.format(url, page, page_num))

COUNTRIES_URL = "http://api.worldbank.org/countries"
POPULATION_URL = "http://api.worldbank.org/countries/all/indicators/SP.POP.TOTL"
WB = "{http://www.worldbank.org}"

class PopulationXML:
    '''РљР»Р°СЃ РґР»СЏ РІРёР·РЅР°С‡РµРЅРЅСЏ СЃРїРёСЃРєСѓ РєСЂР°С—РЅ Р· Р·РјС–РЅР°РјРё РЅР°СЃРµР»РµРЅРЅСЏ Р·Р° РїРµСЂС–РѕРґ
       Р·Р° РґР°РЅРёРјРё РЎРІС–С‚РѕРІРѕРіРѕ Р‘Р°РЅРєСѓ Р· РІРёРєРѕСЂРёСЃС‚Р°РЅРЅСЏРј XML.

       РџРѕР»СЏ:
        self.countries - СЃР»РѕРІРЅРёРє РєСЂР°С—РЅ. РљР»СЋС‡ - РґРІРѕС…СЃРёРјРІРѕР»СЊРЅРёР№ РєРѕРґ РєСЂР°С—РЅРё.
                         Р”Р°РЅС– - СЃРїРёСЃРѕРє РєРѕСЂС‚РµР¶С–РІ Р· РЅР°Р·РІРё РєСЂР°С—РЅРё С‚Р° РЅР°СЃРµР»РµРЅРЅСЏ Сѓ
                         РїРѕС‡Р°С‚РєРѕРІРѕРјСѓ С‚Р° РєС–РЅС†РµРІРѕРјСѓ СЂРѕРєР°С…
        self.pop_change - СЃРїРёСЃРѕРє РєРѕСЂС‚РµР¶С–РІ (<Р·РјС–РЅР° РЅР°СЃРµР»РµРЅРЅСЏ>, <РєРѕРґ РєСЂР°С—РЅРё>, <РЅР°Р·РІР°>)
        self_start_year - РїРѕС‡Р°С‚РєРѕРІРёР№ СЂС–Рє
        self.fin_year   - РєС–РЅС†РµРІРёР№ СЂС–Рє
        self.list_index - С–РЅРґРµРєСЃ Сѓ СЃРїРёСЃРєСѓ РґР»СЏ РЅР°СЃРµР»РµРЅРЅСЏ РєСЂР°С—РЅРё
                          (РїРѕС‡Р°С‚РєРѕРІРёР№ СЂС–Рє - 1, РєС–РЅС†РµРІРёР№ СЂС–Рє - 2)
    '''
    def __init__(self, start_year, fin_year):
        self.countries = {}
        self.pop_change = []
        self.start_year = start_year
        self.fin_year = fin_year

    def evaluate_changes(self):
        '''РћС†С–РЅСЋС” Р·РјС–РЅРё РЅР°СЃРµР»РµРЅРЅСЏ.'''
        # Р‘СѓРґСѓС” СЃР»РѕРІРЅРёРє РєСЂР°С—РЅ
        multipage_reader(COUNTRIES_URL, self.process_countries_page)
#        print(self.countries)
        # Р‘СѓРґСѓС” СЃРїРёСЃРѕРє РєРѕСЂС‚РµР¶С–РІ (<Р·РјС–РЅР° РЅР°СЃРµР»РµРЅРЅСЏ>, <РєРѕРґ РєСЂР°С—РЅРё>, <РЅР°Р·РІР°>)
        self.list_index = 1
        multipage_reader(POPULATION_URL, self.process_population_page,
                         date=self.start_year)
        self.list_index = 2
        multipage_reader(POPULATION_URL, self.process_population_page,
                         date=self.fin_year)
        for country, c_list in self.countries.items():
            if c_list[1] and c_list[2]:
                coeff = c_list[2] / c_list[1]
                self.pop_change.append((coeff, country, c_list[0]))
        self.pop_change.sort(reverse=True)
#        print(self.countries)
        return self.pop_change

    def process_countries_page(self, response):
        '''РћР±СЂРѕР±Р»СЏС” СЃС‚РѕСЂС–РЅРєСѓ Р· РґР°РЅРёРјРё РїСЂРѕ РєСЂР°С—РЅРё, Р±СѓРґСѓС” СЃР»РѕРІРЅРёРє РєСЂР°С—РЅ.'''
        page_countries = {}
        for country in response.findall(WB + 'country'):
            key = country.find(WB + "iso2Code").text
            c_name = country.find(WB + "name").text
            region = country.find(WB + "region").text
            if region != "Aggregates":
                page_countries[key] = [c_name, 0, 0]
        self.countries.update(page_countries)

    def process_population_page(self, response):
        '''РћР±СЂРѕР±Р»СЏС” СЃС‚РѕСЂС–РЅРєСѓ Р· РґР°РЅРёРјРё РїСЂРѕ РЅР°СЃРµР»РµРЅРЅСЏ, Р·РјС–РЅСЋС” СЃР»РѕРІРЅРёРє РєСЂР°С—РЅ.

           Р—Р°РЅРѕСЃРёС‚СЊ РґР°РЅС– РїСЂРѕ РЅР°СЃРµР»РµРЅРЅСЏ Сѓ РІС–РґРїРѕРІС–РґРЅРёР№ РµР»РµРјРµРЅС‚ СЃРїРёСЃРєСѓ РґР»СЏ РєРѕР¶РЅРѕС— РєСЂР°С—РЅРё.
           Р†РЅРґРµРєСЃ РµР»РµРјРµРЅС‚Р° Р·Р°РґР°С” self.list_index (1 Р°Р±Рѕ 2)
        '''
        for data in response.findall(WB + "data"):
            country_id = data.find(WB + "country").get("id")
            population = data.find(WB + "value").text
#            print(country_id, population)
            if country_id in self.countries and population:
                self.countries[country_id][self.list_index] = int(population)


START_DEFAULT = 1995
FIN_DEFAULT = 2015

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        start = START_DEFAULT
        fin = FIN_DEFAULT
    else:
        start = sys.argv[1]
        fin = sys.argv[2]

    p_xml = PopulationXML(start, fin)
    result = p_xml.evaluate_changes()
    print("\nРџРµСЂС–РѕРґ: {} - {}".format(start,  fin))
    ten = min(len(result), 10)
    print('10 РїРµСЂС€РёС… РєСЂР°С—РЅ Р·Р° Р·СЂРѕСЃС‚Р°РЅРЅСЏРј (Р·РјРµРЅС€РµРЅРЅСЏРј) РЅР°СЃРµР»РµРЅРЅСЏ')
    for i in range(ten):
        print('{:40} {:.2f}'.format(result[i][2], result[i][0]))

    print('\n10 РѕСЃС‚Р°РЅРЅС–С… РєСЂР°С—РЅ Р·Р° Р·СЂРѕСЃС‚Р°РЅРЅСЏРј (Р·РјРµРЅС€РµРЅРЅСЏРј) РЅР°СЃРµР»РµРЅРЅСЏ')
    for i in range(-ten, 0):
        print('{:40} {:.2f}'.format(result[i][2], result[i][0]))
