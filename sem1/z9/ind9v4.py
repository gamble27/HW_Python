'''
Скласти програму з графічним інтерфейсом для розв’язання задачі.
Задана непорожня послідовність ненульових цілих чисел, за якою йде 0. Визначити
кількість змін знаку в цій послідовності. Наприклад, у послідовності 1, -34, 8,14, -5, 0
знак змінюється три рази.
Для введення елементів послідовності використати одне поле введення. Кнопка
«Обробити» повинна ініціювати обробку введеного елементу послідовності та
очищення поля введення.
Показати результат обчислень.
'''

# T23_01_v2
# Обчислення значення числа Фібоначчі. Графічний інтерфейс
# Введення номера числа у графічному режимі

from tkinter import *

def task(seq):
    res = 0
    for i in range(len(seq)-1):
        if seq[i]*seq[i+1] < 0:
            res += 1
        elif seq[i]*seq[i+1] > 0:
            continue
        else:
            return res

def calc():
    seq = list(map(int, (ein.get()).split()))
    f = task(seq)
    rezult = 'Result: {}'.format(f)  # побудова рядка для відображення
    lrez.configure(text=rezult)  # зміна надпису значенням результату


top = Tk()  # створення вікна

linput = Label(top,
               text='Gimme sequence: ',
               font=('arial', 16))  # створення надпису
linput.pack()  # додавання надпису до вікна
ein = Entry(top, font=('arial', 16))  # створення поля введення
ein.pack()  # додавання поля введення до вікна
lrez = Label(top, text='Result will appear here',
             font=('arial', 16))  # створення надпису
lrez.pack()  # додавання надпису до вікна
bcalc = Button(top, text='Get Results!',
               command=calc,
               font=('arial', 16))  # кнопка "Обчислити"
bcalc.pack()
bquit = Button(top, text='IQuit',
               command=top.quit,
               font=('arial', 16))  # кнопка "Закрити"
bquit.pack()

top.mainloop()