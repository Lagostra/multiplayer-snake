import socket
import threading

from server.lobby import Lobby
from common.socketwrapper import SocketWrapper


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
        threading.Thread(target=lambda: self.run()).start()
        self.user_input()

    def stop(self):
        print('Stopping server...')
        self.running = False
        self.socket.close()
        self.lobby.stop()

    def run(self):
        while self.running:
            try:
                (client_socket, address) = self.socket.accept()
            except OSError:
                continue
            client_socket = SocketWrapper(client_socket)
            self.lobby.add_client(client_socket)
            client_socket.start_listening()

    def user_input(self):
        while self.running:
            args = input('>> ').split()
            cmd = args[0]

            if cmd in ['close', 'exit', 'stop']:
                self.stop()
                return
            elif cmd == 'users':
                print(','.join(map(lambda x: x.username, self.lobby.users)))
            elif cmd == 'games':
                print(','.join(map(lambda x: str(x.id) + ':' + x.name, self.lobby.games)))
            elif cmd == 'game':
                try:
                    game = self.lobby.get_game(int(args[1]))
                    print('ID: ' + str(game.id) + ', Name: ' + game.name + ', Players: ' + str(len(game.players)))
                except ValueError:
                    print('Invalid format')
