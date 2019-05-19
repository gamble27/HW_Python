import socket

HOST = 'localhost'
PORT = 30000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    to_send = input('?: ')
    if not to_send: break
    s.sendall(bytes(to_send, encoding='utf-8'))
    data = s.recv(1024)
    print(str(data, encoding='utf-8'))

s.close()
