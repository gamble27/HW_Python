#T26_01_v1 Р’С–РґРєСЂРёС‚С‚СЏ СЃС‚РѕСЂС–РЅРєРё Сѓ Р†РЅС‚РµСЂРЅРµС‚

import sys
from urllib.request import urlopen

if len(sys.argv) == 1:
    url = 'http://matfiz.univ.kiev.ua/pages/13'
else:
    url = sys.argv[1]

http_file = urlopen(url)
for line in http_file:
    s = str(line, encoding = 'utf-8')
    # print(s, end='')
    print(s)
