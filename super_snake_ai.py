import numpy as np
from snake_env import Game, Direction
import pygame
import sys
from collections import deque
class SuperSnakeAI:


    def __init__(self):
        self.n_game = 0
        self.path = []  # 存储当前路径

    def get_state(self, game):
        """获取游戏状态"""
        head = game.snake.blocks[0]
        berry = game.berry.position

        return {
            'head': head,
            'berry': berry,
            'snake': game.snake.blocks,
            'walls': game.wall.map,
            'direction': game.snake.current_direction
        }

    def manhattan_distance(self, pos1, pos2):
        """曼哈顿距离"""
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)

    def is_safe(self, pos, snake, walls):
        """检查位置是否安全"""
        # 检查墙壁
        if walls[pos.y][pos.x] == '1':
            return False
        # 检查边界
        if pos.x <= 0 or pos.x >= 39 or pos.y <= 0 or pos.y >= 29:
            return False
        # 检查蛇身（除了尾部，因为移动后尾部会消失）
        if pos in snake[:-1]:  # 排除尾部
            return False
        return True

    def find_path_astar(self, start, goal, snake, walls):
        """A*寻路算法"""
        from queue import PriorityQueue

        # 方向：右、左、下、上
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, goal)}

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                # 重建路径
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for dx, dy in directions:
                neighbor = Position(current.x + dx, current.y + dy)

                if not self.is_safe(neighbor, snake, walls):
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.manhattan_distance(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))

        return []  # 没找到路径

    def get_action(self, game):
        """获取动作"""
        state = self.get_state(game)
        head = state['head']
        berry = state['berry']
        snake = state['snake']
        walls = state['walls']
        current_dir = state['direction']

        # 方向映射
        dir_to_action = {
            Direction.right: {  # 当前向右
                'straight': 0,
                'right': 1,    # 向下
                'left': 2       # 向上
            },
            Direction.left: {   # 当前向左
                'straight': 0,
                'right': 1,    # 向上
                'left': 2       # 向下
            },
            Direction.up: {     # 当前向上
                'straight': 0,
                'right': 1,    # 向右
                'left': 2       # 向左
            },
            Direction.down: {   # 当前向下
                'straight': 0,
                'right': 1,    # 向左
                'left': 2       # 向右
            }
        }

        # 使用A*寻路
        path = self.find_path_astar(head, berry, snake, walls)

        if len(path) >= 1:
            next_pos = path[0]

            # 确定需要转向的方向
            if next_pos.x > head.x:  # 需要向右
                if current_dir == Direction.right:
                    return 0  # 直行
                elif current_dir == Direction.up:
                    return 1  # 右转（向下转右？实际上是右转）
                elif current_dir == Direction.down:
                    return 2  # 左转
                else:  # 向左
                    return 1  # 右转

            elif next_pos.x < head.x:  # 需要向左
                if current_dir == Direction.left:
                    return 0
                elif current_dir == Direction.up:
                    return 2  # 左转
                elif current_dir == Direction.down:
                    return 1  # 右转
                else:  # 向右
                    return 2  # 左转

            elif next_pos.y < head.y:  # 需要向上
                if current_dir == Direction.up:
                    return 0
                elif current_dir == Direction.right:
                    return 2  # 左转
                elif current_dir == Direction.left:
                    return 1  # 右转
                else:  # 向下
                    return 2  # 左转

            elif next_pos.y > head.y:  # 需要向下
                if current_dir == Direction.down:
                    return 0
                elif current_dir == Direction.right:
                    return 1  # 右转
                elif current_dir == Direction.left:
                    return 2  # 左转
                else:  # 向上
                    return 1  # 右转

        # 没找到路径，使用安全方向
        safe_dirs = []

        # 检查四个方向
        for dx, dy, dir_check in [(1, 0, Direction.right), (-1, 0, Direction.left),
                                  (0, 1, Direction.down), (0, -1, Direction.up)]:
            next_pos = Position(head.x + dx, head.y + dy)
            if self.is_safe(next_pos, snake, walls):
                safe_dirs.append(dir_check)

        if safe_dirs:
            # 优先选择直行方向
            if current_dir in safe_dirs:
                return 0
            # 否则选择第一个安全方向
            target_dir = safe_dirs[0]
            # 转换为动作
            if target_dir == Direction.right:
                if current_dir == Direction.up:
                    return 1
                elif current_dir == Direction.down:
                    return 2
                else:
                    return 1
            elif target_dir == Direction.left:
                if current_dir == Direction.up:
                    return 2
                elif current_dir == Direction.down:
                    return 1
                else:
                    return 2
            elif target_dir == Direction.up:
                if current_dir == Direction.right:
                    return 2
                elif current_dir == Direction.left:
                    return 1
                else:
                    return 2
            elif target_dir == Direction.down:
                if current_dir == Direction.right:
                    return 1
                elif current_dir == Direction.left:
                    return 2
                else:
                    return 1

        return 0  # 默认直行

def play_super_ai():
    """使用超级AI玩游戏"""
    game = Game(visualize=True)
    ai = SuperSnakeAI()

    record = 0
    scores = []

    print("=" * 60)
    print("超级贪吃蛇AI - 使用A*寻路算法")
    print("=" * 60)
    print("\n开始游戏... 按 Ctrl+C 退出")
    print("按 ESC 键退出游戏\n")

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.close()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.close()
                        sys.exit()

            action = ai.get_action(game)
            reward, done, score = game.play_step(action)

            if done:
                game.reset()
                ai.n_game += 1
                scores.append(score)

                if score > record:
                    record = score
                    print(f"\n🎉 新纪录！分数: {record}")

                # 计算平均分
                avg_score = np.mean(scores[-10:]) if scores else 0
                print(f'游戏 {ai.n_game}: 分数 {score}, 最高记录: {record}, 最近10局平均: {avg_score:.1f}')

    except KeyboardInterrupt:
        print("\n\n游戏结束")
        if scores:
            print(f"\n📊 统计信息:")
            print(f"总游戏局数: {len(scores)}")
            print(f"平均分数: {np.mean(scores):.2f}")
            print(f"最高分数: {max(scores)}")
            print(f"最低分数: {min(scores)}")
    finally:
        game.close()

if __name__ == '__main__':
    from snake_env import Position
    play_super_ai()
