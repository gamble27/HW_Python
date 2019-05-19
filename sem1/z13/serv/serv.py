# t25_01_v1 Сервер паліндромів
# Очікує передачі рядка та перевіряє, чи є він паліндромом

import socket
import sqlite3

class Student():
    def __init__(self):
        self.name = None
        self.card_no = None
        self.birth = None
        self.phone = None

db = sqlite3.connect('students.db')
cs = db.cursor()
cs.execute("""CREATE TABLE IF NOT EXISTS studs
            (name text, id text, birthday text, phone text)""")
db.commit()


def add_stud(std):
    cs.execute("""INSERT INTO studs VALUES
                ('{name}', '{id}', '{bday}', '{phone}')""".format(
        name = std.name, id = std.card_no,
        bday = std.birth, phone = std.phone
    ))


HOST = ''                 # Комп'ютер для з'єднання
PORT = 20002              # Порт для з'єднання

# створити гніздо
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))        # зв'язати з комп'ютером та портом
s.listen(1)                 # очікувати на з'єднання
conn, addr = s.accept()     # отримати параметри з'єднання
print('Connected by', addr)

i = 0
std = Student()

while True:
    data = conn.recv(1024)  # отримати дані (рядок байтів)
    if not data: break      # якщо рядок порожній, закінчити
    # перетворити рядок байтів у рядок символів
    info = str(data, encoding = 'utf-8')
    if i%4==0:
        std.name = info
    elif i%4==1:
        std.card_no = info
    elif i%4==2:
        std.birth = info
    else:
        std.phone = info
        add_stud(std)
        std = Student()
#    print(pal)
    # перевірити на паліндром та відправити відповідь
    #res = bytes(add_stud(info,i%4)) + b'\n'
#    print(res)
    i += 1
    conn.sendall(True)
conn.close()                # закрити з'єднання
db.close()
