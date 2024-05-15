#!/usr/bin/env python3
""" create class cache """
import redis
import typing
import uuid


class Cache():
    """ Cache class """
    def __init__(self) -> None:
        """ create constructor """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: typing.Union[str, bytes, int, float]) -> str:
        """ create store function"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
