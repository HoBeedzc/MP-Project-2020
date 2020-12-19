import asyncio
from functools import wraps
import os
import re
import sys


class CONFIG:
    """
    """
    TEXT_FILE = ['.txt', '.csv', '.java', '.c', '.py', '.md', '.tex']
    WORD_FILE = ['.doc', '.docx']
    KEY_WORD = 'HoBee'
    FLOAT_LENGTH = 3

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
    ID = 0

    def __init__(self, name, path, line, content):
        self.id = Result.ID
        Result.ID += 1
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

    @staticmethod
    async def search(path):
        """
        """
        while True:
            # path = yield  # 获取参数
            g = os.walk(path)
            for _dir, _, files in g:
                for file in files:
                    ext = os.path.splitext(file)[-1]
                    if ext in CONFIG.TEXT_FILE:
                        file_path = os.path.join(_dir, file)
                        await TextOpener.open(file_path)  # 传值给别的生成器
                    elif ext in CONFIG.WORD_FILE:
                        file_path = os.path.join(_dir, file)
                        await TextOpener.open(file_path)
                    else:
                        continue
        pass


class Opener:
    """
    a parent class for open files
    """

    def __init__(self):
        pass

    @staticmethod
    def _check_title(filepath):
        pass

    @staticmethod
    def open(filepath):
        pass


class TextOpener(Opener):
    """

    """

    def __init__(self):
        super(TextOpener, self).__init__()
        pass

    @staticmethod
    async def open(filepath):
        TextOpener._check_title(filepath)
        with open(filepath, 'r') as f:
            await TextReader.read(filepath, f)
        pass


class Reader:
    """
    a parent class for read files
    """

    def __init__(self):
        pass

    @staticmethod
    def read(filepath, f):
        pass


class TextReader(Reader):
    """

    """

    def __init__(self):
        super(TextReader, self).__init__()
        pass

    @staticmethod
    async def read(filepath, f):
        i = 0
        for line in f:
            i += 1
            flag = await Judger.judge(filepath, i, line)
            if flag:
                break
            else:
                continue


class Judger:
    """
    """

    def __init__(self):
        pass

    @staticmethod
    async def judge(filepath, line_number, content):
        res = re.search(CONFIG.KEY_WORD, content)
        if res is None:
            return 0
        else:
            li, ri = res.span()
            li_n = max(0, li - CONFIG.FLOAT_LENGTH)
            ri_n = min(len(content), ri + CONFIG.FLOAT_LENGTH)
            new_con = content[li_n:li] + '==' + res.group(0) + '==' + content[ri + 1:ri_n]
            fname, etx = os.path.splitext(filepath)
            name_ = fname.split(r'/')[-1] + etx
            resc = Result(name_, filepath, line_number, new_con)
            await Hitter.hit(resc)
            return 1
        pass


class Hitter:
    """
    a parent class for hit
    """

    def __init__(self):
        pass

    @staticmethod
    async def hit(resc):
        print('{},{},{},{},{}'.format(resc.id, resc.name, resc.path, resc.line, resc.content))
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
