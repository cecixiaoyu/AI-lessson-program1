import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
from snake_env import Game
from snake_agent import Agent

# 全局绘图列表
plot_scores = []
plot_mean_scores = []
plot_losses = []

def plot(scores, mean_scores):
    plt.figure(1)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Mean Score')
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], f"{mean_scores[-1]:.2f}")
    plt.legend()
    plt.pause(0.001)

def evaluate(agent, num_episodes=5):
    print(f"\n开始评估模式，运行 {num_episodes} 局...")
    game = Game(visualize=True)
    scores = []
    for _ in range(num_episodes):
        game.reset()
        while True:
            state_old = game.get_state()
            final_move = agent.get_action(state_old, explore=False)
            reward, done, score = game.play_step(final_move)
            if done:
                scores.append(score)
                print(f"游戏结束，得分: {score}")
                break
    avg_score = np.mean(scores) if scores else 0
    print(f"评估完成！平均得分: {avg_score:.2f}")
    game.close()

def train(num_episodes=5000, load_pretrained=False):
    global plot_scores, plot_mean_scores, plot_losses

    if load_pretrained and os.path.exists('model.pth'):
        print("加载预训练模型...")
        agent = Agent()
        agent.model.load()
    else:
        agent = Agent()

    game = Game(visualize=False)
    total_step = 0

    print(f"开始训练循环，共 {num_episodes} 局...")
    try:
        for episode in range(num_episodes):
            game.reset()
            state_old = game.get_state()
            while True:
                final_move = agent.get_action(state_old, explore=True)
                reward, done, score = game.play_step(final_move)
                state_new = game.get_state()

                agent.train_short_memory(state_old, final_move, reward, state_new, done)
                agent.remember(state_old, final_move, reward, state_new, done)

                state_old = state_new
                total_step += 1

                if done:
                    break

            agent.n_game += 1
            plot_scores.append(score)
            mean_score = np.mean(plot_scores[-20:]) if len(plot_scores) >= 20 else np.mean(plot_scores)
            plot_mean_scores.append(mean_score)

            if agent.n_game % 10 == 0:
                print(f"Game {agent.n_game}, Score: {score}, Mean Score: {mean_score:.2f}")

            if agent.n_game % 50 == 0:
                agent.model.save()
                print(f"模型已保存 (第 {agent.n_game} 局)")

            if agent.n_game % 20 == 0:
                try:
                    plot(plot_scores, plot_mean_scores)
                except Exception as e:
                    print(f"绘图失败: {e}")

        print("训练完成！")
        agent.model.save()
        print("最终模型已保存为 'model.pth'")

    except KeyboardInterrupt:
        print("\n训练被用户中断。")
        agent.model.save()
        print("当前模型已保存。")
    finally:
        game.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train or evaluate a Snake AI using DQN.")
    parser.add_argument('--mode', choices=['train', 'eval'], default='train',
                        help="运行模式：'train' 训练模型，'eval' 评估模型")
    parser.add_argument('--episodes', type=int, default=5000,
                        help="训练的局数（仅在 train 模式下有效）")
    parser.add_argument('--load', action='store_true',
                        help="是否加载已存在的 model.pth 进行继续训练或评估")

    args = parser.parse_args()

    if args.mode == 'train':
        train(num_episodes=args.episodes, load_pretrained=args.load)
    elif args.mode == 'eval':
        agent = Agent()
        if args.load and os.path.exists('model.pth'):
            agent.model.load()
            print("已加载 model.pth 进行评估。")
        else:
            print("警告：未找到 model.pth，将使用随机策略进行评估。")
        evaluate(agent, num_episodes=3)
