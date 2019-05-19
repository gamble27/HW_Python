#T26_01_v2 Р’С–РґРєСЂРёС‚С‚СЏ СЃС‚РѕСЂС–РЅРєРё Сѓ Р†РЅС‚РµСЂРЅРµС‚.
#Р’РёР·РЅР°С‡РµРЅРЅСЏ РєРѕРѕРґСѓРІР°РЅРЅСЏ Р·Р° РґРѕРїРѕРјРѕРіРѕСЋ Р·Р°РіРѕР»РѕРІРєС–РІ

import sys
import re
from urllib.request import urlopen

P_ENC = r'\bcharset=(?P<ENC>.+)\b'

def getencoding(http_file):
    '''РћС‚СЂРёРјР°С‚Рё РєРѕРґСѓРІР°РЅРЅСЏ С„Р°Р№Р»Сѓ http_file Р· Р†РЅС‚РµСЂРЅРµС‚.'''
    headers = http_file.getheaders()    # РѕС‚СЂРёРјР°С‚Рё Р·Р°РіРѕР»РѕРІРєРё С„Р°Р№Р»Сѓ
    # print(headers)
    dct = dict(headers)                 # РїРµСЂРµС‚РІРѕСЂРёС‚Рё Сѓ СЃР»РѕРІРЅРёРє
    content = dct.get('Content-Type','')# Р·РЅР°Р№С‚Рё 'Content-Type'
    # print(content)
    mt = re.search(P_ENC, content)      # Р·РЅР°Р№С‚Рё РєРѕРґСѓРІР°РЅРЅСЏ (РїС–СЃР»СЏ 'charset=' )
    # print(mt.group())
    if mt:
        enc = mt.group('ENC').lower().strip() # РІРёРґС–Р»РёС‚Рё РєРѕРґСѓРІР°РЅРЅСЏ
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc

if __name__ == '__main__':
    if len(sys.argv) == 1:
        url = 'http://matfiz.univ.kiev.ua/pages/13'
    else:
        url = sys.argv[1]

    http_file = urlopen(url)
    print("Status:", http_file.status)

    enc = getencoding(http_file)
    #print(enc)

    if enc:
        for line in http_file:
            s = str(line, encoding = enc)
            print(s, end='')

