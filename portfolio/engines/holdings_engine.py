# =============================================================================
# File Name : portfolio/engines/holdings_engine.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

from collections import defaultdict

import pandas as pd

from portfolio.models.portfolio_holding import PortfolioHolding


class HoldingsEngine:
    """
    Portfolio Holdings Calculation Engine

    Responsibilities
    ----------------
    ✓ Process transaction history
    ✓ Calculate current holdings
    ✓ Calculate average cost
    ✓ Calculate invested value

    NOT responsible for

    ✗ Market prices
    ✗ XIRR
    ✗ Benchmark
    ✗ Allocation
    ✗ Tax
    """

    # ------------------------------------------------------------------
    # Build Holdings
    # ------------------------------------------------------------------

    @staticmethod
    def build(
        transactions: pd.DataFrame,
    ) -> list[PortfolioHolding]:

        if transactions.empty:
            return []

        holdings: dict[int, PortfolioHolding] = {}

        grouped = transactions.groupby("investment_id")

        for investment_id, df in grouped:

            df = df.sort_values(
                [
                    "transaction_date",
                    "transaction_id",
                ]
            )

            first = df.iloc[0]

            units = 0.0

            invested = 0.0

            for _, row in df.iterrows():

                transaction_type = (
                    str(row["transaction_type"])
                    .upper()
                    .strip()
                )

                qty = float(row["units"])

                amount = float(row["amount"])

                # ----------------------------------------------------------
                # BUY
                # ----------------------------------------------------------

                if transaction_type == "BUY":

                    units += qty

                    invested += amount

                # ----------------------------------------------------------
                # SELL
                #
                # Will be implemented in Phase-2
                # ----------------------------------------------------------

                elif transaction_type == "SELL":

                    pass

            average_cost = 0.0

            if units > 0:

                average_cost = invested / units

            holdings[investment_id] = PortfolioHolding(

                investment_id=investment_id,

                asset_id=first["asset_id"],

                asset_name=first["asset_name"],

                asset_type=first["asset_type"],

                symbol=first["symbol"],

                category=first["category"],

                subcategory=first["subcategory"],

                portfolio_name=first["portfolio_name"],

                account_name=first["account_name"],

                broker=first["broker"],

                units=units,

                average_cost=average_cost,

                invested_value=invested,

                current_price=0.0,

                current_value=0.0,

                profit_loss=0.0,

                profit_loss_percent=0.0,

            )

        return list(holdings.values())