# =============================================================================
# File Name : controllers/stock_controller.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.services.stock_service import StockService


class StockController:

    def __init__(self):

        self.service = StockService()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
    ):

        if not keyword:

            return []

        return self.service.search(
            keyword
        )

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        symbol: str
    ) -> float:

        return self.service.latest_price(symbol)

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        symbol: str
    ) -> dict:

        return self.service.metadata(symbol)

    # -------------------------------------------------------------------------
    # Save Investment
    # -------------------------------------------------------------------------

    def save(
        self,
        **kwargs
    ):

        return self.service.save(**kwargs)