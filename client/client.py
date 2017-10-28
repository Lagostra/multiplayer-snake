import pygame

from game_screen import GameScreen


class Client:

    running = False

    def __init__(self, dimensions):
        pygame.init()
        self.display = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.screen = GameScreen(dimensions)

    def start(self):
        self.running = True
        self.run()

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
                    self.stop()

            self.render()


if __name__ == '__main__':
    client = Client((800, 600))
    client.start()
