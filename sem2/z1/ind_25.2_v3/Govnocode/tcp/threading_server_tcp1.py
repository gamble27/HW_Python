import socketserver
import threading
# import socket

"""
BaseRequestHandler
    self.request
                .sendall()
                .recv(bytes_no)
"""

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request.accept()
        print("Connected from: {}".format(self.client_address))
        data = str(self.request.recv(1024), 'utf-8')
        # if not data: pass
        print(data)
        current_thread = threading.current_thread()
        if current_thread.name not in self.server.clients:
            self.server.clients[current_thread.name] = self.request
        response = bytes('{cl}:{msg}'.format(
            cl = current_thread.name, msg = data
        ),'utf-8')
        print(self.server.clients.keys())
        for name in self.server.clients:
            if name == current_thread.name: continue
            self.server.clients[name].sendall(response)  #  ,self.server.clients[name])
            # self.server.clients[name].sendall(response)

    # def finish(self):


class ChatServer(socketserver.ThreadingTCPServer):
    def __init__(self,server_address, RequestHasndlerClass):
        socketserver.ThreadingTCPServer.__init__(
            self, server_address, RequestHasndlerClass
        )
        self.clients = {}  # name: addr
        print("===== Chat Server =====")


# def client(ip, port, message):
#     import socket
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.connect((ip, port))
#         sock.sendall(bytes(message, 'utf-8'))
#         resp = str(sock.recv(1024), 'utf-8')
#         if not resp: sock.close()
#         print('Received: {}'.format(resp))

if __name__ == "__main__":
    HOST, PORT = "localhost", 20002

    server = ChatServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.serve_forever()
