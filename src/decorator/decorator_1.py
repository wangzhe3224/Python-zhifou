'''
## 什么是装饰器（decorator）
装饰器是一个**函数**，它的第一个参数是被装饰的函数，返回值是另一个函数。
知识点：参数是函数，返回值也是函数，的函数，就被成为高阶函数。

## 如何写装饰器

## 常用的装饰器实例

## 更加有趣的装饰器（下一期）: 带状态装饰器，装饰器类，缓存。。。
'''
import functools
import time


# 按照定义我们写一个装饰器
def d1(func):

    def inner():
        print('做点什么？调用函数好了。。')
        func()
        print('调用完了')
    
    return inner

def do_twice(func):
    def wrapper_do_twice():
        func()
        func()
    return wrapper_do_twice

def do_twice_v2(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice

def do_twice_v3(func):
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


def do_twice_v4(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer

@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i**2 for i in range(10000)])

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug


if __name__ == '__main__':

    def useful():
        print('Hello World')

    def useful_v2(name):
        print(f'Hello {name}')

    def useful_v3(name):
        print(f'Hello {name}')
        return name

    useful()
    # 装饰器其实就是一个语法糖：
    # d1(useful)()

    # 装饰器是可以叠加的

    # 装饰器可以接受参数

    # 装饰器可以返回值

    # @functools.wraps(func) 更好的文档！

    # 实用的装饰器举例
    
    ## timer

    ## debug

    ## 神奇的缓存
    # import functools

    # @timer
    # @functools.lru_cache(maxsize=4)
    # def fibonacci(num):
    #     if num < 2:
    #         return num
    #     return fibonacci(num - 1) + fibonacci(num - 2)
    
    # print(fibonacci(20))
