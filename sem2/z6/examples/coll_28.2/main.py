from urllib.request import urlopen
import zlib

from urllib.parse import urlencode
from xml.etree.ElementTree import fromstring

from abc import ABCMeta, abstractmethod

# import numpy as np
# import matplotlib.pyplot as plt


COUNTRIES_URL = "http://api.worldbank.org/countries"
WB = "{http://www.worldbank.org}"

class PageReader(ABCMeta):

    @abstractmethod
    def read_single_page(self, url_params):
        request = urlopen(url_params)
        if request.getheader("Content-Encoding"):
            data_zipped = request.read()
            data = zlib.decompress(data_zipped, zlib.MAX_WBITS | 16)  # magic :) P.S. ну офигеть теперь
        else:
            data = request.read()
        data = data.decode('utf-8')
        request.close()
        return data

    @abstractmethod
    def read_multiple_page(self, url, page_process_func, **params):
        """Функція читає багатосторінковий документ з url з параметрами params.

        page_proc_func - функція, яка обробляє одну сторінку xml.
        Кожна сторінка документу повинна мати заголовок - елемент XML -
        та список елементів-значень.
        Заголовок, зокрема, повинен містити атрибут - кількість сторінок ("pages").
        """
        if params:
            query = urlencode(params, encoding='utf-8')
            url_params = url + '?' + query
        else:
            params = {}
            url_params = url
        data = self.read_single_page(url_params)
        response = fromstring(data)
        page_process_func(response)
        page_num = int(response.get("pages"))
        print('url {} page {} of {}'.format(url, 1, page_num))
        for page in range(2, page_num + 1):
            params["page"] = str(page)
            query = urlencode(params, encoding='utf-8')
            url_params = url + '?' + query
            data = self.read_single_page(url_params)
            response = fromstring(data)
            page_process_func(response)
            print('url {} page {} of {}'.format(url, page, page_num))


class GDPParser:

    def __init__(self):
        self.countries = {}

    def get_gdp_list(self, country, period):
        """

        :param country: string country
        :param period: (start_year, end_year)
        :return: list of gdp values per year
        """
        pass

    def process_countries_page(self, response):
        page_countries = {}
        for country in response.findall(WB + 'country'):
            key = country.find(WB + "iso2Code").text
            c_name = country.find(WB + "name").text
            region = country.find(WB + "region").text
            if region != "Aggregates":
                page_countries[key] = [c_name, 0, 0]
        self.countries.update(page_countries)


if __name__ == "__main__":
    prs = GDPParser()
