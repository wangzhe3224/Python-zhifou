import time
from functools import wraps
from pympler import asizeof
from typing import Union


class Article:
    def __init__(self, date, writer):
        self.date = date
        self.writer = writer


class ArticleWithSlots:
    __slots__ = ["date", "writer"]

    def __init__(self, date, writer):
        self.date = date
        self.writer = writer


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print(f"@timefn: {fn.__name__} with {args} took {t2-t1:.4f} seconds")
        return result

    return measure_time

@timefn
def create_object(cls, size):
    for i in range(size):
        arc = cls("2021-01-01", f"Python知否:{i}")

@timefn
def attri_access(obj: Union[Article, ArticleWithSlots], size): 
    for i in range(size):
        ar = obj.writer
        br = obj.date
    return ar, br
    


if __name__ == '__main__':
    
    N = 10000000
    create_object(Article, N)
    create_object(ArticleWithSlots, N)
    attri_access(Article('a', 'b'), N)
    attri_access(ArticleWithSlots('a', 'b'), N)