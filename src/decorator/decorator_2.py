import time
import functools

def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(f"Cal {wrapper.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    
    wrapper.num_calls = 0
    return wrapper


def repeat(num_times=4):
    def dec_repeat(func):
        functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper

    return dec_repeat


def slow_down(_func=None, *, rate=1):
    
    def deco_slow_down(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)
        return wrapper

    if _func is None:
        return deco_slow_down
    else:
        return deco_slow_down(_func)


def cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper.cache:
            wrapper.cache[cache_key] = func(*args, **kwargs)
        return wrapper.cache[cache_key]
    
    wrapper.cache = dict()
    return wrapper


if __name__ == '__main__':

    @repeat(num_times=3)
    @count_calls
    def test():
        print('Hi')

    test()
    # test()
    # test()

    @slow_down(rate=2)
    def test():
        print('Slow..')

    # test()

    @cache
    @count_calls
    def fibonacci(num):
        if num < 2:
            return num
        return fibonacci(num - 1) + fibonacci(num - 2)

    fibonacci(8)