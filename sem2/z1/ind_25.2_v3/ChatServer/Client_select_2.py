import socket
import sys
import select

HOST, PORT = 'localhost', 22012

class ChatClient:
    def __init__(self, address):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)

        self.connected = True

    def run(self):
        while self.connected:
            readable, writeable, exceptional = select.select(
                [sys.stdin, self.sock], [], []
            )
            for sock in readable:
                if sock == sys.stdin:
                    data = sys.stdin.readline().strip()
                    if data:self.send(data)
                elif sock == self.sock:
                    data = str(self.sock.recv(1024).strip(),encoding='utf-8')
                    if data: sys.stdout.write(data+'\n')

    def send(self, data):
        self.sock.send(bytes(data, encoding='utf-8'))


if __name__ == '__main__':
    client = ChatClient((HOST, PORT))
    client.run()
