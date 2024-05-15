#!/usr/bin/env python3
""" create class cache """
import redis
import typing
import uuid
from functools import wraps


def count_calls(method: typing.Callable) -> typing.Callable:
    """ Tracks the number of calls made to a method in a Cache class """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> typing.Any:
        """ Invokes the given method after incrementing its call counter """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache():
    """ Cache class """
    def __init__(self) -> None:
        """ create constructor """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """ create store function"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: typing.Callable = None) -> typing.Union[str, bytes, int, float]:
        """ get function to change the returned datatype """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)
    
    def get_str(self, key: str) -> str:
        """ return string """
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """ return int """
        return self.get(key, fn=int)
    
cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value
