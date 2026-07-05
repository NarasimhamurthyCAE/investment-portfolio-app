# =============================================================================
# File Name : data/network/rate_limiter.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Enterprise Rate Limiter
#
# Features
# --------
# ✓ Thread Safe
# ✓ Configurable Requests Per Second
# ✓ Configurable Burst Size
# ✓ Decorator Support
# ✓ Context Manager Support
#
# =============================================================================

from __future__ import annotations

import threading
import time
from collections import deque
from functools import wraps


class RateLimiter:
    """
    Sliding Window Rate Limiter
    """

    def __init__(
        self,
        max_requests: int = 5,
        period: float = 1.0
    ) -> None:

        self.max_requests = max_requests
        self.period = period

        self._lock = threading.Lock()

        self._timestamps = deque()

    # -------------------------------------------------------------------------
    # Wait
    # -------------------------------------------------------------------------

    def wait(self) -> None:

        with self._lock:

            now = time.monotonic()

            while (

                self._timestamps

                and

                now - self._timestamps[0] >= self.period

            ):

                self._timestamps.popleft()

            if len(self._timestamps) >= self.max_requests:

                sleep_time = (

                    self.period

                    -

                    (

                        now

                        -

                        self._timestamps[0]

                    )

                )

                if sleep_time > 0:

                    time.sleep(sleep_time)

                    now = time.monotonic()

                    while (

                        self._timestamps

                        and

                        now - self._timestamps[0] >= self.period

                    ):

                        self._timestamps.popleft()

            self._timestamps.append(

                time.monotonic()

            )

    # -------------------------------------------------------------------------
    # Decorator
    # -------------------------------------------------------------------------

    def limit(self):

        def decorator(function):

            @wraps(function)

            def wrapper(*args, **kwargs):

                self.wait()

                return function(

                    *args,

                    **kwargs

                )

            return wrapper

        return decorator

    # -------------------------------------------------------------------------
    # Context Manager
    # -------------------------------------------------------------------------

    def __enter__(self):

        self.wait()

        return self

    # -------------------------------------------------------------------------

    def __exit__(

        self,

        exc_type,

        exc,

        traceback

    ):

        return False


# =============================================================================
# Default Global Rate Limiters
# =============================================================================

MFAPI_LIMITER = RateLimiter(

    max_requests=3,

    period=1.0

)

NSE_LIMITER = RateLimiter(

    max_requests=2,

    period=1.0

)

YAHOO_LIMITER = RateLimiter(

    max_requests=5,

    period=1.0

)

MONEYCONTROL_LIMITER = RateLimiter(

    max_requests=2,

    period=1.0

)