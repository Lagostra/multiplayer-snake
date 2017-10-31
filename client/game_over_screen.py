import pygame

from common.GUI.button import Button


class GameOverScreen(pygame.Surface):

    def __init__(self, position, dimensions, game_screen):
        super().__init__(dimensions)

        self.position = position
        self.game_screen = game_screen

        self.results = None

        self.restart_button = Button((self.get_width()/2 - 50, self.get_height() - 100), (100, 40), text='Restart',
                                     click_handlers=[game_screen.restart])

    def update(self, events):
        if self.game_screen.is_admin:
            self.restart_button.update(events)

    def render(self):
        self.restart_button.render()

        self.fill((100, 100, 100))

        game_over = pygame.font.SysFont('Georgia', 60, bold=True).render('Game Over', True, (0, 0, 0))
        self.blit(game_over, ((self.get_width() - game_over.get_width()) / 2, 50))

        if self.results:
            font = pygame.font.SysFont('Arial', 20, bold=True)
            label = font.render('{:<15}{:<50}{:>10}{:>15}'.format('Position', 'Username',
                                                                  'Score', 'Victories'), True, (0, 0, 0))
            self.blit(label, ((self.get_width() - label.get_width()) / 2, 200))
            font = pygame.font.SysFont('Arial', 20)
            for i in range(min(len(self.results), 5)):
                r = self.results[i]
                label = font.render('{:<15}{:<50}{:>10}{:>15}'.format(str(i), r['username'],
                                                                      str(r['score']), str(r['wins'])), True, (0, 0, 0))
                self.blit(label, ((self.get_width() - label.get_width()) / 2, 200 + 25 * (i + 1)))

        if self.game_screen.is_admin:
            self.blit(self.restart_button, self.restart_button.position)
