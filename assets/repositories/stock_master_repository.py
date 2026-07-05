# =============================================================================
# File Name : assets/repositories/stock_master_repository.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Repository for Stocks Master
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class StockMasterRepository(BaseRepository):

    TABLE_NAME = "stocks_master"

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
        limit: int = 25,
    ) -> pd.DataFrame:

        keyword = f"%{keyword}%"

        query = """
        SELECT *

        FROM stocks_master

        WHERE

            listing_status='ACTIVE'

            AND

            (

                company_name ILIKE %s

                OR

                symbol ILIKE %s

            )

        ORDER BY company_name

        LIMIT %s
        """

        return self.fetch_dataframe(

            query,

            (

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
        symbol: str,
    ):

        query = """
        SELECT *

        FROM stocks_master

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
    # Insert
    # -------------------------------------------------------------------------

    def insert_stock(
        self,
        data: dict,
    ):

        query = """
        INSERT INTO stocks_master
        (
            symbol,
            yahoo_symbol,
            company_name,
            isin,
            exchange,
            sector,
            industry,
            currency,
            country,
            market_cap,
            listing_status
        )
        VALUES
        (
            %(symbol)s,
            %(yahoo_symbol)s,
            %(company_name)s,
            %(isin)s,
            %(exchange)s,
            %(sector)s,
            %(industry)s,
            %(currency)s,
            %(country)s,
            %(market_cap)s,
            %(listing_status)s
        )
        ON CONFLICT (symbol)
        DO UPDATE SET

            yahoo_symbol   = EXCLUDED.yahoo_symbol,
            company_name   = EXCLUDED.company_name,
            isin           = EXCLUDED.isin,
            exchange       = EXCLUDED.exchange,
            sector         = EXCLUDED.sector,
            industry       = EXCLUDED.industry,
            currency       = EXCLUDED.currency,
            country        = EXCLUDED.country,
            market_cap     = EXCLUDED.market_cap,
            listing_status = EXCLUDED.listing_status,
            updated_at     = CURRENT_TIMESTAMP;
        """

        values = {
            "symbol": data.get("symbol"),
            "yahoo_symbol": data.get("yahoo_symbol", data.get("symbol")),
            "company_name": data.get("company_name"),
            "isin": data.get("isin"),
            "exchange": data.get("exchange"),
            "sector": data.get("sector"),
            "industry": data.get("industry"),
            "currency": data.get("currency", "INR"),
            "country": data.get("country", "India"),
            "market_cap": data.get("market_cap"),
            "listing_status": data.get("listing_status", "ACTIVE"),
        }

        self.execute(query, values)

    # -------------------------------------------------------------------------
    # Bulk Insert
    # -------------------------------------------------------------------------

    def bulk_insert(
        self,
        dataframe: pd.DataFrame,
    ):

        for _, row in dataframe.iterrows():

            self.insert_stock(row.to_dict())