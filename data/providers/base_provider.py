# =============================================================================
# File Name : data/providers/base_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Abstract Market Data Provider
#
# Every external data provider must inherit this class.
#
# Examples
# --------
# MFAPI
# NSE
# Yahoo Finance
# Moneycontrol
# AlphaVantage
# TwelveData
# Polygon
#
# =============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd


class BaseProvider(ABC):

    """
    Abstract Market Data Provider
    """

    provider_name = "Base Provider"

    # -------------------------------------------------------------------------
    # Latest Price / NAV
    # -------------------------------------------------------------------------

    @abstractmethod
    def latest_price(

        self,

        symbol: str

    ) -> float:

        """
        Returns latest price.

        """

        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    @abstractmethod
    def historical_data(

        self,

        symbol: str,

        start_date=None,

        end_date=None

    ) -> pd.DataFrame:

        """
        Returns historical data.

        """

        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    @abstractmethod
    def search(

        self,

        keyword: str

    ) -> list:

        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Validate Symbol
    # -------------------------------------------------------------------------

    @abstractmethod
    def validate(

        self,

        symbol: str

    ) -> bool:

        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    @abstractmethod
    def ping(self) -> bool:

        raise NotImplementedError