import pickle
from tqdm import tqdm


def _load_info_(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    vernum = int(lines[0].split()[-1]) + 2
    res = []
    for i in lines[vernum + 1:]:
        res.append(i.split('\t'))
    return res


def init_edge(file_path):
    '''
    实现边信息的加载及简单处理
    :param file_path: 储存有边信息的文件路径
    :return: 包含边信息的列表,每个信息以字典形式存储
    '''
    attr_list = ['out id', 'in id', 'power']
    edge_list = _load_info_(file_path)
    res = []
    flag = 1
    for i in tqdm(edge_list):
        temp = {}
        for j in range(3):
            temp[attr_list[j]] = i[j]
        temp['power'] = int(temp['power'])
        for j in res:
            flag = 1
            if temp['out id'] == j['out id'] and temp['in id'] == j['in id']:
                flag = 0
                j['power'] += 1
                break
        if flag:
            res.append(temp)
    return res


def init_graph(node_list, edges):
    '''
    整合节点信息与边信息
    :param node_list: 储存有节点信息的列表 可以直接传入 init_node 返回值
    :param edges: 储存有边信息的列表 可以直接传入 init_edge 返回值
    :return: 包含节点信息和边信息的字典
    '''
    graph = {}
    graph['node'] = node_list
    graph['edge'] = edges
    return graph


def save_graph(graph, file_path=r'./'):
    '''
    对图结构进行序列化
    :param graph: 要进行序列化的图
    :param file_path: 序列化文件存储路径
    :return: None
    '''
    fw = open(file_path, 'wb')
    pickle.dump(graph, fw)
    fw.close()
    return None


def load_graph(file_path):
    '''
    对图进行反序列化
    :param file_path: 序列化文件存储路径
    :return: 反序列化后的图文件
    '''
    fr = open(file_path, 'rb')
    graph = pickle.load(fr)
    fr.close()
    return graph
