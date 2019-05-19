# t25_01_v1 Сервер паліндромів
# Очікує передачі рядка та перевіряє, чи є він паліндромом

import socket


HOST = ''                 # Комп'ютер для з'єднання
PORT = 20003             # Порт для з'єднання

# створити гніздо
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))        # зв'язати з комп'ютером та портом
s.listen(1)                 # очікувати на з'єднання
conn, addr = s.accept()     # отримати параметри з'єднання
print('Connected by', addr)


while True:
    data = conn.recv(1024)  # отримати дані (рядок байтів)
    if not data: break      # якщо рядок порожній, закінчити
    # перетворити рядок байтів у рядок символів
    print(str(data, encoding = 'utf-8'))

    # перевірити на паліндром та відправити відповідь
    #res = bytes(add_stud(info,i%4)) + b'\n'
#    print(res)
    conn.sendall(bytes(input('?: '),encoding='utf-8'))
conn.close()                # закрити з'єднання
