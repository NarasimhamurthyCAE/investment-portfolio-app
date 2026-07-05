# =============================================================================
# File Name : domain/benchmark.py
# Project   : Investment Portfolio App V2
# Module    : Domain Model
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Benchmark Domain Model
#
# Represents one benchmark index used to compare investment performance.
#
# Examples
# --------
# NIFTY 50 TRI
# NIFTY 500 TRI
# NIFTY Midcap 150 TRI
# NASDAQ 100
# Gold ETF
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Optional


@dataclass(slots=True)
class Benchmark:
    """
    Benchmark Entity
    """

    # -------------------------------------------------------------------------
    # Primary Key
    # -------------------------------------------------------------------------

    id: Optional[int] = None

    # -------------------------------------------------------------------------
    # Benchmark Information
    # -------------------------------------------------------------------------

    benchmark_name: str = ""

    benchmark_code: str = ""

    benchmark_type: str = "Index"

    market: str = "India"

    provider: str = ""

    currency: str = "INR"

    # -------------------------------------------------------------------------
    # Investment Mapping
    # -------------------------------------------------------------------------

    asset_type: str = "Mutual Fund"

    applicable_category: str = ""

    fund_name: str = ""

    scheme_code: Optional[int] = None

    # -------------------------------------------------------------------------
    # Latest Value
    # -------------------------------------------------------------------------

    latest_value: float = 0.0

    latest_date: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Performance
    # -------------------------------------------------------------------------

    one_day_return: float = 0.0

    one_month_return: float = 0.0

    three_month_return: float = 0.0

    six_month_return: float = 0.0

    one_year_return: float = 0.0

    three_year_return: float = 0.0

    five_year_return: float = 0.0

    since_inception_return: float = 0.0

    # -------------------------------------------------------------------------
    # Benchmark Simulation
    # -------------------------------------------------------------------------

    invested_amount: float = 0.0

    benchmark_units: float = 0.0

    benchmark_value: float = 0.0

    benchmark_xirr: float = 0.0

    benchmark_cagr: float = 0.0

    benchmark_gain: float = 0.0

    benchmark_gain_percent: float = 0.0

    # -------------------------------------------------------------------------
    # Status
    # -------------------------------------------------------------------------

    is_active: bool = True

    remarks: str = ""

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def __post_init__(self):

        self.benchmark_name = (
            self.benchmark_name.strip()
        )

        self.market = (
            self.market.strip()
        )

        self.currency = (
            self.currency.strip().upper()
        )

        if self.latest_value < 0:
            raise ValueError(
                "Benchmark value cannot be negative."
            )

        if self.invested_amount < 0:
            raise ValueError(
                "Invested amount cannot be negative."
            )

    # -------------------------------------------------------------------------
    # Update Benchmark Gain
    # -------------------------------------------------------------------------

    def update_gain(self) -> None:

        self.benchmark_gain = round(

            self.benchmark_value
            - self.invested_amount,

            2

        )

    # -------------------------------------------------------------------------
    # Update Benchmark Gain %
    # -------------------------------------------------------------------------

    def update_gain_percent(self) -> None:

        if self.invested_amount == 0:

            self.benchmark_gain_percent = 0.0

            return

        self.benchmark_gain_percent = round(

            (
                self.benchmark_gain
                / self.invested_amount
            )
            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Refresh
    # -------------------------------------------------------------------------

    def refresh(self):

        self.update_gain()

        self.update_gain_percent()

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

    def __str__(self):

        return (

            f"Benchmark("

            f"name='{self.benchmark_name}', "

            f"value={self.latest_value}"

            f")"

        )

    # -------------------------------------------------------------------------
    # Representation
    # -------------------------------------------------------------------------

    def __repr__(self):

        return self.__str__()