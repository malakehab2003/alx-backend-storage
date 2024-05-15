#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable
import time


def get_page(url: str) -> str:
    # Create a Redis connection
    redis_conn = redis.Redis()

    # Check if the URL is in the cache
    cached_content = redis_conn.get(url)
    if cached_content:
        # If cached content exists, return it
        return cached_content.decode("utf-8")

    # If not cached, fetch the content from the URL
    response = requests.get(url)
    content = response.text

    # Cache the content with an expiration time of 10 seconds
    redis_conn.setex(url, 10, content)

    # Increment the access count for the URL
    redis_conn.incr(f"count:{url}")

    # Return the content
    return content
