# =============================================================================
# File Name : api/mfapi_client.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# MFAPI Client
#
# Wrapper around https://api.mfapi.in
#
# =============================================================================

from __future__ import annotations

import requests

import pandas as pd

from api.cache_manager import cache
from api.rate_limiter import RateLimiter
from api.retry import retry


class MFAPIClient:
    """
    Mutual Fund API Client.
    """

    BASE_URL = "https://api.mfapi.in"

    def __init__(self):

        self.session = requests.Session()

        self.rate_limiter = RateLimiter()

    # -------------------------------------------------------------------------
    # GET Request
    # -------------------------------------------------------------------------

    @retry()
    def _get(self, endpoint: str):

        self.rate_limiter.acquire()

        url = f"{self.BASE_URL}/{endpoint}"

        response = self.session.get(

            url,

            timeout=20

        )

        response.raise_for_status()

        return response.json()

    # -------------------------------------------------------------------------
    # Scheme Details
    # -------------------------------------------------------------------------

    def scheme_details(
        self,
        scheme_code: str
    ):

        cache_key = f"scheme:{scheme_code}"

        data = cache.get(cache_key)

        if data is not None:

            return data

        data = self._get(

            f"mf/{scheme_code}"

        )

        cache.set(

            cache_key,

            data,

            ttl=3600

        )

        return data

    # -------------------------------------------------------------------------
    # Latest NAV
    # -------------------------------------------------------------------------

    def latest_nav(
        self,
        scheme_code: str
    ):

        data = self.scheme_details(scheme_code)

        print(type(data))
        print(data)

        return 0.0

    # -------------------------------------------------------------------------
    # Historical NAV
    # -------------------------------------------------------------------------

    def historical_nav(
        self,
        scheme_code: str
    ):

        data = self.scheme_details(

            scheme_code

        )

        return data["data"]

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        scheme_code: str
    ):

        data = self.scheme_details(

            scheme_code

        )

        meta = data.get(

            "meta",

            {}

        )

        return {

            "scheme_code": scheme_code,

            "name": meta.get(

                "scheme_name",

                ""

            ),

            "fund_house": meta.get(

                "fund_house",

                ""

            ),

            "scheme_type": meta.get(

                "scheme_type",

                ""

            ),

            "scheme_category": meta.get(

                "scheme_category",

                ""

            ),

        }


        # -------------------------------------------------------------------------
    # Search Schemes
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
        limit: int = 25
    ):

        cache_key = "mf_scheme_list"

        schemes = cache.get(cache_key)

        if schemes is None:

            schemes = self._get("mf")

            cache.set(
                cache_key,
                schemes,
                ttl=86400  # 24 hours
            )

        keyword = keyword.lower().strip()

        results = []

        for scheme in schemes:

            name = scheme.get("schemeName", "")

            if keyword in name.lower():

                results.append({

                    "scheme_code": scheme.get("schemeCode"),

                    "scheme_name": name

                })

            if len(results) >= limit:

                break

        return pd.DataFrame(results)

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(
        self,
        scheme_code: str
    ) -> bool:

        try:

            self.scheme_details(

                scheme_code

            )

            return True

        except Exception:

            return False