"""
Python知否：3.10尝鲜互动

介绍Python 3.10 新的出错提示、结构化模式匹配和类型系统更新。
欢迎关注微信视频号：Python知否
欢迎关注公众号：泛程序员 - 一个为非计算机专业程序员充电的地方
"""
# Hi!
print("hi")
# 1. 解析数据结构

user = {
    "name": {"first": "Pablo", "last": "Galindo Salgado"},
    "title": "Python 3.10 release manager",
}

# match ... case ...
match user:
    case {"name": {"first": first_name}}:
        print(first_name)


def sum_list(numbers):
    match numbers:
        case []: 
            return 0
            # Union[int, float]
        case [int(first) | float(first), *rest]:
            return first + sum_list(rest)
        case _:
            _type = numbers.__class__.__name__
            raise ValueError(f'wrong type: {_type}')

print(sum_list([1.2, 1.3, 1]))


name = '?'

match name:
    case "zzz":
        print('hi zzz')
    case "?":
        print("???")

# Type 
from typing import Union

def mean(nums: Union[int, float]):
    ...

def mean(nums: int | float):
    ...

isinstance(1, int | float)
isinstance(1, int) or isinstance(1, float)
isinstance(1 , Union[int, float])