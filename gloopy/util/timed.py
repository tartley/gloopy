
from time import clock

def timed(func):
    '''
    decorator for timing a function
    '''
    def inner(*args, **kwargs):
        start = clock()
        result = func(*args, **kwargs)
        print func.__name__, clock() - start
        return result

    return inner

