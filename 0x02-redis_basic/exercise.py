#!/usr/bin/env python3
"""
This module provides a class to store data in a cache
"""
import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts how many times a method is called.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call
        count and then calls the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs for a function.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores the input
        arguments and output of the method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the inputs
        self._redis.rpush(input_key, str(args))

        # Call the original method
        result = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.
    """
    redis_client = method.__self__._redis
    method_name = method.__qualname__

    calls = redis_client.get(f"{method_name}")
    if calls is None:
        print(f"{method_name} has not been called yet.")
        return

    calls = int(calls)
    print(f"{method_name} was called {calls} times:")

    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    for i, (input_args, output) in enumerate(zip(inputs, outputs)):
        input_args = input_args.decode("utf-8")
        output = output.decode("utf-8")
        print(f"{method_name}(*{input_args}) -> {output}")


class Cache:
    """
    A class to store data in a cache
    """

    def __init__(self):
        """
        Initialize the cache
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in the cache and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None,
    ) -> Union[
        str,
        bytes,
        int,
        float,
        None,
    ]:
        """
        Retrieve the data from the cache using the given key.
        If a conversion function is provided, apply it to the retrieved data.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieve the data from the cache as a string using the given key.
        """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieve the data from the cache as an integer using the given key.
        """
        return self.get(key, int)
