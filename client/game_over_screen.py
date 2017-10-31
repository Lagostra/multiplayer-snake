import pygame

from common.GUI.button import Button


class GameOverScreen(pygame.Surface):

    def __init__(self, position, dimensions, game_screen):
        super().__init__(dimensions)

        self.position = position
        self.game_screen = game_screen

        self.restart_button = Button((self.get_width()/2 - 50, self.get_height() - 100), (100, 40), text='Restart',
                                     click_handlers=[game_screen.restart])

    def update(self, events):
        self.restart_button.update(events)

    def render(self):
        self.restart_button.render()

        self.fill((100, 100, 100))

        game_over = pygame.font.SysFont('Georgia', 60, bold=True).render('Game Over', True, (0, 0, 0))
        self.blit(game_over, ((self.get_width() - game_over.get_width()) / 2, 50))

        self.blit(self.restart_button, self.restart_button.position)
