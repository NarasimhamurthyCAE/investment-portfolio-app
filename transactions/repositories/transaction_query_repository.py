# =============================================================================
# File Name : transactions/repositories/transaction_query_repository.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class TransactionQueryRepository(BaseRepository):
    """
    Read-only repository for Transactions module.

    Responsibilities
    ----------------
    ✓ Load transactions
    ✓ Search transactions
    ✓ Reporting

    Never:

    ✗ Insert
    ✗ Update
    ✗ Delete

    Those belong to TransactionWriteRepository.
    """

    TABLE_NAME = "transactions"

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        super().__init__()

    # -------------------------------------------------------------------------
    # Load Transactions
    # -------------------------------------------------------------------------

    def load_transactions(
        self,
        user_id: int = 1,
    ) -> pd.DataFrame:

        query = """

        SELECT

            ------------------------------------------------------------------
            -- Transaction
            ------------------------------------------------------------------

            t.transaction_id,
            t.transaction_date,
            t.transaction_type,

            t.units,
            t.price,
            t.amount,

            t.charges,
            t.taxes,

            (t.amount + t.charges + t.taxes) AS gross_outflow,

            CASE

                WHEN UPPER(t.transaction_type)='BUY'

                    THEN -(t.amount+t.charges+t.taxes)

                ELSE

                    (t.amount-t.charges-t.taxes)

            END AS net_cash_flow,

            t.currency,
            t.reference_number,
            t.remarks,

            ------------------------------------------------------------------
            -- Investment
            ------------------------------------------------------------------

            i.investment_id,
            i.portfolio_name,
            i.account_name,
            i.broker,

            ------------------------------------------------------------------
            -- Asset
            ------------------------------------------------------------------

            a.asset_id,

            a.asset_name,

            a.symbol,

            a.asset_type,

            a.category,

            a.subcategory,

            a.industry,

            a.sector

        FROM transactions t

        INNER JOIN investments i

            ON i.investment_id=t.investment_id

        INNER JOIN assets a

            ON a.asset_id=i.asset_id

        WHERE

            i.user_id=%s

        ORDER BY

            a.asset_name,

            t.transaction_date DESC,

            t.transaction_id DESC;

        """

        return self.fetch_dataframe(

            query,

            (

                user_id,

            ),

        )