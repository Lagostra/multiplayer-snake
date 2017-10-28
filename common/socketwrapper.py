from socket import socket
import struct
import threading

class SocketWrapper:

    listeners = []
    listening = False

    def __init__(self, socket):
        self.socket = socket

    def start_listening(self):
        if self.listening:
            return False
        threading.Thread(target=lambda: self.listen()).start()
        self.listening = True
        return True

    def stop_listening(self):
        self.listening = False

    def listen(self):
        while self.listening:
            try:
                size = struct.unpack("i", self.socket.recv(struct.calcsize('i')))[0]
                message = b''
                while len(message) < size:
                    part = self.socket.recv(size - len(message))
                    if not part:
                        continue
                    message += part
                message = message.decode('utf-8')
            except OSError as e:
                continue

            for listener in self.listeners:
                listener(self, message)

            if not message:
                self.stop_listening()

    def send(self, message):
        message = bytes(message, 'utf-8')
        try:
            self.socket.send(struct.pack('i', len(message)) + message)
            return True
        except ConnectionResetError:
            return False
