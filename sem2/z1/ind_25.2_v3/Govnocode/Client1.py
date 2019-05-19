import socket

HOST, PORT = 'localhost', 22000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    client.send(bytes(input().strip(), encoding='utf-8'))
    print(str(client.recv(1024).strip(),encoding='utf-8'))
