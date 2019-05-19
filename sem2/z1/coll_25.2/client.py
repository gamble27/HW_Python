import socket

HOST = 'localhost'
PORT = 20003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:

    path = input('Full path to the file?\n ')
    if not path: break
    with open (path) as f:
        to_send = f.read()

    s.sendall(bytes(to_send, encoding='utf-8'))
    # print('sent')

    f = True
    while f:
        inp = input('Path to the file on server(including name)?\n')
        # print(inp)
        s.sendall(bytes(inp, encoding='utf-8'))
        f = eval(str(s.recv(1024),encoding='utf-8'))  # 'False' -> False
        # print(f)

    print(str(s.recv(1024),encoding='utf-8'))

s.close()
