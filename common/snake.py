

class Snake:

    def __init__(self, pos, identity, direction = None):
        self.id = identity
        self.body = [pos]
        self.direction = direction  # North = 0, East = 1, South = 2, West = 3
        self.pooping = False
        self.score = 0

    def get_len(self):
        return len(self.body)