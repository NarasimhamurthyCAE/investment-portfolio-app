# =============================================================================
# File Name : transactions/controllers/transaction_controller.py
# =============================================================================

from __future__ import annotations

from transactions.services.transaction_service import TransactionService


class TransactionController:

    def __init__(self):

        self.service = TransactionService()

    # -------------------------------------------------------------------------
    # Dashboard
    # -------------------------------------------------------------------------

    def dashboard(
        self,
        user_id: int = 1,
    ):

        return self.service.dashboard(
            user_id
        )

    # -------------------------------------------------------------------------
    # Transactions
    # -------------------------------------------------------------------------

    def transactions(
        self,
        user_id: int = 1,
    ):

        return self.service.transactions(
            user_id
        )

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
        user_id: int = 1,
    ):

        return self.service.search(
            keyword,
            user_id,
        )