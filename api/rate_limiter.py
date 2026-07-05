# =============================================================================
# File Name : api/rate_limiter.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Rate Limiter
#
# Prevents excessive API requests.
#
# =============================================================================

from __future__ import annotations

import threading
import time


class RateLimiter:
    """
    Simple thread-safe rate limiter.

    Parameters
    ----------
    calls : int
        Maximum number of calls allowed.

    period : float
        Time period (seconds).
    """

    def __init__(
        self,
        calls: int = 5,
        period: float = 1.0,
    ):

        self.calls = calls
        self.period = period

        self.timestamps = []

        self.lock = threading.Lock()

    # -------------------------------------------------------------------------
    # Acquire
    # -------------------------------------------------------------------------

    def acquire(self):

        with self.lock:

            now = time.time()

            self.timestamps = [

                t

                for t in self.timestamps

                if now - t < self.period

            ]

            if len(self.timestamps) >= self.calls:

                sleep_time = self.period - (

                    now - self.timestamps[0]

                )

                if sleep_time > 0:

                    time.sleep(sleep_time)

                now = time.time()

                self.timestamps = [

                    t

                    for t in self.timestamps

                    if now - t < self.period

                ]

            self.timestamps.append(now)