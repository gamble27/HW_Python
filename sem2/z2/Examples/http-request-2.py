# T26_21_v2 Р’РёРєРѕРЅР°РЅРЅСЏ Р·Р°РїРёС‚Сѓ POST
# Р—Р°РїРёС‚ РЅР°СЏРІРЅРѕСЃС‚С– Р»С–С‚РµСЂР°С‚СѓСЂРё Сѓ Р±С–Р±Р»С–РѕС‚РµС†С– СѓРЅС–РІРµСЂСЃРёС‚РµС‚Сѓ

import sys
from open_2 import *
from urllib.request import urlopen
from urllib.parse import urlencode

if len(sys.argv) == 1:
    title = input('Title: ')
    author = input('Author: ')
else:
    title = sys.argv[1]
    author = sys.argv[1]

url = 'http://ecatalog.univ.kiev.ua'
http_file = urlopen(url)
enc = getencoding(http_file)    # РѕС‚СЂРёРјР°С‚Рё РєРѕРґСѓРІР°РЅРЅСЏ
print(enc)

params = {'title': title, 'author': author}
query = urlencode(params, encoding=enc) # С„РѕСЂРјСѓРІР°РЅРЅСЏ СЂСЏРґРєР° РїР°СЂР°РјРµС‚СЂС–РІ Р·Р°РїРёС‚Сѓ

url = 'http://ecatalog.univ.kiev.ua/ukr/elcat/new/result.php3'
#print(url)

request = urlopen(url, bytes(query, encoding=enc))# РІС–РґРїСЂР°РІРєР° Р·Р°РїРёС‚Сѓ

# С‡РёС‚Р°РЅРЅСЏ СЃС‚РѕСЂС–РЅРєРё РІС–РґРїРѕРІС–РґС– СЃРµСЂРІРµСЂР°
data = str(request.read(), encoding = enc, errors='ignore')
'''
for line in request:
    s = str(line, encoding = enc, errors='ignore')
    print(s, end='')
'''
# Р·Р°РїРёСЃ СЃС‚РѕСЂС–РЅРєРё Сѓ Р»РѕРєР°Р»СЊРЅРёР№ С„Р°Р№Р»
with open(title + '.html', 'w') as fout:
    fout.write(data)
