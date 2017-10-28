import json

class Game:

    started = False
    players = []
    admin_user = None

    def __init__(self, admin_user):
        self.add_player(admin_user)
        self.admin_user = admin_user

    def start(self):
        self.started = True

    def add_player(self, user):
        self.players.append(Player(user))

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

class Player:

    def __init__(self, user):
        self.user = user