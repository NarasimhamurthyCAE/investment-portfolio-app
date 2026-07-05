# =============================================================================
# File Name : assets/services/stock_master_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Business Service for Stocks Master
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.repositories.stock_master_repository import (
    StockMasterRepository,
)


class StockMasterService:
    """
    Business logic for Stock Master.
    """

    def __init__(self):

        self.repository = StockMasterRepository()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> pd.DataFrame:

        keyword = keyword.strip()

        if len(keyword) < 2:

            return pd.DataFrame()

        return self.repository.search(keyword)

    # -------------------------------------------------------------------------
    # Get Stock by Symbol
    # -------------------------------------------------------------------------

    def by_symbol(
        self,
        symbol: str,
    ):

        return self.repository.by_symbol(symbol)

    # -------------------------------------------------------------------------
    # Add Stock
    # -------------------------------------------------------------------------

    def add_stock(
        self,
        data: dict,
    ):

        return self.repository.insert_stock(data)

    # -------------------------------------------------------------------------
    # Bulk Import
    # -------------------------------------------------------------------------

    def bulk_import(
        self,
        dataframe: pd.DataFrame,
    ):

        self.repository.bulk_insert(dataframe)

    # -------------------------------------------------------------------------
    # Reload Stock
    # -------------------------------------------------------------------------

    def reload(
        self,
        symbol: str,
    ):
        """
        Reload the latest stock information from stocks_master.

        Used after Metadata Engine refreshes sector, industry,
        market cap, etc.
        """

        return self.repository.by_symbol(

            symbol

        )