# =============================================================================
# File Name : domain/investment.py
# Project   : Investment Portfolio App V2
# Module    : Domain Model
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Investment Domain Model
#
# This class represents ONE investment transaction.
#
# Business logic DOES NOT belong here.
#
# Repository -> Stores/Retrieves
# Service    -> Business Rules
# UI          -> Displays Data
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Investment:
    """
    Investment Entity

    Represents one BUY or SELL transaction.
    """

    # -------------------------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------------------------

    id: Optional[int] = None

    # -------------------------------------------------------------------------
    # User
    # -------------------------------------------------------------------------

    user_id: int = 1

    # -------------------------------------------------------------------------
    # Transaction
    # -------------------------------------------------------------------------

    transaction_date: datetime | None = None

    transaction_type: str = "BUY"

    # -------------------------------------------------------------------------
    # Asset
    # -------------------------------------------------------------------------

    asset_type: str = "Mutual Fund"

    fund_type: str = ""

    fund_name: str = ""

    scheme_code: Optional[int] = None

    benchmark: str = ""

    # -------------------------------------------------------------------------
    # Investment
    # -------------------------------------------------------------------------

    amount: float = 0.0

    purchase_nav: float = 0.0

    nav_date: Optional[datetime] = None

    latest_nav: float = 0.0

    units: float = 0.0

    # -------------------------------------------------------------------------
    # Performance
    # -------------------------------------------------------------------------

    current_value: float = 0.0

    invested_value: float = 0.0

    gain_loss: float = 0.0

    gain_loss_percent: float = 0.0

    xirr: float = 0.0

    cagr: float = 0.0

    absolute_return: float = 0.0

    holding_days: int = 0

    holding_years: float = 0.0

    # -------------------------------------------------------------------------
    # Charges
    # -------------------------------------------------------------------------

    expense_ratio: float = 0.0

    exit_load: float = 0.0

    stamp_duty: float = 0.0

    brokerage: float = 0.0

    taxes: float = 0.0

    # -------------------------------------------------------------------------
    # Goal Mapping
    # -------------------------------------------------------------------------

    goal: str = ""

    account_name: str = ""

    notes: str = ""

    tags: list[str] = field(default_factory=list)

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    is_active: bool = True

    is_deleted: bool = False

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def __post_init__(self):

        self.transaction_type = (
            self.transaction_type.upper().strip()
        )

        if self.transaction_type not in (
            "BUY",
            "SELL"
        ):
            raise ValueError(
                "Transaction type must be BUY or SELL."
            )

        if self.amount < 0:
            raise ValueError(
                "Amount cannot be negative."
            )

        if self.purchase_nav < 0:
            raise ValueError(
                "Purchase NAV cannot be negative."
            )

        if self.latest_nav < 0:
            raise ValueError(
                "Latest NAV cannot be negative."
            )

        if self.units < 0:
            raise ValueError(
                "Units cannot be negative."
            )

    # -------------------------------------------------------------------------
    # Update Current Value
    # -------------------------------------------------------------------------

    def update_current_value(self) -> None:

        self.current_value = round(
            self.units * self.latest_nav,
            2
        )

    # -------------------------------------------------------------------------
    # Update Gain Loss
    # -------------------------------------------------------------------------

    def update_gain_loss(self) -> None:

        self.gain_loss = round(
            self.current_value - self.amount,
            2
        )

    # -------------------------------------------------------------------------
    # Update Gain %
    # -------------------------------------------------------------------------

    def update_gain_percent(self) -> None:

        if self.amount == 0:

            self.gain_loss_percent = 0.0

            return

        self.gain_loss_percent = round(

            (self.gain_loss / self.amount) * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Update Holding Days
    # -------------------------------------------------------------------------

    def update_holding_days(self) -> None:

        if self.transaction_date is None:

            self.holding_days = 0

            self.holding_years = 0

            return

        days = (
            datetime.today()
            - self.transaction_date
        ).days

        self.holding_days = days

        self.holding_years = round(
            days / 365.25,
            2
        )

    # -------------------------------------------------------------------------
    # Refresh Calculated Fields
    # -------------------------------------------------------------------------

    def refresh(self) -> None:

        self.update_current_value()

        self.update_gain_loss()

        self.update_gain_percent()

        self.update_holding_days()

    # -------------------------------------------------------------------------
    # Buy Transaction
    # -------------------------------------------------------------------------

    @property
    def is_buy(self) -> bool:

        return self.transaction_type == "BUY"

    # -------------------------------------------------------------------------
    # Sell Transaction
    # -------------------------------------------------------------------------

    @property
    def is_sell(self) -> bool:

        return self.transaction_type == "SELL"

    # -------------------------------------------------------------------------
    # Dictionary
    # -------------------------------------------------------------------------

    def to_dict(self) -> dict:

        return {

            key: value

            for key, value

            in self.__dict__.items()

        }

    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------

    def __str__(self) -> str:

        return (

            f"Investment("

            f"id={self.id}, "

            f"fund='{self.fund_name}', "

            f"type='{self.transaction_type}', "

            f"amount={self.amount:,.2f}"

            f")"

        )

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self) -> str:

        return self.__str__()