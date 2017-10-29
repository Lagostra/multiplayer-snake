import random

from apple import Apple
from block import Block
from level import Level
from snake import Snake


class GameLogic:

    def __init__(self):
        self.eat_percent = 0.9
        self.level = Level((30, 20))
        self.dir_list = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    def player_move(self, snake, direction):
        if direction not in range(0, 4):
            return
        if len(snake.body) > 1:
            d = self.dir_list[direction]
            if snake.body[1][0] == snake.body[0][0] + d[0] and snake.body[1][1] == snake.body[0][1] + d[1]:
                return
        snake.direction = direction

    def tick(self):
        temp_level = self.level
        for snake in temp_level.snakes:
            self.move_snake(snake)
        self.check_collision(temp_level)
        self.level = temp_level


    def move_snake(self, snake):
        snake.body.insert(0, (snake.body[0][0] + self.dir_list[snake.direction][0],
                          snake.body[0][1] + self.dir_list[snake.direction][1]))

    def spawn_apples(self):
        while len(self.level.apples) < self.level.num_apples:
            x = random.randint(-self.level.dimensions[0] // 2, self.level.dimensions[0] // 2 - 1)
            y = random.randint(-self.level.dimensions[1] // 2, self.level.dimensions[1] // 2 - 1)

            if (x, y) not in self.level.all_blocks():
                self.level.apples.append(Apple((x, y)))

    def check_collision(self, level):
        snakes_collided = []
        # check box collision
        for snake in level.snakes:
            if snake.body[0] in map(lambda x: x.position, level.blocks):
                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body)))))
                snakes_collided.append(snake)
        # check wall collision
        for snake in level.snakes:
            if snake.body[0][0] <= -level.dimensions[0]/2 - 1 or snake.body[0][0] >= level.dimensions[0]/2:
                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body)))))
                snakes_collided.append(snake)
            if snake.body[0][1] <= -level.dimensions[1]/2 - 1 or snake.body[0][1] >= level.dimensions[1]/2:
                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body)))))
                snakes_collided.append(snake)
        # check snake collision
        for snake in level.snakes:
            for o_snake in level.snakes:
                if snake == o_snake:
                    if snake.body[0] in snake.body[1:]:
                        level.blocks.extend(list(map(lambda x: Block(x), snake.body[1:])))
                        snakes_collided.append(snake)
                else: # not self duhh
                    # head to head
                    if snake.body[0] in o_snake.body:
                        if snake.body[0] == o_snake.body[0] or \
                                (snake.body[0] == o_snake.body[1] and snake.body[1] == o_snake.body[0]):
                            level.blocks.extend(
                                list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body[:-1])))))
                            level.blocks.extend(
                                list(map(lambda x: Block(x), (filter(lambda x: x, o_snake.body[:-1])))))
                            if snake not in snakes_collided:
                                snakes_collided.append(snake)
                            if o_snake not in snakes_collided:
                                snakes_collided.append(o_snake)
                        else:  # head to something diff
                            if len(snake.body)/len(o_snake.body) > self.eat_percent:
                                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0],
                                                            o_snake.body[o_snake.body.index(snake.body[0])+1:])))))
                                o_snake.body = o_snake.body[:o_snake.body.index(snake.body[0]) + 1]
                            else:
                                #cant eat, to low
                                level.blocks.extend(
                                    list(map(lambda x: Block(x),
                                             (filter(lambda x: x, snake.body[1:])))))
                                if snake not in snakes_collided:
                                    snakes_collided.append(snake)

        for dead_snake in snakes_collided:
            level.snakes.remove(dead_snake)

        for snake in level.snakes:
            if snake.body[0] in list(map(lambda x: x.position, level.apples)):
                apple_pop_i = None
                for ind, apple in enumerate(level.apples):
                    if apple.position == snake.body[0]:
                        apple_pop_i = ind
                level.apples.pop(apple_pop_i)
            else:
                snake.body.pop()

    def add_snake(self):
        while True:
            x = random.randint(-self.level.dimensions[0] // 2, self.level.dimensions[0] // 2 - 1)
            y = random.randint(-self.level.dimensions[1] // 2, self.level.dimensions[1] // 2 - 1)

            if (x, y) not in self.level.all_blocks():
                new_snake = Snake((x, y))
                if x < 0:
                    new_snake.direction = 1
                if x >= 0:
                    new_snake.direction = 3
                return new_snake







