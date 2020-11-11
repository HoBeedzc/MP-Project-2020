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
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def big_data_generate(self):
        '''
        '''
        print('Generate Data with Size {}'.format(self.size))
        self._big_data = []
        for _ in range(self.size):
            self._big_data.append(self.faker.name())
        pass

    def big_data_traversal(self, func=str, show=False):
        '''
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
        '''
        if is_relative_path:
            file_path = self.path + file_path
        with open(file_path, 'rb') as f:
            self._big_data = pickle.load(f)
        pass


class CCCDecoratorTools:
    '''
    '''
    def __init__(self):
        pass

    @staticmethod
    def show_running_time(func):
        '''
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
                    real_path = re.search(r'[.A-Za-z0-9/]*/',
                                          kwargs[path]).group(0)
                except AttributeError:
                    real_path = r'./'
                if not os.path.exists(real_path):
                    print('Path {} is not exist!'.format(real_path))
                    print('Make a folder for {} ...'.format(real_path))
                    os.makedirs(real_path)
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
    '''
    def __init__(self, *args, **kwargs):
        self.ccc = CorpusChristiClockCore(*args, **kwargs)
        pass

    # test run tqdm
    def big_data_generate(self):
        '''
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
        '''
        self.ccc.big_data_traversal(func, show=show)
        pass

    # test check_path
    @CCCDecoratorTools.check_path('file_path')
    def big_data_pickle(self,
                        file_path=r'BigDataPickle.ccc',
                        is_relative_path=True):
        '''
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
        '''
        self.ccc.big_data_unpickle(file_path=file_path,
                                   is_relative_path=is_relative_path)
        pass


class CCCTest:
    '''
    '''
    def __init__(self, *args, **kwargs):
        self.cccp = CCCProxy(*args, **kwargs)
        pass

    def tqdm_test(self):
        '''
        '''
        self.cccp.big_data_generate()
        pass

    def time_test(self):
        '''
        '''
        self.cccp.big_data_traversal(func=str)
        pass

    def check_path_test(self):
        '''
        '''
        self.cccp.big_data_pickle()
        pass

    def memory_test(self):
        '''
        '''
        self.cccp.big_data_unpickle()
        pass

    @classmethod
    def generate_example(cls, *args, **kwargs):
        '''
        '''
        print("generate a example from class {}".format(cls.__name__))
        return cls(*args, **kwargs)

    @staticmethod
    @CCCDecoratorTools.play_music_after_running(r'./music demo/demo.mp3')
    def play_music_test(*args, **kwargs):
        '''
        '''
        ex = CCCTest.generate_example(*args, **kwargs)
        print()
        print('Tqdm Test...')
        ex.tqdm_test()
        print()
        print('Run Time Test...')
        ex.time_test()
        print()
        print('Check Path Test...')
        ex.check_path_test()
        print()
        print('Memory Usage Test...')
        ex.memory_test()
        pass


def main():
    CCCTest.play_music_test(size=10)
    pass


if __name__ == '__main__':
    main()
