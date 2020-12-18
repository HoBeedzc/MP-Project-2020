import asyncio
from functools import wraps


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

    def __init__(self,name,path,line,content):
        self.name = name
        self.path = path
        self.line = line
        self.content = content
        pass

class Search:
    """
    """

    def __init__(self):
        pass


class Reader:
    """
    """
    pass


class Hit:
    """
    """
    pass

class TextSearch(Search):
    """

    """
    def __init__(self):
        super().__init__()
        pass

class SearchResult:
    """
    """
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
