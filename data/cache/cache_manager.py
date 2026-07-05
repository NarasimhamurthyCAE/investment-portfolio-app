# =============================================================================
# File Name : data/cache/cache_manager.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Enterprise Cache Manager
#
# Features
# --------
# ✓ In-Memory Cache
# ✓ TTL (Time-To-Live)
# ✓ Thread Safe
# ✓ Cache Statistics
# ✓ Pattern Removal
# ✓ Manual Invalidation
#
# =============================================================================

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any


# =============================================================================
# Cache Entry
# =============================================================================

@dataclass(slots=True)
class CacheEntry:

    value: Any

    created_at: float

    ttl: int

    hits: int = 0

    @property
    def expired(self) -> bool:

        return (

            time.time()

            >

            self.created_at + self.ttl

        )


# =============================================================================
# Cache Manager
# =============================================================================

class CacheManager:

    def __init__(self):

        self._cache = {}

        self._lock = threading.RLock()

        self._hits = 0

        self._misses = 0

    # -------------------------------------------------------------------------
    # Set
    # -------------------------------------------------------------------------

    def set(

        self,

        key: str,

        value,

        ttl: int = 3600

    ):

        with self._lock:

            self._cache[key] = CacheEntry(

                value=value,

                created_at=time.time(),

                ttl=ttl

            )

    # -------------------------------------------------------------------------
    # Get
    # -------------------------------------------------------------------------

    def get(

        self,

        key: str,

        default=None

    ):

        with self._lock:

            entry = self._cache.get(key)

            if entry is None:

                self._misses += 1

                return default

            if entry.expired:

                del self._cache[key]

                self._misses += 1

                return default

            entry.hits += 1

            self._hits += 1

            return entry.value

    # -------------------------------------------------------------------------
    # Exists
    # -------------------------------------------------------------------------

    def exists(

        self,

        key: str

    ) -> bool:

        return self.get(key) is not None

    # -------------------------------------------------------------------------
    # Remove
    # -------------------------------------------------------------------------

    def remove(

        self,

        key: str

    ):

        with self._lock:

            self._cache.pop(

                key,

                None

            )

    # -------------------------------------------------------------------------
    # Clear
    # -------------------------------------------------------------------------

    def clear(self):

        with self._lock:

            self._cache.clear()

    # -------------------------------------------------------------------------
    # Remove Pattern
    # -------------------------------------------------------------------------

    def remove_pattern(

        self,

        pattern: str

    ):

        with self._lock:

            keys = [

                key

                for key

                in self._cache

                if pattern in key

            ]

            for key in keys:

                del self._cache[key]

    # -------------------------------------------------------------------------
    # Cache Size
    # -------------------------------------------------------------------------

    def size(self):

        return len(

            self._cache

        )

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def statistics(self):

        total = self._hits + self._misses

        hit_ratio = (

            0

            if total == 0

            else

            self._hits / total

        )

        return {

            "items": len(self._cache),

            "hits": self._hits,

            "misses": self._misses,

            "hit_ratio": round(

                hit_ratio,

                4

            )

        }

    # -------------------------------------------------------------------------
    # Cleanup Expired
    # -------------------------------------------------------------------------

    def cleanup(self):

        with self._lock:

            expired = [

                key

                for key, value

                in self._cache.items()

                if value.expired

            ]

            for key in expired:

                del self._cache[key]


# =============================================================================
# Global Cache
# =============================================================================

GLOBAL_CACHE = CacheManager()