# =============================================================================
# File Name : assets/engines/asset_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Asset Engine
#
# High-level business engine for Mutual Funds, ETFs and Stocks.
#
# Responsibilities
# ----------------
# ✓ Portfolio
# ✓ Search
# ✓ Summary
# ✓ Valuation
# ✓ Transactions
# ✓ Market Data
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.services.asset_service import AssetService
from assets.services.portfolio_service import PortfolioService
from assets.services.transaction_service import TransactionService
from assets.services.valuation_service import ValuationService


class AssetEngine:
    """
    Asset Engine

    Coordinates all asset-related services.
    """

    def __init__(self):

        self.asset_service = AssetService()

        self.portfolio_service = PortfolioService()

        self.transaction_service = TransactionService()

        self.valuation_service = ValuationService()

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int
    ) -> pd.DataFrame:

        return self.portfolio_service.portfolio(user_id)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def summary(
        self,
        user_id: int
    ) -> dict:

        return self.portfolio_service.summary(user_id)

    # -------------------------------------------------------------------------
    # Search Market
    # -------------------------------------------------------------------------

    def search_market(
        self,
        asset_type: str,
        keyword: str
    ) -> pd.DataFrame:

        return self.asset_service.search_market(
            asset_type,
            keyword
        )

    # -------------------------------------------------------------------------
    # Asset Filter
    # -------------------------------------------------------------------------

    def assets(
        self,
        user_id: int,
        asset_type: str
    ) -> pd.DataFrame:

        return self.asset_service.assets(
            user_id,
            asset_type
        )

    # -------------------------------------------------------------------------
    # Latest Price / NAV
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        asset_type: str,
        identifier: str
    ) -> float:

        return self.asset_service.latest_price(
            asset_type,
            identifier
        )

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    def historical_data(
        self,
        asset_type: str,
        identifier: str,
        start_date=None,
        end_date=None
    ):

        return self.asset_service.historical_data(
            asset_type,
            identifier,
            start_date,
            end_date
        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        asset_type: str,
        identifier: str
    ):

        return self.asset_service.metadata(
            asset_type,
            identifier
        )

    # -------------------------------------------------------------------------
    # Buy
    # -------------------------------------------------------------------------

    def buy(self, **kwargs):

        return self.transaction_service.buy(**kwargs)

    # -------------------------------------------------------------------------
    # Sell
    # -------------------------------------------------------------------------

    def sell(self, **kwargs):

        return self.transaction_service.sell(**kwargs)

    # -------------------------------------------------------------------------
    # Portfolio Summary
    # -------------------------------------------------------------------------

    def portfolio_summary(
        self,
        portfolio: pd.DataFrame
    ) -> dict:

        return self.valuation_service.portfolio_summary(
            portfolio
        )

    # -------------------------------------------------------------------------
    # Supported Assets
    # -------------------------------------------------------------------------

    def supported_assets(self):

        return self.asset_service.supported_assets()

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(
        self,
        user_id: int,
        limit: int = 10
    ) -> pd.DataFrame:

        return self.portfolio_service.top_holdings(
            user_id,
            limit
        )


    # -------------------------------------------------------------------------
    # Add Investment
    # -------------------------------------------------------------------------

    def add_investment(
        self,
        *,
        user_id: int,
        asset_type: str,
        identifier: str,
        investment_date,
        amount: float,
        price: float,
        charges: float = 0.0,
        remarks: str = "",
    ) -> int:
        """
        Creates a new investment together with its
        initial BUY transaction.
        """

        return self.asset_service.add_investment(

            user_id=user_id,

            asset_type=asset_type,

            identifier=identifier,

            investment_date=investment_date,

            amount=amount,

            price=price,

            charges=charges,

            remarks=remarks,

        )