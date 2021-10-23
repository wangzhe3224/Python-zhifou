"""
match expression:
    case pattern1: # do something
    case pattern2: # do something else

- 文学模式
- 通配符
- 序列
- 字典
- 类
- OR
- AS

Python知否：3.10深度尝鲜 - 模式匹配

Python知否：3.10深度尝鲜 - 模式匹配
介绍模式匹配的基本语法和可能的工程应用。
"""
from typing import Sequence
from dataclasses import dataclass

Number = float | int

# 文学匹配 和 统配符
def weekday(num: int):
    match int(num * 1):
        case 1:
            return "星期一"
        case 2:
            return "星期二"
        case _:
            return "哈哈"

def http_error(code: int):
    match code:
        case 200:
            return 'good'
        case 401 | 402 | 404:
            return '4xx error'

# 对象属性抽取
@dataclass
class Point:
    x: int
    y: int

@dataclass
class Line:
    node1: Point
    node2: Point

def location(point):
    match point:
        case Point(x=0, y=0):
            print("Origin is the point's location.")
        case Point(x=0, y=y):
            print(f"Y={y} and the point is on the y-axis.")
        case Point(x=x, y=0):
            print(f"X={x} and the point is on the x-axis.")
        case Point():
            print("The point is located somewhere else on the plane.")
        case _:
            print("Not a point")

def show_line(line):
    match line:
        case Line(node1=Point(x=xx, y=yy), node2=n2):  # wow!! 
            print(xx, yy, n2)  
            match n2:
                case Point(x=x,y=y):
                    print(f"{x = } {y = }")

# 序列匹配，类型匹配
def sum(nums: Sequence[Number]):
    match nums:
        case []:
            return 0
        case [int(first) | float(first), *rest]:
            return first + sum(rest)
        case _:
            raise ValueError()

# AS 
def check(var):
    match var:
        case str() as val:   # isinstance()
            return "String"
        case int() as val:
            return "String"
        # None

# 抽取数据 和 守卫
def data_extract():
    user = {
        "name": {"first": "Pablo", "last": "Galindo Salgado"},
        "title": "Python 3.10 release manager",
        "page": 100
    }

    # match ... case ...
    match user:
        case {"name": {"first": first_name}, "page": page} if page > 90:
            print(first_name)
            print(page)
        case _:
            print('?')


if __name__ == '__main__':
    
    # print(weekday(1))
    # print(weekday(2))
    # print(weekday(10))

    # nums = [1,2,3]
    # print(sum(nums))

    # print(check([123]))

    data_extract()

    # p1 = Point(0, 0)
    # p2 = Point(1, 1)
    # l = Line(p1, p2)
    # show_line(l)