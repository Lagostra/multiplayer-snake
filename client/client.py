import pygame
import socket
import sys
import os

from socketwrapper import SocketWrapper
from game_screen import GameScreen
import preferences


class Client:

    running = False
    socket = None

    def __init__(self, dimensions):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.display = pygame.display.set_mode(dimensions)
        pygame.display.set_caption('Snakes')


        self.clock = pygame.time.Clock()
        self.connect(preferences.preferences['server'])
        self.screen = GameScreen(dimensions, self.socket)

    def start(self):
        self.running = True
        self.run()

    def connect(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        self.socket = SocketWrapper(sock)
        self.socket.start_listening()

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
            self.clock.tick(30)

            events = pygame.event.get()

            self.update(events)

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)  # Force quit - maybe change this later...
                    #self.stop()

            self.render()


if __name__ == '__main__':
    preferences.load()
    preferences.save()

    client = Client(preferences.preferences['resolution'])
    client.start()
