from ..NetworkBuilder import stat
from matplotlib import pyplot as plt
import sys
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）


def plot_nodes_attr(graph, feature, plot_type='line', save_to=''):
    '''
    画出节点属性分布图
    :param graph: 要画分布图的网络
    :param feature: 要画图的属性
    :return: None
    '''
    feature_list = stat.get_attr_distribution(graph, feature)
    x_label = [i for i in feature_list.keys()]
    y_bar = [i for i in feature_list.values()]
    x_bar = [i + 1 for i in range(len(y_bar))]
    if plot_type == 'line':
        plt.plot(x_bar, y_bar, label='graph')
    elif plot_type == 'bar':
        plt.bar(x_bar, y_bar, label='graph')
    elif plot_type == 'pie':
        plt.pie(x_bar, y_bar, label='graph')
    else:
        print('Sorry, not suppoet this plot_type', file=sys.stderr)
        return -1
    plt.legend()
    plt.xticks(x_bar, x_label)
    plt.title('节点{}分布图'.format(feature))
    plt.xlabel('分类')
    plt.ylabel('节点数量')
    if save_to:
        plt.savefig(save_to, dpi=300)
    plt.show()
    pass
