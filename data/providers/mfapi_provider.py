# =============================================================================
# File Name : data/providers/mfapi_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# MFAPI Provider
#
# Responsibilities
# ----------------
# ✓ Latest NAV
# ✓ NAV History
# ✓ Scheme Information
# ✓ Search (future)
#
# Uses
# ----
# HTTP Client
# Retry
# Rate Limiter
# Cache
#
# API
# ----
# https://api.mfapi.in/mf/<scheme_code>
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from core.logger import get_logger

from data.cache.cache_manager import GLOBAL_CACHE
from data.network.http_client import HTTPClient
from data.network.rate_limiter import MFAPI_LIMITER
from data.network.retry import retry

from data.providers.base_provider import BaseProvider


LOGGER = get_logger(__name__)


class MFAPIProvider(BaseProvider):

    provider_name = "MFAPI"

    BASE_URL = "https://api.mfapi.in/mf"

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.client = HTTPClient()

    # -------------------------------------------------------------------------
    # Latest NAV
    # -------------------------------------------------------------------------

    @retry()
    def latest_price(

        self,

        scheme_code: str

    ) -> float:

        cache_key = f"mf_latest_{scheme_code}"

        cached = GLOBAL_CACHE.get(cache_key)

        if cached is not None:

            return cached

        with MFAPI_LIMITER:

            url = (

                f"{self.BASE_URL}/"

                f"{scheme_code}"

            )

            data = self.client.get_json(url)

        nav = float(

            data["data"][0]["nav"]

        )

        GLOBAL_CACHE.set(

            cache_key,

            nav,

            ttl=3600

        )

        return nav

    # -------------------------------------------------------------------------
    # NAV History
    # -------------------------------------------------------------------------

    @retry()
    def historical_data(

        self,

        scheme_code: str,

        start_date=None,

        end_date=None

    ) -> pd.DataFrame:

        cache_key = (

            f"mf_history_{scheme_code}"

        )

        cached = GLOBAL_CACHE.get(

            cache_key

        )

        if cached is not None:

            return cached.copy()

        with MFAPI_LIMITER:

            url = (

                f"{self.BASE_URL}/"

                f"{scheme_code}"

            )

            data = self.client.get_json(

                url

            )

        history = pd.DataFrame(

            data["data"]

        )

        history["date"] = pd.to_datetime(

            history["date"],

            dayfirst=True,

            errors="coerce"

        )

        history["nav"] = (

            history["nav"]

            .astype(float)

        )

        history.sort_values(

            "date",

            inplace=True

        )

        if start_date is not None:

            history = history[

                history["date"]

                >=

                pd.to_datetime(start_date)

            ]

        if end_date is not None:

            history = history[

                history["date"]

                <=

                pd.to_datetime(end_date)

            ]

        history.reset_index(

            drop=True,

            inplace=True

        )

        GLOBAL_CACHE.set(

            cache_key,

            history,

            ttl=86400

        )

        return history.copy()

    # -------------------------------------------------------------------------
    # Scheme Information
    # -------------------------------------------------------------------------

    @retry()
    def scheme_information(

        self,

        scheme_code: str

    ) -> dict:

        cache_key = (

            f"mf_info_{scheme_code}"

        )

        cached = GLOBAL_CACHE.get(

            cache_key

        )

        if cached is not None:

            return cached

        with MFAPI_LIMITER:

            url = (

                f"{self.BASE_URL}/"

                f"{scheme_code}"

            )

            data = self.client.get_json(

                url

            )

        info = {

            "scheme_code": scheme_code,

            "scheme_name": data.get(

                "meta",

                {}

            ).get(

                "scheme_name",

                ""

            ),

            "fund_house": data.get(

                "meta",

                {}

            ).get(

                "fund_house",

                ""

            ),

            "scheme_type": data.get(

                "meta",

                {}

            ).get(

                "scheme_type",

                ""

            ),

            "scheme_category": data.get(

                "meta",

                {}

            ).get(

                "scheme_category",

                ""

            )

        }

        GLOBAL_CACHE.set(

            cache_key,

            info,

            ttl=86400

        )

        return info

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(

        self,

        keyword: str

    ) -> list:

        raise NotImplementedError(

            "MFAPI does not provide search."

        )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(

        self,

        scheme_code: str

    ) -> bool:

        try:

            self.latest_price(

                scheme_code

            )

            return True

        except Exception:

            return False

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    def ping(self) -> bool:

        return self.client.ping(

            "https://api.mfapi.in"

        )