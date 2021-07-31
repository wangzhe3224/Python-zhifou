"""
## 什么是装饰器（decorator）
装饰器是一个**函数**，它的第一个参数是被装饰的函数，返回值是另一个函数。
知识点：参数是函数，返回值也是函数，的函数，就被成为高阶函数。

## 如何写装饰器
## 常用的装饰器实例
## 更加有趣的装饰器（下一期）: 带状态装饰器，装饰器类，缓存。。。
"""
import functools
import time


def d1(func):

    def _d1():
        print('进入装饰器')
        func()
        print('装饰结束。。。')

    return _d1

def d2(func):

    def _d2(*args, **kwargs):
        print('进入装饰器')
        res = func(*args, **kwargs)
        print('装饰结束。。。')
        return res

    return _d2

if __name__ == '__main__':

    # @d1


    # useful()

    @d2
    def useful_v2(name):
        print(f'Hello {name}')

    @d2
    def useful_v3(name):
        print(f'Hello {name}')
        return f'Hello {name}'


    def do_twice(func):

        def _do_t():
            func()
            func()

        return _do_t

    # @do_twice
    # @do_twice
    # @do_twice
    # def useful():
    #     print('Hello World')

    # useful()

    @functools.lru_cache(maxsize=4)
    def fibonacci(num):
        if num < 2:
            return num
        return fibonacci(num - 1) + fibonacci(num - 2)
    
    start = time.time()
    fibonacci(30)
    end = time.time()
    print(f"used {end-start}")
