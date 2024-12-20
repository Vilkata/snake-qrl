import numpy as np
import random

class SnakeGame:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.width = grid_size * cell_size
        self.height = grid_size * cell_size
        self.snake = None
        self.food = None
        self.last_action = None  
        self.reset()

    def reset(self):
        start_x = self.grid_size // 2
        start_y = self.grid_size // 2
        self.snake = [(start_x, start_y), (start_x, start_y - 1), (start_x, start_y - 2)]
        self.last_action = random.choice([0, 1, 2, 3])  
        self._place_food()
        return self.state

    @property
    def state(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        for segment in self.snake:
            if 0 <= segment[0] < self.grid_size and 0 <= segment[1] < self.grid_size:
                grid[segment] = 1.0
        if 0 <= self.food[0] < self.grid_size and 0 <= self.food[1] < self.grid_size:
            grid[self.food] = -1.0
        return grid

    def _place_food(self):
        while True:
            food_position = (random.randint(0, self.grid_size - 1),
                             random.randint(0, self.grid_size - 1))
            if food_position not in self.snake:
                self.food = food_position
                break

    def _move_snake(self, action):
        self.last_action = action  # Актуализиране на последното движение
        if action == 0:  # Нагоре
            new_head = (self.snake[0][0] - 1, self.snake[0][1])
        elif action == 1:  # Надясно
            new_head = (self.snake[0][0], self.snake[0][1] + 1)
        elif action == 2:  # Надолу
            new_head = (self.snake[0][0] + 1, self.snake[0][1])
        elif action == 3:  # Наляво
            new_head = (self.snake[0][0], self.snake[0][1] - 1)
        else:
            raise ValueError(f"Invalid action: {action}")

        self.snake.insert(0, new_head)
        if self.snake[0] != self.food:
            self.snake.pop()

    def _check_collision(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            return "self_collision"  
        if head[0] < 0 or head[0] >= self.grid_size or head[1] < 0 or head[1] >= self.grid_size:
            return "wall_collision"  
        return None

    def step(self, action):
        # Проверка за противоположно движение
        if (self.last_action == 0 and action == 2) or \
           (self.last_action == 2 and action == 0) or \
           (self.last_action == 1 and action == 3) or \
           (self.last_action == 3 and action == 1):
            action = self.last_action

        old_head = self.snake[0]
        self._move_snake(action)

        # Проверка за сблъсъци
        collision = self._check_collision()
        if collision == "self_collision":
            return self.state, -10, True  
        elif collision == "wall_collision":
            return self.state, -10, True  

        # Проверка за изядена храна
        if self.snake[0] == self.food:
            self._place_food()
            return self.state, 10, False 

        # Награди за приближаване/отдалечаване от храната
        old_distance = abs(old_head[0] - self.food[0]) + abs(old_head[1] - self.food[1])
        new_distance = abs(self.snake[0][0] - self.food[0]) + abs(self.snake[0][1] - self.food[1])
        if new_distance < old_distance:
            return self.state, 0.5, False  
        else:
            return self.state, -0.5, False 
