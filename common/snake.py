

class Snake():

    def __init__(self, pos):
        self.body = [pos]

    def get_len(self):
        return len(self.body)