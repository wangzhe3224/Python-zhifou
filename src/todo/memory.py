"""
1. `data = None` 会释放内存吗？会的
2. 字典扩容后会释放字典本身的内存吗？不会
"""
import gc
import uuid
import random
from sys import getsizeof
from decimal import Decimal

import guppy
from guppy import hpy
# from pympler import asizeof # this import takes 6 MB memory....

heap = hpy()
MB = 1024 * 1024

def gen_kv():
    return uuid.uuid4(), 1

def allocation_dict(size, factory):
    return {str(k): (factory(k), factory(k)) for k in range(size)}


def allocation_dict_int(size=10000):
    return allocation_dict(size, int)

def allocation_dict_float(size=10000):
    return allocation_dict(size, float)


def allocation_dict_tuple(size=10000):
    return allocation_dict(size, lambda x: (x, x))


def allocation_dict_decimal(size=10000):
    return {k: (Decimal(k), Decimal(k)) for k in range(size)}

def report_heap():
    status = heap.heap()
    print(f"Heap size: {status.size / MB: .2f} MB.")


def test(size, factory):
    print(f"Allocation dict with {size=} and {factory.__name__}")
    dt = factory(size)
    # d2 = dt
    report_heap()
    print(f"Set dict to None.")
    dt = None
    report_heap()
    print()


def q1():
    print(f"Heap status: ")
    hs1 = heap.heap()
    print(f"Initial heap size: {hs1.size / 1024 / 1024: .2f} MB.")
    print(f"Reset heap compute reference.")
    heap.setref()
    report_heap()
    print()

    size = 1_000_000 
    test(size, allocation_dict_int)
    test(size, allocation_dict_float)

def q2():
    size = 2_000_00
    d = {}
    prevs = getsizeof(d)
    report_heap()
    print(f"Add {size} entries in dict.")
    for i in range(size):
        k, v = gen_kv()
        d[k] = v
        s = getsizeof(d)
        diff = s - prevs
        if diff != 0:
            print(f"    Double dict allocation: Length {i: <6} Size: {s: <10} Increased: {diff: <10} (Only dict itself)")
            # report_heap()
        prevs = getsizeof(d)
    
    # print(f"deep size of dict {asizeof.asizesof(d)}")
    report_heap()
    
    number = size // 2
    print(f"Deleting {number} entries")
    del_k = random.sample(list(d.keys()), k=number)
    for k in del_k:
        del d[k]

    # gc.collect()
    # print(f"deep size of dict {asizeof.asizesof(d)}")
    report_heap()



if __name__ == '__main__':

    # q1()
    q2()