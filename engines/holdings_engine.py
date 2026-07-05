# =============================================================================
# File Name : engines/holdings_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Holdings Engine
#
# Responsibilities
# ----------------
# ✓ Portfolio Holdings
# ✓ Top Holdings
# ✓ Duplicate Holdings
# ✓ Holdings Summary
# ✓ Portfolio Concentration
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.investment_query_repository import (
    InvestmentQueryRepository,
)


class HoldingsEngine:
    """
    Portfolio Holdings Engine
    """

    def __init__(self):

        self.repository = InvestmentQueryRepository()

    # -------------------------------------------------------------------------
    # Portfolio Holdings
    # -------------------------------------------------------------------------

    def holdings(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return self.repository.load_portfolio(
            user_id
        )

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(
        self,
        user_id: int = 1,
        n: int = 10
    ) -> pd.DataFrame:

        portfolio = self.holdings(user_id)

        if portfolio.empty:
            return portfolio

        return (

            portfolio

            .sort_values(

                "current_value",

                ascending=False

            )

            .head(n)

            .reset_index(drop=True)

        )

    # -------------------------------------------------------------------------
    # Holdings Count
    # -------------------------------------------------------------------------

    def count(
        self,
        user_id: int = 1
    ) -> int:

        return len(

            self.holdings(user_id)

        )

    # -------------------------------------------------------------------------
    # Total Value
    # -------------------------------------------------------------------------

    def total_value(
        self,
        user_id: int = 1
    ) -> float:

        portfolio = self.holdings(user_id)

        if portfolio.empty:

            return 0.0

        return round(

            portfolio["current_value"].sum(),

            2

        )

    # -------------------------------------------------------------------------
    # Largest Holding
    # -------------------------------------------------------------------------

    def largest(
        self,
        user_id: int = 1
    ):

        top = self.top_holdings(

            user_id,

            1

        )

        if top.empty:

            return None

        return top.iloc[0]

    # -------------------------------------------------------------------------
    # Duplicate Funds
    # -------------------------------------------------------------------------

    def duplicates(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        portfolio = self.holdings(user_id)

        if portfolio.empty:

            return pd.DataFrame()

        duplicate = (

            portfolio

            .groupby(

                "fund_name",

                dropna=False

            )

            .size()

            .reset_index(name="count")

        )

        duplicate = duplicate[

            duplicate["count"] > 1

        ]

        return duplicate.reset_index(drop=True)

    # -------------------------------------------------------------------------
    # Concentration
    # -------------------------------------------------------------------------

    def concentration(
        self,
        user_id: int = 1,
        top: int = 10
    ) -> float:

        portfolio = self.holdings(user_id)

        if portfolio.empty:

            return 0.0

        total = portfolio["current_value"].sum()

        if total == 0:

            return 0.0

        top_value = (

            portfolio

            .sort_values(

                "current_value",

                ascending=False

            )

            .head(top)

            ["current_value"]

            .sum()

        )

        return round(

            top_value

            / total

            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Holdings Summary
    # -------------------------------------------------------------------------

    def summary(
        self,
        user_id: int = 1
    ) -> dict:

        return {

            "holdings":

                self.count(user_id),

            "portfolio_value":

                self.total_value(user_id),

            "top10_concentration":

                self.concentration(

                    user_id,

                    top=10

                ),

            "duplicates":

                len(

                    self.duplicates(

                        user_id

                    )

                )

        }