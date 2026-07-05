# =============================================================================
# File Name : api/retry.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Retry Decorator
#
# Automatically retries failed API requests.
#
# =============================================================================

from __future__ import annotations

import logging
import time
from functools import wraps


logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions=(Exception,),
):
    """
    Retry decorator.

    Parameters
    ----------
    max_attempts : int
        Maximum retry attempts.

    delay : float
        Initial delay in seconds.

    backoff : float
        Delay multiplier.

    exceptions : tuple
        Exceptions to retry.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            current_delay = delay

            last_exception = None

            for attempt in range(1, max_attempts + 1):

                try:

                    return func(*args, **kwargs)

                except exceptions as ex:

                    last_exception = ex

                    logger.warning(

                        "%s failed (%s/%s): %s",

                        func.__name__,

                        attempt,

                        max_attempts,

                        ex,

                    )

                    if attempt == max_attempts:

                        break

                    time.sleep(current_delay)

                    current_delay *= backoff

            raise last_exception

        return wrapper

    return decorator