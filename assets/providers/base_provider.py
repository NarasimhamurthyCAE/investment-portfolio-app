# =============================================================================
# File Name : assets/providers/base_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Base Market Data Provider
#
# All providers inherit from this class.
#
# Supported Assets
# ----------------
# ✓ Mutual Funds
# ✓ ETFs
# ✓ Stocks
#
# =============================================================================

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd


class BaseProvider(ABC):
    """
    Base interface for all market data providers.
    """

    PROVIDER_NAME = "Unknown"

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    @abstractmethod
    def search(
        self,
        keyword: str
    ) -> pd.DataFrame:
        """
        Search assets.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Latest Price / NAV
    # -------------------------------------------------------------------------

    @abstractmethod
    def latest_price(
        self,
        identifier: str
    ) -> float:
        """
        Latest market price or NAV.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    @abstractmethod
    def historical_data(
        self,
        identifier: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        """
        Historical data.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    @abstractmethod
    def validate(
        self,
        identifier: str
    ) -> bool:
        """
        Check if asset exists.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    @abstractmethod
    def metadata(
        self,
        identifier: str
    ) -> dict:
        """
        Asset metadata.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    def health(self) -> dict:

        return {

            "provider": self.PROVIDER_NAME,

            "status": "Available"

        }

    # -------------------------------------------------------------------------
    # Name
    # -------------------------------------------------------------------------

    @property
    def name(self) -> str:

        return self.PROVIDER_NAME