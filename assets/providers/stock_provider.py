# =============================================================================
# File Name : assets/providers/stock_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Stock Provider
#
# Responsibilities
# ----------------
# ✓ Stock Search
# ✓ Latest Price
# ✓ Historical Price
# ✓ Company Information
# ✓ Sector
# ✓ Industry
# ✓ Market Cap
# ✓ Corporate Actions
#
# NOTE
# ----
# Data source implementation will be added later.
#
# =============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd
from api.yahoo_client import YahooClient


class BaseStockProvider(ABC):
    """
    Abstract base class for stock market providers.
    """

    @abstractmethod
    def search(self, keyword: str) -> pd.DataFrame:
        """
        Search stocks by symbol or company name.
        """
        raise NotImplementedError

    @abstractmethod
    def latest_price(self, symbol: str) -> float:
        """
        Get latest traded price.
        """
        raise NotImplementedError

    @abstractmethod
    def historical_prices(
        self,
        symbol: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        """
        Historical OHLCV data.
        """
        raise NotImplementedError

    @abstractmethod
    def company_profile(
        self,
        symbol: str,
    ) -> dict:
        """
        Company information.
        """
        raise NotImplementedError

    @abstractmethod
    def dividends(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        """
        Dividend history.
        """
        raise NotImplementedError

    @abstractmethod
    def splits(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        """
        Stock split history.
        """
        raise NotImplementedError

    @abstractmethod
    def bonus(self, symbol: str) -> pd.DataFrame:
        """
        Bonus issue history.
        """
        raise NotImplementedError

    @abstractmethod
    def rights(self, symbol: str) -> pd.DataFrame:
        """
        Rights issue history.
        """
        raise NotImplementedError


class StockProvider(BaseStockProvider):
    """
    Yahoo Finance Stock Provider
    """

    PROVIDER_NAME = "YAHOO"

    def __init__(self):

        self.client = YahooClient()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
    ) -> pd.DataFrame:

        """
        Temporary search.

        Yahoo Finance doesn't provide a searchable
        stock master.

        We'll connect this later with our
        stocks_master table.
        """

        return pd.DataFrame(
            [
                {
                    "symbol": keyword.upper(),
                    "company_name": keyword.upper(),
                    "exchange": "NSE",
                }
            ]
        )

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        symbol: str,
    ) -> float:

        return self.client.latest_price(
            symbol
        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        symbol: str,
    ) -> dict:

        return self.client.metadata(
            symbol
        )
        

    def historical_prices(
        self,
        symbol: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    def company_profile(
        self,
        symbol: str,
    ) -> dict:
        return {}

    def dividends(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    def splits(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    def bonus(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        return pd.DataFrame()

    def rights(
        self,
        symbol: str,
    ) -> pd.DataFrame:
        return pd.DataFrame()