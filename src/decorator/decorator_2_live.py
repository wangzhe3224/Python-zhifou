import functools

def count_calls(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.num_calls += 1
        print(f"Call {wrapper.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)
    wrapper.num_calls = 0
    return wrapper

def cache(func):

    @functools.wraps(func)
    def dec(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in dec.cache:
            dec.cache[cache_key] = func(*args, **kwargs)
        return dec.cache[cache_key]
    dec.cache = dict()
    return dec


def repeat(num_times=4):
    def dec_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value
        return wrapper
    return dec_repeat


@repeat(num_times=2)
@count_calls
def test():
    print('Hi')

test()

@cache
@count_calls
def fibonacci(num):
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)

# fibonacci(5)
