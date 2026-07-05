# =============================================================================
# File Name : domain/user.py
# Project   : Investment Portfolio App V2
# Module    : Domain Model
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# User Domain Entity
#
# Represents one application user.
#
# Future Ready Features
# ---------------------
# • Multiple users
# • Family portfolios
# • Advisor accounts
# • Multiple currencies
# • Risk profiles
# • Tax profiles
#
# No database code.
# No Streamlit code.
# No business logic.
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class User:

    # -------------------------------------------------------------------------
    # Database
    # -------------------------------------------------------------------------

    id: Optional[int] = None

    # -------------------------------------------------------------------------
    # Basic Information
    # -------------------------------------------------------------------------

    first_name: str = ""

    last_name: str = ""

    full_name: str = ""

    email: str = ""

    mobile: str = ""

    # -------------------------------------------------------------------------
    # Login
    # -------------------------------------------------------------------------

    username: str = ""

    password_hash: str = ""

    # -------------------------------------------------------------------------
    # Location
    # -------------------------------------------------------------------------

    country: str = "India"

    state: str = ""

    city: str = ""

    timezone: str = "Asia/Kolkata"

    currency: str = "INR"

    # -------------------------------------------------------------------------
    # Investment Profile
    # -------------------------------------------------------------------------

    risk_profile: str = "Moderate"

    investment_style: str = "Long Term"

    preferred_market: str = "India"

    benchmark: str = "NIFTY 500 TRI"

    # -------------------------------------------------------------------------
    # Goals
    # -------------------------------------------------------------------------

    retirement_goal: float = 0.0

    emergency_fund_goal: float = 0.0

    child_education_goal: float = 0.0

    house_goal: float = 0.0

    # -------------------------------------------------------------------------
    # Preferences
    # -------------------------------------------------------------------------

    dark_theme: bool = False

    notifications: bool = True

    email_alerts: bool = False

    mobile_alerts: bool = False

    language: str = "English"

    # -------------------------------------------------------------------------
    # Account
    # -------------------------------------------------------------------------

    is_active: bool = True

    is_admin: bool = False

    email_verified: bool = False

    mobile_verified: bool = False

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    portfolio_count: int = 1

    total_investment: float = 0.0

    total_current_value: float = 0.0

    total_profit: float = 0.0

    total_xirr: float = 0.0

    # -------------------------------------------------------------------------
    # Notes
    # -------------------------------------------------------------------------

    tags: list[str] = field(default_factory=list)

    notes: str = ""

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    last_login: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def __post_init__(self):

        self.email = self.email.lower().strip()

        self.currency = self.currency.upper().strip()

        self.country = self.country.strip()

        self.timezone = self.timezone.strip()

        if not self.full_name:

            self.full_name = (

                f"{self.first_name} "

                f"{self.last_name}"

            ).strip()

    # -------------------------------------------------------------------------
    # Refresh Portfolio
    # -------------------------------------------------------------------------

    def refresh_portfolio(

        self,

        investment: float,

        current_value: float,

        xirr: float

    ):

        self.total_investment = round(

            investment,

            2

        )

        self.total_current_value = round(

            current_value,

            2

        )

        self.total_profit = round(

            current_value

            - investment,

            2

        )

        self.total_xirr = round(

            xirr,

            2

        )

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

            f"User("

            f"{self.full_name}, "

            f"{self.email}"

            f")"

        )

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self):

        return self.__str__()