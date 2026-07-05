# =============================================================================
# File Name : api/cache_manager.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# In-Memory Cache Manager
#
# Used by:
#   ✓ MFAPI
#   ✓ Yahoo Finance
#   ✓ NSE
#   ✓ MoneyControl
#
# =============================================================================

from __future__ import annotations

import threading
import time
from typing import Any


class CacheManager:
    """
    Simple thread-safe in-memory cache with TTL support.
    """

    def __init__(self):

        self._cache: dict[str, tuple[Any, float]] = {}

        self._lock = threading.Lock()

    # -------------------------------------------------------------------------
    # Get
    # -------------------------------------------------------------------------

    def get(self, key: str):

        with self._lock:

            if key not in self._cache:

                return None

            value, expiry = self._cache[key]

            if expiry < time.time():

                del self._cache[key]

                return None

            return value

    # -------------------------------------------------------------------------
    # Set
    # -------------------------------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
        ttl: int = 300,
    ):

        with self._lock:

            expiry = time.time() + ttl

            self._cache[key] = (

                value,

                expiry,

            )

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete(
        self,
        key: str,
    ):

        with self._lock:

            self._cache.pop(

                key,

                None,

            )

    # -------------------------------------------------------------------------
    # Clear
    # -------------------------------------------------------------------------

    def clear(self):

        with self._lock:

            self._cache.clear()

    # -------------------------------------------------------------------------
    # Contains
    # -------------------------------------------------------------------------

    def contains(
        self,
        key: str,
    ) -> bool:

        return self.get(key) is not None

    # -------------------------------------------------------------------------
    # Size
    # -------------------------------------------------------------------------

    def size(self) -> int:

        with self._lock:

            return len(self._cache)


# -----------------------------------------------------------------------------
# Singleton Cache
# -----------------------------------------------------------------------------

cache = CacheManager()