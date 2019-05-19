# t25_02_v1 Клієнт паліндром
# Відправляє на сервер рядок для перевірки, чи є він паліндромом

import socket

HOST = 'localhost'    # Комп'ютер для з'єднання з сервером
PORT = 20002          # Порт для з'єднання з сервером

# створити гніздо
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT)) # з'єднатися з сервером
while True:
    confirmation = False
    while not confirmation:
        to_send = input('ФИО: ') # ввести рядок для перевірки
        if not to_send: break
        # перетворити у рядок байтів та передати серверу
        s.sendall(bytes(to_send, encoding='utf-8'))
        confirmation = s.recv(1024)
        s.sendall(bytes('1',encoding='utf-8'))
#       print('sent')
        confirmation = s.recv(1024)     # отримати відповідь сервера
#       print('received')
        if not confirmation: print(to_send,'Криво, переделывай')

    confirmation = False

    while not confirmation:
        to_send = input('Студак: ') # ввести рядок для перевірки
        if not to_send: break
        # перетворити у рядок байтів та передати серверу
        s.sendall(bytes(to_send, encoding='utf-8'))
        confirmation = s.recv(1024)
        s.sendall(bytes('2',encoding='utf-8'))
#       print('sent')
        confirmation = s.recv(1024)     # отримати відповідь сервера
#       print('received')
        if not confirmation: print(to_send,'Думаешь, я не знаю, какой у студака формат?')

    confirmation = False

    while not confirmation:
        to_send = input('Дата рождения: ') # ввести рядок для перевірки
        if not to_send: break
        # перетворити у рядок байтів та передати серверу
        s.sendall(bytes(to_send, encoding='utf-8'))
        confirmation = s.recv(1024)
        s.sendall(bytes('3',encoding='utf-8'))
#       print('sent')
        confirmation = s.recv(1024)     # отримати відповідь сервера
#       print('received')
        if not confirmation: print(to_send,'Формат даты: дд(д).мм(м).гггг \n',
                                   'мм(м)/гггг/дд(д) \n',
                                   'гггг-мм(м)-дд(д)\n')

    confirmation = False

    while not confirmation:
        to_send = input('Телефон: ') # ввести рядок для перевірки
        if not to_send: break
        # перетворити у рядок байтів та передати серверу
        s.sendall(bytes(to_send, encoding='utf-8'))
        confirmation = s.recv(1024)
        s.sendall(bytes('4',encoding='utf-8'))
#       print('sent')
        confirmation = s.recv(1024)     # отримати відповідь сервера
#       print('received')
        if not confirmation: print(to_send,'Да ладно!?')

    s.sendall(bytes('lorem ipsum',encoding='utf-8'))
    s.sendall(bytes('5',encoding='utf-8'))
    confirmation = s.recv(1024)
    if confirmation: print(to_send,'Деканат выражает признательность за сотрудничество')


s.close()                   # завершити з'єднання
