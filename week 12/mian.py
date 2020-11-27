from multiprocessing import Process
from multiprocessing import Pipe
from multiprocessing import Queue
import time
import pkuseg as ps
from functools import wraps
import os


class Map(Process):
    '''
    '''
    ID = 0

    def __init__(self, fq, rq):
        super().__init__()
        self._name = 'Map {}'.format(Map.ID)
        Map.ID += 1
        self.fq = fq
        self.rq = rq
        self.seg = ps.pkuseg()

    @property
    def name(self):
        return self._name

    def get_news(self):
        '''
        '''
        data = self.fq.get()
        if data is None:
            print('{} will close.'.format(self.name))
            return None
        else:
            print('{} gets {} from file Queue.'.format(self.name, data))
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
        print('{} puts {} result into result Queue.'.format(self.name, news))
        pass

    def run(self):
        while True:
            data = self.get_news()
            if data is None:
                self.rq.put(None)
                print('{} puts None into result Queue.'.format(self.name))
                break
            else:
                res = self.read_news(data)
                self.send_res(res, data)
        pass


class Reduce(Process):
    '''
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
        '''
        data = self.rq.get()
        if data is None:
            self.none_cnt += 1
            if self.none_cnt == self.map_num:
                print('All process has ended')
                return None
            print('{} processes have ended'.format(self.none_cnt))
            return 0
        else:
            print('{} get a res though Queue'.format(self.name))
            return data

    def merge_result(self, data: dict) -> None:
        for key, value in data.items():
            self.res_dict[key] = self.res_dict.get(key, 0) + value
        pass

    def send_summary(self):
        '''
        '''
        self.sp.send(self.res_dict)
        print('{} puts summary result though Pipe.'.format(self.name))
        pass

    def run(self):
        while True:
            data = self.receive_result()
            if data is None:
                break
            elif data == 0:
                continue
            else:
                self.merge_result(data)
        self.send_summary()
        pass


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
            print('{} puts None into file Queue.'.format(self.name))
            self.fq.put(None)

    def put_file(self, path=r'./week 12/THUCN/test/'):
        '''
        '''
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            print('{} puts {} into file Queue.'.format(self.name, file_path))
            self.fq.put(file_path)

    def run(self):
        self.put_file()
        self.put_none()
        print('All file has been puts.')
        pass


class Master:
    '''
    '''
    def __init__(self, map_num):
        self.map_num = map_num
        self.map = []
        self.distribute = None
        self.reduce = None
        pass

    def create_map_process(self, fq, rq):
        '''
        '''
        for _ in range(self.map_num):
            temp = Map(fq, rq)
            self.map.append(temp)
        pass

    def create_reduce_process(self, rq, sp):
        '''
        '''
        temp = Reduce('Reduce Zero', rq, sp, self.map_num)
        self.reduce = temp
        pass

    def create_distribute_process(self, fq):
        '''
        '''
        temp = Distribute('Distribute Zero', fq, self.map_num)
        self.distribute = temp
        pass

    def start_distribute_process(self):
        '''
        '''
        self.distribute.start()
        pass

    def start_map_process(self):
        for i in self.map:
            i.start()
        pass

    def start_reduce_process(self):
        self.reduce.start()
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

    def join_reduce_process(self):
        self.reduce.join()
        pass

    def receive_summary(self, sp):
        '''
        '''
        res = None
        while True:
            res = sp[0].recv()
            print('Master receive summary result for pipe')
            return res

    def main(self):
        file_queue = Queue()
        result_queue = Queue()
        summary_pipe = Pipe()
        self.create_map_process(file_queue, result_queue)
        self.create_reduce_process(result_queue, summary_pipe)
        self.create_distribute_process(file_queue)
        self.start_distribute_process()
        self.start_map_process()
        self.start_reduce_process()
        self.join_distribute_process()
        self.join_map_process()
        # self.join_reduce_process()
        print(self.receive_summary(summary_pipe))
        summary_pipe[0].close()
        summary_pipe[1].close()
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
def main():
    t = Master(1)
    t.main()
    pass


if __name__ == '__main__':
    main()
    pass
