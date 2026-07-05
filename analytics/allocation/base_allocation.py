# =============================================================================
# File Name : analytics/allocation/base_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Base Allocation Engine
#
# Parent class for:
#   AssetAllocationEngine
#   CategoryAllocationEngine
#   AMCAllocationEngine
#   SectorAllocationEngine
#   CountryAllocationEngine
#   MarketCapAllocationEngine
#   BenchmarkAllocationEngine
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class BaseAllocationEngine:

    GROUP_COLUMN = ""

    VALUE_COLUMN = "current_value"

    @classmethod
    def calculate(
        cls,
        portfolio: pd.DataFrame
    ) -> pd.DataFrame:

        if portfolio.empty:
            return pd.DataFrame()

        required = {
            cls.GROUP_COLUMN,
            cls.VALUE_COLUMN
        }

        missing = required - set(portfolio.columns)

        if missing:
            raise ValueError(
                f"Missing columns: {sorted(missing)}"
            )

        allocation = (
            portfolio
            .groupby(
                cls.GROUP_COLUMN,
                dropna=False
            )[cls.VALUE_COLUMN]
            .sum()
            .reset_index()
        )

        total = allocation[cls.VALUE_COLUMN].sum()

        allocation["allocation_percent"] = (
            0.0
            if total == 0
            else (
                allocation[cls.VALUE_COLUMN]
                / total
                * 100
            ).round(2)
        )

        allocation.sort_values(
            by=cls.VALUE_COLUMN,
            ascending=False,
            inplace=True
        )

        allocation.reset_index(
            drop=True,
            inplace=True
        )

        return allocation

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
                df[cls.GROUP_COLUMN],
                df["allocation_percent"]
            )
        )

    @classmethod
    def largest(
        cls,
        portfolio: pd.DataFrame
    ):

        df = cls.calculate(portfolio)

        if df.empty:
            return None

        return df.iloc[0]

    @classmethod
    def top(
        cls,
        portfolio: pd.DataFrame,
        n: int = 10
    ) -> pd.DataFrame:

        return cls.calculate(portfolio).head(n)

    @classmethod
    def total_value(
        cls,
        portfolio: pd.DataFrame
    ) -> float:

        if portfolio.empty:
            return 0.0

        return round(
            portfolio[cls.VALUE_COLUMN].sum(),
            2
        )