# stdlib
import time
import functools

"""
This is a decorator tends to calculate the execution time of a function.
"""


def timer(original_func):
    @functools.wraps(original_func)
    def time_wrapper(*args, **kwargs):
        start_time = time.time()
        result = original_func(*args, **kwargs)
        end_time = time.time() - start_time
        print(f"[Timer] Function '{original_func.__name__}' executed in {end_time:.4f}s")
        return result

    return time_wrapper
