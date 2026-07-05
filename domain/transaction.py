# =============================================================================
# File Name : domain/transaction.py
# Project   : Investment Portfolio App V2
# Module    : Domain Model
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Generic Transaction Entity
#
# This class represents ANY portfolio transaction.
#
# Supported Transaction Types
# ---------------------------
# BUY
# SELL
# SIP
# SWP
# STP
# SWITCH
# BONUS
# DIVIDEND
# SPLIT
# TRANSFER
#
# Future Proof
# ------------
# Mutual Funds
# ETFs
# Stocks
# Gold
# Silver
# Bonds
# REITs
# Crypto (optional future)
#
# No database code.
# No business logic.
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from typing import Optional


VALID_TRANSACTION_TYPES = {

    "BUY",

    "SELL",

    "SIP",

    "SWP",

    "STP",

    "SWITCH",

    "BONUS",

    "DIVIDEND",

    "SPLIT",

    "TRANSFER"

}


@dataclass(slots=True)
class Transaction:

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    id: Optional[int] = None

    user_id: int = 1

    # -------------------------------------------------------------------------
    # Asset
    # -------------------------------------------------------------------------

    asset_type: str = "Mutual Fund"

    fund_name: str = ""

    scheme_code: Optional[int] = None

    symbol: str = ""

    # -------------------------------------------------------------------------
    # Transaction
    # -------------------------------------------------------------------------

    transaction_type: str = "BUY"

    transaction_date: Optional[datetime] = None

    transaction_reference: str = ""

    # -------------------------------------------------------------------------
    # Financial
    # -------------------------------------------------------------------------

    amount: float = 0.0

    units: float = 0.0

    nav: float = 0.0

    price: float = 0.0

    brokerage: float = 0.0

    stamp_duty: float = 0.0

    taxes: float = 0.0

    other_charges: float = 0.0

    # -------------------------------------------------------------------------
    # Derived Values
    # -------------------------------------------------------------------------

    total_cost: float = 0.0

    net_amount: float = 0.0

    average_price: float = 0.0

    realized_profit: float = 0.0

    unrealized_profit: float = 0.0

    # -------------------------------------------------------------------------
    # Notes
    # -------------------------------------------------------------------------

    broker: str = ""

    account_name: str = ""

    platform: str = ""

    remarks: str = ""

    tags: list[str] = field(default_factory=list)

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

            self.transaction_type

            .upper()

            .strip()

        )

        if self.transaction_type not in VALID_TRANSACTION_TYPES:

            raise ValueError(

                f"Invalid transaction type : "

                f"{self.transaction_type}"

            )

        if self.amount < 0:

            raise ValueError(

                "Amount cannot be negative."

            )

        if self.units < 0:

            raise ValueError(

                "Units cannot be negative."

            )

        if self.nav < 0:

            raise ValueError(

                "NAV cannot be negative."

            )

        if self.price < 0:

            raise ValueError(

                "Price cannot be negative."

            )

    # -------------------------------------------------------------------------
    # Calculate Total Cost
    # -------------------------------------------------------------------------

    def calculate_total_cost(self):

        self.total_cost = round(

            self.amount

            + self.brokerage

            + self.stamp_duty

            + self.taxes

            + self.other_charges,

            2

        )

    # -------------------------------------------------------------------------
    # Net Amount
    # -------------------------------------------------------------------------

    def calculate_net_amount(self):

        self.net_amount = round(

            self.amount

            - self.brokerage

            - self.taxes

            - self.other_charges,

            2

        )

    # -------------------------------------------------------------------------
    # Refresh
    # -------------------------------------------------------------------------

    def refresh(self):

        self.calculate_total_cost()

        self.calculate_net_amount()

    # -------------------------------------------------------------------------
    # BUY
    # -------------------------------------------------------------------------

    @property
    def is_buy(self):

        return self.transaction_type == "BUY"

    # -------------------------------------------------------------------------
    # SELL
    # -------------------------------------------------------------------------

    @property
    def is_sell(self):

        return self.transaction_type == "SELL"

    # -------------------------------------------------------------------------
    # SIP
    # -------------------------------------------------------------------------

    @property
    def is_sip(self):

        return self.transaction_type == "SIP"

    # -------------------------------------------------------------------------
    # SWP
    # -------------------------------------------------------------------------

    @property
    def is_swp(self):

        return self.transaction_type == "SWP"

    # -------------------------------------------------------------------------
    # Dividend
    # -------------------------------------------------------------------------

    @property
    def is_dividend(self):

        return self.transaction_type == "DIVIDEND"

    # -------------------------------------------------------------------------
    # Dictionary
    # -------------------------------------------------------------------------

    def to_dict(self):

        return {

            key: value

            for key, value

            in self.__dict__.items()

        }

    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------

    def __str__(self):

        return (

            f"Transaction("

            f"{self.transaction_type}, "

            f"{self.fund_name}, "

            f"{self.amount:,.2f}"

            f")"

        )

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self):

        return self.__str__()