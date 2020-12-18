import asyncio
from functools import wraps


class CONFIG:
    """
    """
    def yeild_init(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            next(res)
            return res

        return wrapper


class Search:
    """
    """
    pass


class Reader:
    """
    """
    pass


class Hit:
    """
    """
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
