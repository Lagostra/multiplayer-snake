
class Server:

    def __init__(self, port):
        self.port = port

    def start(self):
        pass

    def stop(self):
        pass


if __name__ == '__main__':
    server = Server(47777)
    server.start()