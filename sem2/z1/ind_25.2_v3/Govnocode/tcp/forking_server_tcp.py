import os
import socket
import threading
import socketserver

HOST = 'localhost'
PORT = 0
BUF_SIZE = 1024
ECHO = 'Hello echo server'

class ForkedClient():
    def __init__(self,ip,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((ip,port))

    def run(self):
        current_process_id = os.getpid()
        print('PID %s Sending message to the server: "%s"' %
              (current_process_id, ECHO))

        sent_data_len = self.sock.send(bytes(ECHO,'utf-8'))

        print("Sent: %d characters, so far.." % sent_data_len)

        response = self.sock.recv(BUF_SIZE)
        print('PID %s received: %s' %
              (current_process_id, response[5:]))

    def shutdown(self):
        self.sock.close()


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # received = str(sock.recv(1024))
        data = str(self.request.recv(BUF_SIZE),'utf-8')

        current_process_id =os.getpid()
        response = '{}:{}'.format(current_process_id, data)
        print("Server sending response {}".format(response))
        self.request.send(bytes(response,'utf-8'))
        return


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
        pass

def main():
    server = ForkingServer((HOST,PORT), ForkingServerRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.setDaemon(True)
    server_thread.start()
    print("Server loop running PID {}".format(os.getpid()))

    # client1 = ForkedClient(ip,port)
    # client1.run()

    # server.shutdown()
    # client1.shutdown()
    # server.socket.close()

if __name__ == "__main__":
    main()
