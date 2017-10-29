import json
import threading
import time

from game_logic import GameLogic


class Game:

    started = False
    running = False
    players = []
    admin_user = None

    def __init__(self, admin_user):
        self.add_player(admin_user)
        self.admin_user = admin_user
        self.game_logic = GameLogic()

    def start(self):
        self.started = True
        self.running = True

        for player in self.players:
            player.snake = self.game_logic.add_snake()

        payload = {
            'level_size': {'width': self.game_logic.level.dimensions[0], 'height': self.game_logic.level.dimensions[1]},
            'snakes': [],
            'apples': [],
            'blocks': []
        }

        for snake in self.game_logic.level.snakes:
            payload['snakes'].append({'id': snake.id,
                                      'x': snake.body[0][0], 'y': snake.body[0][1],
                                     'dir': snake.direction})

        for apple in self.game_logic.level.apples:
            payload['apples'].append({'x': apple.position[0], 'y': apple.position[1]})

        for block in self.game_logic.level.blocks:
            payload['blocks'].append({'x': block.position[0], 'y': block.position[1]})

        message = json.dumps({
            'type': 'init',
            'payload': payload
        })

        self.send_to_all(message)

        threading.Thread(target=lambda: self.run()).start()

    def stop(self):
        self.running = False

    def add_player(self, user):
        self.players.append(Player(user))
        user.socket.listeners.append(self.handle_message)

    def send_to_all(self, message):
        for player in self.players:
            player.user.socket.send(message)

    def handle_message(self, socket, message):
        player = next(filter(lambda x: x.user.socket == socket, self.players), None)

        if not player:
            return

        try:
            message = json.loads(message)
        except json.decoder.JSONDecodeError:
            # Invalid JSON format - ignore message
            return

        if player.user == self.admin_user:
            # Message was from administrator
            
            if message['type'] == 'start_game' and not self.started:
                self.start()

        if message['type'] == 'move' and self.started:
            self.game_logic.player_move(player.snake, int(message['payload']))

    def tick(self):
        self.game_logic.tick()
        self.game_logic.spawn_apples()

        payload = self.game_logic.get_json()
        message = json.dumps({
            'type': 'tick',
            'payload': payload
        })
        self.send_to_all(message)

    def run(self):
        last_tick = 0
        while self.running:
            cur = time.time()
            diff = cur - last_tick
            if diff >= 0.12:
                last_tick = cur
                self.tick()
            #elif diff > 0.01:
            #    time.sleep(diff - 0.01)


class Player:

    snake = None

    def __init__(self, user):
        self.user = user