import pygame


class GameScreen(pygame.Surface):

    def __init__(self, dimensions):
        super().__init__(dimensions)

        self.game = None
        self.dimensions = dimensions

    def render(self):
        self.fill(0)
        level = self.game.level
        tile_width = min([self.dimensions[0] // level.dimensions[0], self.dimensions[1] // level.dimensions[1]])

        for apple in level.apples:
            pygame.draw.rect(self, (255, 0, 0), (apple.position, (tile_width, tile_width)))

        for block in level.blocks:
            pygame.draw.rect(self, (0, 0, 0), (block.position, (tile_width, tile_width)))

        for snake in level.snakes:
            for segment in snake.body:
                pygame.draw.rect(self, (0, 0, 0), (block.position, (tile_width, tile_width)))
