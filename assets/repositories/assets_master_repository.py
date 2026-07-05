# =============================================================================
# File Name : assets/repositories/assets_master_repository.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Repository for Assets Master
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class AssetsMasterRepository(BaseRepository):

    TABLE_NAME = "assets_master"

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        asset_type: str,
        keyword: str,
        limit: int = 25
    ) -> pd.DataFrame:

        query = """
        SELECT *

        FROM assets_master

        WHERE

            asset_type = %s

            AND is_active = TRUE

            AND (

                asset_name ILIKE %s

                OR UPPER(symbol) LIKE UPPER(%s)

            )

        ORDER BY asset_name

        LIMIT %s
        """

        keyword = f"%{keyword}%"

        return self.fetch_dataframe(
            query,
            (
                asset_type,
                keyword,
                keyword,
                limit,
            ),
        )

    # -------------------------------------------------------------------------
    # By Symbol
    # -------------------------------------------------------------------------

    def by_symbol(
        self,
        symbol: str
    ):

        query = """
        SELECT *

        FROM assets_master

        WHERE symbol = %s

        LIMIT 1
        """

        return self.fetch_one(
            query,
            (symbol,),
        )

    # -------------------------------------------------------------------------
    # Insert
    # -------------------------------------------------------------------------

    def insert_asset(
        self,
        data: dict
    ):

        return self.insert(data)

    # -------------------------------------------------------------------------
    # Bulk Insert
    # -------------------------------------------------------------------------

    def bulk_insert(
        self,
        dataframe: pd.DataFrame
    ):

        for _, row in dataframe.iterrows():

            self.insert(row.to_dict())