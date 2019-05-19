import html.parser

import os

from urllib.error import HTTPError

import pandas as pd

from works.urlparsing_guide.url_get import *

class SentimentVocabulary:

    def __init__(self):

        self.__dataframe = pd.read_csv(os.path.join(os.getcwd(), 'tone-dict-uk.tsv'),
                                       sep='\t', na_filter=False)
        self.__fix()

    def __fix(self):

        self.__dataframe = self.__dataframe.loc[:, ~self.__dataframe.columns.str.contains('^Unnamed')]

    @property
    def get_dataframe(self):

        return self.__dataframe

if __name__ == '__main__':
    v = SentimentVocabulary(); print(v.get_dataframe); del v

class ArticleParsing(html.parser.HTMLParser):

    def __init__(self, *args, **kwargs):

        html.parser.HTMLParser.__init__(self, *args, **kwargs)

        self.in_article = False

        self.readable = False

        self.data = ""

        self.cnt = 0

    def handle_starttag(self, tag, attrs):

        if tag == 'div' and ("class", "post_news__text") in attrs:
            self.in_article = True

        if self.in_article and tag == 'p':
            self.readable = True

        if self.in_article and tag == 'div' and attrs:
            self.cnt += 1

    def handle_endtag(self, tag):
        if self.in_article and tag == 'div' and not self.cnt:
            self.in_article = False

        elif self.in_article and tag == 'div' and self.cnt:
            self.cnt -= 1

    def handle_data(self, data):
        if self.in_article and self.readable:
            self.data += data
            self.readable = False

    @property
    def get_article(self):

        return self.data


class ArticleClass:

    def __init__(self, url):

        self.url = url

        self.data = ''

        try:
            http_file = urlopen(self.url)
            enc = getencoding(http_file)

            data = str(http_file.read(), encoding=enc, errors='ignore')

            ap = ArticleParsing()
            ap.feed(data)
            self.data = ap.get_article

        except HTTPError as e:
            print(e)
            sys.exit()

    def __str__(self):
        return self.data

    @property
    def get_article(self):

        return self.data


class Analyzer:

    def __init__(self):

        self.__dataframe = self.__get_dataframe()

        self.pattern_positive, self.pattern_negative = self.__initialize_patterns()

    def __get_dataframe(self):

        return SentimentVocabulary().get_dataframe

    def __initialize_patterns(self):

        df_pos = self.__dataframe.loc[self.__dataframe['POINTS'] == 1]["WORD"]
        df_neg = self.__dataframe.loc[self.__dataframe['POINTS'] == -1]["WORD"]

        str_l = ['', '']

        for i, word in enumerate(df_pos):
            if i < len(df_pos):
                str_l[0] += word + '|'
            else:
                str_l[0] += word

        for i, word in enumerate(df_neg):
            if i < len(df_neg):
                str_l[-1] += word + '|'
            else:
                str_l[-1] += word

        return (re.compile(str_l[0], re.I), re.compile(str_l[-1], re.I))

    def sentiment_analysis(self, text):
        if text == '':
            print("=== WARN: Помилка під час обробки тексту через методи класу ArticleClass ===")

        if [x for x in re.findall(self.pattern_positive, text) if len(x) > 0]\
                < [x for x in re.findall(self.pattern_negative, text) if len(x) > 0]:
            return 'Негативна спрямованість'
        elif [x for x in re.findall(self.pattern_positive, text) if len(x) > 0]\
                > [x for x in re.findall(self.pattern_negative, text) if len(x) > 0]:
            return 'Позитивна спрямованість'
        else:
            return 'Нейтральна спрямованість'
