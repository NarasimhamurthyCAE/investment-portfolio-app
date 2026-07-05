# =============================================================================
# File Name : analytics/portfolio_analytics.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Analytics Facade
#
# Single entry point for all portfolio analytics.
#
# Responsibilities
# ----------------
# ✓ Asset Allocation
# ✓ Category Allocation
# ✓ AMC Allocation
# ✓ Sector Allocation
# ✓ Country Allocation
# ✓ Market Cap Allocation
# ✓ Benchmark Allocation
# ✓ Returns
# ✓ CAGR
# ✓ XIRR
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from analytics.allocation.amc_allocation import AMCAllocationEngine
from analytics.allocation.asset_allocation import AssetAllocationEngine
from analytics.allocation.benchmark_allocation import BenchmarkAllocationEngine
from analytics.allocation.category_allocation import CategoryAllocationEngine
from analytics.allocation.country_allocation import CountryAllocationEngine
from analytics.allocation.marketcap_allocation import MarketCapAllocationEngine
from analytics.allocation.sector_allocation import SectorAllocationEngine

from analytics.cagr_engine import CAGRCalculator
from analytics.return_engine import ReturnEngine
from analytics.xirr_engine import XIRREngine


class PortfolioAnalytics:
    """
    Portfolio Analytics Facade
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(
        self,
        portfolio: pd.DataFrame
    ):

        self.portfolio = portfolio

    # -------------------------------------------------------------------------
    # Allocation Engines
    # -------------------------------------------------------------------------

    def asset_allocation(self):

        return AssetAllocationEngine.calculate(

            self.portfolio

        )

    def category_allocation(self):

        return CategoryAllocationEngine.calculate(

            self.portfolio

        )

    def amc_allocation(self):

        return AMCAllocationEngine.calculate(

            self.portfolio

        )

    def sector_allocation(self):

        return SectorAllocationEngine.calculate(

            self.portfolio

        )

    def country_allocation(self):

        return CountryAllocationEngine.calculate(

            self.portfolio

        )

    def marketcap_allocation(self):

        return MarketCapAllocationEngine.calculate(

            self.portfolio

        )

    def benchmark_allocation(self):

        return BenchmarkAllocationEngine.calculate(

            self.portfolio

        )

    # -------------------------------------------------------------------------
    # Portfolio Totals
    # -------------------------------------------------------------------------

    def total_investment(self):

        if self.portfolio.empty:

            return 0.0

        return round(

            self.portfolio["amount"].sum(),

            2

        )

    def total_current_value(self):

        if self.portfolio.empty:

            return 0.0

        return round(

            self.portfolio["current_value"].sum(),

            2

        )

    def total_profit(self):

        invested = self.total_investment()

        current = self.total_current_value()

        return ReturnEngine.profit(

            invested,

            current

        )

    def total_return_percent(self):

        invested = self.total_investment()

        current = self.total_current_value()

        return ReturnEngine.return_percent(

            invested,

            current

        )

    # -------------------------------------------------------------------------
    # CAGR
    # -------------------------------------------------------------------------

    def portfolio_cagr(

        self,

        years: float

    ):

        return CAGRCalculator.calculate(

            self.total_investment(),

            self.total_current_value(),

            years

        )

    # -------------------------------------------------------------------------
    # XIRR
    # -------------------------------------------------------------------------

    def portfolio_xirr(

        self,

        cashflows

    ):

        return XIRREngine.portfolio_xirr(

            cashflows

        )

    # -------------------------------------------------------------------------
    # Dashboard Summary
    # -------------------------------------------------------------------------

    def summary(

        self,

        years: float = 1.0,

        cashflows=None

    ) -> dict:

        result = {

            "investment":

            self.total_investment(),

            "current_value":

            self.total_current_value(),

            "profit":

            self.total_profit(),

            "return_percent":

            self.total_return_percent()

        }

        result["cagr"] = (

            self.portfolio_cagr(

                years

            )

        )

        if cashflows:

            result["xirr"] = (

                self.portfolio_xirr(

                    cashflows

                )

            )

        else:

            result["xirr"] = None

        return result

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(

        self,

        n: int = 10

    ):

        if self.portfolio.empty:

            return pd.DataFrame()

        return (

            self.portfolio

            .sort_values(

                "current_value",

                ascending=False

            )

            .head(n)

        )