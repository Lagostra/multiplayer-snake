import socket

import preferences
from lobby import Lobby
from socketwrapper import SocketWrapper

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
            client_socket = SocketWrapper(client_socket)
            self.lobby.add_client(client_socket)
            client_socket.start_listening()

if __name__ == '__main__':
    preferences.load()
    preferences.save()

    server = Server(47777)
    server.start()