import GraphStat as gs
import networkx as nx
from tqdm import tqdm


def main():
    # 初始化节点并打印信息
    nodes = gs.init_node(r'.\data\newmovies.txt')
    gs.print_node(nodes[10])

    # 初始化图
    edges = gs.init_edge(r'.\data\newmovies.txt')
    a_graph = gs.init_graph(nodes, edges)

    # 序列化与反序列化
    gs.save_graph(a_graph, r'.\data\graph.graph')
    a_graph = gs.load_graph(r'.\data\graph.graph')

    # 使用networkx储存网络 后续利用gephi画图
    G = nx.Graph()
    for i in tqdm(a_graph['node']):
        G.add_node(gs.get_id(i))
    for i in tqdm(a_graph['edge']):
        G.add_edge(i['in id'], i['out id'])
    nx.write_gexf(G, r'./data/natwork.gexf')

    # 使用GraphStat画图
    gs.plot_dgree_distribution(a_graph,
                               'line',
                               save_to=r'./data/degree_plot.png')
    gs.plot_dgree_distribution(a_graph,
                               'bar',
                               save_to=r'./data/degree_bar.png')
    gs.plot_nodes_attr(a_graph, 'type', save_to=r'./data/type_plot.png')
    gs.plot_nodes_attr(a_graph,
                       'type',
                       plot_type='bar',
                       save_to=r'./data/type_bar.png')
    gs.plot_nodes_attr(a_graph, 'power', save_to=r'./data/power_plot.png')
    gs.plot_nodes_attr(a_graph,
                       'power',
                       plot_type='bar',
                       save_to=r'./data/power_bar.png')


if __name__ == '__main__':
    main()
