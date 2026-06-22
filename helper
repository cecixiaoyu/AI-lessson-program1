import matplotlib.pyplot as plt
from IPython import display

def plot(scores, mean_scores):
    try:
        display.clear_output(wait=True)
        display.display(plt.gcf())
        plt.clf()
        plt.title('Training Progress')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(scores, label='Score')
        plt.plot(mean_scores, label='Mean Score')
        plt.ylim(ymin=0)
        plt.legend()
        
        if len(scores) > 0:
            plt.text(len(scores)-1, scores[-1], str(scores[-1]))
        if len(mean_scores) > 0:
            plt.text(len(mean_scores)-1, mean_scores[-1], f'{mean_scores[-1]:.1f}')
        
        plt.show(block=False)
        plt.pause(0.1)
    except Exception as e:
        print(f"绘图错误: {e}")
