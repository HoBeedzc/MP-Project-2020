import os
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
plt.style.use('ggplot')


def cut(data):
    res = re.search(r': [0-9.]* sec', data).group(0)[2:-4]
    return float(res)


def plot():
    with open("./week 12/runtimeinfo_jieba.txt", 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')
        data = list(map(cut, lines))
    x = [i + 1 for i in range(len(data))]
    plt.plot(x, data)
    plt.xlabel('进程数：个')
    plt.ylabel('运行时间：秒')
    plt.title('进程数与程序运行时间折线图-数据量1k')
    plt.show()


def main():
    print('begin')
    os.system(r'cd "e:\Program Products\Python Files\MP_project"')
    for i in tqdm(range(19, 21)):
        os.system(
            '>> "./week 12/runtimeinfo.txt" set /p="Map numbers : {} , " <nul'.
            format(i))
        os.system(
            r'python "./week 12/main.py" {} >> "./week 12/runtimeinfo.txt"'.
            format(i))
    print('finish')
    plot()
    pass


def main_opti():
    print('begin')
    os.system(r'cd "e:\Program Products\Python Files\MP_project"')
    for i in tqdm(range(8, 16)):
        for j in tqdm(range(1, i + 1)):
            os.system(
                '>> "./week 12/runtimeinfo.txt" set /p="Map numbers : {} , Mid_R numbers : {}, " <nul'
                .format(i, j))
            os.system(
                r'python "./week 12/mian-opti.py" {} {} >> "./week 12/runtimeinfo.txt"'
                .format(i, j))
    print('finish')
    plot()
    pass


def main_jieba():
    print('begin')
    os.system(r'cd "e:\Program Products\Python Files\MP_project"')
    for i in tqdm(range(1, 26)):
        os.system(
            '>> "./week 12/runtimeinfo_jieba.txt" set /p="Map numbers : {} , " <nul'
            .format(i))
        os.system(
            r'python "./week 12/mian_jieba.py" {} >> "./week 12/runtimeinfo_jieba.txt"'
            .format(i))
    print('finish')
    plot()
    pass


def main_jiebe_opti():
    print('begin')
    os.system(r'cd "e:\Program Products\Python Files\MP_project"')
    for i in tqdm(range(1, 21)):
        for j in tqdm(range(1, i + 1)):
            os.system(
                '>> "./week 12/runtimeinfo_jieba_opti.txt" set /p="Map numbers : {} , Mid_R numbers : {}, " <nul'
                .format(i, j))
            os.system(
                r'python "./week 12/main_jieba-opti.py" {} {} >> "./week 12/runtimeinfo_jieba_opti.txt"'
                .format(i, j))
    print('finish')
    plot()
    pass


if __name__ == '__main__':
    main()
    # main_opti()
    # main_jieba()
    # main_jiebe_opti()
    # plot()
