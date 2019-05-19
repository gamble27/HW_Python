#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from requests import get
import re

from common_parse_stuff import *


class SOUPPravdaParser:
    def __init__(self, parser='html.parser'):
        self.parser = parser
        self.authors = tuple()

        # f = open('new1.txt','w')
        url = "https://blogs.pravda.com.ua/"
        # page = urlopen("https://blogs.pravda.com.ua/")
        self.authors_page = get(url).text
        # for line in page:
        #     try:
        #         self.authors_page += str(line, encoding = 'utf-8')
        #         print(str(line, encoding = 'utf-8'), file=f)
        #     except:
        #         pass
        # print(self.authors_page)



        self.authors_soup = BeautifulSoup(self.authors_page, self.parser)

        self.authors = {}
        self._get_authors()

    def _get_authors(self):
        AUTHOR = r'[А-ЯЇ][а-яї]+ [А-ЯЇ][а-яї]+'
        for link in self.authors_soup.find_all('a'):
            try:
                if re.findall(AUTHOR, link.string):
                    self.authors[link.string] = link.get('href')
                    # print(link.string)
            except Exception as e:
                pass
                # print(e)
                # print(link.get('href'))

    def __call__(self, *args, **kwargs):
        return "BeautifulSoup"

    def get_author_columns(self, author, start_date, end_date):
        '''

        :param author: string author
        :param start_date: int (d,m,y)
        :param end_date: int (d,m,y)
        :return:
        '''
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
        columns = []
        if author not in self.authors:
            return ParserError('404 author not found')
        else:
            try:
                flag = False
                for page_no in range(1, 600):
                    url = 'https://blogs.pravda.com.ua' + self.authors[author] + 'page_{}/'.format(page_no)
                    page = get(url).text
                    soup = BeautifulSoup(page, self.parser)
                    hrefs = soup.find_all("a", {"class": "bpost0"})
                    for href in hrefs:
                        tag = href.findNext("span", {"class": "bdate"})

                        date = tag.string.split()
                        date_x = [ int(date[0]),
                                   months[date[1]],
                                   int(date[2][:-1]) ]

                        if date_belongs_to_interval(date_x, start_date, end_date):
                            columns.append(self.get_article_text(href.get('href')))
                        elif date_is_less_than_start(date_x,start_date):
                            flag = True
                            break
                    if flag: break
            except Exception as e: # stop iteration, page limit exceeded
                print(page_no-1)
                print(e)
        # print(hrefs[0])
        # return hrefs
        return columns

    def get_article_text(self, link):
        link1 = "https://blogs.pravda.com.ua" + link
        page = get(link1).text
        soup = BeautifulSoup(page, self.parser)
        # paragraph = soup.findall("p", {"data-io-article-url": link1})[0]
        # ToDo: find a bug and get text from the paragraph
        paragraph = soup.find("p")
        # res = paragraph.string
        res = ''
        child = paragraph.next
        rr = paragraph.nextSibling
        while child != rr:
            if child.string:
                res += child.string
            child = child.next
        return res

if __name__ == "__main__":
    print("BeautifulSoup Parser File")
