# services/data_collector/src/utils/exceptions.py
from functools import wraps
import time
import logging
from typing import Type, Union

class DataCollectorException(Exception):
    """Base exception class for data collector"""
    pass

class APIRateLimitError(DataCollectorException):
    """Raised when hitting API rate limits"""
    pass

class ValidationError(DataCollectorException):
    """Raised when data validation fails"""
    pass

class ConnectionError(DataCollectorException):
    """Raised when connection issues occur"""
    pass 

def retry_with_backoff(
    retries: int = 3,
    backoff_in_seconds: int = 1,
    exceptions: Union[Type[Exception], tuple] = Exception
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retry_count += 1
                    if retry_count == retries:
                        raise
                    wait_time = (backoff_in_seconds * (2 ** (retry_count - 1)))
                    logging.warning(
                        f"Retry {retry_count}/{retries} for {func.__name__} "
                        f"after {wait_time}s. Error: {str(e)}"
                    )
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator