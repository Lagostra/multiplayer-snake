import pygame
from client.game_screen import GameScreen

class Display:

    running = False

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.screen = GameScreen()

    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False

    def render(self):
        self.screen.render()

        self.screen.blit(self.screen, (0, 0))

        self.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(30)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()

            self.render()

if __name__ == '__main__':
    display = Display()
    display.start()