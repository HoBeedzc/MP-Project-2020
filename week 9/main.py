import os
import re
import sys
import time
import pickle
import inspect as isp
import line_profiler as lp
import memory_profiler as mp
from tqdm import tqdm
from faker import Faker
from functools import wraps
from playsound import playsound


class FuncNotCallableError(ValueError):
    pass


class MusicNotPlayError(ValueError):
    pass


class MusicNotFoundError(FileNotFoundError):
    pass


class PathParamNotFoundError(ValueError):
    pass


class CorpusChristiClockBase():
    '''
    CorpusChristiClockBase class
    instance properties: size, path, faker
    '''
    def __init__(self, size=1000000, path=r'./rundata/'):
        self._size = size
        self._path = path
        self._faker = Faker('zh_CN')
        self._big_data = []
        pass

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        self._size = new_size
        return None

    @size.deleter
    def size(self):
        self._size = 0
        return None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, new_path):
        self._path = new_path
        return None

    @path.deleter
    def path(self):
        self._path = ''
        return None

    @property
    def faker(self):
        return self._faker

    @faker.setter
    def faker(self, new_locale):
        self._faker = Faker(new_locale)
        return None

    @faker.deleter
    def faker(self):
        self._faker = None
        return None


class CorpusChristiClockCore(CorpusChristiClockBase):
    '''
    CorpusChristiClockCore class
    instance properties: size, path, faker
    methods: big_data_generate, big_data_traversal, big_data_pickle, big_data_unpickle
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def big_data_generate(self):
        '''
        大型数据结构的创建
        :return: None
        '''
        print('Generate Data with Size {}'.format(self.size))
        self._big_data = []
        for _ in range(self.size):
            self._big_data.append(self.faker.name())
        pass

    def big_data_traversal(self, func=str, show=False):
        '''
        大型数据结构的遍历
        :param func: 遍历时要执行的函数
        :param show: 是否输出执行结果
        :return: None
        '''
        if not callable(func):
            raise FuncNotCallableError(
                '{} is not a callable object!'.format(func))
        for i in range(self.size):
            self._big_data[i] = func(self._big_data[i])
            if show:
                print(self._big_data[i])
        pass

    def big_data_pickle(self,
                        file_path='BigDataPickle.ccc',
                        is_relative_path=True):
        '''
        大型数据结构序列化
        :param file_path: 序列化文件路径
        :param is_relative_path: 是否为相对路径
        :return: None
        '''
        if is_relative_path:
            file_path = self.path + file_path
        with open(file_path, 'wb') as f:
            pickle.dump(self._big_data, f)
        pass

    def big_data_unpickle(self,
                          file_path='BigDataPickle.ccc',
                          is_relative_path=True):
        '''
        大型数据结构反序列化
        :param file_path: 序列化文件路径
        :param is_relative_path: 是否为相对路径
        :return: None
        '''
        if is_relative_path:
            file_path = self.path + file_path
        with open(file_path, 'rb') as f:
            self._big_data = pickle.load(f)
        pass


class CCCDecoratorTools:
    '''
    CCCDecoratorTools class
    instance properties: None
    static methods: show_running_time, show_run_info, check_path, play_music_after_running
    '''
    def __init__(self):
        pass

    @staticmethod
    def show_running_time(func):
        '''
        显示函数的运行时间
        :param func:要装饰的函数
        :return: 装饰器
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            fun_res = func(*args, **kwargs)
            end = time.time()
            print('func {} running time : {} sec.'.format(
                func.__name__, end - start))
            return fun_res

        return wrapper

    @staticmethod
    def show_run_info(func):
        '''
        显示函数逐行语句的运行时间
        :param func:要装饰的函数
        :return: 装饰器
        '''
        @wraps(func)
        def wrapper(*args, **kwargs):
            profile = lp.LineProfiler(func)  # 把函数传递到性能分析器
            profile.enable()  # 开始分析
            fun_res = func(*args, **kwargs)
            profile.disable()  # 停止分析
            profile.print_stats(sys.stdout)  # 打印出性能分析结果
            return fun_res

        return wrapper

    @staticmethod
    def check_path(path):
        '''
        检查函数路径是否正确
        :param path: 要检查的函数中对应的路径参数
        :return: 装饰器
        '''
        def decorator(func):  # 高阶函数
            @wraps(func)
            def wrapper(*args, **kwargs):
                pathflag = kwargs.get(path, -1)
                if pathflag == -1:  # 未输入路径参数 检查是否存在默认路径
                    params = isp.signature(func)
                    plist = list(params.parameters.keys())
                    if path not in plist:
                        raise PathParamNotFoundError(
                            'There no param {} in func {}!'.format(
                                path, func.__name__))
                    else:
                        path_index = plist.index(path)
                        path_value = str(
                            list(params.parameters.values())
                            [path_index]).split('=')[-1].strip("'")
                        kwargs[path] = path_value
                try:
                    real_path = re.search(r'[.A-Za-z0-9/ ]*/',
                                          kwargs[path]).group(0)
                except AttributeError:
                    real_path = r'./'
                if not os.path.exists(r'./rundata/' + real_path):
                    print('Path {} is not exist!'.format(real_path))
                    print('Make a folder for {} ...'.format(real_path))
                    os.makedirs(r'./rundata/' + real_path)
                else:
                    print('Path {} exist!'.format(real_path))
                return func(*args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def __check_music_file(file):
        return os.path.exists(file)

    @staticmethod
    def __check_music_type(file):
        try:
            res = re.search(r'\.[A-Za-z0-9]+$', file).group(0)[1:]
        except AttributeError:
            res = ''
        if res == 'mp3':
            return 1
        else:
            return 0

    @staticmethod
    def play_music_after_running(mfile):
        '''
        函数运行结束后播放一条音乐
        :param mfile: 音乐文件的路径
        :return: 装饰器
        '''
        def decorator(func):  # 高阶函数
            @wraps(func)
            def wrapper(*args, **kwargs):
                fun_res = func(*args, **kwargs)
                print('Run successfully! Play music to celebrate!')
                if not CCCDecoratorTools.__check_music_file(mfile):
                    raise MusicNotFoundError(
                        '{} music does not exit!'.format(mfile))
                if not CCCDecoratorTools.__check_music_type(mfile):
                    raise MusicNotPlayError(
                        'Sorry, {} music can not play!\n'
                        'We just support .mp3 file'.format(mfile))
                playsound(mfile)
                return fun_res

            return wrapper

        return decorator


class CCCProxy(CorpusChristiClockBase):
    '''
    CCCProxy class
    instance properties: size, path, faker
    methods: big_data_generate, big_data_traversal, big_data_pickle, big_data_unpickle
    '''
    def __init__(self, *args, **kwargs):
        self.ccc = CorpusChristiClockCore(*args, **kwargs)
        pass

    # test run tqdm
    def big_data_generate(self):
        '''
        大型数据结构的创建
        :return: None
        '''
        print('Generate Data with Size {}'.format(self.ccc.size))
        self.ccc._big_data = []
        for _ in tqdm(range(self.ccc.size)):
            self.ccc._big_data.append(self.ccc.faker.name())
        pass

    # test runtime
    @CCCDecoratorTools.show_running_time
    @CCCDecoratorTools.show_run_info
    def big_data_traversal(self, func=str, show=False):
        '''
        大型数据结构的遍历
        :param func: 遍历时要执行的函数
        :param show: 是否输出执行结果
        :return: None
        '''
        self.ccc.big_data_traversal(func, show=show)
        pass

    # test check_path
    @CCCDecoratorTools.check_path('file_path')
    def big_data_pickle(self,
                        file_path=r'BigDataPickle.ccc',
                        is_relative_path=True):
        '''
        大型数据结构序列化
        :param file_path: 序列化文件路径
        :param is_relative_path: 是否为相对路径
        :return: None
        '''
        self.ccc.big_data_pickle(file_path=file_path,
                                 is_relative_path=is_relative_path)
        pass

    # test memory use
    @mp.profile(precision=4)
    def big_data_unpickle(self,
                          file_path='BigDataPickle.ccc',
                          is_relative_path=True):
        '''
        大型数据结构反序列化
        :param file_path: 序列化文件路径
        :param is_relative_path: 是否为相对路径
        :return: None
        '''
        self.ccc.big_data_unpickle(file_path=file_path,
                                   is_relative_path=is_relative_path)
        pass


class CCCTest:
    '''
    CCCTest class
    instance properties: cccp
    methods: tqdm_test, time_test, check_path_test, memory_test
    class methods: generate_example
    static methods: play_music_test
    '''
    def __init__(self, *args, **kwargs):
        self.cccp = CCCProxy(*args, **kwargs)
        pass

    def tqdm_test(self):
        '''
        进度条测试
        :return: None
        '''
        self.cccp.big_data_generate()
        pass

    def time_test(self):
        '''
        函数运行时间测试
        :return: None
        '''
        self.cccp.big_data_traversal(func=str)
        pass

    def check_path_test(self, file_path=r'BigDataPickle.ccc'):
        '''
        函数路径检查测试
        :return: None
        '''
        self.cccp.big_data_pickle(file_path=file_path)
        pass

    def memory_test(self):
        '''
        函数内存占用测试测试
        :return: None
        '''
        self.cccp.big_data_unpickle()
        pass

    @classmethod
    def generate_example(cls, *args, **kwargs):
        '''
        创建CCCTest类实例
        :return: 类实例
        '''
        print("generate a example from class {}".format(cls.__name__))
        return cls(*args, **kwargs)

    @staticmethod
    @CCCDecoratorTools.play_music_after_running(r'./music demo/demo.mp3')
    def play_music_test(*args, **kwargs):
        '''
        播放音乐测试
        :return: None
        '''
        ex = CCCTest.generate_example(*args, **kwargs)
        print()
        print('Tqdm Test...')
        ex.tqdm_test()
        print()
        print('Run Time Test...')
        ex.time_test()
        print()
        print('Check Path Test...exist')
        ex.check_path_test()
        print()
        print('Check Path Test...not exist')
        ex.check_path_test(file_path=r'not exist/BigDataPickle.ccc')
        print()
        print('Memory Usage Test...')
        ex.memory_test()
        pass


def main():
    CCCTest.play_music_test(size=1000000)
    pass


if __name__ == '__main__':
    main()
