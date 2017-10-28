import pygame

from game_logic import GameLogic


class GameScreen(pygame.Surface):

    local_game = True

    def __init__(self, dimensions):
        super().__init__(dimensions)

        self.game = GameLogic()
        self.dimensions = dimensions

    def update(self, events):
        if self.local_game:
            for event in events:
                if event.type == pygame.K_UP:
                    self.game.move_snake(self.game.level.snakes[0], 0)
                elif event.type == pygame.K_DOWN:
                    self.game.move_snake(self.game.level.snakes[0], 2)
                elif event.type == pygame.K_LEFT:
                    self.game.move_snake(self.game.level.snakes[0], 3)
                elif event.type == pygame.K_RIGHT:
                    self.game.move_snake(self.game.level.snakes[0], 1)

        self.game.tick()


    def render(self):
        self.fill((255, 255, 255))
        level = self.game.level
        tile_size = min([self.dimensions[0] // level.dimensions[0], self.dimensions[1] // level.dimensions[1]])

        w = level.dimensions[0] * tile_size
        h = level.dimensions[1] * tile_size
        x_offset = (self.dimensions[0] - w) // 2
        y_offset = (self.dimensions[1] - h) // 2



        pygame.draw.rect(self, (0, 0, 0), (x_offset, y_offset, w, h))

        for apple in level.apples:
            x = (apple.position[0] + level.dimensions[0] // 2) * tile_size
            y = (apple.position[1] + level.dimensions[1] // 2) * tile_size
            pygame.draw.rect(self, (255, 0, 0), (x + x_offset, y + y_offset, tile_size, tile_size))

        for block in level.blocks:
            x = (block.position[0] + level.dimensions[0] // 2) * tile_size
            y = (block.position[1] + level.dimensions[1] // 2) * tile_size
            pygame.draw.rect(self, (0, 0, 255), (x + x_offset, y + y_offset, tile_size, tile_size))

        for snake in level.snakes:
            for segment in snake.body:
                x = (segment[0] + level.dimensions[0] // 2) * tile_size
                y = (segment[1] + level.dimensions[1] // 2) * tile_size
                print(x, y)
                pygame.draw.rect(self, (0, 255, 0), (x + x_offset, y + y_offset, tile_size, tile_size))
