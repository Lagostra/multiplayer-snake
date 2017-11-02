import json

import pygame
import socket
import os

from client.main_menu import MainMenu
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
        self.dimensions = dimensions

        self.clock = pygame.time.Clock()
        self.screen = MainMenu(dimensions, self)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.display = pygame.display.set_mode(preferences.preferences['resolution'], pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(preferences.preferences['resolution'])

    def start(self):
        self.running = True
        self.run()

    def start_game(self, single_player):
        if not single_player:
            self.connect((preferences.preferences['server'], preferences.preferences['port']))

        self.screen = GameScreen(self.dimensions, self.socket)

    def connect(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        self.socket = SocketWrapper(sock)
        self.socket.start_listening()
        self.socket.send(json.dumps({'type': 'change_username', 'payload': preferences.preferences['username']}))

    def stop(self):
        self.running = False
        if self.socket:
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