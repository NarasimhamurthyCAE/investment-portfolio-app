# =============================================================================
# File Name : controllers/stock_master_controller.py
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.services.stock_master_service import StockMasterService

from core.metadata.services.metadata_service import MetadataService


class StockMasterController:

    def __init__(self):

        self.service = StockMasterService()

        self.metadata_service = MetadataService()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> pd.DataFrame:

        return self.service.search(keyword)

    # -------------------------------------------------------------------------
    # By Symbol
    # -------------------------------------------------------------------------

    def by_symbol(
        self,
        symbol: str,
    ):

        return self.service.by_symbol(symbol)

    # -------------------------------------------------------------------------
    # Import
    # -------------------------------------------------------------------------

    def import_master(
        self,
        dataframe: pd.DataFrame,
    ):

        self.service.bulk_import(dataframe)

    # -------------------------------------------------------------------------
    # Refresh Metadata
    # -------------------------------------------------------------------------

    def refresh_metadata(
        self,
        symbol: str,
    ):
        """
        Refresh metadata for a stock and return the latest metadata.
        """

        return self.metadata_service.refresh_if_required(

            symbol=symbol,

            asset_type="STOCK",

        )