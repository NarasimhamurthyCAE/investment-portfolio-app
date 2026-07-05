# =============================================================================
# File Name : analytics/allocation/sector_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Sector Allocation Engine
#
# Calculates portfolio allocation by sector.
#
# Examples
# --------
# Financial Services
# Information Technology
# Healthcare
# Consumer Goods
# Industrials
# Energy
# Automobile
# Realty
# Telecom
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class SectorAllocationEngine:
    """
    Sector Allocation Calculator
    """

    REQUIRED_COLUMNS = {

        "sector",

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

        cls._validate(portfolio)

        if portfolio.empty:

            return pd.DataFrame()

        allocation = (

            portfolio

            .groupby(

                "sector",

                dropna=False

            )["current_value"]

            .sum()

            .reset_index()

        )

        total = allocation["current_value"].sum()

        if total == 0:

            allocation["allocation_percent"] = 0.0

        else:

            allocation["allocation_percent"] = (

                allocation["current_value"]

                / total

                * 100

            ).round(2)

        allocation.sort_values(

            by="current_value",

            ascending=False,

            inplace=True

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

        df = cls.calculate(portfolio)

        if df.empty:

            return {}

        return dict(

            zip(

                df["sector"],

                df["allocation_percent"]

            )

        )

    # -------------------------------------------------------------------------
    # Largest Sector
    # -------------------------------------------------------------------------

    @classmethod
    def largest(
        cls,
        portfolio: pd.DataFrame
    ):

        df = cls.calculate(portfolio)

        if df.empty:

            return None

        return df.iloc[0]

    # -------------------------------------------------------------------------
    # Number of Sectors
    # -------------------------------------------------------------------------

    @classmethod
    def count(
        cls,
        portfolio: pd.DataFrame
    ) -> int:

        cls._validate(portfolio)

        if portfolio.empty:

            return 0

        return portfolio["sector"].nunique()

    # -------------------------------------------------------------------------
    # Allocation Lookup
    # -------------------------------------------------------------------------

    @classmethod
    def allocation_for(
        cls,
        portfolio: pd.DataFrame,
        sector: str
    ) -> float:

        df = cls.calculate(portfolio)

        row = df[

            df["sector"] == sector

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0]["allocation_percent"]

        )

    # -------------------------------------------------------------------------
    # Value Lookup
    # -------------------------------------------------------------------------

    @classmethod
    def value_for(
        cls,
        portfolio: pd.DataFrame,
        sector: str
    ) -> float:

        df = cls.calculate(portfolio)

        row = df[

            df["sector"] == sector

        ]

        if row.empty:

            return 0.0

        return float(

            row.iloc[0]["current_value"]

        )

    # -------------------------------------------------------------------------
    # Top N Sectors
    # -------------------------------------------------------------------------

    @classmethod
    def top(
        cls,
        portfolio: pd.DataFrame,
        n: int = 10
    ) -> pd.DataFrame:

        return cls.calculate(

            portfolio

        ).head(n)

    # -------------------------------------------------------------------------
    # Others Group
    # -------------------------------------------------------------------------

    @classmethod
    def top_with_others(
        cls,
        portfolio: pd.DataFrame,
        n: int = 8
    ) -> pd.DataFrame:

        allocation = cls.calculate(portfolio)

        if len(allocation) <= n:

            return allocation

        top = allocation.head(n).copy()

        others = allocation.iloc[n:]

        other_value = others["current_value"].sum()

        other_percent = others["allocation_percent"].sum()

        top.loc[len(top)] = {

            "sector": "Others",

            "current_value": round(other_value, 2),

            "allocation_percent": round(other_percent, 2)

        }

        return top.reset_index(drop=True)