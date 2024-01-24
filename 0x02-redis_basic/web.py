#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker
'''
import redis
import requests
from typing import Callable
from functools import wraps


store = redis.Redis()


def the_cache(method: Callable) -> Callable:
    '''tracking how many times a particular URL was accessed
    '''
    @wraps(method)
    def wraper(url) -> str:
        '''wrapper function
        '''
        store.incr(f'count:{url}')
        response = store.get(f'response:{url}')
        if response:
            return response.decode('utf-8')
        response = method(url)
        store.set(f'count:{url}', 0)
        store.setex(f'response:{url}', 10, response)
        return response
    return wraper


@the_cache
def get_page(url: str) -> str:
    '''obtain the HTML content of a particular URL
    '''
    return requests.get(url).text
