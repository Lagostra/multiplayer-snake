import json

import pygame

from game_logic import GameLogic


class GameScreen(pygame.Surface):

    local_game = True

    def __init__(self, dimensions, socket=None):
        super().__init__(dimensions)

        self.game = GameLogic()
        self.dimensions = dimensions
        self.local_game = socket is None
        self.socket = socket

    def update(self, events):
        if self.local_game:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.player_move(self.game.level.snakes[0], 0)
                    elif event.key == pygame.K_DOWN:
                        self.game.player_move(self.game.level.snakes[0], 2)
                    elif event.key == pygame.K_LEFT:
                        self.game.player_move(self.game.level.snakes[0], 3)
                    elif event.key == pygame.K_RIGHT:
                        self.game.player_move(self.game.level.snakes[0], 1)

                    if event.key == pygame.K_w:
                        self.game.player_move(self.game.level.snakes[1], 0)
                    elif event.key == pygame.K_s:
                        self.game.player_move(self.game.level.snakes[1], 2)
                    elif event.key == pygame.K_a:
                        self.game.player_move(self.game.level.snakes[1], 3)
                    elif event.key == pygame.K_d:
                        self.game.player_move(self.game.level.snakes[1], 1)
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 0}))
                    elif event.key == pygame.K_DOWN:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 2}))
                    elif event.key == pygame.K_LEFT:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 1}))
                    elif event.key == pygame.K_RIGHT:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 3}))

        self.game.tick()

        if self.local_game:
            self.game.spawn_apples()


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
                pygame.draw.rect(self, (0, 255, 0), (x + x_offset, y + y_offset, tile_size, tile_size))
