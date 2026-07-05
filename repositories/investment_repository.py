# =============================================================================
# File Name : repositories/investment_repository.py
# Project   : Investment Portfolio App V2
# Module    : Repository Layer
# =============================================================================

from __future__ import annotations

from typing import Optional

import pandas as pd

from domain.investment import Investment
from repositories.base_repository import BaseRepository


class InvestmentRepository(BaseRepository):
    """
    Repository responsible for CRUD operations on the investments table.
    """

    TABLE_NAME = "investments"

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        super().__init__()

    # ------------------------------------------------------------------
    # Insert Investment
    # ------------------------------------------------------------------

    def insert(
        self,
        investment: Investment
    ) -> None:

        query = """
        INSERT INTO investments
        (
            user_id,
            date,
            fund_type,
            fund_name,
            transaction_type,
            amount,
            purchase_nav,
            nav_date,
            latest_nav,
            units,
            current_value,
            gain_loss,
            holding_years,
            cagr
        )
        VALUES
        (
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s
        )
        """

        params = (

            investment.user_id,

            investment.transaction_date,

            investment.fund_type,

            investment.fund_name,

            investment.transaction_type,

            investment.amount,

            investment.purchase_nav,

            investment.nav_date,

            investment.latest_nav,

            investment.units,

            investment.current_value,

            investment.gain_loss,

            investment.holding_years,

            investment.cagr

        )

        self.execute(
            query=query,
            params=params
        )

    # ------------------------------------------------------------------
    # Update Investment
    # ------------------------------------------------------------------

    def update(
        self,
        investment: Investment
    ) -> None:

        query = """
        UPDATE investments
        SET

            date=%s,

            fund_type=%s,

            fund_name=%s,

            transaction_type=%s,

            amount=%s,

            purchase_nav=%s,

            nav_date=%s,

            latest_nav=%s,

            units=%s,

            current_value=%s,

            gain_loss=%s,

            holding_years=%s,

            cagr=%s

        WHERE id=%s
        """

        params = (

            investment.transaction_date,

            investment.fund_type,

            investment.fund_name,

            investment.transaction_type,

            investment.amount,

            investment.purchase_nav,

            investment.nav_date,

            investment.latest_nav,

            investment.units,

            investment.current_value,

            investment.gain_loss,

            investment.holding_years,

            investment.cagr,

            investment.id

        )

        self.execute(
            query=query,
            params=params
        )

    # ------------------------------------------------------------------
    # Delete Investment
    # ------------------------------------------------------------------

    def delete_by_id(
        self,
        investment_id: int
    ) -> None:

        query = """
        DELETE
        FROM investments
        WHERE id=%s
        """

        self.execute(
            query,
            (investment_id,)
        )

    # ------------------------------------------------------------------
    # Get Investment
    # ------------------------------------------------------------------

    def get_by_id(
        self,
        investment_id: int
    ):

        query = """
        SELECT *
        FROM investments
        WHERE id=%s
        """

        return self.fetch_one(
            query,
            (investment_id,)
        )

    # ------------------------------------------------------------------
    # Portfolio
    # ------------------------------------------------------------------

    def load_portfolio(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        query = """
        SELECT
            id,
            date,
            fund_type,
            fund_name,
            transaction_type,
            amount,
            purchase_nav,
            nav_date,
            latest_nav,
            units,
            current_value,
            gain_loss,
            holding_years,
            cagr

        FROM investments

        WHERE user_id=%s

        ORDER BY date
        """

        return self.fetch_dataframe(
            query=query,
            params=(user_id,)
        )

    # ------------------------------------------------------------------
    # User Investments
    # ------------------------------------------------------------------

    def get_user_transactions(
        self,
        user_id: int = 1
    ):

        query = """
        SELECT *
        FROM investments
        WHERE user_id=%s
        ORDER BY date
        """

        return self.fetch_all(
            query,
            (user_id,)
        )

    # ------------------------------------------------------------------
    # Total Invested
    # ------------------------------------------------------------------

    def total_invested(
        self,
        user_id: int = 1
    ) -> float:

        query = """
        SELECT
            COALESCE(
                SUM(amount),
                0
            )
        FROM investments
        WHERE user_id=%s
        """

        row = self.fetch_one(
            query,
            (user_id,)
        )

        return float(row[0])

    # ------------------------------------------------------------------
    # Number of Transactions
    # ------------------------------------------------------------------

    def transaction_count(
        self,
        user_id: int = 1
    ) -> int:

        query = """
        SELECT COUNT(*)
        FROM investments
        WHERE user_id=%s
        """

        row = self.fetch_one(
            query,
            (user_id,)
        )

        return int(row[0])