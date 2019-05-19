from works.webscrapping.lookup_for_articles import *
from works.webscrapping.sentiment_analysis_of_articles import *

from works.matfiz_extreme.folder_with_examples.t17_11_benchmark_v3 import *

import time

# Скласти програму, яка аналізує статті (колонки) заданого автора за
# заданий період на сайті http://www.pravda.com.ua. Статті доступні за посиланням
# http://www.pravda.com.ua/columns/page_<xxx>/, де xxx – номер сторінки. Перевірити, чи
# мають ці статті позитивну чи негативну спрямованість. Про спрямованість статті
# свідчить використання слів: при позитивній спрямованості кількість позитивних слів
# суттєво перевищує кількість негативних. Використати словник, що складається з
# позитивних та негативних слів.

i = 1

links = {}

#TODO: Наладить обработку тэгов в sentiment_analysis_of_articles --> Наладил через text_wizard ((:
#TODO: Итерация в lookup_for_articles кривая

print('=== Аналізатор ===')


@benchmark
def text_wizard(i):
    global ac

    ac = ArticleClass(i)

    if len(ac.get_article) == 0:
        time.sleep(0.1)
        del ac
        return text_wizard(i)

while True:
    try:
        cc = ColumnsClass(i, 'Олег Петровець', '2018/10/1'.split('/'), '2018/12/19'.split('/'))
        if cc.get_hrefs != None:
            links.update(cc.get_hrefs)

        if not cc: print('* Пошук завершено *\n'); break
        else: print('* Оброблено сторінку #{} *'.format(i)); i += 1

    except HTTPError as e:
        print('* {}: Ліміт по кількості сторінок *\n'.format(e))
        break

time.sleep(1.25)

pp.pprint(links)

if len(links) > 0:
    analyzer = Analyzer()
    for link in links:
        print("=== Аналіз колонки за {}, автор: {} ===\n".format(links[link][-1], links[link][0]))

        text_wizard(link)

        print("\n* Результат: {} *\n".format(analyzer.sentiment_analysis(ac.get_article)))
        del ac
        time.sleep(0.75)

# Павло Казарін
# Георгій Зубко
# Василь Стоякін
# Ольга Ситник
# Сергій Тарута
# Олег Петровець
# Юрій Радзієвский
