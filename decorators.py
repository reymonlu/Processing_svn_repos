import time
from typing import Any, Callable


def timer(func: Callable) -> Callable:
    """Add timer to a function

    Args:
        func (Callable): function to time

    Returns:
        Callable:
    """

    async def _wrapper(*args, **kwargs):
        start: float = time.time()
        func_result: Any = await func(*args, **kwargs)
        time_elapsed: float = time.time() - start
        return func_result, round(time_elapsed, 2)

    return _wrapper
