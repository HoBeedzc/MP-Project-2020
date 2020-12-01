from multiprocessing import Process, Pipe, Queue
import time
import pkuseg as ps
from functools import wraps
import os
import sys


class Map(Process):
    '''
    class Map, a subclass for Process
    '''
    ID = 0

    def __init__(self, fq, rq):
        super().__init__()
        self._name = 'Map {}'.format(Map.ID)
        Map.ID += 1
        self.fq = fq
        self.rq = rq

    @property
    def name(self):
        return self._name

    def get_news(self):
        '''
        获取要解析的文件
        :return: 要解析文件的文件路径
        '''
        data = self.fq.get()
        if data is None:
            self.write_log('{} will close.'.format(self.name))
            return None
        else:
            self.write_log('{} gets {} from file Queue.'.format(
                self.name, data))
            return data

    def read_news(self, news) -> dict:
        '''
        进行文本解析 （文本词频统计）
        :param news: 要解析文件的文件路径
        :return: 解析后的字典文件
        '''
        with open(news, 'r', encoding='utf-8') as f:
            lines = f.read()
            fut = self.seg.cut(lines)
        res_dict = {}
        for i in fut:
            res_dict[i] = res_dict.get(i, 0) + 1
        return res_dict

    def send_res(self, res, news):
        '''
        将解析结果发送给 Reduce 进程
        :param res: 文件解析结果
        :param news: 要发送的文件路径（方便记录日志）
        :return: None
        '''
        self.rq.put(res)
        self.write_log('{} puts {} result into result Queue.'.format(
            self.name, news))
        pass

    def run(self):
        self.logfile = open(r'./week 12/log/{}.txt'.format(self.name), 'w')
        self.seg = ps.pkuseg()
        while True:
            data = self.get_news()
            if data is None:
                self.rq.put(None)
                self.write_log('{} puts None into result Queue.'.format(
                    self.name))
                break
            else:
                res = self.read_news(data)
                self.send_res(res, data)
        self.logfile.close()
        pass

    def write_log(self, info):
        '''
        写入日志
        :param info: 要写入的日志信息
        :return: None
        '''
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')
        return None


class Reduce(Process):
    '''
    class Reduce, a subclass for Process
    '''
    def __init__(self, name, rq, sp: Pipe, map_num):
        super().__init__()
        self._name = name
        self.rq = rq
        self.sp = sp[1]
        self.res_dict = {}
        self.none_cnt = 0
        self.map_num = map_num

    @property
    def name(self):
        return self._name

    def receive_result(self):
        '''
        从 Map 进程接收结果
        :return: 接收到的内容，或结果状态
        '''
        data = self.rq.get()
        if data is None:
            self.none_cnt += 1
            if self.none_cnt == self.map_num:
                self.write_log('All process has ended')
                return None
            self.write_log('{} processes have ended'.format(self.none_cnt))
            return 0
        else:
            self.write_log('{} get a res though Queue'.format(self.name))
            return data

    def merge_result(self, data: dict) -> None:
        '''
        合并接收到的结果
        :param data: 要合并的结果
        :return: None
        '''
        for key, value in data.items():
            self.res_dict[key] = self.res_dict.get(key, 0) + value
        pass

    def send_summary(self):
        '''
        向主进程发送最终结果
        :return: None
        '''
        self.sp.send(self.res_dict)
        self.write_log('{} puts summary result though Pipe.'.format(self.name))
        pass

    def run(self):
        self.logfile = open(r'./week 12/log/{}.txt'.format(self.name), 'w')
        while True:
            data = self.receive_result()
            if data is None:
                break
            elif data == 0:
                continue
            else:
                self.merge_result(data)
        self.send_summary()
        self.logfile.close()
        pass

    def write_log(self, info):
        '''
        写入日志
        :param info: 要写入的日志信息
        :return: None
        '''
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')
        pass


class Distribute(Process):
    '''
    class Distribute, a subclass for Process
    '''
    def __init__(self, name, fq: Queue, map_num):
        super().__init__()
        self._name = name
        self.fq = fq
        self.map_num = map_num

    @property
    def name(self):
        return self._name

    def put_none(self):
        '''
        向队列中放入 None
        :return: None
        '''
        for _ in range(self.map_num):
            self.write_log('{} puts None into file Queue.'.format(self.name))
            self.fq.put(None)
        pass

    def put_file(self, path=r'./week 12/THUCN/4w/'):
        '''
        向队列中放入待处理的文件（向 Map 进程分发任务）
        :param path: 文件夹路径
        :return: None
        '''
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            self.write_log('{} puts {} into file Queue.'.format(
                self.name, file_path))
            self.fq.put(file_path)
        pass

    def run(self):
        self.logfile = open(r'./week 12/log/{}.txt'.format(self.name), 'w')
        self.put_file()
        self.put_none()
        self.write_log('All file has been puts.')
        self.logfile.close()
        pass

    def write_log(self, info):
        '''
        写入日志
        :param info: 要写入的日志信息
        :return: None
        '''
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')
        pass


class Master:
    '''
    class Master
    '''
    def __init__(self, map_num):
        self.map_num = map_num
        self.map = []
        self.distribute = None
        self.reduce = None
        pass

    def create_map_process(self, fq, rq):
        '''
        建立并开启 Map 进程
        :param fq: Map 进程与 Distribute 进程之间的管道
        :param rq: Map 进程与 Reduce 进程之间的管道
        :return: None
        '''
        for _ in range(self.map_num):
            temp = Map(fq, rq)
            temp.start()
            self.map.append(temp)
        pass

    def create_reduce_process(self, rq, sp):
        '''
        建立并开启 Reduce 进程
        :param rq: Reduce 进程与 Map 进程之间的管道
        :param sp: Reduce 进程与 Master 进程之间的管道
        :return: None
        '''
        temp = Reduce('Reduce Zero', rq, sp, self.map_num)
        temp.start()
        self.reduce = temp
        pass

    def create_distribute_process(self, fq):
        '''
        建立并开启 Distribute 进程
        :param fq: Distribute 进程与 Map 进程之间的管道
        :return: None
        '''
        temp = Distribute('Distribute Zero', fq, self.map_num)
        temp.start()
        self.distribute = temp
        pass

    def join_distribute_process(self):
        '''
        Master 进程等待 Distribute 进程
        :return: None
        '''
        self.distribute.join()
        pass

    def join_map_process(self):
        '''
        Master 进程等待 Map 进程
        :return: None
        '''
        for i in self.map:
            i.join()
        pass

    def receive_summary(self, sp):
        '''
        Master 进程从 Reduce 进程接收汇总数据
        :return: 接收到的数据结果
        '''
        res = None
        while True:
            res = sp[0].recv()
            self.write_log('Master receive summary result for pipe')
            return res

    def main(self):
        self.logfile = open(r'./week 12/log/Master.txt', 'w')
        file_queue = Queue()
        result_queue = Queue()
        summary_pipe = Pipe()
        self.create_distribute_process(file_queue)
        self.create_map_process(file_queue, result_queue)
        self.create_reduce_process(result_queue, summary_pipe)
        self.join_distribute_process()
        self.join_map_process()
        self.receive_summary(summary_pipe)
        summary_pipe[0].close()
        summary_pipe[1].close()
        self.logfile.close()
        pass

    def write_log(self, info):
        '''
        写入日志文件
        :param info: 要写入的内容
        :return: None
        '''
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')
        pass


def show_running_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        fun_res = func(*args, **kwargs)
        end = time.time()
        print('func {} running time : {} sec.'.format(func.__name__,
                                                      end - start))
        return fun_res

    return wrapper


@show_running_time
def test(num):
    t = Master(num)
    t.main()
    pass


def run_from_shell():
    test(int(sys.argv[1]))
    pass


def main():
    for i in range(1, 11):
        test(i)


if __name__ == '__main__':
    # main()
    run_from_shell()
    pass
