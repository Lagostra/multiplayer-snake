import json

from server.game import Game


class Lobby:

    user_counter = 1
    game_counter = 1
    games = []

    def __init__(self):
        self.users = []

    def add_client(self, socket):
        user = User(socket, self.user_counter)
        self.users.append(user)
        self.user_counter += 1
        socket.listeners.append(self.handle_message)

        # Automatically join first unstarted game, or create a new one
        game = None
        for g in self.games:
            if not g.started:
                game = g
                break
        if not game:
            self.games.append(Game(user, self.game_counter, 'Game ' + str(self.game_counter)))
            self.game_counter += 1
        else:
            game.add_player(user)

    def send_to(self, user, msg_type, payload):
        message = json.dumps({'type': msg_type, 'payload': payload})
        if not user.socket.send(message):
            self.users.remove(user)

    def get_games(self):
        self.games = list(filter(lambda x: not x.stopped, self.games))
        return self.games

    def get_game(self, identity):
        return next(filter(lambda x: x.id == identity, self.get_games()))

    def send_to_all(self, msg_type, payload):
        for user in self.users:
            self.send_to(user, msg_type, payload)


    def handle_message(self, socket, message):
        # Find the user belonging to this socket
        user = next(filter(lambda x: x.socket == socket, self.users), None)
        if not user:
            # Socket not bound to a user - ignore message...
            return

        # If the socket receives an empty message, the connection has been closed
        if not message:
            if user:
                self.users.remove(user)
                return

        try:
            message = json.loads(message)
        except json.decoder.JSONDecodeError:
            # Invalid JSON format - ignore message
            return

        # Handle message
        try:
            if message['type'] == 'change_username':
                username = message['payload']
                taken_usernames = map(lambda x: x.username, self.users)
                count = 1
                while username in taken_usernames:
                    username = message['payload'] + str(count)
                    count += 1

                user.username = username
                socket.send(json.dumps({'type': 'set_username', 'payload': username}))
            elif message['type'] == 'message':
                payload = {'user': user.username, 'message': message['payload']}
                self.send_to_all('message', payload)
        except KeyError:
            # Invalid message - ignore
            return

    def stop(self):
        for game in self.games:
            game.stop()

        for user in self.users:
            user.socket.stop_listening()

class User:

    def __init__(self, socket, user_no):
        self.socket = socket
        self.username = 'User' + str(user_no)
