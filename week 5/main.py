import GraphStat as gs


def main():
    nodes = gs.init_node(r'.\data\newmovies.txt')
    edges = gs.init_edge(r'.\data\newmovies.txt')
    a_graph = gs.init_graph(nodes, edges)
    gs.plot_dgree_distribution(a_graph, 'line')
    gs.plot_nodes_attr(a_graph, 'type')


if __name__ == '__main__':
    main()
