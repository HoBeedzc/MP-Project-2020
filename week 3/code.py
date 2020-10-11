# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
# 引入相关库
import pandas as pd
import re
import pkuseg as ps
from tqdm import tqdm
import matplotlib.pyplot as plt
import math
import folium
import webbrowser
import numpy as np


# %%
# 载入数据 使用本地载入
def load_data(path, flag=0):
    '''
    实现本地数据的读取
    :param path: 要读取的文件所在的路径
    :param flag: 读取文件的类型，0表示txt，1表示tsv
    :return: 文件内容按行分割后生成的列表
    '''
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
    if flag:
        res = []
        for i in lines:
            res.append(i.split('\t'))
        return res
    else:
        return lines


wb = load_data(r'./data/weibo.txt', flag=1)

wb[-5:]

# %%
# 使用正则库去除噪声
# 剔除掉除文字之外的其他信息


def remove_date(data_list):
    '''
    实现对文本信息的提取
    :param data_list: 博文信息列表
    :return: 仅包含文本信息的列表
    '''
    res = []
    for i in data_list:
        try:
            end_index = re.search(r'https?://t.cn[A-Za-z0-9/.]*',
                                  i[0]).span()[0]
            res.append(i[0][:end_index])
        except AttributeError:
            res.append(i[0])
    return res


wb_ap = remove_date(wb)

wb_ap[-5:]


# %%
# 处理文本 包括中英文去标点符号 英文去大小写等
def remove_punctuation(data):
    '''
    实现对文本信息中标点符号的去除
    :param data: 仅包含文本信息的列表
    :return: 仅包含文本信息并去除标点符号的列表
    '''
    punctuation = '''`~!@#$%^&*()-=_+\[\]{}|;:,.<>/?·！￥……（）【】‘“《》，。、？"：；～'\\ '''
    res = []
    for i in data:
        res.append(re.sub(r'[{}]+'.format(punctuation), ' ', i).lower())
    return res


wb_ow = remove_punctuation(wb_ap)

wb_ow[-5:]

# %%
# 进行分词 并导入
# 本次分词使用的库并非是jieba 而是北京大学开发的中文分词库pkuseg https://github.com/lancopku/pkuseg-python
# 该分词包的web模型使用微博语料进行预训练，因此更适合本题。 但我好像发现用默认模式分词更好一点


def cut_word(df):
    '''
    实现对文本信息的分词
    :param df: 仅包含文本信息的列表 （去掉标点符号后）
    :return: 将文本信息进行分词后的列表
    '''
    res = []
    seg = ps.pkuseg(model_name="default",
                    user_dict=r'./data/emotion_dict/total.txt',
                    postag=False)
    for i in tqdm(df):
        res.append(seg.cut(i))
    return res


wb_cut = cut_word(wb_ow)

wb_cut[-5:]


# %%
# 过滤停用词
def refresh_stopwords_list():
    '''
    更新停用词表
    :return: 停用词表
    '''
    with open(r'.\data\stopwords_list.txt', 'r') as f:
        sl = f.read().strip().split('\n')
    return sl


def filter_stopwords(data, sw_list, ignore_list):
    '''
    实现对分词后文本信息中停用词的过滤
    :param data: 文本信息分词后的列表
    :param sw_list: 停用词表
    :param ignore_list: 反停用词表（即情绪词典）
    :return: 过滤停用词后的文本信息列表
    '''
    res = []
    for i in tqdm(data):
        temp = []
        for j in i:
            if (j not in sw_list) or (j in ignore_list):
                temp.append(j)
        res.append(temp)
    return res


sl = refresh_stopwords_list()
il = load_data(r'./data/emotion_dict/total.txt')
wb_fst = filter_stopwords(wb_cut, sl, il)

wb_fst[-5:]

# %%
# 进行情绪分析
# 基于现实情况考虑 我们认为情感倾向是多维的 因此每一条情感的输出都是一个5维向量 分别代表该条中每个情感所占的比例
# 但为了方便后面分析 我们将该条情感向量中最大的量作为主情感 后面的时空分析均是基于主情感展开的
# 要求使用闭包实现
# 返回的list 指 生气 厌恶 害怕 开心 失望


def emotional_tag():
    anger_list = load_data(r'./data/emotion_dict/anger.txt')
    disgust_list = load_data(r'./data/emotion_dict/disgust.txt')
    fear_list = load_data(r'./data/emotion_dict/fear.txt')
    joy_list = load_data(r'./data/emotion_dict/joy.txt')
    sadness_list = load_data(r'./data/emotion_dict/sadness.txt')

    def tagging(data):
        em_list = [0 for _ in range(5)]
        for i in data:
            if i in anger_list:
                em_list[0] += 1
            elif i in disgust_list:
                em_list[1] += 1
            elif i in fear_list:
                em_list[2] += 1
            elif i in joy_list:
                em_list[3] += 1
            elif i in sadness_list:
                em_list[4] += 1
            else:
                pass
        return em_list

    return tagging


def emotional_analysis(data_list):
    '''
    实现情绪文本向量化
    :param data_list: 要进行情绪向量化的文本列表
    :return: 文本情绪向量化列表
    '''
    ea_tools = emotional_tag()
    res = []
    for i in tqdm(data_list):
        res.append(ea_tools(i))
    return res


wb_ea = emotional_analysis(wb_fst)

wb_ea[-5:]

# %%
# 将情绪向量转换为标签
# 单一情绪词 表示为 single 单一
# 未出现情绪词 表示为 peace 平静
# 多个情绪词相同得分表示为 mix 混合
# 返回形式为列表 第一个词为标识位 剩余词为情感标签


def give_em_tag(em_vec):
    '''
    根据向量表情进行情绪标注
    :param em_vec: 向量化的情绪列表
    :return: 情绪标注的结果列表
    '''
    flag = ['single', 'peace', 'mix']
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    res = []
    for vec in em_vec:
        temp = []
        max_em = max(vec)
        if max_em:
            if vec.count(max_em) == 1:
                temp.append(flag[0])
                temp.append(em_[vec.index(max_em)])
            else:
                temp.append(flag[2])
                for i in range(len(vec)):
                    if vec[i] == max_em:
                        temp.append(em_[i])
        else:
            temp.append(flag[1])
        res.append(temp)
    return res


wb_emtag = give_em_tag(wb_ea)

wb_emtag[-5:]

# %%
get_ipython().run_line_magic('matplotlib', 'inline')


# 根据情绪类别简单分析
def simple_plot(data):
    flag = ['single', 'peace', 'mix']
    res = [0 for _ in range(3)]
    for i in data:
        if i[0] == 'single':
            res[0] += 1
        elif i[0] == 'peace':
            res[1] += 1
        else:
            res[2] += 1
    explode = (0.1, 0, 0)
    plt.rcParams['font.sans-serif'] = ['SimHei']  #解决中文乱码
    plt.figure(figsize=(6, 9))  #调节图形大小
    plt.pie(
        res,
        explode=explode,
        labels=flag,
        colors=['pink', 'orange', 'yellowgreen'],
        shadow=False,  #无阴影设置
        startangle=90,  #逆时针起始角度设置
        counterclock=False,  #顺时针
        autopct='%.3f%%',
        rotatelabels=True)  #标签指向轴心
    plt.savefig(r'.\img\大情绪分类饼图.png', dpi=300)
    plt.show()


simple_plot(wb_emtag)

# %%
# 根据情绪标签进行画图
# 有标签的按标签分类 没有的忽略


def tag_plot(data):
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    res = [0 for _ in range(5)]
    for i in data:
        if i[0] == 'single':
            res[em_.index(i[1])] += 1
        elif i[0] == 'peace':
            pass
        else:
            for j in i[1:]:
                res[em_.index(j)] += 1
    explode = (0, 0, 0, 0.1, 0)
    plt.rcParams['font.sans-serif'] = ['SimHei']  #解决中文乱码
    plt.figure(figsize=(6, 9))  #调节图形大小
    plt.pie(
        res,
        explode=explode,
        labels=em_,
        colors=['pink', 'orange', 'yellowgreen', 'gray', 'yellow'],
        shadow=False,  #无阴影设置
        startangle=90,  #逆时针起始角度设置
        counterclock=False,  #顺时针
        autopct='%.3f%%',
        rotatelabels=True)  #标签指向轴心
    plt.savefig(r'.\img\小情绪分类饼图.png', dpi=300)
    plt.show()


tag_plot(wb_emtag)

# %%
# 微博中包含时间，可以讨论不同时间情绪比例的变化趋势，观察并分析小时模式等。
# 结合时间进行分析
# 首先提取时间


def extract_time(data, em_list):
    '''
    提取情绪标签与时间信息
    :param data: 包含全部信息的文本列表
    :param em_list: 情绪标签列表
    :return: 时间信息与情绪标签列表
    '''
    res = []
    for i in range(len(data)):
        res.append([data[i][-1].split(), em_list[i]])
    return res


wb_time = extract_time(wb, wb_emtag)

wb_time[-5:]

# %%
# 经过验证 该数据集为东八区连续两天的数据 因此适合进行小时分析


def time_plot(data):
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'peace']
    time_box = [[0 for _ in range(24)] for __ in range(6)]
    for i in data:
        hour_index = int(i[0][3][:2])
        em = i[1]
        if em[0] == 'single':
            time_box[em_.index(em[1])][hour_index] += 1
        elif em[0] == 'peace':
            time_box[em_.index(em[0])][hour_index] += 1
        else:
            for j in em[1:]:
                time_box[em_.index(j)][hour_index] += 1
    for i in range(6):
        plt.plot(time_box[i], label=em_[i])
    plt.legend()
    plt.xlabel("时间")  #X轴标签
    plt.ylabel("情绪标签水平")  #Y轴标签
    plt.title('情绪水平小时模式图')
    plt.savefig(r'.\img\情绪水平小时模式图.png', dpi=300)
    plt.show()
    return time_box


wb_time_box = time_plot(wb_time)


# %%
# 再画一个
def time_plot_2(time_box):
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'peace']
    color = ['#00CED1', '#DC143C', '#00FFFF', '#98FB98', '#D3D3D3', '#FFB6C1']
    for i in range(6):
        plt.bar(range(len(time_box[i])),
                time_box[i],
                label=em_[i],
                fc=color[i],
                bottom=np.sum(time_box[:i], axis=0))
    plt.legend()
    plt.xlabel("时间")  #X轴标签
    plt.ylabel("情绪标签水平")  #Y轴标签
    plt.title('情绪水平小时模式图-2')
    plt.savefig(r'.\img\情绪水平小时模式图_2.png', dpi=300)
    plt.show()


time_plot_2(wb_time_box)


# %%
# 空间分布
# 首先进行坐标转换 并提取坐标和情绪信息
# lng纬度 lat经度
def GCJ02_to_WGS84(gcj_lng, gcj_lat):
    '''
    实现GCJ02坐标系向WGS84坐标系的转换
    :param gcj_lng: GCJ02坐标系下的经度
    :param gcj_lat: GCJ02坐标系下的纬度
    :return: 转换后的WGS84下经纬度
    '''
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    pi = math.pi  # π
    a = 6378245.0  # 长半轴
    es = 0.00669342162296594323  # 偏心率平方

    def transformlat(lng, lat):
        ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(
            math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) +
                20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lat * pi) +
                40.0 * math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(lat / 12.0 * pi) +
                320 * math.sin(lat * pi / 30.0)) * 2.0 / 3.0
        return ret

    def transformlng(lng, lat):
        ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(
            math.fabs(lng))
        ret += (20.0 * math.sin(6.0 * lng * pi) +
                20.0 * math.sin(2.0 * lng * pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(lng * pi) +
                40.0 * math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(lng / 12.0 * pi) +
                300.0 * math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
        return ret

    dlat = transformlat(gcj_lng - 105.0, gcj_lat - 35.0)
    dlng = transformlng(gcj_lng - 105.0, gcj_lat - 35.0)
    radlat = gcj_lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - es * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - es)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = gcj_lat + dlat
    mglng = gcj_lng + dlng
    lng = gcj_lng * 2 - mglng
    lat = gcj_lat * 2 - mglat
    return lng, lat


def extract_area(data, em_list):
    '''
    提取情绪标签与时间信息
    :param data: 包含全部信息的文本列表
    :param em_list: 情绪标签列表
    :return: 位置信息与情绪标签列表
    '''
    res = []
    for i in range(len(data)):
        res.append([
            GCJ02_to_WGS84(float(data[i][-2]), float(data[i][-3])), em_list[i]
        ])
    return res


wb_area = extract_area(wb, wb_emtag)

wb_area[-5:]


# %%
# 画出空间分布散点图
def area_plot(data):
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'peace']
    color = ['#00CED1', '#DC143C', '#00FFFF', '#98FB98', '#D3D3D3', '#FFB6C1']
    area_box = [[[], []] for _ in range(6)]
    for i in data:
        em = i[1]
        if em[0] == 'single':
            area_box[em_.index(em[1])][0].append(i[0][0])
            area_box[em_.index(em[1])][1].append(i[0][1])
        elif em[0] == 'peace':
            area_box[em_.index(em[0])][0].append(i[0][0])
            area_box[em_.index(em[0])][1].append(i[0][1])
        else:
            for j in em[1:]:
                area_box[em_.index(j)][0].append(i[0][0])
                area_box[em_.index(j)][1].append(i[0][1])
    for i in range(len(area_box)):
        plt.scatter(area_box[i][0],
                    area_box[i][1],
                    s=math.pi * 3**2,
                    c=color[i],
                    alpha=0.4,
                    label=em_[i])
    plt.xlabel('纬度')
    plt.ylabel('经度')
    plt.title('情绪水平地区模式图')
    plt.legend()
    plt.savefig(r'.\img\情绪水平地区模式图.png', dpi=300)
    plt.show()


area_plot(wb_area)


# %%
# 进行空间分布可视化
def draw_map(data):
    em_ = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'peace']
    color = ['#00CED1', '#DC143C', '#00FFFF', '#98FB98', '#D3D3D3', '#FFB6C1']
    m = folium.Map(location=[39.7853, 116.3521],
                   control_scale=True,
                   tiles='CartoDB dark_matter',
                   zoom_start=12)  # 绘制初始地图
    m.add_child(folium.LatLngPopup())  # 显示经纬度
    for i in tqdm(data):
        em = i[1]
        pos = i[0]
        if em[0] == 'single':
            folium.Circle(location=pos,
                          radius=50,
                          color=color[em_.index(em[1])],
                          popup=em[1],
                          fill=True).add_to(m)
        elif em[0] == 'peace':
            folium.Circle(location=pos,
                          radius=50,
                          color=color[em_.index(em[0])],
                          popup=em[0],
                          fill=True).add_to(m)
        else:
            for j in em[1:]:
                folium.Circle(location=pos,
                              radius=50,
                              color=color[em_.index(j)],
                              popup=j,
                              fill=True).add_to(m)
    for i in range(6):
        folium.FeatureGroup(name='<span style="color: {col};">{txt}</span>'.
                            format(txt=em_[i], col=color[i])).add_to(m)
    folium.PolyLine(locations=[[39.8586, 116.1015], [39.8586, 116.6721],
                               [39.7204, 116.6721], [39.7204, 116.1015],
                               [39.8586, 116.1015]],
                    color='blue').add_to(m)
    folium.map.LayerControl('topleft', collapsed=False).add_to(m)  # 控制图例位置
    m.save('空间可视化.html')
    return m


wb_map = draw_map(wb_area)

wb_map


# %%
# 写个main函数吧（如果真的需要的话）
def main():
    wb = load_data(r'./data/weibo.txt', flag=1)
    wb_ap = remove_date(wb)
    wb_ow = remove_punctuation(wb_ap)
    wb_cut = cut_word(wb_ow)
    sl = refresh_stopwords_list()
    il = load_data(r'./data/emotion_dict/total.txt')
    wb_fst = filter_stopwords(wb_cut, sl, il)
    wb_ea = emotional_analysis(wb_fst)
    wb_emtag = give_em_tag(wb_ea)
    simple_plot(wb_emtag)
    tag_plot(wb_emtag)
    wb_time = extract_time(wb, wb_emtag)
    wb_time_box = time_plot(wb_time)
    time_plot_2(wb_time_box)
    wb_area = extract_area(wb, wb_emtag)
    area_plot(wb_area)
    wb_map = draw_map(wb_area)
    print('Over')
    pass


if __name__ == '__main__':
    main()
