import pygame

class Client:

    running = False

    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))

    def start(self):
        self.running = True
        self.run()

    def stop(self):
        self.running = False

    def run(self):

        while self.running:

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.stop()


if __name__ == '__main__':
    client = Client(800, 600)
    client.start()
