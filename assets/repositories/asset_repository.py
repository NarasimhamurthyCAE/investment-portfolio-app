# =============================================================================
# File Name : assets/repositories/asset_repository.py
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class AssetRepository(BaseRepository):
    TABLE_NAME = "assets"

    # -------------------------------------------------------------------------
    # Get Asset by Symbol
    # -------------------------------------------------------------------------

    def get_by_symbol(
        self,
        symbol: str,
    ):
        """
        Returns asset by stock / ETF symbol.
        """

        query = """
        SELECT *
        FROM assets
        WHERE UPPER(symbol)=UPPER(%s)
        LIMIT 1
        """

        return self.fetch_one(
            query,
            (
                symbol,
            ),
        )

    # -------------------------------------------------------------------------
    # Get Asset by Scheme Code
    # -------------------------------------------------------------------------

    def get_by_scheme_code(
        self,
        scheme_code: str,
    ):
        """
        Returns asset by mutual fund scheme code.
        """

        query = """
        SELECT *
        FROM assets
        WHERE scheme_code=%s
        LIMIT 1
        """

        return self.fetch_one(
            query,
            (
                scheme_code,
            ),
        )

    # -------------------------------------------------------------------------
    # Create Asset
    # -------------------------------------------------------------------------

    def create(
        self,
        asset: dict,
    ) -> int:
        """
        Creates asset and returns asset_id.
        """

        query = """
        INSERT INTO assets
        (
            asset_type,
            asset_name,
            symbol,
            scheme_code,
            exchange,
            currency,
            sector,
            industry,
            isin,
            provider,
            provider_symbol
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        RETURNING asset_id
        """

        row = self.fetch_one(
            query,
            (
                asset.get("asset_type"),
                asset.get("asset_name"),
                asset.get("symbol"),
                asset.get("scheme_code"),
                asset.get("exchange"),
                asset.get("currency"),
                asset.get("sector"),
                asset.get("industry"),
                asset.get("isin"),
                asset.get("provider"),
                asset.get("provider_symbol"),
            ),
        )

        return row["asset_id"]


    # -------------------------------------------------------------------------
    # Update Metadata
    # -------------------------------------------------------------------------

    def update_metadata(
        self,
        asset_id: int,
        asset: dict,
    ) -> None:
        """
        Update asset metadata after refreshing from Yahoo.
        """

        query = """
        UPDATE assets
        SET

            asset_name=%s,

            exchange=%s,

            currency=%s,

            sector=%s,

            industry=%s,

            isin=%s,

            provider=%s,

            provider_symbol=%s,

            last_metadata_refresh=%s,

            updated_at=CURRENT_TIMESTAMP

        WHERE asset_id=%s
        """

        self.execute(

            query,

            (

                asset.get("asset_name"),

                asset.get("exchange"),

                asset.get("currency"),

                asset.get("sector"),

                asset.get("industry"),

                asset.get("isin"),

                asset.get("provider"),

                asset.get("provider_symbol"),

                asset.get("last_metadata_refresh"),

                asset_id,

            ),

        )

    # -------------------------------------------------------------------------
    # Find Or Create Asset
    # -------------------------------------------------------------------------

    def find_or_create(
        self,
        asset: dict,
    ) -> int:
        """
        Returns existing asset_id or creates a new asset.
        """

        asset_type = asset.get("asset_type")

        if asset_type == "MUTUAL_FUND":

            row = self.get_by_scheme_code(
                asset.get("scheme_code")
            )

        else:

            row = self.get_by_symbol(
                asset.get("symbol")
            )

        if row:

            self.update_metadata(

                row["asset_id"],

                asset,

            )

            return row["asset_id"]

        return self.create(asset)

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int,
    ) -> pd.DataFrame:

        query = """
        SELECT

            i.investment_id,

            a.asset_id,

            a.asset_name,

            a.asset_type,

            a.symbol,

            a.category,

            a.subcategory,

            i.portfolio_name,

            i.broker,

            i.account_name,

            i.notes,

            i.is_active,

            i.created_at

        FROM investments i

        INNER JOIN assets a

            ON i.asset_id = a.asset_id

        WHERE

            i.user_id = %s

            AND i.is_active = TRUE

        ORDER BY

            a.asset_name
        """

        return self.fetch_dataframe(
            query,
            (user_id,),
        )

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        user_id: int,
        keyword: str,
    ) -> pd.DataFrame:

        query = """
        SELECT

            i.investment_id,

            a.*

        FROM investments i

        INNER JOIN assets a

            ON i.asset_id = a.asset_id

        WHERE

            i.user_id=%s

            AND

            (

                a.asset_name ILIKE %s

                OR

                a.symbol ILIKE %s

            )

        ORDER BY

            a.asset_name
        """

        like = f"%{keyword}%"

        return self.fetch_dataframe(
            query,
            (
                user_id,
                like,
                like,
            ),
        )

    # -------------------------------------------------------------------------
    # Asset Types
    # -------------------------------------------------------------------------

    def asset_types(self):

        query = """
        SELECT DISTINCT

            asset_type

        FROM assets

        ORDER BY asset_type
        """

        rows = self.fetch_all(query)

        return [

            row["asset_type"]

            for row in rows

        ]

    # -------------------------------------------------------------------------
    # By Asset Type
    # -------------------------------------------------------------------------

    def by_asset_type(
        self,
        user_id: int,
        asset_type: str,
    ):

        query = """
        SELECT

            i.investment_id,

            a.*

        FROM investments i

        INNER JOIN assets a

            ON i.asset_id=a.asset_id

        WHERE

            i.user_id=%s

            AND

            a.asset_type=%s

        ORDER BY

            a.asset_name
        """

        return self.fetch_dataframe(
            query,
            (
                user_id,
                asset_type,
            ),
        )

    # -------------------------------------------------------------------------
    # By Investment ID
    # -------------------------------------------------------------------------

    def by_id(
        self,
        investment_id: int,
    ):

        query = """
        SELECT

            *

        FROM investments

        WHERE investment_id=%s
        """

        return self.fetch_one(
            query,
            (
                investment_id,
            ),
        )