import socket


HOST = ''
PORT = 20003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)


while True:
    data = conn.recv(1024)
    if not data: break
    text = str(data, encoding = 'utf-8')

    f = True
    while f:
        data = conn.recv(1024)
        # print(str(data,encoding='utf-8'))
        f = not bool(str(data,encoding='utf-8'))
        # print(f)
        conn.sendall(bytes(str(f),encoding='utf-8'))

    try:
        f = open(str(data, encoding = 'utf-8'), 'w')
        f.write(text)
        f.close()
    except Exception as e:
        print(e)

    conn.sendall(bytes('Success',encoding='utf-8'))

conn.close()
