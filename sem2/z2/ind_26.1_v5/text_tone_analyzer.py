#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class ToneAnalyzer:
    def __init__(self, tone_dictionary="/home/olga/Projects/domashki/sem2/z2/ind_26.1_v5/word_tones/tone-dict-uk.tsv"):
        self.words = {}
        with open(tone_dictionary) as dct:
            flag = True
            while flag:
                try:
                    key, arg = dct.readline().strip().split()
                    self.words[key] = int(arg)
                except Exception as e:
                    flag = False

    def get_author_tone(self, articles):
        if len(articles) == 0: return 0

        author_tone = 0
        for article in articles:
            author_tone += self.get_text_tone(article)
        author_tone /= len(articles)
        return author_tone

    def get_text_tone(self, text):
        text_words = re.split(r'[,.:\- \'\"]', text)
        text_tone = 0
        for word in text_words:
            text_tone += self.get_word_tone(word)
        text_tone /= len(text_words)
        return text_tone

    def get_word_tone(self, word):
        return self.words[word] if word in self.words else 0


if __name__ == "__main__":
    pass
    # authors = parser.get_authors()
    # with open('authors.txt', 'w') as f:
    #     print(*parser.authors, file=f, sep='\n')

    # parser = SOUPPravdaParser()
    # f = parser.get_author_columns('Дзюнсей Терасава', (1,1,2018), (1,1,2019))
    # an = ToneAnalyzer()

    # print(an.get_text_tone(f[0]))
    # print(*f, sep='\n')
