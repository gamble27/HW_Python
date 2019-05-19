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
        response = bytes('{cl}:{msg}'.format(
            cl = current_thread.name, msg = data
        ),'utf-8')
        self.request.sendall(response)


# class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
#     pass


# def client(ip, port, message):
#     import socket
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.connect((ip, port))
#         sock.sendall(bytes(message, 'utf-8'))
#         resp = str(sock.recv(1024), 'utf-8')
#         if not resp: sock.close()
#         print('Received: {}'.format(resp))

if __name__ == "__main__":
    HOST, PORT = "localhost", 20001

    server = socketserver.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        ip, port = server.server_address

        # server_thread = threading.Thread(target=server.serve_forever)
        # server_thread.daemon = True
        # server_thread.start()
        server.serve_forever()
        # client(ip,port,'lorem ipsum')
        # client(ip,port,'dolor sit amet')
