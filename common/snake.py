

class Snake:

    def __init__(self):
        self.body = []
        self.direction = None  # North = 0, East = 1, South = 2, West = 3

    def get_len(self):
        return len(self.body)