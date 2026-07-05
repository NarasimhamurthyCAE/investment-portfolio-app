# =============================================================================
# File Name : domain/portfolio.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Aggregate Root
#
# Represents the complete investment portfolio.
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

import pandas as pd


@dataclass(slots=True)
class Portfolio:

    """
    Portfolio Aggregate
    """

    investments: pd.DataFrame = field(

        default_factory=pd.DataFrame

    )

    benchmark: pd.DataFrame = field(

        default_factory=pd.DataFrame

    )

    cashflows: list = field(

        default_factory=list

    )

    holdings: pd.DataFrame = field(

        default_factory=pd.DataFrame

    )

    metadata: dict = field(

        default_factory=dict

    )

    # -------------------------------------------------------------------------
    # Empty
    # -------------------------------------------------------------------------

    @property
    def empty(self):

        return self.investments.empty

    # -------------------------------------------------------------------------
    # Investment
    # -------------------------------------------------------------------------

    @property
    def invested_amount(self):

        if self.empty:

            return 0.0

        return round(

            self.investments["amount"].sum(),

            2

        )

    # -------------------------------------------------------------------------
    # Current Value
    # -------------------------------------------------------------------------

    @property
    def current_value(self):

        if self.empty:

            return 0.0

        return round(

            self.investments["current_value"].sum(),

            2

        )

    # -------------------------------------------------------------------------
    # Profit
    # -------------------------------------------------------------------------

    @property
    def profit(self):

        return round(

            self.current_value

            - self.invested_amount,

            2

        )

    # -------------------------------------------------------------------------
    # Holdings
    # -------------------------------------------------------------------------

    @property
    def total_holdings(self):

        if self.empty:

            return 0

        return len(

            self.investments

        )