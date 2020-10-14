import sys


def _load_info_(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    res = []
    for i in range(int(lines[0].split()[-1]) + 1):
        res.append(lines[i + 1].split('\t'))
    return res


def init_node(file_path):
    '''
    实现节点信息的加载及简单处理
    :param file_path: 储存有节点信息的文件路径
    :return: 包含节点信息的列表,每个信息以字典形式存储
    '''
    attr_list = ['id', 'name', 'power', 'type', 'other info']
    node_list = _load_info_(file_path)
    res = []
    for i in node_list:
        temp = {}
        for j in range(5):
            temp[attr_list[j]] = i[j]
        res.append(temp)
    return res


def _get_attr_(node, key):
    return node[key]


def get_id(node):
    '''
    获取节点的 id 属性
    :param node: 节点元素字典
    :return: 节点 id 属性字符串
    '''
    return _get_attr_(node, 'id')


def get_name(node):
    '''
    获取节点的 name 属性
    :param node: 节点元素字典
    :return: 节点 name 属性字符串
    '''
    return _get_attr_(node, 'name')


def get_power(node):
    '''
    获取节点的 power 属性
    :param node: 节点元素字典
    :return: 节点 power 属性字符串
    '''
    return _get_attr_(node, 'power')


def get_type(node):
    '''
    获取节点的 type 属性
    :param node: 节点元素字典
    :return: 节点 type 属性字符串
    '''
    return _get_attr_(node, 'type')


def get_other_info(node):
    '''
    获取节点的 other info 属性
    :param node: 节点元素字典
    :return: 节点 other info 属性字符串
    '''
    return _get_attr_(node, 'other info')


def print_node(node):
    '''
    显示节点的全部信息
    :param node: 节点元素字典
    :return: None
    '''
    if float(sys.version[:3]) >= 3.6:
        res = f'''Node info\nid: {node['id']}\nname: {node['name']}\npower: {node['power']}\ntype: {node['type']}\nother info: (split by ';' )\n{node['other info']}'''
    else:
        res = '''Node info\n\nid: {0['id']}\nname: {0['name']}\npower: {0['power']}\ntype: {0['type']}\nother info: (split by ';' )\n{0['other info']}'''.format(
            node)
    print(res)
    return None
