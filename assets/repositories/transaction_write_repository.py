# =============================================================================
# File Name : assets/repositories/transaction_write_repository.py
# =============================================================================

from __future__ import annotations

from repositories.base_repository import BaseRepository


class TransactionWriteRepository(BaseRepository):
    TABLE_NAME = "transactions"

    # -------------------------------------------------------------------------
    # Create Transaction
    # -------------------------------------------------------------------------

    def create(
        self,
        investment_id: int,
        transaction_type: str,
        transaction_date,
        units: float,
        price: float,
        amount: float,
        charges: float = 0.0,
        taxes: float = 0.0,
        currency: str = "INR",
        reference_number: str | None = None,
        remarks: str | None = None,
    ) -> int:

        query = """
        INSERT INTO transactions
        (
            investment_id,
            transaction_type,
            transaction_date,
            units,
            price,
            amount,
            charges,
            taxes,
            currency,
            reference_number,
            remarks
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        RETURNING transaction_id
        """

        row = self.fetch_one(
            query,
            (
                investment_id,
                transaction_type,
                transaction_date,
                units,
                price,
                amount,
                charges,
                taxes,
                currency,
                reference_number,
                remarks,
            ),
        )

        return row["transaction_id"]

    # -------------------------------------------------------------------------
    # Update Transaction
    # -------------------------------------------------------------------------

    def update(
        self,
        transaction_id: int,
        transaction_type: str,
        transaction_date,
        units: float,
        price: float,
        amount: float,
        charges: float,
        taxes: float,
        remarks: str | None,
    ) -> None:

        query = """
        UPDATE transactions
        SET
            transaction_type=%s,
            transaction_date=%s,
            units=%s,
            price=%s,
            amount=%s,
            charges=%s,
            taxes=%s,
            remarks=%s,
            updated_at=NOW()
        WHERE transaction_id=%s
        """

        self.execute(
            query,
            (
                transaction_type,
                transaction_date,
                units,
                price,
                amount,
                charges,
                taxes,
                remarks,
                transaction_id,
            ),
        )

    # -------------------------------------------------------------------------
    # Delete Transaction
    # -------------------------------------------------------------------------

    def delete(
        self,
        transaction_id: int,
    ) -> None:

        query = """
        DELETE
        FROM transactions
        WHERE transaction_id=%s
        """

        self.execute(
            query,
            (
                transaction_id,
            ),
        )