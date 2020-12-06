from multiprocessing import Process, Pipe, Queue
import time
import pkuseg as ps
from functools import wraps
import os
import sys


class Map(Process):
    '''
    '''
    ID = 0

    def __init__(self, fq, rq, mr_num):
        super().__init__()
        self._name = 'Map {}'.format(Map.ID)
        Map.ID += 1
        self.fq = fq
        self.rq = rq
        self.mr_num = mr_num

    @property
    def name(self):
        return self._name

    def get_news(self):
        '''
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
        '''
        with open(news, 'r', encoding='utf-8') as f:
            lines = f.read()
            fcut = self.seg.cut(lines)
        res_dict = {}
        for i in fcut:
            res_dict[i] = res_dict.get(i, 0) + 1
        return res_dict

    def send_res(self, res, news):
        '''
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
                for _ in range(self.mr_num):
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
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')


class MidReduce(Process):
    '''
    '''
    def __init__(self, name, rq, rq2, map_num):
        super().__init__()
        self.name = name
        self.rq = rq
        self.rq2 = rq2
        self.res_dict = {}
        self.none_cnt = 0
        self.map_num = map_num

    def receive_result(self):
        '''
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
        for key, value in data.items():
            self.res_dict[key] = self.res_dict.get(key, 0) + value
        pass

    def send_result(self):
        '''
        '''
        self.rq2.put(self.res_dict)
        self.write_log('{} puts mid result though res Queue-2.'.format(
            self.name))
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
        self.send_result()
        self.rq2.put(None)
        self.write_log('{} puts None though res Queue-2.'.format(self.name))
        self.logfile.close()
        pass

    def write_log(self, info):
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')


class Reduce(Process):
    '''
    '''
    def __init__(self, name, rq, sp: Pipe, mr_num):
        super().__init__()
        self._name = name
        self.rq = rq
        self.sp = sp[1]
        self.res_dict = {}
        self.none_cnt = 0
        self.mr_num = mr_num

    @property
    def name(self):
        return self._name

    def receive_result(self):
        '''
        '''
        data = self.rq.get()
        if data is None:
            self.none_cnt += 1
            if self.none_cnt == self.mr_num:
                self.write_log('All process has ended')
                return None
            self.write_log('{} processes have ended'.format(self.none_cnt))
            return 0
        else:
            self.write_log('{} get a res though Queue - 2'.format(self.name))
            return data

    def merge_result(self, data: dict) -> None:
        for key, value in data.items():
            self.res_dict[key] = self.res_dict.get(key, 0) + value
        pass

    def send_summary(self):
        '''
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
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')


class Distribute(Process):
    '''
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
        '''
        for _ in range(self.map_num):
            self.write_log('{} puts None into file Queue.'.format(self.name))
            self.fq.put(None)

    def put_file(self, path=r'./week 12/THUCN/4w/'):
        '''
        '''
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            self.write_log('{} puts {} into file Queue.'.format(
                self.name, file_path))
            self.fq.put(file_path)

    def run(self):
        self.logfile = open(r'./week 12/log/{}.txt'.format(self.name), 'w')
        self.put_file()
        self.put_none()
        self.write_log('All file has been puts.')
        self.logfile.close()
        pass

    def write_log(self, info):
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')


class Master:
    '''
    '''
    def __init__(self, map_num, mr_num):
        self.map_num = map_num
        self.mr_num = mr_num
        self.map = []
        self.mr = []
        self.distribute = None
        self.reduce = None
        pass

    def create_map_process(self, fq, rq):
        '''
        '''
        for _ in range(self.map_num):
            temp = Map(fq, rq, self.mr_num)
            temp.start()
            self.map.append(temp)
        pass

    def create_mr_process(self, rq, rq2):
        '''
        '''
        for i in range(self.mr_num):
            temp = MidReduce('Mid Reduce {}'.format(i), rq, rq2, self.map_num)
            temp.start()
            self.mr.append(temp)
        pass

    def create_reduce_process(self, rq, sp):
        '''
        '''
        temp = Reduce('Reduce Zero', rq, sp, self.mr_num)
        temp.start()
        self.reduce = temp
        pass

    def create_distribute_process(self, fq):
        '''
        '''
        temp = Distribute('Distribute Zero', fq, self.map_num)
        temp.start()
        self.distribute = temp
        pass

    def join_distribute_process(self):
        '''
        '''
        self.distribute.join()
        pass

    def join_map_process(self):
        for i in self.map:
            i.join()
        pass

    def receive_summary(self, sp):
        '''
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
        result_queue_2 = Queue()
        summary_pipe = Pipe()
        self.create_distribute_process(file_queue)
        self.create_map_process(file_queue, result_queue)
        self.create_mr_process(result_queue, result_queue_2)
        self.create_reduce_process(result_queue_2, summary_pipe)
        self.join_distribute_process()
        self.join_map_process()
        self.receive_summary(summary_pipe)
        summary_pipe[0].close()
        summary_pipe[1].close()
        self.logfile.close()
        pass

    def write_log(self, info):
        self.logfile.write(str(time.time()) + '\t')
        self.logfile.write(info)
        self.logfile.write('\n')


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
def test(n1, n2):
    t = Master(n1, n2)
    t.main()
    pass


def run_from_shell():
    test(int(sys.argv[1]), int(sys.argv[2]))
    pass


def main():
    test(5, 3)


if __name__ == '__main__':
    run_from_shell()
    pass
