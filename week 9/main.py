import os
import re
import sys
import time
import pickle
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

    def big_data_traversal(self, func, show=False):
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
                        file_path=r'BigDataPickle.ccc',
                        is_relative_path=True):
        '''
        '''
        if is_relative_path:
            file_path = self.path + file_path
        with open(file_path, 'w') as f:
            pickle.dump(self._big_data, f)
        pass

    def big_data_unpickle(self,
                          file_path=r'BigDataPickle.ccc',
                          is_relative_path=True):
        '''
        '''
        if is_relative_path:
            file_path = self.path + file_path
        with open(file_path, 'r') as f:
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
        def wrapper(*args,**kwargs):
            start = time.time()
            fun_res = func(*args,**kwargs)
            end = time.time()
            print('func {} running time : {} sec.'.format(func.__name__,end-start))
            return fun_res
        return wrapper

    @staticmethod
    def show_process_rate():
        '''
        '''
        pass

    @staticmethod
    def show_memory_useage():
        '''
        '''
        pass

    @staticmethod
    def show_run_info():
        '''
        '''
        pass

    @staticmethod
    def check_path(path):
        '''
        '''
        def decorator(func):  # 高阶函数
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not os.path.exists(path):
                    print('{} is not exist!'.format(path))
                    print('Make a folder for {} ...'.format(path))
                    os.makedirs(path)
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

    def big_data_generate(self):
        '''
        '''
        self.ccc.big_data_generate()
        pass

    def big_data_traversal(self, func, show=False):
        '''
        '''
        self.ccc.big_data_traversal(func, show=show)
        pass

    def big_data_pickle(self,
                        file_path=r'BigDataPickle.ccc',
                        is_relative_path=True):
        '''
        '''
        self.ccc.big_data_pickle(file_path=file_path,
                                 is_relative_path=is_relative_path)
        pass

    def big_data_unpickle(self,
                          file_path=r'BigDataPickle.ccc',
                          is_relative_path=True):
        '''
        '''
        self.ccc.big_data_unpickle(file_path=file_path,
                                   is_relative_path=is_relative_path)
        pass


class CCCTest:
    '''
    '''
    def __init__(self,*args,**kwargs):
        self.cccp = CCCProxy(*args,**kwargs)
        pass

    def generate_test(self):
        '''
        '''
        pass

    def traversal_test(self):
        '''
        '''
        pass

    def pickle_test(self):
        '''
        '''
        pass

    def unpickle_test(self):
        '''
        '''
        pass

def test():
    ctest = CCCTest()
    ctest.generate_test()
    ctest.traversal_test()
    ctest.pickle_test()
    ctest.unpickle_test()


def main():
    c = CorpusChristiClockCore(size=1000000)
    c.big_data_generate()
    pass


if __name__ == '__main__':
    main()