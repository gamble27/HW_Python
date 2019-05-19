# T23_01_v2
# Обчислення значення числа Фібоначчі. Графічний інтерфейс
# Введення номера числа у графічному режимі

from tkinter import *

def difference(s1,s2):
    s1set = set(iter(s1))
    s2set = set(iter(s2))
    return ', '.join(s1set-s2set)


def calc():
    s1 = ein1.get()  # отримання значення поля введення
    s2 = ein2.get()
    f = difference(s1,s2)
    res = 'Result: {}'.format(f)  # побудова рядка для відображення
    lrez.configure(text=res)  # зміна надпису значенням результату


top = Tk()  # створення вікна

l1input = Label(top,
               text='String: ',
               font=('arial', 16))  # створення надпису
l1input.pack()  # додавання надпису до вікна
ein1 = Entry(top, font=('arial', 16))  # створення поля введення
ein1.pack()  # додавання поля введення до вікна


l2input = Label(top,
               text='Specimen: ',
               font=('arial', 16))  # створення надпису
l2input.pack()  # додавання надпису до вікна

ein2 = Entry(top, font=('arial', 16))  # створення поля введення
ein2.pack()  # додавання поля введення до вікна

lrez = Label(top,
             text='Result:   ',
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