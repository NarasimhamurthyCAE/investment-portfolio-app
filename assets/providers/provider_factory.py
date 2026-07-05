# =============================================================================
# File Name : assets/providers/provider_factory.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Provider Factory
#
# Returns the correct provider for each asset class.
#
# =============================================================================

from __future__ import annotations

from assets.providers.mf_provider import MFProvider
from assets.providers.etf_provider import ETFProvider
from assets.providers.stock_provider import StockProvider


class ProviderFactory:

    _providers = {

        "MUTUAL_FUND": MFProvider(),

        "ETF": ETFProvider(),

        "STOCK": StockProvider(),

    }

    @classmethod
    def get(
        cls,
        asset_type: str
    ):

        asset_type = asset_type.upper()

        if asset_type not in cls._providers:

            raise ValueError(

                f"Unsupported asset type: {asset_type}"

            )

        return cls._providers[asset_type]

    @classmethod
    def supported_assets(cls):

        return list(

            cls._providers.keys()

        )