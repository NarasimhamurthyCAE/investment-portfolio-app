# =============================================================================
# File Name : data/orchestrator/market_data_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Central Market Data Service
#
# Responsibilities
# ----------------
# ✓ Provider selection
# ✓ Latest NAV
# ✓ Historical NAV
# ✓ Scheme Information
# ✓ Future provider failover
#
# IMPORTANT
# ---------
# No other module should directly call MFAPI, Yahoo, NSE etc.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from core.enums import AssetType

from data.providers.mfapi_provider import MFAPIProvider


class MarketDataService:

    """
    Central Market Data Service.

    All market data flows through this class.
    """

    def __init__(self):

        self.mfapi = MFAPIProvider()

        # Future Providers
        self.yahoo = None
        self.nse = None
        self.moneycontrol = None

    # -------------------------------------------------------------------------
    # Provider Selection
    # -------------------------------------------------------------------------

    def provider(

        self,

        asset_type: str

    ):

        if asset_type == AssetType.MUTUAL_FUND.value:

            return self.mfapi

        if asset_type == AssetType.ETF.value:

            if self.yahoo:

                return self.yahoo

        if asset_type == AssetType.STOCK.value:

            if self.yahoo:

                return self.yahoo

        raise ValueError(

            f"No provider configured for "

            f"{asset_type}"

        )

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(

        self,

        asset_type: str,

        symbol: str

    ) -> float:

        provider = self.provider(

            asset_type

        )

        return provider.latest_price(

            symbol

        )

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    def historical_data(

        self,

        asset_type: str,

        symbol: str,

        start_date=None,

        end_date=None

    ) -> pd.DataFrame:

        provider = self.provider(

            asset_type

        )

        return provider.historical_data(

            symbol,

            start_date,

            end_date

        )

    # -------------------------------------------------------------------------
    # Scheme Information
    # -------------------------------------------------------------------------

    def scheme_information(

        self,

        scheme_code: str

    ):

        return self.mfapi.scheme_information(

            scheme_code

        )

    # -------------------------------------------------------------------------
    # Validate Instrument
    # -------------------------------------------------------------------------

    def validate(

        self,

        asset_type: str,

        symbol: str

    ) -> bool:

        provider = self.provider(

            asset_type

        )

        return provider.validate(

            symbol

        )

    # -------------------------------------------------------------------------
    # Provider Health
    # -------------------------------------------------------------------------

    def health(self):

        return {

            "MFAPI":

            self.mfapi.ping(),

            "Yahoo":

            None if self.yahoo is None

            else self.yahoo.ping(),

            "NSE":

            None if self.nse is None

            else self.nse.ping(),

            "Moneycontrol":

            None if self.moneycontrol is None

            else self.moneycontrol.ping()

        }


# =============================================================================
# Global Singleton
# =============================================================================

market_data = MarketDataService()