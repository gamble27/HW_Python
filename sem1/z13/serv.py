# t25_01_v1 Сервер паліндромів
# Очікує передачі рядка та перевіряє, чи є він паліндромом

import socket
import sqlite3
import re

class Student:
    def __init__(self):
        name = None
        card_no = None
        birthday = None
        phone = None

#DB func

def collect_data(student):
    db = sqlite3.connect('students.db')
    crs = db.cursor()

    crs.execute("""INSERT INTO studs VALUES
                    ('{name}', '{id}',
                    '{birth}', '{tphone}')""".format(
        name=student.name, id=student.card_no,
        birth=student.birthday, tphone=student.phone
    ))
    db.commit()

    db.close()

#SERV func

def confirm(inp,p,stud):
    if p%5==1:
        #fio
        ok = set([chr(i) for i in range(ord('a'),ord('z')+1)])
        ok.add("'")
        ok.add('"')
        ok.add([chr(i) for i in range(ord('а'),ord('я')+1)])
        if all(list(map(lambda chr: chr in ok,
                        iter(inp.lower())))):
            stud.name = inp
            return True
        else:
            return False
    elif p%5==2:
        #studak
        ok = set(range(9))
        try:
            if not all(list(map(lambda chr: chr in ok,
                                iter(inp)))):
                raise ValueError
            stud.card_no = inp[len(inp)-8:]
            return True
        except:
            return False
        pass
    elif p%5==3:
        #bday
        ok = set(range(9))
        stud.birthday = '11-11-2011'
        pass
    elif p%5==4:
        #phone
        #cut for 066 666 66 66
        md = ''.join(inp.split())
        ok = set(range(9))
        try:
            if not all(list(map(lambda chr: chr in ok,
                                iter(md)))): raise ValueError
            stud.phone = md[len(md)-10:]
            return True
        except:
            return False
    else:
        collect_data(stud)
        return True

################___DATABASE___#######################

db = sqlite3.connect('students.db')
crs = db.cursor()
crs.execute("""CREATE TABLE IF NOT EXISTS studs 
                (name text, id_card text,
                 birth text, phone text)""")
db.commit()
db.close()

##################___DATA___#########################

stdnt = Student()

#################___SERVER___########################

HOST = ''                 # Комп'ютер для з'єднання
PORT = 20002              # Порт для з'єднання

# створити гніздо
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))        # зв'язати з комп'ютером та портом
s.listen(1)                 # очікувати на з'єднання
conn, addr = s.accept()     # отримати параметри з'єднання
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    print('ok')
    conn.sendall(bytes(True)+b'\n')
    p_data = conn.recv(1024)  # отримати дані (рядок байтів)
    print('ok2')
    if not data: break      # якщо рядок порожній, закінчити
    # перетворити рядок байтів у рядок символів
    info = str(data, encoding = 'utf-8')
    p = int(p_data[0])
    print(p)
    # перевірити на паліндром та відправити відповідь
    res = bytes(confirm(info,p,stdnt)) + b'\n'
#    print(res)
    conn.sendall(res)
conn.close()                # закрити з'єднання
