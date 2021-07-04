import timeit
import numpy as np
from numba import jit

# Python知否: 如何更快的循环
# 更多相关文章: 
# 让 Python 加速飞 : https://wangzhe3224.github.io/2021/03/21/python_spped/
# 高性能Python编程（1）: https://wangzhe3224.github.io/2021/06/24/high_perform_python/


N = 100_000_000

def while_loop(n=N):
    i, s = 0, 0
    while i < n:
        s += i
        i += 1
    return s


def for_loop(n=N):
    s = 0
    for i in range(n):
        s += i 
    return s


def for_loop_with_inc(n=N):
    s = 0
    for i in range(n):
        s += i 
        i += 1  # no effect 
    return s


def for_loop_with_test(n=N):
    s = 0
    for i in range(n):
        if i < n: pass
        s += i
    return s


def sum_range(n=N):
    return sum(range(n))

def sum_generator(n=N):
    return sum(i for i in range(n))


def sum_numpy(n=N):
    return np.sum(n)

@jit
def for_loop_jit(n=N):
    s = 0
    for i in range(n):
        s += i 
    return s


def main():
    # print(f"{timeit.timeit(while_loop, number=1) = }")
    # print(f"{timeit.timeit(for_loop, number=1) = }")
    # print(f"{timeit.timeit(for_loop_with_inc, number=1) = }")
    # print(f"{timeit.timeit(for_loop_with_test, number=1) = }")
    # print(f"{timeit.timeit(sum_range, number=1) = }")
    # print(f"{timeit.timeit(sum_generator, number=1) = }")
    # print(f"{timeit.timeit(sum_numpy, number=1) = }")
    # # 
    for_loop_jit()
    print(f"{timeit.timeit(for_loop_jit, number=1) = }")

if __name__ == '__main__':
    main()