import pygame
from pygame.locals import *
import random
import numpy as np

# 定义方向枚举
class Direction:
    right = 1
    left = 2
    up = 3
    down = 4

# 位置类
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# 蛇类
class Snake:
    def __init__(self, block_size=20, initial_length=3):
        self.block_size = block_size
        self.blocks = []
        self.current_direction = Direction.right
        # 初始化蛇在屏幕中央
        start_x = 10
        start_y = 10
        for i in range(initial_length):
            self.blocks.append(Position(start_x - i, start_y))

    def handle_action(self, action):
        # action: [straight, right, left]
        clock_wise = [Direction.right, Direction.down, Direction.left, Direction.up]
        idx = clock_wise.index(self.current_direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # straight
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn

        self.current_direction = new_dir

        head = self.blocks[0]
        if self.current_direction == Direction.right:
            new_head = Position(head.x + 1, head.y)
        elif self.current_direction == Direction.left:
            new_head = Position(head.x - 1, head.y)
        elif self.current_direction == Direction.up:
            new_head = Position(head.x, head.y - 1)
        elif self.current_direction == Direction.down:
            new_head = Position(head.x, head.y + 1)
        self.blocks.insert(0, new_head)

# 浆果类
class Berry:
    def __init__(self, space_width, space_height):
        self.space_width = space_width
        self.space_height = space_height
        self.position = Position(0, 0)
        self.randomize()

    def randomize(self):
        self.position = Position(
            random.randint(1, self.space_width),
            random.randint(1, self.space_height)
        )

# 游戏主类
class Game:
    def __init__(self, visualize=False, block_size=20, width=640, height=480):
        self.visualize = visualize
        self.block_size = block_size
        self.width = width
        self.height = height
        self.Space_width = width // block_size
        self.Space_height = height // block_size

        self.snake = Snake(block_size)
        self.berry = Berry(self.Space_width, self.Space_height)
        self.score = 0
        self.reward = 0
        self.total_step = 0
        self.frame = 0
        self.clock = None
        self.display = None

        if self.visualize:
            pygame.init()
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Snake AI')
            self.clock = pygame.time.Clock()

    def reset(self):
        self.snake = Snake(self.block_size)
        self.berry.randomize()
        self.score = 0
        self.total_step = 0
        self.reward = 0

    def position_berry(self):
        while True:
            self.berry.randomize()
            if not any(block.x == self.berry.position.x and block.y == self.berry.position.y for block in self.snake.blocks):
                break

    def berry_collision(self):
        head = self.snake.blocks[0]
        if head.x == self.berry.position.x and head.y == self.berry.position.y:
            self.position_berry()
            self.score += 1
            return True
        else:
            self.snake.blocks.pop()  # 没吃到就移除尾巴
            return False

    def head_hit_body(self, pos=None):
        head = self.snake.blocks[0] if pos is None else pos
        for block in self.snake.blocks[1:]:
            if block.x == head.x and block.y == head.y:
                return True
        return False

    def head_hit_wall(self, pos=None):
        head = self.snake.blocks[0] if pos is None else pos
        if head.x < 1 or head.x > self.Space_width or head.y < 1 or head.y > self.Space_height:
            return True
        return False

    def play_step(self, action):
        game_over = False
        self.reward = 0

        if self.visualize:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return self.reward, True, self.score

        self.total_step += 1
        self.snake.handle_action(action)

        ate_berry = self.berry_collision()
        if ate_berry:
            self.reward = 10
        else:
            self.reward = -0.1

        if self.head_hit_wall() or self.head_hit_body():
            game_over = True
            self.reward = -10
        elif self.total_step > 100 * len(self.snake.blocks):
            game_over = True
            self.reward = -5

        if self.visualize:
            self.draw()
            if self.clock:
                self.clock.tick(60)

        return self.reward, game_over, self.score

    def get_state(self):
        head = self.snake.blocks[0]
        point_l = Position(head.x - 1, head.y)
        point_r = Position(head.x + 1, head.y)
        point_u = Position(head.x, head.y - 1)
        point_d = Position(head.x, head.y + 1)

        dir_l = self.snake.current_direction == Direction.left
        dir_r = self.snake.current_direction == Direction.right
        dir_u = self.snake.current_direction == Direction.up
        dir_d = self.snake.current_direction == Direction.down

        state = [
            # Danger straight
            (dir_r and self.head_hit_wall(point_r)) or 
            (dir_l and self.head_hit_wall(point_l)) or 
            (dir_u and self.head_hit_wall(point_u)) or 
            (dir_d and self.head_hit_wall(point_d)),

            # Danger right
            (dir_u and self.head_hit_wall(point_r)) or 
            (dir_d and self.head_hit_wall(point_l)) or 
            (dir_l and self.head_hit_wall(point_u)) or 
            (dir_r and self.head_hit_wall(point_d)),

            # Danger left
            (dir_d and self.head_hit_wall(point_r)) or 
            (dir_u and self.head_hit_wall(point_l)) or 
            (dir_r and self.head_hit_wall(point_u)) or 
            (dir_l and self.head_hit_wall(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location 
            self.berry.position.x < head.x,  # food left
            self.berry.position.x > head.x,  # food right
            self.berry.position.y < head.y,  # food up
            self.berry.position.y > head.y   # food down
        ]

        return np.array(state, dtype=int)

    def draw(self):
        self.display.fill((0, 0, 0))

        # Draw snake
        for idx, block in enumerate(self.snake.blocks):
            color = (0, 255, 0) if idx == 0 else (0, 200, 0)
            rect = pygame.Rect(
                (block.x - 1) * self.block_size,
                (block.y - 1) * self.block_size,
                self.block_size, self.block_size
            )
            pygame.draw.rect(self.display, color, rect)
            pygame.draw.rect(self.display, (0, 100, 0), rect, 1)

        # Draw berry
        berry_rect = pygame.Rect(
            (self.berry.position.x - 1) * self.block_size,
            (self.berry.position.y - 1) * self.block_size,
            self.block_size, self.block_size
        )
        pygame.draw.rect(self.display, (255, 0, 0), berry_rect)

        pygame.display.flip()

    def close(self):
        if self.visualize:
            pygame.quit()
