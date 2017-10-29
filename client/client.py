import pygame
import socket
from socketwrapper import SocketWrapper

from game_screen import GameScreen


class Client:

    running = False
    socket = None

    def __init__(self, dimensions):
        pygame.init()
        self.display = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.connect('192.168.1.100', 47777)
        self.screen = GameScreen(dimensions, self.socket)

    def start(self):
        self.running = True
        self.run()

    def connect(self, address, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((address, port))
        self.socket = SocketWrapper(sock)
        self.socket.listeners.append(lambda x, y: print(y))

    def stop(self):
        self.running = False

    def render(self):
        self.screen.render()
        self.display.blit(self.screen, (0, 0))
        pygame.display.flip()

    def update(self, events):
        self.screen.update(events)

    def run(self):

        while self.running:
            self.clock.tick(10)

            events = pygame.event.get()

            self.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()

            self.render()


if __name__ == '__main__':
    client = Client((800, 600))
    client.start()
