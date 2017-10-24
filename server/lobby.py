import threading
import json

class Lobby:

    user_counter = 1

    def __init__(self):
        self.users = []

    def add_client(self, socket):
        self.users.append(User(socket, self.user_counter))
        self.user_counter += 1
        threading.Thread(target=lambda: self.handle_message(socket)).start()

    @staticmethod
    def send_to(self, user, type, payload):
        message = json.dumps({'type': type, 'payload': payload})
        user.socket.send(message)

    def send_to_all(self, type, payload):
        for user in self.users:
            self.send_to(user, type, payload)


    def handle_message(self, socket):
        while True:
            message = socket.recv(1024).decode('utf-8')

            user = next(filter(lambda x: x.socket == socket, self.users), None)
            if not user:
                # Socket not bound to a user - ignore message...
                continue

            if not message:
                if user:
                    self.users.remove(user)
                    return
            print(message)

            try:
                message = json.loads(message)
            except json.decoder.JSONDecodeError:
                # Invalid JSON format - ignore message
                continue


            # Handle message
            try:
                if message['type'] == 'change_username':
                    user.username = message['payload']
                elif message['type'] == 'message':
                    payload = json.dumps({'user': user.username, 'message': message['payload']})
                    self.send_to_all('message', payload)
            except KeyError:
                # Invalid message - ignore
                continue


class User:

    def __init__(self, socket, user_no):
        self.socket = socket
        self.username = 'User' + str(user_no)
