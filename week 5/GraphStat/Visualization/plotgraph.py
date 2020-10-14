from ..NetworkBuilder import stat
from matplotlib import pyplot as plt
import sys
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


def plot_dgree_distribution(graph, plot_type='line', save_to=''):
    '''
    画出图的度分布
    :param graph: 要画网络分布的图
    :return: None 若返回值为-1 则代表没有找到这种画图类型
    '''
    dedist = stat.cal_degree_distribution(graph)
    x_bar = [i for i in dedist.keys()]
    y_bar = [i for i in dedist.values()]
    if plot_type == 'line':
        plt.plot(x_bar, y_bar, label='graph')
    elif plot_type == 'bar':
        plt.bar(x_bar, y_bar, label='graph')
    elif plot_type == 'pie':
        plt.pie(x_bar, y_bar, label='graph')
    else:
        print('Sorry, not suppoet this plot_type', file=sys.stderr)
        return -1
    plt.title('节点度分布图')
    plt.xlabel('度')
    plt.ylabel('节点数量')
    plt.legend()
    if save_to:
        plt.savefig(save_to, dpi=300)
    plt.show()
