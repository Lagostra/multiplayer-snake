import pygame
import socket
import sys
import os

from common.socketwrapper import SocketWrapper
from client.game_screen import GameScreen
from common import preferences


class Client:

    running = False
    socket = None
    alt_down = False

    def __init__(self, dimensions):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        if preferences.preferences['fullscreen']:
            self.fullscreen = True
            self.display = pygame.display.set_mode(dimensions, pygame.FULLSCREEN)
        else:
            self.fullscreen = False
            self.display = pygame.display.set_mode(dimensions)
        pygame.display.set_caption('Snakes')


        self.clock = pygame.time.Clock()
        self.connect(preferences.preferences['server'])
        self.screen = GameScreen(dimensions, self.socket)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.display = pygame.display.set_mode(preferences.preferences['resolution'], pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(preferences.preferences['resolution'])

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
        self.socket.stop_listening()
        pygame.quit()

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
                    self.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        self.alt_down = True
                    elif self.alt_down and event.key == pygame.K_F4:
                        self.stop()
                        return
                    elif self.alt_down and event.key == pygame.K_RETURN:
                        self.toggle_fullscreen()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                        self.alt_down = False

            self.render()