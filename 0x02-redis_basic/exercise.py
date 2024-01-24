#!/usr/bin/env python3
'''Redis data storage.
'''
import redis
import uuid
from typing import Any, Callable, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''counting the number of calls  of a method
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''function that increments the count for that key every
        time the method is called'''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''store the history of inputs and outputs for a particular function.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''output.
        '''
        inp_k = '{}:inputs'.format(method.__qualname__)
        out_k = '{}:outputs'.format(method.__qualname__)
        self._redis.rpush(inp_k, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_k, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    '''replay function to display the history of calls of a particular function
    '''
    store = redis.Redis()
    inp_k = '{}:inputs'.format(fn.__qualname__)
    out_k = '{}:outputs'.format(fn.__qualname__)
    inputs = store.lrange(inp_k, 0, -1)
    outputs = store.lrange(out_k, 0, -1)
    liste = [(key.decode("utf-8"), value.decode("utf-8"))
             for key, value in zip(inputs, outputs)]
    print('{} was called {} times:'.format(fn.__qualname__, len(liste)))
    for key, value in liste:
        print('{}(*{}) -> {}'.format(
            fn.__qualname__,
            key,
            value,
        ))


class Cache:
    ''' Cache class.
    '''
    def __init__(self) -> None:
        '''Initialization of instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''store the input data in Redis using the random key
        and return the key.
        '''
        key_id = str(uuid.uuid4())
        self._redis.set(key_id, data)
        return key_id

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''convert the data back to the desired format.
        '''
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        '''convert the data back to the desired format string.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''convert the data back to the desired format int
        '''
        return self.get(key, lambda x: int(x))
