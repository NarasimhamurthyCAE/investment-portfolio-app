# =============================================================================
# File Name : assets/services/stock_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Stock Service
#
# Business logic for Stocks.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.providers.stock_provider import StockProvider


class StockService:
    """
    Stock Business Service
    """

    def __init__(self):

        self.provider = StockProvider()

    # -------------------------------------------------------------------------
    # Search Stocks
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str
    ) -> pd.DataFrame:

        return self.provider.search(keyword)

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        symbol: str
    ) -> float:

        return self.provider.latest_price(symbol)

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        symbol: str
    ) -> dict:

        return self.provider.metadata(symbol)

    # -------------------------------------------------------------------------
    # Save Investment
    # -------------------------------------------------------------------------

    def save(
        self,
        **kwargs
    ):

        """
        Database save will be added later.
        """

        return kwargs