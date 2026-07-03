"""Generic decorator/wrapper for exponential backoff and retry operations."""

from __future__ import annotations

import time
import functools
from typing import Callable, Any, Type, Tuple, Union
from streaming.logging import logger

def with_retry(
    max_retries: int = 3,
    initial_backoff_sec: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
) -> Callable:
    """Decorator to retry a function invocation with exponential backoff."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            retries = 0
            backoff = initial_backoff_sec
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logger.error(
                            f"Function '{func.__name__}' failed after {max_retries} attempts: {e}"
                        )
                        raise e
                    logger.warning(
                        f"Exception caught in '{func.__name__}': {e}. "
                        f"Retrying attempt {retries}/{max_retries} in {backoff:.2f} seconds..."
                    )
                    time.sleep(backoff)
                    backoff *= backoff_factor
        return wrapper
    return decorator
