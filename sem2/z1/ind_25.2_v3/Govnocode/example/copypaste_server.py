import socketserver
import socket
import sys
import select

class ChatServer(socket.socket):
    def __init__(self, host, port, max_clients=5):
        socket.socket.__init__(self, socket.AF_INET,
                               socket.SOCK_STREAM)
        self.setblocking(0)
        self.bind((host,port))
        self.listen(max_clients)

        self.running = True

    def run(self):
        # inputs =[self,sys.stdin]
        inputs = [self]
        readable, writeable, exceptional = select.select(
            inputs, [], []
        )
        while self.running:
            for s in readable:
                if s is self:
                    connection, client_addr = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)


class ThreadingChatServer(socketserver.ThreadingTCPServer):
    def __init__(self, address, RequestHandlerClass, max_clients=5):
        socketserver.ThreadingTCPServer.__init__(
            self, address, RequestHandlerClass
        )
        self.max_clients = max_clients
        self.clients = []
        self.running = False

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass


class Chatclient:
    pass
