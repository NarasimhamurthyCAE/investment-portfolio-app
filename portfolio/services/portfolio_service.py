# =============================================================================
# File Name : portfolio/services/portfolio_service.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.providers.stock_provider import StockProvider
from portfolio.engines.holdings_engine import HoldingsEngine
from portfolio.repositories.portfolio_query_repository import (
    PortfolioQueryRepository,
)


class PortfolioService:
    """
    Portfolio Business Service

    Responsibilities
    ----------------
    ✓ Load portfolio transactions
    ✓ Build holdings
    ✓ Fetch latest market prices
    ✓ Calculate current portfolio values

    No UI.
    No SQL.
    """

    # ---------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------

    def __init__(self):

        self.repository = PortfolioQueryRepository()

        self.stock_provider = StockProvider()

    # ---------------------------------------------------------------------
    # Portfolio
    # ---------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int = 1,
    ) -> pd.DataFrame:

        transactions = self.repository.load_transactions(
            user_id
        )

        holdings = HoldingsEngine.build(
            transactions
        )

        rows = []

        for holding in holdings:

            # -------------------------------------------------------------
            # Latest Price
            # -------------------------------------------------------------

            try:

                current_price = self.stock_provider.latest_price(
                    holding.symbol
                )

            except Exception:

                current_price = 0.0

            # -------------------------------------------------------------
            # Portfolio Values
            # -------------------------------------------------------------

            holding.current_price = current_price

            holding.current_value = (

                holding.units

                * current_price

            )

            holding.profit_loss = (

                holding.current_value

                - holding.invested_value

            )

            if holding.invested_value > 0:

                holding.profit_loss_percent = (

                    holding.profit_loss

                    / holding.invested_value

                    * 100

                )

            rows.append(

                {

                    "investment_id": holding.investment_id,

                    "asset_id": holding.asset_id,

                    "asset_name": holding.asset_name,

                    "asset_type": holding.asset_type,

                    "symbol": holding.symbol,

                    "category": holding.category,

                    "subcategory": holding.subcategory,

                    "portfolio_name": holding.portfolio_name,

                    "account_name": holding.account_name,

                    "broker": holding.broker,

                    "units": holding.units,

                    "average_cost": holding.average_cost,

                    "invested_value": holding.invested_value,

                    "current_price": holding.current_price,

                    "current_value": holding.current_value,

                    "profit_loss": holding.profit_loss,

                    "profit_loss_percent": holding.profit_loss_percent,

                }

            )

        return pd.DataFrame(rows)

    # ---------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------

    def summary(
        self,
        user_id: int = 1,
    ) -> dict:

        portfolio = self.portfolio(user_id)

        if portfolio.empty:

            return {

                "invested_value": 0.0,

                "current_value": 0.0,

                "profit_loss": 0.0,

                "profit_loss_percent": 0.0,

                "holdings": 0,

            }

        invested = portfolio["invested_value"].sum()

        current = portfolio["current_value"].sum()

        profit = current - invested

        percent = 0.0

        if invested > 0:

            percent = profit / invested * 100

        return {

            # ---------------------------------------------------------
            # Legacy UI compatibility
            # ---------------------------------------------------------

            "invested": invested,

            "current_value": current,

            "profit": profit,

            "profit_percent": percent,

            "return_percent": percent,

            # ---------------------------------------------------------
            # New Portfolio Model
            # ---------------------------------------------------------

            "invested_value": invested,

            "profit_loss": profit,

            "profit_loss_percent": percent,

            "holdings": len(portfolio),

        }