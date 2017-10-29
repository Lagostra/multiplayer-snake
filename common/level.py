import itertools

from apple import Apple
from block import Block
from snake import Snake


class Level:

    def __init__(self, dimensions=None):
        self.num_apples = 1

        self.snakes = []
        self.apples = []
        self.blocks = []

        if dimensions:
            self.dimensions = dimensions
        else:
            self.dimensions = (0, 0)

    def init_from_json(self, json):
        self.snakes = []
        self.apples = []
        self.blocks = []

        self.dimensions = (json['level_size']['width'], json['level_size']['width'])

        for snake in json['snakes']:
            self.snakes.append(Snake((snake['x'], snake['y']), snake['id'], snake['dir']))

        self.snakes.sort(key=lambda x: x.id)

        for apple in json['apples']:
            self.apples.append(Apple((apple['x'], apple['y'])))

        for block in json['blocks']:
            self.apples.append(Block((block['x'], block['y'])))

    def all_blocks(self):
        return itertools.chain(itertools.chain.from_iterable(map(lambda x: x.body, self.snakes)),
                map(lambda x: x.position, self.apples), map(lambda x: x.position, self.blocks))
