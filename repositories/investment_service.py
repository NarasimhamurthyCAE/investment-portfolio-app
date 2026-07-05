# =============================================================================
# File Name : services/investment_service.py
# Project   : Investment Portfolio App V2
# Module    : Service Layer
#
# Description
# -----------------------------------------------------------------------------
# Investment Service
#
# Responsibilities
# ----------------
# ✓ Business Logic
# ✓ Validation
# ✓ Portfolio Calculations
# ✓ Repository Coordination
# ✓ Current Value Calculation
# ✓ Gain/Loss Calculation
# ✓ Holding Period Calculation
#
# NO SQL HERE
# NO STREAMLIT HERE
#
# =============================================================================

from __future__ import annotations

from datetime import datetime

from domain.investment import Investment

from repositories.investment_repository import InvestmentRepository
from repositories.investment_query_repository import (
    InvestmentQueryRepository,
)


class InvestmentService:

    """
    Investment Business Layer
    """

    def __init__(self):

        self.repository = InvestmentRepository()

        self.query_repository = InvestmentQueryRepository()

    # -------------------------------------------------------------------------
    # Save Investment
    # -------------------------------------------------------------------------

    def save(
        self,
        investment: Investment
    ) -> None:

        self.validate(investment)

        investment.refresh()

        self.repository.insert(investment)

    # -------------------------------------------------------------------------
    # Update Investment
    # -------------------------------------------------------------------------

    def update(
        self,
        investment: Investment
    ) -> None:

        self.validate(investment)

        investment.refresh()

        self.repository.update(investment)

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete(
        self,
        investment_id: int
    ) -> None:

        self.repository.delete_by_id(
            investment_id
        )

    # -------------------------------------------------------------------------
    # Get
    # -------------------------------------------------------------------------

    def get(
        self,
        investment_id: int
    ):

        return self.repository.get_by_id(
            investment_id
        )

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int = 1
    ):

        return self.query_repository.load_portfolio(
            user_id
        )

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str,
        user_id: int = 1
    ):

        return self.query_repository.search_fund(

            keyword,

            user_id

        )

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    def statistics(
        self,
        user_id: int = 1
    ) -> dict:

        return {

            "investment":

            self.query_repository.total_invested(

                user_id

            ),

            "current_value":

            self.query_repository.total_current_value(

                user_id

            ),

            "gain":

            self.query_repository.total_gain(

                user_id

            ),

            "transactions":

            self.query_repository.total_transactions(

                user_id

            )

        }

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(
        self,
        investment: Investment
    ) -> None:

        if investment.fund_name == "":

            raise ValueError(

                "Fund Name cannot be empty."

            )

        if investment.amount <= 0:

            raise ValueError(

                "Investment amount must be greater than zero."

            )

        if investment.purchase_nav <= 0:

            raise ValueError(

                "Purchase NAV must be greater than zero."

            )

        if investment.units <= 0:

            raise ValueError(

                "Units must be greater than zero."

            )

    # -------------------------------------------------------------------------
    # Calculate Units
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate_units(
        amount: float,
        nav: float
    ) -> float:

        return round(

            amount / nav,

            6

        )

    # -------------------------------------------------------------------------
    # Calculate Current Value
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate_current_value(
        units: float,
        latest_nav: float
    ) -> float:

        return round(

            units * latest_nav,

            2

        )

    # -------------------------------------------------------------------------
    # Gain Loss
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate_gain(
        invested: float,
        current_value: float
    ) -> float:

        return round(

            current_value

            - invested,

            2

        )

    # -------------------------------------------------------------------------
    # Gain %
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate_gain_percent(

        invested,

        gain

    ):

        if invested == 0:

            return 0

        return round(

            gain

            / invested

            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Holding Years
    # -------------------------------------------------------------------------

    @staticmethod
    def holding_years(

        investment_date

    ):

        if investment_date is None:

            return 0

        days = (

            datetime.today()

            - investment_date

        ).days

        return round(

            days / 365.25,

            2

        )

    # -------------------------------------------------------------------------
    # Refresh Investment
    # -------------------------------------------------------------------------

    def refresh(
        self,
        investment: Investment
    ):

        investment.current_value = (

            self.calculate_current_value(

                investment.units,

                investment.latest_nav

            )

        )

        investment.gain_loss = (

            self.calculate_gain(

                investment.amount,

                investment.current_value

            )

        )

        investment.gain_loss_percent = (

            self.calculate_gain_percent(

                investment.amount,

                investment.gain_loss

            )

        )

        investment.holding_years = (

            self.holding_years(

                investment.transaction_date

            )

        )

        return investment