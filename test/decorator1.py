def count(f):
    def inner(*args, **kargs):
        inner.counter += 1
        return f(*args, **kargs)
    inner.counter = 0
    return inner

@count
def my_fnc():
    pass

if __name__ == '__main__':
    my_fnc()
    my_fnc()
    my_fnc()

    print 'my_fnc.counter=',my_fnc.counter