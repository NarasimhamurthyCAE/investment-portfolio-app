# =============================================================================
# File Name : engines/portfolio_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Engine
#
# Coordinates portfolio business workflows.
#
# Responsibilities
# ----------------
# ✓ Portfolio Summary
# ✓ Analytics
# ✓ Market Data
# ✓ Repository Access
# ✓ Dashboard Data
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from analytics.portfolio_analytics import PortfolioAnalytics

from repositories.investment_query_repository import (
    InvestmentQueryRepository,
)

from data.orchestrator.market_data_service import (
    market_data,
)


class PortfolioEngine:
    """
    Central Portfolio Engine
    """

    def __init__(self):

        self.repository = InvestmentQueryRepository()

    # -------------------------------------------------------------------------
    # Load Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return self.repository.load_portfolio(
            user_id
        )

    # -------------------------------------------------------------------------
    # Analytics
    # -------------------------------------------------------------------------

    def analytics(
        self,
        user_id: int = 1
    ) -> PortfolioAnalytics:

        df = self.portfolio(user_id)

        return PortfolioAnalytics(df)

    # -------------------------------------------------------------------------
    # Dashboard Summary
    # -------------------------------------------------------------------------

    def dashboard(
        self,
        user_id: int = 1,
        years: float = 1.0,
        cashflows=None
    ) -> dict:

        analytics = self.analytics(user_id)

        return analytics.summary(
            years=years,
            cashflows=cashflows
        )

    # -------------------------------------------------------------------------
    # Refresh NAV
    # -------------------------------------------------------------------------

    def refresh_nav(
        self,
        scheme_code: str
    ) -> float:

        return market_data.latest_price(
            "Mutual Fund",
            scheme_code
        )

    # -------------------------------------------------------------------------
    # Asset Allocation
    # -------------------------------------------------------------------------

    def asset_allocation(
        self,
        user_id: int = 1
    ):

        return self.analytics(
            user_id
        ).asset_allocation()

    # -------------------------------------------------------------------------
    # Category Allocation
    # -------------------------------------------------------------------------

    def category_allocation(
        self,
        user_id: int = 1
    ):

        return self.analytics(
            user_id
        ).category_allocation()

    # -------------------------------------------------------------------------
    # AMC Allocation
    # -------------------------------------------------------------------------

    def amc_allocation(
        self,
        user_id: int = 1
    ):

        return self.analytics(
            user_id
        ).amc_allocation()

    # -------------------------------------------------------------------------
    # Sector Allocation
    # -------------------------------------------------------------------------

    def sector_allocation(
        self,
        user_id: int = 1
    ):

        return self.analytics(
            user_id
        ).sector_allocation()

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(
        self,
        user_id: int = 1,
        n: int = 10
    ):

        return self.analytics(
            user_id
        ).top_holdings(n)