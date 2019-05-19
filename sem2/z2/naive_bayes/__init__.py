'''
naive bayes good/bad word classificator

uses neutral naive bayes classificator

last word in each dataset file
must be true or false,
introducing article status -
True for bad one
False in other one
'''

import re
import json
from os import listdir
import os.path as pth

class DatasetError(Exception):
    pass

class Classificator:
    def __init__(self, json_file):
        self._json = json_file
        # if pth.exists(json_file):
        #     self._word_counters = json.loads(json_file, encoding='utf-8')
        # else:
        #     self._word_counters = {}
        self._word_counters = {}
        self._bad_ones = 0
        self._good_ones = 0

    def __str__(self):
        return self._json

    def teach_classificator(self, dataset):
        for textfile in dataset:
            words = self._get_words(textfile)  # got a wordlist
            try:
                bad = eval(words[-1].capitalize())  # figured out whether the article is 'bad'
                self._bad_ones += int(bad)
            except Exception as e:
                #handle eval errrors, it's feckin' important
                print('something went wrong with {}'.format(textfile))
                print('please verify if True(False) is the last word in the text')
                # continue
                # raise DatasetError
                exit(0)
            for word in words:
                if word in self._word_counters:
                    self._word_counters[word][bad] += 1 # increases number of good ar bad articles where this word appears
                else:
                    self._word_counters[word] = {}
                    self._word_counters[word][bad] = 1
                    self._word_counters[word][not bad] = 0

        self._good_ones += len(dataset) - self._bad_ones

        # self._save_json()

    def _save_json(self):
        f = open(self._json, 'w')
        json.dump(self._word_counters, f, encoding='utf-8')

    def _conditional_frequency(self,word,bad = True):
        #calculates conditional frequency of the word in [bad=True] messages
        # if word not in self.word_counters: raise DatasetError('word not found')
        return (self._word_counters[word][bad]/
                (self._bad_ones if bad else self._good_ones))

    def _prob_word(self,word):
        if word not in self._word_counters: return 0.5  # raise DatasetError('word not found')
        bad_cond = self._conditional_frequency(word)
        good_cond = self._conditional_frequency(word, bad=False)
        if bad_cond == 0:
            print('yell')
            return 0.01
        elif good_cond == 0:
            print('eejit')
            return 0.99
        else:
            return bad_cond / (bad_cond + good_cond)

    def _get_words(self, textfile):
        #тупо парсит слова из текстового файла, lowercase included
        WORD = r'[a-zа-яьюяїієґ]+'
        with open(textfile, 'r') as f:
            s = f.read()
            s = s.lower()
        return re.findall(WORD,s)

    def check_article(self, article):
        # article should be text file
        # calculate badness of article in %
        words = self._get_words(article)
        probs = [self._prob_word(word) for word in words]
        prob_bad = 1
        prob_good = 1
        for prob in probs:
            # if prob == 0: print ('yell')
            # if prob == 1: print ('eejit')
            prob_bad *= prob
            prob_good *= 1-prob
        # print(prob_bad, prob_good)
        return prob_bad/(prob_good+prob_bad)

if __name__ == '__main__':
    analyzer = Classificator('/home/olga/PyCharm/domashki/sem2/z2/naive_bayes/words1.json')

    DATA_DIR = '/home/olga/PyCharm/domashki/sem2/z2/naive_bayes/Dataset'

    data = listdir(DATA_DIR)
    data = [DATA_DIR+'/'+i for i in data]
    analyzer.teach_classificator(data)

    print(analyzer.check_article('/home/olga/PyCharm/domashki/sem2/z2/naive_bayes/article1.txt'))
