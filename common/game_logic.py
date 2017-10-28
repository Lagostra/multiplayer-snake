from level import Level


class GameLogic:

    def __init__(self):
        self.level = Level((30, 20))
        self.dir_dict = {0: (0, -1), 1: {1, 0}, 2: {0, 1}, 3: {-1, 0}}

    def player_move(self, snake, direction):
        # check if valid - fix this one
        filter(lambda x: x == snake, self.level.snake_list).direction = direction

    def tick(self):
        temp_level = self.level
        for snake in temp_level.snakes:
            self.move_snake(snake)
        self.level = temp_level

    def move_snake(self, snake):
        snake.body.insert(snake.body[0][0] + self.dir_dict[snake.direction][0],
                          snake.body[0][1] + self.dir_dict[snake.direction][1])











