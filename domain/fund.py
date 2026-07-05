# =============================================================================
# File Name : domain/fund.py
# Project   : Investment Portfolio App V2
# Module    : Domain Model
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Mutual Fund / ETF / Stock Domain Model
#
# Represents a financial instrument.
#
# This object is used throughout the application by:
#
# • Repository Layer
# • Service Layer
# • Analytics Engine
# • Advisor Engine
# • Portfolio Engine
#
# No business logic should be written here.
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime

from typing import Optional


@dataclass(slots=True)
class Fund:
    """
    Financial Instrument
    """

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    id: Optional[int] = None

    # -------------------------------------------------------------------------
    # Identification
    # -------------------------------------------------------------------------

    scheme_code: Optional[int] = None

    isin: str = ""

    symbol: str = ""

    name: str = ""

    short_name: str = ""

    amc: str = ""

    # -------------------------------------------------------------------------
    # Classification
    # -------------------------------------------------------------------------

    asset_class: str = "Mutual Fund"

    category: str = ""

    sub_category: str = ""

    benchmark: str = ""

    risk_level: str = ""

    market: str = "India"

    currency: str = "INR"

    # -------------------------------------------------------------------------
    # NAV / Price
    # -------------------------------------------------------------------------

    latest_nav: float = 0.0

    previous_nav: float = 0.0

    nav_date: Optional[datetime] = None

    daily_change: float = 0.0

    daily_change_percent: float = 0.0

    # -------------------------------------------------------------------------
    # Performance
    # -------------------------------------------------------------------------

    one_month: float = 0.0

    three_month: float = 0.0

    six_month: float = 0.0

    one_year: float = 0.0

    three_year: float = 0.0

    five_year: float = 0.0

    ten_year: float = 0.0

    since_inception: float = 0.0

    # -------------------------------------------------------------------------
    # Ratings
    # -------------------------------------------------------------------------

    morningstar_rating: float = 0.0

    crisil_rating: float = 0.0

    expense_ratio: float = 0.0

    exit_load: float = 0.0

    aum: float = 0.0

    fund_manager: str = ""

    launch_date: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Holdings
    # -------------------------------------------------------------------------

    total_holdings: int = 0

    equity_percentage: float = 0.0

    debt_percentage: float = 0.0

    cash_percentage: float = 0.0

    overseas_percentage: float = 0.0

    gold_percentage: float = 0.0

    silver_percentage: float = 0.0

    # -------------------------------------------------------------------------
    # Tax
    # -------------------------------------------------------------------------

    ltcg_tax: float = 0.0

    stcg_tax: float = 0.0

    indexation_allowed: bool = False

    # -------------------------------------------------------------------------
    # Flags
    # -------------------------------------------------------------------------

    direct_plan: bool = True

    growth_option: bool = True

    active: bool = True

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    tags: list[str] = field(default_factory=list)

    notes: str = ""

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def __post_init__(self):

        self.asset_class = self.asset_class.strip()

        self.name = self.name.strip()

        self.amc = self.amc.strip()

        self.market = self.market.strip()

        self.currency = self.currency.upper().strip()

        if self.latest_nav < 0:
            raise ValueError(
                "Latest NAV cannot be negative."
            )

        if self.previous_nav < 0:
            raise ValueError(
                "Previous NAV cannot be negative."
            )

        if self.expense_ratio < 0:
            raise ValueError(
                "Expense ratio cannot be negative."
            )

        if self.exit_load < 0:
            raise ValueError(
                "Exit load cannot be negative."
            )

        if self.aum < 0:
            raise ValueError(
                "AUM cannot be negative."
            )

    # -------------------------------------------------------------------------
    # Update Daily Change
    # -------------------------------------------------------------------------

    def calculate_daily_change(self):

        self.daily_change = round(

            self.latest_nav
            - self.previous_nav,

            4

        )

    # -------------------------------------------------------------------------
    # Daily %
    # -------------------------------------------------------------------------

    def calculate_daily_change_percent(self):

        if self.previous_nav == 0:

            self.daily_change_percent = 0.0

            return

        self.daily_change_percent = round(

            (
                self.daily_change
                / self.previous_nav
            ) * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Refresh
    # -------------------------------------------------------------------------

    def refresh(self):

        self.calculate_daily_change()

        self.calculate_daily_change_percent()

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

            f"Fund("

            f"name='{self.name}', "

            f"nav={self.latest_nav}"

            f")"

        )

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self):

        return self.__str__()
        