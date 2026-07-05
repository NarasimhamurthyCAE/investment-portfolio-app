# =============================================================================
# File Name : assets/services/valuation_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Valuation Service
#
# Calculates valuation metrics for
# Mutual Funds, ETFs and Stocks.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from analytics.return_engine import ReturnEngine
from analytics.cagr_engine import CAGRCalculator
from analytics.xirr_engine import XIRREngine


class ValuationService:
    """
    Portfolio Valuation Service
    """

    # -------------------------------------------------------------------------
    # Current Value
    # -------------------------------------------------------------------------

    @staticmethod
    def current_value(
        units: float,
        latest_price: float
    ) -> float:

        return ReturnEngine.current_value(
            units,
            latest_price
        )

    # -------------------------------------------------------------------------
    # Unrealized Profit
    # -------------------------------------------------------------------------

    @staticmethod
    def unrealized_profit(
        invested: float,
        current_value: float
    ) -> float:

        return ReturnEngine.profit(
            invested,
            current_value
        )

    # -------------------------------------------------------------------------
    # Return %
    # -------------------------------------------------------------------------

    @staticmethod
    def return_percent(
        invested: float,
        current_value: float
    ) -> float:

        return ReturnEngine.return_percent(
            invested,
            current_value
        )

    # -------------------------------------------------------------------------
    # CAGR
    # -------------------------------------------------------------------------

    @staticmethod
    def cagr(
        invested: float,
        current_value: float,
        years: float
    ) -> float:

        return CAGRCalculator.calculate(
            invested,
            current_value,
            years
        )

    # -------------------------------------------------------------------------
    # XIRR
    # -------------------------------------------------------------------------

    @staticmethod
    def xirr(
        cashflows
    ) -> float:

        return XIRREngine.portfolio_xirr(
            cashflows
        )

    # -------------------------------------------------------------------------
    # Daily Change
    # -------------------------------------------------------------------------

    @staticmethod
    def daily_change(
        previous_price: float,
        latest_price: float,
        units: float
    ) -> dict:

        if previous_price <= 0:

            return {

                "change": 0.0,

                "change_percent": 0.0

            }

        change = (

            latest_price

            - previous_price

        ) * units

        change_percent = (

            (

                latest_price

                - previous_price

            )

            / previous_price

            * 100

        )

        return {

            "change": round(change, 2),

            "change_percent": round(change_percent, 2)

        }

    # -------------------------------------------------------------------------
    # Portfolio Weight
    # -------------------------------------------------------------------------

    @staticmethod
    def portfolio_weight(
        asset_value: float,
        portfolio_value: float
    ) -> float:

        if portfolio_value <= 0:

            return 0.0

        return round(

            asset_value

            / portfolio_value

            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Complete Summary
    # -------------------------------------------------------------------------

    @classmethod
    def summary(
        cls,
        invested: float,
        units: float,
        latest_price: float,
        years: float,
        cashflows=None
    ) -> dict:

        current = cls.current_value(
            units,
            latest_price
        )

        result = {

            "invested": invested,

            "current_value": current,

            "profit": cls.unrealized_profit(
                invested,
                current
            ),

            "return_percent": cls.return_percent(
                invested,
                current
            ),

            "cagr": cls.cagr(
                invested,
                current,
                years
            )

        }

        if cashflows:

            result["xirr"] = cls.xirr(
                cashflows
            )

        else:

            result["xirr"] = None

        return result

    # -------------------------------------------------------------------------
    # Portfolio Summary
    # -------------------------------------------------------------------------

    @classmethod
    def portfolio_summary(
        cls,
        portfolio: pd.DataFrame
    ) -> dict:

        holdings = 0 if portfolio.empty else len(portfolio)

        return {

            # Old UI compatibility
            "invested": 0.0,

            # New UI compatibility
            "investment": 0.0,

            "current_value": 0.0,

            "profit": 0.0,

            "return_percent": 0.0,

            "xirr": 0.0,

            "cagr": 0.0,

            "holdings": holdings
        }