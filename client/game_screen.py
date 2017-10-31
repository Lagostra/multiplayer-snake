import json

import pygame

from common.GUI.button import Button
from common.game_logic import GameLogic


class GameScreen(pygame.Surface):

    local_game = True
    is_admin = False
    started = False
    game_over = False

    tick_queue = []
    player_snake = None

    def __init__(self, dimensions, socket=None):
        super().__init__(dimensions)

        self.countdown = 0
        self.game = GameLogic()
        self.dimensions = dimensions
        self.local_game = socket is None
        self.socket = socket
        if socket:
            socket.listeners.append(self.handle_message)

        self.start_button = Button((self.get_width()/2 - 50, self.get_height()/2 - 20), (100, 40),
                                   text='Start Game', click_handlers=[self.start])

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
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 0}))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 2}))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 3}))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.socket.send(json.dumps({'type': 'move', 'payload': 1}))
                    elif event.key == pygame.K_SPACE:
                        self.socket.send(json.dumps({'type': 'poop'}))
                    elif event.key == pygame.K_RETURN:
                        self.start()
                    elif event.key == pygame.K_r:
                        self.socket.send(json.dumps({'type': 'restart'}))

        if self.local_game:
            self.game.tick()
            self.game.spawn_apples()
        elif len(self.tick_queue):
            self.game.read_json(self.tick_queue.pop(0))
            self.game.tick()

        self.start_button.update(events)


    def render(self):
        self.fill((0, 0, 0))
        level = self.game.level
        tile_size = min([self.dimensions[0] // level.dimensions[0], self.dimensions[1] // level.dimensions[1]])

        w = level.dimensions[0] * tile_size
        h = level.dimensions[1] * tile_size
        x_offset = (self.dimensions[0] - w) // 2
        y_offset = (self.dimensions[1] - h) // 2

        pygame.draw.rect(self, (83, 89, 99), (x_offset, y_offset, w, h))

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
                if snake == self.player_snake:
                    pygame.draw.rect(self, (72, 192, 232), (x + x_offset, y + y_offset, tile_size, tile_size))
                else:
                    if len(self.player_snake.body)/len(snake.body) > self.game.eat_percent:
                        pygame.draw.rect(self, (0, 255, 0), (x + x_offset, y + y_offset, tile_size, tile_size))
                    else:
                        pygame.draw.rect(self, (255, 255, 0), (x + x_offset, y + y_offset, tile_size, tile_size))

        if self.countdown:
            font = pygame.font.SysFont('Arial', 40)
            label = font.render(str(self.countdown), 1, (0, 0, 0))
            self.blit(label, (self.get_width()/2 - label.get_width() / 2, self.get_height() / 2 - label.get_height() / 2))

        if not self.started and not self.game_over:
            self.start_button.render()
            self.blit(self.start_button, self.start_button.position)

    def start(self):
        if not self.started:
            if not self.local_game:
                self.socket.send(json.dumps({'type': 'start_game'}))

    def handle_message(self, socket, message):
        # If falsy message, connection is lost
        if not message:
            return

        try:
            message = json.loads(message)
        except json.decoder.JSONDecodeError:
            # Invalid JSON format - ignore message
            return

        if message['type'] == 'countdown':
            self.countdown = message['payload']
        elif message['type'] == 'init':
            self.started = True
            self.game_over = False
            self.game.level.init_from_json(message['payload'])
            self.player_snake = next(filter(lambda x: x.id == message['payload']['player_snake'], self.game.level.snakes))
        elif message['type'] == 'tick':
            self.tick_queue.append(message['payload'])
            #self.game.read_json(message['payload'])
            #self.game.tick()
        elif message['type'] == 'game_over':
            self.started = False
            self.game_over = True
            print('Game Over')
            print(message['payload']['scores'])
        elif message['type'] == 'is_admin':
            self.is_admin = True