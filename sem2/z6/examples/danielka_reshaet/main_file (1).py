import xml.etree.ElementTree as ElementTree
import zlib

import matplotlib.pyplot as plt
import numpy as np

from collections import OrderedDict
from datetime import datetime
from math import ceil
from urllib.request import urlopen
from urllib.parse import urlencode

from matplotlib import colors as m_p_lib_colors
from matplotlib import pylab


COLORS = dict(m_p_lib_colors.BASE_COLORS, **m_p_lib_colors.CSS4_COLORS)

START_DEFAULT = 1960
FIN_DEFAULT = int(datetime.today().strftime('%Y')) - 1

WB = '{http://www.worldbank.org}'


class GetData:

    def __init__(self, info, pages=1):

        self.url = 'http://api.worldbank.org/countries/{code}/indicators/NY.GDP.MKTP.CD'

        self.info = info

        self.pages = pages

        self.data = {}

        self.name = None

        self._iterate()

    def _get_page(self, url_params):

        request = urlopen(url_params)

        if request.getheader("Content-Encoding"):

            data_zipped = request.read()

            data = zlib.decompress(data_zipped, zlib.MAX_WBITS | 16)  # magic :) <- клёвые шутки

        else:

            data = request.read()

        data = data.decode('utf-8')

        request.close()

        return data

    def _set_params(self, url, page):

        query = {'date': ':'.join(self.info[1:]), 'page': page}

        return url + '?' + urlencode(query, encoding='utf-8')

    def _iterate(self):

        for p in range(1, self.pages + 1):

            data = self._get_page(self._set_params(self.url.format(code=self.info[0]), p))

            response = ElementTree.fromstring(data)

            self.data.update(self._process_data(response))

    def _process_data(self, xml_thing):

        values = {}

        for data in xml_thing.findall(WB + 'data'):

            if self.name is None:

                self.name = data.find(WB + "country").text

            if data.find(WB + "value").text is None:

                values[data.find(WB + "date").text] = np.NaN

            else:

                values[data.find(WB + "date").text] = float(data.find(WB + "value").text)

        return values

    @property
    def get_data(self):

        return self.data

    @property
    def get_country_name(self):

        return self.name


class ClassGDPstats:

    def __init__(self, code, period):

        self.y_0, self.y_1 = period

        self._fix()

        self.x_array = np.arange(0, self.y_1 - self.y_0 + 1)

        self._data = {}

        if self.x_array.size <= 50:

            gt = GetData(list(map(str, [code, self.y_0, self.y_1])))

        else:

            gt = GetData(list(map(str, [code, self.y_0, self.y_1])),
                         pages=ceil(self.x_array.size / 50))

        self._data = OrderedDict(sorted(gt.get_data.items()))

        self._country_name = gt.get_country_name

        self.z_array = np.array(list(self._data.values()), dtype=float)

        self.y_array = np.array(list(self._data.keys()))

    def _fix(self):

        if self.y_0 > self.y_1:

            self.y_0, self.y_1 = self.y_1, self.y_0

        if all(y < START_DEFAULT for y in [self.y_0, self.y_1]):

            self.y_1 = self.y_0 = START_DEFAULT

        else:

            if self.y_0 < START_DEFAULT:

                self.y_0 = START_DEFAULT

        if all(y > FIN_DEFAULT for y in [self.y_0, self.y_1]):

            self.y_1, self.y_0 = FIN_DEFAULT, FIN_DEFAULT

        else:

            if self.y_1 > FIN_DEFAULT:

                self.y_1 = FIN_DEFAULT

    def plot(self):

        color = COLORS[list(COLORS.keys())[np.random.randint(0, len(COLORS))]]

        plt.plot(self.y_array, self.z_array, color, label=self._country_name)

        plt.scatter(self.y_array, self.z_array, color=color, s=10, marker='o')


def plot_operations(codenames_lst, years_tuple):

    plt.title('Графік обсягу валового внутрішнього продукту по роках',
              fontdict={'fontsize': 10},
              loc='right')

    plt.xlabel('Years')

    plt.ylabel('Values')

    plt.xticks(rotation=90)

    for j in range(len(codenames_lst)):

        ClassGDPstats(codenames_lst[j], years_tuple).plot()

    plt.grid()

    handles, labels = plt.gca().get_legend_handles_labels()

    by_label = OrderedDict(zip(labels, handles))

    plt.legend(by_label.values(), by_label.keys())

    fig = pylab.gcf()

    fig.canvas.set_window_title('Результат')

    mng = plt.get_current_fig_manager()

    mng.resize(*mng.window.maxsize())

    plt.show()


if __name__ == '__main__':

    codenames = []

    """Введите код страны: ua
Введите код страны: ru
Введите код страны: by
Введите код страны: pl
Введите код страны: jp
Начало периода: 1977
Конец периода: 2016
    """

    # TODO: Надо бы предложить Алисе встречаться

    # UA RU GB US FR JP CN CR HR DE LT LV FI IN IT IL LU MT MX ( лишний график может образоваться, если что ((: )

    for i in range(int(input('num = '))):

        codenames.append(input('Введите код страны: ')[:2].upper())

    while True:

        years = input('Начало периода: '), input('Конец периода: ')

        print(years)

        try:

            years = list(map(int, years))

        except ValueError:

            print('Некорректно введены данные!')

        else:

            break

    plot_operations(codenames, years)
