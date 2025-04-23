import functools 
import time 
from core.logger import logger

def retry(max_retries = 5, backoff = 2, delay = 1):
    def wrapper(func):
        @functools.wraps(func)
        def core_logic(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func()
                except:
                    time.sleep(delay)
                    delay *= backoff
                    retries += 1
                    logger.error(f"Retrying {func.__name__} after {retries} retries.")
            raise RuntimeError(f"Function {func.__name__} failed after {max_retries}.")
        return core_logic
    return wrapper
            