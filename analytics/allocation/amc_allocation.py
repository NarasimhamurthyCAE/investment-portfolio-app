# =============================================================================
# File Name : analytics/allocation/amc_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# AMC Allocation Engine
#
# Calculates allocation by Asset Management Company (AMC).
#
# Examples
# --------
# HDFC
# SBI
# ICICI Prudential
# Nippon India
# Motilal Oswal
# Axis
# Kotak
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class AMCAllocationEngine:
    """
    AMC Allocation Calculator
    """

    REQUIRED_COLUMNS = {

        "amc",

        "current_value"

    }

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    @classmethod
    def _validate(

        cls,

        portfolio: pd.DataFrame

    ) -> None:

        if portfolio.empty:

            return

        missing = (

            cls.REQUIRED_COLUMNS

            - set(portfolio.columns)

        )

        if missing:

            raise ValueError(

                f"Missing columns: {sorted(missing)}"

            )

    # -------------------------------------------------------------------------
    # Calculate
    # -------------------------------------------------------------------------

    @classmethod
    def calculate(

        cls,

        portfolio: pd.DataFrame

    ) -> pd.DataFrame:

        cls._validate(

            portfolio

        )

        if portfolio.empty:

            return pd.DataFrame()

        allocation = (

            portfolio

            .groupby(

                "amc",

                dropna=False

            )["current_value"]

            .sum()

            .reset_index()

        )

        total = allocation[

            "current_value"

        ].sum()

        allocation["allocation_percent"] = (

            0.0

            if total == 0

            else

            (

                allocation["current_value"]

                / total

                * 100

            ).round(2)

        )

        allocation = allocation.sort_values(

            by="current_value",

            ascending=False

        )

        allocation.reset_index(

            drop=True,

            inplace=True

        )

        return allocation

    # -------------------------------------------------------------------------
    # Dictionary
    # -------------------------------------------------------------------------

    @classmethod
    def as_dict(

        cls,

        portfolio: pd.DataFrame

    ) -> dict:

        df = cls.calculate(

            portfolio

        )

        if df.empty:

            return {}

        return dict(

            zip(

                df["amc"],

                df["allocation_percent"]

            )

        )

    # -------------------------------------------------------------------------
    # Largest AMC
    # -------------------------------------------------------------------------

    @classmethod
    def largest(

        cls,

        portfolio: pd.DataFrame

    ):

        df = cls.calculate(

            portfolio

        )

        if df.empty:

            return None

        return df.iloc[0]

    # -------------------------------------------------------------------------
    # AMC Count
    # -------------------------------------------------------------------------

    @classmethod
    def count(

        cls,

        portfolio: pd.DataFrame

    ) -> int:

        cls._validate(

            portfolio

        )

        if portfolio.empty:

            return 0

        return portfolio[

            "amc"

        ].nunique()

    # -------------------------------------------------------------------------
    # Allocation for AMC
    # -------------------------------------------------------------------------

    @classmethod
    def allocation_for(

        cls,

        portfolio: pd.DataFrame,

        amc: str

    ) -> float:

        df = cls.calculate(

            portfolio

        )

        row = df[

            df["amc"]

            == amc

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0][

                "allocation_percent"

            ]

        )

    # -------------------------------------------------------------------------
    # Value for AMC
    # -------------------------------------------------------------------------

    @classmethod
    def value_for(

        cls,

        portfolio: pd.DataFrame,

        amc: str

    ) -> float:

        df = cls.calculate(

            portfolio

        )

        row = df[

            df["amc"]

            == amc

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0][

                "current_value"

            ]

        )

    # -------------------------------------------------------------------------
    # Top N AMCs
    # -------------------------------------------------------------------------

    @classmethod
    def top(

        cls,

        portfolio: pd.DataFrame,

        n: int = 10

    ) -> pd.DataFrame:

        df = cls.calculate(

            portfolio

        )

        return df.head(n)