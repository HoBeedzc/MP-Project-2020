import sys


def _get_number_of_node_(graph):
    return len(graph['node'])


def _get_number_of_edge_(graph):
    return len(graph['edge'])


def _get_node_degree_(graph):
    degree = [0 for _ in range(_get_number_of_node_(graph))]
    for i in graph['edge']:
        degree[int(i['out id'])] += 1
        degree[int(i['in id'])] += 1
    return degree


def cal_average_dgree(graph):
    '''
    计算网络中的平均度
    :param graph: 要计算平均度的网络
    :return: 网络的平均度
    '''
    nnum = _get_number_of_node_(graph)
    enum = _get_number_of_edge_(graph)
    ave_degree = enum * 2 / nnum
    return ave_degree


def get_attr_distribution(graph, feature):
    '''
    计算网络中的某个节点属性的分布
    :param graph: 要计算节点属性分布的网络
    :param graph: 要计算分布的属性
    :return: 网络的节点属性分布 若返回值为-1 则代表没有找到该属性
    '''
    attr_list = ['id', 'name', 'power', 'type', 'other info']
    if feature not in attr_list:
        print('Sorry, no such attr found!', file=sys.stderr)
        return -1
    node_list = graph['node']
    feature_dict = {}
    for i in node_list:
        feature_dict[i[feature]] = feature_dict.get(i[feature], 0) + 1
    return feature_dict


def cal_degree_distribution(graph):
    '''
    计算网络中的度分布
    :param graph: 要计算度分布的网络
    :return: 网络的度分布
    '''
    degree = _get_node_degree_(graph)
    max_degree = max(degree)
    min_degree = min(degree)
    dedist = {}
    for i in range(min_degree, max_degree + 1):
        dedist[i] = degree.count(i)
    return dedist
