from block import Block
from snake import Snake


class Level:

    def __init__(self, dimensions):
        self.snakes = []
        self.apples = []
        self.blocks = []

        self.snakes.append(Snake((5, 0)))
        self.snakes[0].direction = 3
        self.snakes.append(Snake((-5, 1)))
        self.snakes[1].direction = 1


        self.blocks.append(Block((-5, -5)))

        self.dimensions = dimensions