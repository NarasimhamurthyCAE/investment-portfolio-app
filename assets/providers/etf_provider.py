# =============================================================================
# File Name : assets/providers/etf_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# ETF Provider
#
# Wrapper around Yahoo/NSE clients.
#
# Responsibilities
# ----------------
# ✓ ETF Search
# ✓ Latest Price
# ✓ Historical Price
# ✓ Metadata
# ✓ Validation
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.providers.base_provider import BaseProvider

from api.yahoo_client import YahooClient
from api.nse_client import NSEClient


class ETFProvider(BaseProvider):

    PROVIDER_NAME = "Yahoo/NSE"

    def __init__(self):

        self.yahoo = YahooClient()

        self.nse = NSEClient()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str
    ) -> pd.DataFrame:

        return self.nse.search(keyword)

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        identifier: str
    ) -> float:

        try:

            return self.nse.latest_price(identifier)

        except Exception:

            return self.yahoo.latest_price(identifier)

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    def historical_data(
        self,
        identifier: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:

        try:

            return self.nse.historical_data(

                identifier,

                start_date,

                end_date

            )

        except Exception:

            return self.yahoo.historical_data(

                identifier,

                start_date,

                end_date

            )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(
        self,
        identifier: str
    ) -> bool:

        return self.nse.validate(identifier)

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        identifier: str
    ) -> dict:

        try:

            return self.nse.metadata(identifier)

        except Exception:

            return self.yahoo.metadata(identifier)