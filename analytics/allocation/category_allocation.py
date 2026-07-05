# =============================================================================
# File Name : analytics/allocation/category_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Category Allocation Engine
#
# Calculates portfolio allocation by investment category.
#
# Examples
# --------
# Large Cap
# Mid Cap
# Small Cap
# Flexi Cap
# ELSS
# Hybrid
# International
# Gold
# Debt
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class CategoryAllocationEngine:
    """
    Portfolio Category Allocation
    """

    REQUIRED_COLUMNS = {

        "category",

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

                "category",

                dropna=False

            )["current_value"]

            .sum()

            .reset_index()

        )

        total = allocation[

            "current_value"

        ].sum()

        if total > 0:

            allocation[

                "allocation_percent"

            ] = (

                allocation["current_value"]

                / total

                * 100

            ).round(2)

        else:

            allocation[

                "allocation_percent"

            ] = 0.0

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

                df["category"],

                df["allocation_percent"]

            )

        )

    # -------------------------------------------------------------------------
    # Largest Category
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
    # Total Categories
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

            "category"

        ].nunique()

    # -------------------------------------------------------------------------
    # Allocation Lookup
    # -------------------------------------------------------------------------

    @classmethod
    def allocation_for(

        cls,

        portfolio: pd.DataFrame,

        category: str

    ) -> float:

        df = cls.calculate(

            portfolio

        )

        row = df[

            df["category"]

            == category

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0][

                "allocation_percent"

            ]

        )

    # -------------------------------------------------------------------------
    # Current Value Lookup
    # -------------------------------------------------------------------------

    @classmethod
    def value_for(

        cls,

        portfolio: pd.DataFrame,

        category: str

    ) -> float:

        df = cls.calculate(

            portfolio

        )

        row = df[

            df["category"]

            == category

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0][

                "current_value"

            ]

        )