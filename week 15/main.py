import asyncio
from functools import wraps
import os
import sys


class CONFIG:
    """
    """
    @staticmethod
    def yeild_init(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            next(res)
            return res

        return wrapper


class Result:
    """
    """
    def __init__(self, name, path, line, content):
        self.name = name
        self.path = path
        self.line = line
        self.content = content
        pass


class Searcher:
    """
    """
    def __init__(self):
        pass

    def search(self,path):
        """
        """
        while True:
            path = yield  #获取参数
            g = os.walk(path)
            for _dir, _, files in g:
                for file in files:
                    if file.find('.py') > 0:
                        file_path = os.path.join(_dir, file)
                        print('in search, start target')
                        target.send(file_path)  #传值给别的生成器
                        print('in search, after the send')
        pass


class Opener:
    """
    a parent class for open files
    """
    def __init__(self):
        pass

    def open(self):
        pass


class Reader:
    """
    a parent class for read files
    """
    def __init__(self):
        pass

    def read(self):
        pass


class Judger:
    """
    """
    def __init__(self):
        pass

    def judge(self):
        pass


class Hitter:
    """
    a parent class for hit
    """
    def __init__(self):
        pass

    def hit(self):
        pass


class LoaclMiner:
    """
    """
    def __init__(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
    pass
