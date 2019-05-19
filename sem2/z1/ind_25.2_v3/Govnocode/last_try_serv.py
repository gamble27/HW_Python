import select
import socket
import sys
import signal
import pickle
import struct
import argparse

HOST = 'localhost'
SERV_NAME = '== chat server =='

#Some utilities
def send(channel, *args):
    buffer = pickle.dumps(*args)
    # print(args)
    # print('args')
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    # channel.send(buffer)
    channel.send(bytes(args[0],'utf-8'))
def receive (channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''
    buf = ""
    while len(buf)<size:
        buf = channel.recv(size-len(buf))
    return pickle.loads(buf)[0]

class ChatServer(object):
    def __init__(self, port, backlog = 5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list of output sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,
                               socket.SO_REUSEADDR, 1)
        self.server.bind((HOST,port))
        print('Server listening to port {}'.format(port))
        self.server.listen(backlog)
        #Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self,signum,frame):
        print("Shutting down the server..")
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, []
                )
            except select.error as e:
                break

            for sock in readable:
                if sock == self.server:
                    #  handle the server socket
                    client, address = self.server.accept()
                    print("got connection {} from {}".format(
                        client.fileno(), address))
                    # Read the login name
                    cname = receive(client).split('NAME: ')[0]
                    # Compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: '+str(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address,cname)
                    # Send joining info to other clients
                    msg = "\n (Connected: new client {} from {})".format(
                        self.clients, self.get_client_name(client)
                    )
                    for output in self.outputs:
                        send(output,msg)
                    self.outputs.append(client)
                elif sock == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = False
                else:
                    #handle all other socks
                    try:
                        data = receive(sock)
                        if data:
                            # Send client's message
                            msg = '\n#[' + self.get_client_name(sock) + ']>>' + data
                            for output in self.outputs:
                                if output != sock:send(output, msg)
                        else:
                            print(data, ' data')
                            print("Chat server {} hung up".format(sock.fileno()))
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            msg = "\n (Now hang up: Client from {})".format(
                                self.get_client_name(sock)
                            )
                            for output in self.outputs:
                                send(output,msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
        self.server.close()


class ChatClient(object):
    def __init__(self, name, port, host=HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        # Initial prompt
        self.prompt = '[' + '@'.join((name,socket.gethostname().split('.')[0])) + ']>'
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, self.port))
            # Send name
            nom = 'NAME: ' + self.name
            send(self.sock,nom)
            print(nom)
            data = receive(self.sock)
            print('received sth')
            # Contains client address, set it
            addr = data.split('CLIENT: ')[0]
            self.prompt = '[' + '@'.join((self.name,addr)) + ']>'
        except socket.error as e:
            print("Failed to connect to the srv from {} port".format(self.port))
            sys.exit(1)

    def run(self):
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # Wait for input from stdin and socket
                readable, writeable, exceptional = select.select(
                    [0,self.sock],[],[]
                )
                for sock in readable:
                    if sock == sys.stdin:
                        data = sys.stdin.readline().strip()
                        if data: send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print("Client sutting down..")
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data+'\n')
                            sys.stdout.flush()
            except KeyboardInterrupt:
                print("Client interrupted")
                self.sock.close()
                break


if __name__ == "__main__":
    serv = ChatServer(9998)
    serv.run()
