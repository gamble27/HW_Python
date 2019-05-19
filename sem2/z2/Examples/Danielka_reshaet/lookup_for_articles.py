import datetime

import html.parser

from urllib.error import HTTPError

from works.urlparsing_guide.url_get import *

import pprint as pp

months = {'січня'    : 1,
          'лютого'   : 2,
          'березня'  : 3,
          'квітня'   : 4,
          'травня'   : 5,
          'червня'   : 6,
          'липня'    : 7,
          'серпня'   : 8,
          'вересня'  : 9,
          'жовтня'   : 10,
          'листопада': 11,
          'грудня'   : 12}


class HrefParser(html.parser.HTMLParser):

    def __init__(self, *args, **kwargs):

        html.parser.HTMLParser.__init__(self, *args, **kwargs)

        self._hrefs = {}

        self._flag = False

        self._flag_title = False

        self._flag_value = False

        self._flag_date = False

        self._current = ''

        self._cnt = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if ('class', 'columns_all') in attrs:
                self._flag = True

            if ('class', 'article__title') in attrs:
                self._flag_title = True

            if ('class', 'article__date') in attrs:
                self._flag_date = True

            if self._flag:
                self._cnt += 1

        if tag == 'a' and self._flag_title:
            for attr in attrs:
                if attr[0] == 'href':
                    self._current = attr[-1]
                    self._hrefs[self._current] = []
                    break

        if tag == 'span' and ('class', 'article__author') in attrs and self._flag_title:
            self._flag_value = True

    def handle_endtag(self, tag):
        if tag == 'div':
            if self._flag:
                if not self._cnt:
                    self._flag = False
                else:
                    self._cnt -= 1

        if tag == 'a' and self._flag_title:
            self._flag_title = False

    def handle_data(self, data):
        if self._flag_value:
            self._hrefs[self._current].append(data)
            self._flag_value = False

        if self._flag_date:
            self._hrefs[self._current].append(data)
            self._flag_date = False

    @property
    def get_hrefs(self):
        return self._hrefs


class ColumnsClass:

    def __init__(self, page, pattern, d1, d2):

        self._flag = True

        self.url = 'https://www.pravda.com.ua/columns/page_{}/'.format(page)

        self.data = None

        self.pattern = re.compile(pattern, re.I)

        self.start_date, self.end_date = datetime.date(int(d1[0]), int(d1[1]), int(d1[2])),\
                                         datetime.date(int(d2[0]), int(d2[1]), int(d2[2]))

        if self.start_date > self.end_date: self.start_date, self.end_date = self.end_date, self.start_date

        try:
            http_file = urlopen(self.url)
            enc = getencoding(http_file)
            data = str(http_file.read(), encoding=enc, errors='ignore')

            hrefs = HrefParser()
            hrefs.feed(data)
            self.data = hrefs.get_hrefs
            self._clear_from_mess()

        except HTTPError as e:
            print(e)
            sys.exit()

    def _clear_from_mess(self):
        # Даниэль ведь криворукий, не может разобраться с парсером
        lst = []

        #TODO: Перенести шаблон на пару строчек ниже
        #TODO: Проверку на совместимость с периодом поставить сюда

        self.data = {'https://www.pravda.com.ua' + href:
                    [val[0], val[1].split(',')[0]] for href, val in self.data.items()\
                    if href.startswith('/columns') and re.findall(self.pattern, val[0])}

        for val in self.data.values():
             if self.start_date < datetime.date(int(val[-1].split()[-1]),
                              int(months[val[-1].split()[1]]),
                              int(val[-1].split()[0])) < self.end_date:
                 lst.append(val)

             if datetime.date(int(val[-1].split()[-1]),
                              int(months[val[-1].split()[1]]),
                              int(val[-1].split()[0])) < self.start_date:
                self._flag = False
                if __name__ == '__main__':
                    print('=== Break point ===')
                break

        self.data = {href: val for href, val in self.data.items() if val in lst}

    @property
    def get_hrefs(self):
        if len(self.data) != 0:
            return self.data

    def __bool__(self):
        return self._flag


if __name__ == '__main__':
    cc = ColumnsClass(int(input('Номер страницы: ')), 'Валентин Ткач', '2018/12/12'.split('/'), '2019/01/19'.split('/'))
    pp.pprint(cc.get_hrefs)
    print('Bool\n')
    pp.pprint(cc.__bool__())
