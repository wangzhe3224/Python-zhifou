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
isinstance(Union[int, float])