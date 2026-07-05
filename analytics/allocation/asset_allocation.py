# =============================================================================
# File Name : analytics/allocation/asset_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Asset Allocation Engine
#
# Calculates portfolio allocation by asset class.
#
# Examples
# --------
# Mutual Fund
# ETF
# Stock
# Gold
# Silver
# Bond
# Cash
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class AssetAllocationEngine:
    """
    Asset Allocation Calculator
    """

    # -------------------------------------------------------------------------
    # Allocation Summary
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate(
        portfolio: pd.DataFrame
    ) -> pd.DataFrame:

        if portfolio.empty:

            return pd.DataFrame()

        required = {

            "asset_type",

            "current_value"

        }

        missing = required - set(portfolio.columns)

        if missing:

            raise ValueError(

                f"Missing columns: {sorted(missing)}"

            )

        allocation = (

            portfolio

            .groupby(

                "asset_type",

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

        allocation = allocation.sort_values(

            by="current_value",

            ascending=False

        ).reset_index(drop=True)

        return allocation

    # -------------------------------------------------------------------------
    # Allocation Dictionary
    # -------------------------------------------------------------------------

    @staticmethod
    def as_dict(
        portfolio: pd.DataFrame
    ) -> dict:

        df = AssetAllocationEngine.calculate(

            portfolio

        )

        if df.empty:

            return {}

        return dict(

            zip(

                df["asset_type"],

                df["allocation_percent"]

            )

        )

    # -------------------------------------------------------------------------
    # Largest Asset
    # -------------------------------------------------------------------------

    @staticmethod
    def largest_asset(
        portfolio: pd.DataFrame
    ):

        df = AssetAllocationEngine.calculate(

            portfolio

        )

        if df.empty:

            return None

        return df.iloc[0]

    # -------------------------------------------------------------------------
    # Total Value
    # -------------------------------------------------------------------------

    @staticmethod
    def total_value(
        portfolio: pd.DataFrame
    ) -> float:

        if portfolio.empty:

            return 0.0

        return round(

            portfolio["current_value"].sum(),

            2

        )