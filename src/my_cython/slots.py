"""
Python知否：数据对象的性能比较

介绍常见数据对象：class, dataclass, __slots__ 和 cython类 的性能和内存使用。
谁更快？谁更节约内存？？
欢迎关注微信视频号：Python知否
欢迎关注公众号：泛程序员 - 一个为非计算机专业程序员充电的地方
"""
import time
from functools import wraps
from pympler import asizeof
from typing import NamedTuple, Union, List, Any
from dataclasses import dataclass
from helloworld import Test


class Article:
    def __init__(self, date, writer):
        self.date = date
        self.writer = writer


class ArticleWithSlots:
    __slots__ = ["date", "writer"]

    def __init__(self, date, writer):
        self.date = date
        self.writer = writer

@dataclass
class ArticalDataclass:
    date: str 
    writer: str

class ArcticalNameTuple(NamedTuple):
    date: str
    writer: str


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
    
def report_size(objs: List[Any]):
    for o in objs:
        print(f"size of {o}: {asizeof.asizeof(o)}")


if __name__ == '__main__':
    
    N = 5_000_000
    create_object(Article, N)
    create_object(ArticleWithSlots, N)
    create_object(ArticalDataclass, N)
    create_object(ArcticalNameTuple, N)
    create_object(Test, N)

    attri_access(Article('a', 'b'), N)
    attri_access(ArticleWithSlots('a', 'b'), N)
    attri_access(ArticalDataclass('a', 'b'), N)
    attri_access(ArcticalNameTuple('a', 'b'), N)
    attri_access(Test('a', 'b'), N)

    a = Article('a', 'b')
    b = ArticleWithSlots('a', 'b')
    c = ArticalDataclass('a', 'b')
    d = ArcticalNameTuple('a', 'b')
    e = {
        'date': 'a',
        'writer': 'b'
    }
    f = ['a', 'b']
    g = ('a', 'b')
    h = Test('a', 'b')
    report_size([a, b, c, d, e, f, g, h])
    # report_size([a, b, c, d, e, f, g])