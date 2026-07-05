# =============================================================================
# File Name : portfolio/repositories/portfolio_query_repository.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class PortfolioQueryRepository(BaseRepository):

    TABLE_NAME = "transactions"
    
    """
    Read-only repository for Portfolio module.

    Responsibilities
    ----------------
    ✓ Load portfolio transactions
    ✓ Join Assets
    ✓ Join Investments
    ✓ Join Transactions

    This repository NEVER performs:

    ✗ Holdings calculation
    ✗ Average cost calculation
    ✗ Profit/Loss calculation
    ✗ XIRR calculation
    ✗ Allocation calculation

    Those belong to HoldingsEngine.
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        super().__init__()

    # -------------------------------------------------------------------------
    # Portfolio Transactions
    # -------------------------------------------------------------------------

    def load_transactions(
        self,
        user_id: int = 1,
    ) -> pd.DataFrame:

        query = """

        SELECT

            ----------------------------------------------------------------
            -- Investment
            ----------------------------------------------------------------

            i.investment_id,
            i.portfolio_name,
            i.account_name,
            i.broker,
            i.is_active,

            ----------------------------------------------------------------
            -- Asset
            ----------------------------------------------------------------

            a.asset_id,
            a.asset_name,
            a.asset_type,
            a.symbol,
            a.category,
            a.subcategory,

            ----------------------------------------------------------------
            -- Transaction
            ----------------------------------------------------------------

            t.transaction_id,
            t.transaction_type,
            t.transaction_date,

            t.units,
            t.price,
            t.amount,
            t.charges,
            t.taxes,
            t.currency,

            t.reference_number,
            t.remarks

        FROM investments i

        INNER JOIN assets a

            ON a.asset_id = i.asset_id

        INNER JOIN transactions t

            ON t.investment_id = i.investment_id

        WHERE

            i.user_id=%s

            AND

            i.is_active=TRUE

        ORDER BY

            a.asset_name,

            t.transaction_date,

            t.transaction_id

        """

        return self.fetch_dataframe(

            query,

            (user_id,)

        )