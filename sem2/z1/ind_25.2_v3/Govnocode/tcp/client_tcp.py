import socket
import sys
import select

HOST, PORT = "localhost", 20002

class ChatClient:
    def __init__(self, name, host='localhost', port = 8800):
        self.name = name
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host,port))
            print('Connected to chat server {} on port {}'.format(host,port))
            self.connected = True
        except Exception as e:
            print("Failed to connect to {} port {}".format(host,port))
            print(e)
            self.connected = False

    def run(self):
        inputs = [self.sock,sys.stdin]
        while self.connected:
            try:
                readable,writable, erroneous = select.select(
                    inputs,[],[])
                for sock in readable:
                    if sock == sys.stdin:
                        data = sys.stdin.readline().strip()
                        if data: self.send(data)
                    elif sock == self.sock:
                        data = self.receive()
                        if not data:
                            # print("Client shutting down..")
                            # self.connected = False
                            # break
                            pass
                        else:
                            sys.stdout.write(data+'\n')
                            sys.stdout.flush()
                    else: pass
            except KeyboardInterrupt:
                print("Client interrupted")
                self.sock.close()
                self.connected = False
                break
            except Exception as e:
                print(e)
                self.connected = False
                break

    def send(self,msg):
        self.sock.send(bytes(msg,'utf-8'))

    def receive(self):
        data = self.sock.recv(1024)
        return str(data,encoding='utf-8')


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST,PORT))
# print('Connected to chat server {} on port {}'.format(HOST,PORT))
# while True:
#     readable, writable, erroneous = select.select([sock.])
#     sent = input('TO_SEND: \n')
#     if not sent: break
#
#     sock.sendall(bytes(sent + "\n", encoding='utf-8'))
#
#     received = str(sock.recv(1024),encoding='utf-8')
#
#     print('sent:{}'.format(sent))
#     print('received:{}'.format(received))
# sock.close()
#
if __name__ == '__main__':
    # client = ChatClient(input("Enter your nickname:\n"),HOST,PORT)
    client = ChatClient('f', HOST, PORT)
    client.run()
