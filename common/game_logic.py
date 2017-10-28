from level import Level


class GameLogic:

    def __init__(self):
        self.level = Level((30, 20))

    def player_move(self, snake, direction):
        filter(lambda x: x == snake, self.level.snake_list).direction = direction

    def tick(self):
        for snakes in self.level.snakes_list:
            self.move_snake(snakes)
        self.check_collision()

    def move_snake(self, snake):
        dir_mod = {0: (0, -1), 1: {1, 0}, 2: {0, 1}, 3: {-1, 0}}
        new_head = (snake.body[0][0] + dir_mod[snake.direction][0], snake.body[0][1] + dir_mod[snake.direction][0][1])
        if new_head not in self.level.apples_list:
            snake.body.pop()
        else:
            self.level.apples_list.pop(self.level.apples_list.find(new_head))
        snake.insert(0, new_head)

    def check_collision(self):
        for snakes in self.level.snakes_list:
            for other_snake in filter(lambda x: x != snakes, self.level.snakes_list):
                if snakes.body[0] in other_snake.body:
                    pass






