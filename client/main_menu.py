import pygame

from common.GUI.button import Button


class MainMenu(pygame.Surface):

    def __init__(self, dimensions, main):
        super().__init__(dimensions)

        self.main = main

        self.singleplayer_button = Button((self.get_width() / 2 - 90, 200), (180, 60), "Single Player",
                                          background_colour=(0, 0, 255), text_colour=(255, 255, 255),
                                          font_size=30, bold=True, click_handlers=[self.on_single_player])

        self.multiplayer_button = Button((self.get_width() / 2 - 90, 280), (180, 60), "Multiplayer",
                                                   background_colour=(0, 0, 255), text_colour=(255, 255, 255),
                                                   font_size=30, bold=True, click_handlers=[self.on_multiplayer])

    def update(self, events):
        self.singleplayer_button.update(events)
        self.multiplayer_button.update(events)

    def render(self):
        self.fill((94, 199, 60))

        font = pygame.font.SysFont("Georgia", 80, True)
        label = font.render("Snakes", True, (255, 255, 255))
        self.blit(label, ((self.get_width() - label.get_width())/2, 75))

        self.singleplayer_button.render()
        self.blit(self.singleplayer_button, self.singleplayer_button.position)

        self.multiplayer_button.render()
        self.blit(self.multiplayer_button, self.multiplayer_button.position)

    def on_single_player(self):
        self.main.start_game(True)

    def on_multiplayer(self):
        self.main.start_game(False)