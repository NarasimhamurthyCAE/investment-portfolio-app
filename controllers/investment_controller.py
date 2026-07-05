# =============================================================================
# File Name : controllers/investment_controller.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

from assets.services.investment_service import (
    InvestmentService,
)


class InvestmentController:
    """
    Investment Controller
    """

    def __init__(self):

        self.service = InvestmentService()

    # -------------------------------------------------------------------------
    # Create Stock Investment
    # -------------------------------------------------------------------------

    def create_stock_investment(
        self,
        **kwargs,
    ) -> int:

        print("CONTROLLER START")

        result = self.service.create_stock_investment(
            **kwargs
        )

        print("CONTROLLER END")

        return result