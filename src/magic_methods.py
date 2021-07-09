# Python知否: 魔法函数(1) 基础知识
from typing import Any
from os.path import join
from sys import getsizeof
 
# 一切皆对象是什么意思？
# dir(1)

# 举例
class Value:
    # base class: object
    def __init__(self, val) -> None:
        self.value = val
        print(f"__init__ called.")

    # def __new__(cls, val) -> Any:
    #     print(f"__new__ called.")
    #     obj = super(Value, cls).__new__(cls)
    #     return obj

    # def __del__(self):
    #     print(f"{self.__repr__()} is GCed")

    # 常用的魔法函数
    # print(v1)
    def __str__(self) -> str:
        return f"!!! Value is {self.value}"

    def __repr__(self) -> str:
        return f"Value({self.value})"

    # v1 == v2
    def __eq__(self, o: object) -> bool:
        return self.value == o.value

    # v1 < v2
    def __lt__(self, o: object) -> bool:
        return self.value < o.value

    # def __call__(self):
    #     print(f"__call__ called.")

    def __add__(self, o):
        return Value(self.value + o.value)

    def __sub__(self, o):
        return -1
        # return Value(self.value - o.value)

    def __mul__(self, o):
        return Value(self.value * o.value)

    def __pow__(self, e):
        return Value(self.value ** e)

    def __or__(self, o):
        return Value(self.value or o.value)

    def __abs__(self):
        return Value(abs(self.value))

    def __iadd__(self, i: int):
        return Value(self.value + i)

    # def __hash__(self) -> int:
    #     # if a == b, hash(a) == hash(b)
    #     return self.value

    # def __sizeof__(self) -> int:
    #     return getsizeof(self.value)


class FileObject:

    def __init__(self, filepath='~', filename='sample.txt'):
        # open a file filename in filepath in read and write mode
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file

if __name__ == '__main__':

    v1 = Value(-1)
    v2 = Value(2)
    # print(v1)

    # lst = [v1, v2]
    # print(lst)
    # print(f"{v1 < v2 = }")
    # print(f"{v1 == v2 = }")
    # print(f"{v1 + v2 = }")
    # print(f"{v1 - v2 = }")
    # print(f"{v1 * v2 = }")
    # print(f"{v2 ** 2 = }")
    # print(f"{v1 | v2 = }")
    # print(f"{abs(v1) = }")
    v1 += 100
    print(f"{v1 = }")

    print(f"{abs(v1) = }")

# 请期待下期：
# Python知否: 魔法函数(2) 容器和上下文 