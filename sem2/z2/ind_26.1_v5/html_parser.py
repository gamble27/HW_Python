#!/usr/bin/env python
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from requests import get

from common_parse_stuff import *


class ColumnsParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        self._months = {'січня'  : 1,
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

        self._columns_list = []

        self._start_date = None
        self._end_date = None

        self._too_early_flag = False

        self._in_date = False

        self._in_href = False
        self._current_href = ''

    def handle_starttag(self, tag, attrs):
        # if tag=="a" and ("href", "/authors/avakov/5c7adf0a80946/") in attrs:
        #     print("+")# ono ego ne vidit((

        if tag=="a" and ("class", "bpost0") in attrs:
            self._in_href = True
            self._current_href = attrs[0][1]
        elif (tag=="span" and self._in_href
              and ("class", "bdate") in attrs):
            self._in_date = True

    def handle_endtag(self, tag):
        if tag=="a" and self._in_href:
            self._in_href = False
        elif tag=="span" and self._in_date:
            self._in_date = False

    def handle_data(self, data):
        if self._in_date:
            buf = data.split()
            date = (int(buf[0]),
                    self._months[buf[1]],
                    int(buf[2][:-1]))
            if date_belongs_to_interval(date, self._start_date, self._end_date):
                self._columns_list.append(self._current_href)
            elif date_is_less_than_start(date, self._start_date):
                self._too_early_flag = True

    def get_columns(self, author_url, start_date, end_date):
        self._start_date = start_date
        self._end_date = end_date
        for page_no in range(1,600):
            page_url = author_url + 'page_{}'.format(page_no)
            self.feed(get(page_url).text)
            if self._too_early_flag:
                break
        return self._columns_list


class AuthorParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        self._author = ''

        self._is_authors_list = False
        self._in_href = False

        self._author_href = ''
        self._current_href = ''

    def handle_starttag(self, tag, attrs):
        if tag=="ul" and ("class", "authors") in attrs:
            self._is_authors_list = True
        elif tag=="a" and self._is_authors_list:
            self._in_href = True
            self._current_href = attrs[0][1]

    def handle_endtag(self, tag):
        if tag=="ul" and self._is_authors_list:
            self._is_authors_list = False
        elif tag=="a" and self._in_href:
            self._in_href = False

    def handle_data(self, data):
        if self._in_href and data==self._author:
            self._author_href = self._current_href


    def get_author_url(self, author):
        self._author = author
        self.feed(get('https://blogs.pravda.com.ua/').text)
        if self._author:
            return self._author_href
        else:
            return ParserError("Wrong author name")


class ArticleParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)

        self._article_url = ''
        self._article_text = ''

        self._in_article = False

    def handle_starttag(self, tag, attrs):
        if tag == "p":
            self._in_article = True

    def handle_endtag(self, tag):
        if tag == "p":
            self._in_article = False

    def handle_data(self, data):
        if self._in_article:
            self._article_text += data

    def get_article(self, article_url):
        self._article_url = article_url
        self.feed(get(article_url).text)
        return self._article_text


class HTMLPravdaParser():
    def __init__(self):
        self.author_parser = None
        self.columns_parser = None
        self.article_parser = None

        self.author_url = ''
        self._articles_links = []
        self.articles = []

    def get_author_columns(self, author, start_date, end_date):
        self.author_url = ("https://blogs.pravda.com.ua" +
            self.get_author_href(author))
        self._articles_links = self._get_articles_links(start_date, end_date)
        if not self.article_parser:
            self.article_parser = ArticleParser()
        for link in self._articles_links:
            self.articles.append(
                self.article_parser.get_article(
                    "https://blogs.pravda.com.ua" + link
                )
            )
        return self.articles


    def _get_articles_links(self, start_date, end_date):
        if not self.columns_parser:
            self.columns_parser = ColumnsParser()
        return self.columns_parser.get_columns(self.author_url, start_date, end_date)

    def get_page_text(self, url):
        return get(url).text

    def get_author_href(self, author):
        if not self.author_parser:
            self.author_parser = AuthorParser()
        return self.author_parser.get_author_url(author)

    def __call__(self, *args, **kwargs):
        return "HTMLParser"

if __name__ == "__main__":
    print("HTML Parser File")
    # prs = ColumnsParser()
    # print(prs.get_columns('https://blogs.pravda.com.ua/authors/avakov/',
    #                 (17, 1, 2019), (6, 3, 2019)))
