# =============================================================================
# File Name : assets/services/assets_master_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Assets Master Service
#
# Business layer for all master assets.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.repositories.assets_master_repository import (
    AssetsMasterRepository,
)


class AssetsMasterService:
    """
    Business logic for Asset Master.
    """

    def __init__(self):

        self.repository = AssetsMasterRepository()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        asset_type: str,
        keyword: str,
    ) -> pd.DataFrame:

        keyword = keyword.strip()

        if len(keyword) < 2:

            return pd.DataFrame()

        return self.repository.search(
            asset_type,
            keyword,
        )

    # -------------------------------------------------------------------------
    # By Symbol
    # -------------------------------------------------------------------------

    def by_symbol(
        self,
        symbol: str,
    ):

        return self.repository.by_symbol(symbol)

    # -------------------------------------------------------------------------
    # Add Asset
    # -------------------------------------------------------------------------

    def add_asset(
        self,
        data: dict,
    ):

        return self.repository.insert_asset(data)

    # -------------------------------------------------------------------------
    # Bulk Import
    # -------------------------------------------------------------------------

    def bulk_import(
        self,
        dataframe: pd.DataFrame,
    ):

        self.repository.bulk_insert(dataframe)