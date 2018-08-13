import functools

def memoize(func):
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        print key
        print cache
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func

@memoize
def fib(n):
    if n == 0:return 0
    if n == 1:return 1
    else: return fib(n-1) + fib(n-2)

print fib(10)

def memoized_fib(n, cache={}):
    if n in cache:
        result = cache[n]
    elif n <= 2:
        result = 1
        cache[n] = result
    else:
        result = memoized_fib(n - 2) + memoized_fib(n - 1)
        cache[n] = result

    return result
