# =============================================================================
# File Name : assets/repositories/investment_write_repository.py
# =============================================================================

from __future__ import annotations

from repositories.base_repository import BaseRepository


class InvestmentWriteRepository(BaseRepository):
    TABLE_NAME = "investments"

    # -------------------------------------------------------------------------
    # Create Investment
    # -------------------------------------------------------------------------

    def create(
        self,
        user_id: int,
        asset_id: int,
        broker: str | None = None,
        account_name: str | None = None,
        portfolio_name: str = "Default",
        notes: str | None = None,
    ) -> int:

        query = """
        INSERT INTO investments
        (
            user_id,
            asset_id,
            broker,
            account_name,
            portfolio_name,
            notes
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        RETURNING investment_id
        """

        row = self.fetch_one(
            query,
            (
                user_id,
                asset_id,
                broker,
                account_name,
                portfolio_name,
                notes,
            ),
        )

        return row["investment_id"]

    # -------------------------------------------------------------------------
    # Update
    # -------------------------------------------------------------------------

    def update(
        self,
        investment_id: int,
        broker: str | None,
        account_name: str | None,
        portfolio_name: str,
        notes: str | None,
    ) -> None:

        query = """
        UPDATE investments
        SET

            broker=%s,

            account_name=%s,

            portfolio_name=%s,

            notes=%s,

            updated_at=NOW()

        WHERE investment_id=%s
        """

        self.execute(
            query,
            (
                broker,
                account_name,
                portfolio_name,
                notes,
                investment_id,
            ),
        )

    # -------------------------------------------------------------------------
    # Soft Delete
    # -------------------------------------------------------------------------

    def delete(
        self,
        investment_id: int,
    ) -> None:

        query = """
        UPDATE investments
        SET

            is_active=FALSE,

            updated_at=NOW()

        WHERE investment_id=%s
        """

        self.execute(
            query,
            (
                investment_id,
            ),
        )

    # -------------------------------------------------------------------------
    # Find Existing Investment
    # -------------------------------------------------------------------------

    def find_existing(
        self,
        user_id: int,
        asset_id: int,
        portfolio_name: str = "Default",
    ):

        query = """
        SELECT investment_id

        FROM investments

        WHERE

            user_id=%s

            AND asset_id=%s

            AND portfolio_name=%s

            AND is_active=TRUE

        LIMIT 1
        """

        return self.fetch_one(
            query,
            (
                user_id,
                asset_id,
                portfolio_name,
            ),
        )