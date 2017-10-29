import itertools

from apple import Apple
from block import Block
from snake import Snake


class Level:

    def __init__(self, dimensions):
        self.num_apples = 1

        self.snakes = []
        self.apples = []
        self.blocks = []

        self.snakes.append(Snake((5, 0)))
        self.snakes[0].direction = 3
        self.snakes.append(Snake((-5, 1)))
        self.snakes[1].direction = 1

        self.apples.append(Apple((5, -5)))


        self.blocks.append(Block((-5, -5)))

        self.dimensions = dimensions

    def all_blocks(self):
        return itertools.chain(itertools.chain.from_iterable(map(lambda x: x.body, self.snakes)),
                map(lambda x: x.position, self.apples), map(lambda x: x.position, self.blocks))
