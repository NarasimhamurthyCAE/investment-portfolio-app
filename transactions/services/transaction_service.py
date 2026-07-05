# =============================================================================
# File Name : transactions/services/transaction_service.py
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.providers.stock_provider import StockProvider
from transactions.engines.transaction_engine import TransactionEngine
from transactions.repositories.transaction_query_repository import (
    TransactionQueryRepository,
)


class TransactionService:

    def __init__(self):

        self.repository = TransactionQueryRepository()

        self.engine = TransactionEngine()

        self.provider = StockProvider()

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    def dashboard(
        self,
        user_id: int = 1,
    ) -> dict:

        transactions = self.repository.load_transactions(user_id)

        summary = self.engine.summary(transactions)

        investments = self.engine.investments(transactions)

        # ---------------------------------------------------------
        # Current Market Prices
        # ---------------------------------------------------------

        for investment in investments.values():

            try:

                price = self.provider.latest_price(

                    investment["symbol"]

                )

            except Exception:

                price = 0.0

            investment["current_price"] = price

            investment["current_value"] = (

                investment["shares_held"]

                * price

            )

            investment["gain"] = (

                investment["current_value"]

                - investment["invested"]

            )

            investment["return_percent"] = 0.0

            if investment["invested"] > 0:

                investment["return_percent"] = (

                    investment["gain"]

                    /

                    investment["invested"]

                    * 100

                )

        # ---------------------------------------------------------
        # Dashboard Totals
        # ---------------------------------------------------------

        summary["current_value"] = sum(

            x["current_value"]

            for x in investments.values()

        )

        summary["gain"] = (

            summary["current_value"]

            - summary["cash_invested"]

        )

        summary["return_percent"] = 0.0

        if summary["cash_invested"] > 0:

            summary["return_percent"] = (

                summary["gain"]

                /

                summary["cash_invested"]

                * 100

            )

        return {

            "summary": summary,

            "investments": investments,

            "transactions": transactions,

        }

    # -------------------------------------------------------------------------
    # Legacy
    # -------------------------------------------------------------------------

    def transactions(
        self,
        user_id: int = 1,
    ) -> pd.DataFrame:

        return self.dashboard(

            user_id

        )["transactions"]

    def search(
        self,
        keyword: str,
        user_id: int = 1,
    ):

        dashboard = self.dashboard(user_id)

        df = dashboard["transactions"]

        if df.empty:

            return dashboard

        keyword = keyword.lower()

        dashboard["transactions"] = df[

            df.astype(str)

            .apply(

                lambda row:

                row.str.lower()

                .str.contains(keyword)

            )

            .any(axis=1)

        ]

        return dashboard