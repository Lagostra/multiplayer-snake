from block import Block
from level import Level


class GameLogic:

    def __init__(self):
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

    def check_collision(self, level):
        snakes_collided = []
        # check box collision
        for snake in level.snakes:
            if snake.body[0] in map(lambda x: x.position, level.blocks):
                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body)))))
                snakes_collided.append(snake)
        # check wall collision
        for snake in level.snakes:
            if snake.body[0][0] < level.dimensions[0]/2 - 1 or snake.body[0][0] > level.dimensions[0]/2:
                level.blocks.extend(list(map(lambda x: Block(x), (filter(lambda x: x != snake.body[0], snake.body)))))
                snakes_collided.append(snake)
        '''
        # check snake collision
        for snake in level.snakes:
            for o_snake in level.snakes:
                if snake == o_snake:
                    if snake.body[0] in snake.body[1:]:
                        level.blocks.extend(list(filter(lambda x: x != snake.body[0], snake.body)))
        '''
        for snake in level.snakes:
            snake.body.pop()









