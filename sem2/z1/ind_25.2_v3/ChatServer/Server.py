# import socketserver
import socket
import sys
import select

HOST, PORT = 'localhost', 22012

class ChatServer(socket.socket):
    def __init__(self, address, backlog=5):
        socket.socket.__init__(self,socket.AF_INET, socket.SOCK_STREAM)
        # self.server.setsockopt(socket.SOL_SOCKET,
        #                        socket.SO_REUSEADDR, 1)
        self.bind(address)

        self.clients = {}
        self.listen(backlog)

        self.running = True

    def run(self):
        inputs = [self, sys.stdin]
        while self.running:
            readable, writeable, exceptional = select.select(
                inputs, self.clients, []
            )
            for sock in readable:
                if sock == self:
                    client, address = self.accept()
                    print('Connected from {},{}'.format(client.fileno(), address))
                    inputs.append(client)
                    self.clients[client] = address
                elif sock == sys.stdin:
                    pass
                else:
                    data = str(sock.recv(1024).strip(), encoding='utf-8')
                    if data:
                        to_send = str(sock.getsockname()[1]) + ':' + data
                        for output in self.clients:
                            if output == sock: continue
                            output.sendall(bytes(to_send,encoding='utf-8'))
        self.close()

#
# class ChatTCPServer(socketserver.ThreadingTCPServer):
#     def __init__(self, address, RequestHandlerClass):
#         socketserver.ThreadingTCPServer.__init__(self, address, RequestHandlerClass)
#
#         self.clients = []
#         self.requests = []
#
#     def process_request_thread(self, request, client_address):
#         """Same as in BaseServer but as a thread.
#
#         In addition, exception handling is done here.
#
#         """
#         try:
#             self.finish_request(request, client_address)
#         except Exception:
#             self.handle_error(request, client_address)
#
#
# class RequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         if self.client_address not in self.server.clients:
#             self.server.clients.append(self.client_address)
#             self.server.requests.append(self.request)
#             print('Connected by {}'.format(self.client_address))
#         msg = str(self.request.recv(1024).strip(),encoding='utf-8')
#         print(self.client_address, ':', msg)
#         to_send = str(self.client_address[1]) + ':' + msg
#         # for client_address in self.server.clients:
#         #     if client_address == self.client_address: continue
#         #     self.request.sendto(bytes(to_send,encoding='utf-8'), client_address)
#         # print(*self.server.requests)
#         for client in self.server.requests:
#             if client == self.request: continue
#             client.sendall(bytes(to_send, encoding='utf-8'))


if __name__ == '__main__':
    # tcp = ChatTCPServer((HOST, PORT), RequestHandler)
    # tcp.serve_forever()
    cht = ChatServer((HOST, PORT))
    cht.run()
