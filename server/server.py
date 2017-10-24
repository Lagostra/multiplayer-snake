import socket
from lobby import Lobby

class Server:

    running = False

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lobby = Lobby()

    def start(self):
        self.running = True
        self.socket.bind(('', self.port))
        self.socket.listen(5)
        self.run()

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            (client_socket, address) = self.socket.accept()
            self.lobby.add_client(client_socket)

if __name__ == '__main__':
    server = Server(47777)
    server.start()