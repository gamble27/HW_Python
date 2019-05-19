import sqlite3 as s3

from datetime import datetime as dt


"""
T29.1 Скласти програму для роботи з базою даних, що містить дати народження
знайомих. Програма повинна реалізовувати функції додавання знайомого, показу
дати народження за прізвищем. При запуску програма повинна показувати дати
народження знайомих, для яких до дня народження залишилось не більше 7 днів.
"""


class BirthDaysDataBase:

    def __init__(self, database_file):

        self.filename = database_file

    def _set_cursor_and_connect(self):

        conn = s3.connect(self.filename)

        curs = conn.cursor()

        return conn, curs

    def _close(self, conn):

        conn.commit()

        conn.close()

    def _append_info(self, curs):

        while True:

            p_name = input("Введите имя:\n")

            try:

                p_dates = dt.strptime(input("Введите дату рождения человека {}:\n".format(p_name)),
                                     '%d-%m-%Y').strftime('%d-%m-%Y')

                print(p_dates)

                print(''.join(p_dates.split(':')[:2][::-1]))

            except ValueError:

                print("Некоррекнтные данные в поле введения даты рождения!")

            else:

                break

        curs.execute("INSERT INTO people VALUES (?, ?, ?)", (p_name, p_dates, ''.join(p_dates.split(':')[:2][::-1])))  # ахахах

    def form_database(self):

        conn, curs = self._set_cursor_and_connect()

        curs.execute("""CREATE TABLE IF NOT EXISTS people
                     (name text, dates text, birthday text)""")

        while True:

            try:

                number = int(input("Количество записей в базе данных:\n"))

            except ValueError:

                print("Некорректное значение!")

            else:

                break

        for j in range(number):

            self._append_info(curs)

        self._close(conn)

    def append_to_database(self):

        conn, curs = self._set_cursor_and_connect()

        self._append_info(curs)

        self._close(conn)

    def show_info(self, p_name):

        conn, curs = self._set_cursor_and_connect()

        curs.execute("SELECT dates FROM people WHERE name=? ", (p_name, ))

        result = curs.fetchone()

        if result:

            res = result[0]

        else:

            res = ""

        conn.close()

        return res

    def show_recent(self):

        conn, curs = self._set_cursor_and_connect()

        #curs.execute("SELECT  dates('now');")

        curs.execute("SELECT dates FROM people")

        result = curs.fetchall()

        print(result)


if __name__ == '__main__':

    filename = 'datess.db'

    database = BirthDaysDataBase(filename)

    while True:

        try:
            k = int(input('|| Выберите режим работы [1-5] (0 - информация о режимах) ||\n'
                          '>>\t')[0])

        except ValueError:

            k = -1

        if not k:

            print('>> Руководство:\n'
                  '[1] - Создать базу данных из заданного количества записей;\n'
                  '[2] - Внести информацию о человеке;\n'
                  '[3] - Вывести дату рождения запрашиваемого человека;\n'
                  '[4] - Вывести список ближайших дней рождения;\n'
                  '[5] - Выход из программы;\n')

        elif k == 1:

            database.form_database()

        elif k == 2:

            database.append_to_database()

        elif k == 3:

            name = input('>> Имя: ')

            dates = database.show_info(name)

            if len(dates) > 0:

                print('>> Дата рождения: ', dates)

            else:

                print('>> Данных нет'.format(name))

        elif k == 4:

            database.show_recent()

        elif k == 5:

            exit(0)

        else:

            print(">> Код не распознан")
