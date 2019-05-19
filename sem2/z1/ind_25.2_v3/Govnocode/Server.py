import socketserver
import socket

class ChatServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.ThreadingTCPServer.__init__(self,
                                                 RequestHandlerClass)
        clients = 0
        # clientd = {}

class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print("connected from:{}".format(self.client_address))

    def finish(self):
        pass

