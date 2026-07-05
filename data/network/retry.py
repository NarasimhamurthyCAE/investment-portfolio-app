# =============================================================================
# File Name : data/network/retry.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Retry Utility
#
# Features
# --------
# ✓ Exponential Backoff
# ✓ Configurable Retries
# ✓ Configurable Delay
# ✓ Logging
#
# =============================================================================

from __future__ import annotations

import time
from functools import wraps

import requests

from core.logger import get_logger


LOGGER = get_logger(__name__)


DEFAULT_RETRIES = 3

DEFAULT_DELAY = 1

BACKOFF_FACTOR = 2


def retry(
    retries: int = DEFAULT_RETRIES,
    delay: float = DEFAULT_DELAY,
    backoff: float = BACKOFF_FACTOR,
    exceptions=(
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.HTTPError,
    ),
):
    """
    Retry decorator.

    Example
    -------

    @retry()

    def fetch():
        ...
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            current_delay = delay

            last_exception = None

            for attempt in range(1, retries + 1):

                try:

                    return function(*args, **kwargs)

                except exceptions as exc:

                    last_exception = exc

                    LOGGER.warning(

                        "%s failed (attempt %d/%d). Retrying in %.1f sec",

                        function.__name__,

                        attempt,

                        retries,

                        current_delay,

                    )

                    if attempt == retries:

                        break

                    time.sleep(current_delay)

                    current_delay *= backoff

            LOGGER.exception(

                "Maximum retries exceeded."

            )

            raise last_exception

        return wrapper

    return decorator