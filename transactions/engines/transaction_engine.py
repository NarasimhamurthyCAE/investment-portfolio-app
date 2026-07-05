# =============================================================================
# File Name : transactions/engines/transaction_engine.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd


class TransactionEngine:
    """
    Business Engine for Transactions.

    Pure calculations.

    No SQL.
    No Streamlit.
    """

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    @staticmethod
    def summary(
        transactions: pd.DataFrame,
    ) -> dict:

        if transactions.empty:

            return {

                "total_transactions": 0,

                "total_investments": 0,

                "cash_invested": 0.0,

                "cash_withdrawn": 0.0,

                "gross_amount": 0.0,

                "charges": 0.0,

                "taxes": 0.0,

                "net_cash_flow": 0.0,

            }

        buy = transactions[
            transactions["transaction_type"]
            .str.upper()
            == "BUY"
        ]

        sell = transactions[
            transactions["transaction_type"]
            .str.upper()
            == "SELL"
        ]

        invested = buy["amount"].sum()

        withdrawn = sell["amount"].sum()

        charges = transactions["charges"].sum()

        taxes = transactions["taxes"].sum()

        net = transactions["net_cash_flow"].sum()

        return {

            "total_transactions": len(transactions),

            "total_investments":

                transactions["investment_id"]

                .nunique(),

            "cash_invested": invested,

            "cash_withdrawn": withdrawn,

            "gross_amount":

                transactions["amount"].sum(),

            "charges": charges,

            "taxes": taxes,

            "net_cash_flow": net,

        }

    # -------------------------------------------------------------------------
    # Investment Groups
    # -------------------------------------------------------------------------

    @staticmethod
    def investments(
        transactions: pd.DataFrame,
    ) -> dict:

        if transactions.empty:

            return {}

        groups = {}

        grouped = transactions.groupby(
            "investment_id",
            sort=False,
        )

        for investment_id, df in grouped:

            first = df.iloc[0]

            buy = df[
                df["transaction_type"]
                .str.upper()
                == "BUY"
            ]

            sell = df[
                df["transaction_type"]
                .str.upper()
                == "SELL"
            ]

            units = (

                buy["units"].sum()

                -

                sell["units"].sum()

            )

            invested = buy["amount"].sum()

            average_price = 0.0

            if buy["units"].sum() > 0:

                average_price = (

                    invested

                    /

                    buy["units"].sum()

                )

            groups[investment_id] = {

                "investment_id": investment_id,

                "asset_name":

                    first["asset_name"],

                "symbol":

                    first["symbol"],

                "industry":

                    first["industry"],

                "asset_type":

                    first["asset_type"],

                "portfolio_name":

                    first["portfolio_name"],

                "broker":

                    first["broker"],

                "shares_held":

                    units,

                "average_buy_price":

                    average_price,

                "invested":

                    invested,

                "transactions":

                    df.reset_index(drop=True),

            }

        return groups