# t25_02_v1 Клієнт паліндром
# Відправляє на сервер рядок для перевірки, чи є він паліндромом

import socket

HOST = 'localhost'    # Комп'ютер для з'єднання з сервером
PORT = 20002          # Порт для з'єднання з сервером

# створити гніздо
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT)) # з'єднатися з сервером

i = 0
while True:
    to_send = input('?: ') # ввести рядок для перевірки
    if not to_send: break
    # перетворити у рядок байтів та передати серверу
    s.sendall(bytes(to_send, encoding='utf-8'))
#    print('sent')

s.close()                   # завершити з'єднання
