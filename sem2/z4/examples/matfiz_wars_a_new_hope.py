import html.parser

import os
import re

from urllib.error import HTTPError
from urllib.request import urlretrieve, urlopen

# from works.urlparsing_guide.url_get import *
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


class TopicListParser(html.parser.HTMLParser):

    def __init__(self, topic, *args, **kwargs):

        html.parser.HTMLParser.__init__(self, *args, **kwargs)

        print(topic[-1].isdigit())

        if topic[-1].isdigit():
            self.pattern = re.compile(topic + '. ', re.I)
            print(self.pattern)
        else:
            self.pattern = re.compile(topic, re.I)

        self.flag = False

        self.current = None

        self.chosen = None

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and ('class', 'list-group-item') in attrs:
            self.flag = True
            self.current = attrs

    def handle_endtag(self, tag):
        if tag == 'a' and self.flag:
            self.flag = False

    def handle_data(self, data):
        print(self.pattern, data)
        if self.flag:
            if re.findall(self.pattern, data):
                self.chosen = self.current

    @property
    def get_ref(self):
        if self.chosen:
            return self.chosen[0][-1]
        else:
            return self.chosen


class ProgramsListParser(html.parser.HTMLParser):

    def __init__(self, *args, **kwargs):

        html.parser.HTMLParser.__init__(self, *args, **kwargs)

        self.url = 'http://www.matfiz.univ.kiev.ua'

        self.link_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and (attr[-1].endswith('.py') or attr[-1].endswith('.pyw')):
                    self.link_list.append(self.url + attr[-1])

    @property
    def get_list(self):
        return self.link_list


class Matfiz:

    def __init__(self, topic):

        self.url = 'http://www.matfiz.univ.kiev.ua'

        self.llist = []

        http_file = urlopen(self.url + '/pages/13')

        enc = getencoding(http_file)

        try:
            tparser = TopicListParser(topic)
            tparser.feed(str(http_file.read(), encoding=enc, errors='ignore'))

            print(self.url + tparser.get_ref)

            http_file = urlopen(self.url + tparser.get_ref)

            pparser = ProgramsListParser()
            pparser.feed(str(http_file.read(), encoding=enc, errors='ignore'))

            self.llist = pparser.get_list

        except (HTTPError, TypeError) as e:
            print(e)

    def download(self, path):
        try:
            os.chdir(path)
        except OSError as e:
            return print(e)

        #print(self.llist)

        for link in self.llist:
            urlretrieve(link, link.split('/')[-1])

        os.chdir(os.path.split(os.path.realpath(__file__))[0])


if __name__ == '__main__':
    topic_name = input('Введите название темы: ')
    path_to_save = input('Укажите путь: ')

    Matfiz(topic_name).download(path_to_save)
