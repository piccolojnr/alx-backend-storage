import redis
import requests
from functools import wraps
from typing import Callable


# Initialize the Redis client
redis_client = redis.Redis()


def cache_page(expiration: int):
    """
    Decorator to cache the result of a
    function for a given expiration time.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Track the URL access count
            redis_client.incr(f"count:{url}")

            # Try to get the cached result
            cached_result = redis_client.get(f"cache:{url}")
            if cached_result:
                return cached_result.decode("utf-8")

            # Fetch the page and cache the result
            result = func(url)
            redis_client.setex(f"cache:{url}", expiration, result)
            return result

        return wrapper

    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/\
        5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))

    # Check how many times the URL was accessed
    access_count = redis_client.get(f"count:{url}")
    print(f"The URL {url} was accessed {int(access_count)} times.")
