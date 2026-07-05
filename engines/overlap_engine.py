# =============================================================================
# File Name : engines/overlap_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Overlap Engine
#
# Calculates overlap and concentration from normalized holdings.
#
# Responsibilities
# ----------------
# ✓ Company overlap
# ✓ Duplicate exposure
# ✓ Portfolio concentration
# ✓ Diversification score
# ✓ Top overlapping companies
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class OverlapEngine:
    """
    Portfolio Overlap Engine
    """

    REQUIRED_COLUMNS = {
        "company",
        "investment_value",
        "weight"
    }

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    @classmethod
    def _validate(
        cls,
        holdings: pd.DataFrame
    ) -> None:

        if holdings.empty:
            return

        missing = cls.REQUIRED_COLUMNS - set(holdings.columns)

        if missing:
            raise ValueError(
                f"Missing columns: {sorted(missing)}"
            )

    # -------------------------------------------------------------------------
    # Company Exposure
    # -------------------------------------------------------------------------

    @classmethod
    def company_exposure(
        cls,
        holdings: pd.DataFrame
    ) -> pd.DataFrame:

        cls._validate(holdings)

        if holdings.empty:
            return pd.DataFrame()

        exposure = (
            holdings
            .groupby(
                "company",
                dropna=False
            )
            .agg(
                investment_value=("investment_value", "sum"),
                weight=("weight", "sum"),
                occurrences=("company", "count")
            )
            .reset_index()
        )

        exposure.sort_values(
            by="investment_value",
            ascending=False,
            inplace=True
        )

        exposure.reset_index(
            drop=True,
            inplace=True
        )

        return exposure

    # -------------------------------------------------------------------------
    # Duplicate Companies
    # -------------------------------------------------------------------------

    @classmethod
    def duplicate_companies(
        cls,
        holdings: pd.DataFrame
    ) -> pd.DataFrame:

        exposure = cls.company_exposure(
            holdings
        )

        return exposure[
            exposure["occurrences"] > 1
        ].reset_index(drop=True)

    # -------------------------------------------------------------------------
    # Diversification Score
    # -------------------------------------------------------------------------

    @classmethod
    def diversification_score(
        cls,
        holdings: pd.DataFrame
    ) -> float:

        exposure = cls.company_exposure(
            holdings
        )

        if exposure.empty:
            return 0.0

        unique_companies = len(exposure)

        total_rows = len(holdings)

        return round(
            unique_companies / total_rows * 100,
            2
        )

    # -------------------------------------------------------------------------
    # Top Companies
    # -------------------------------------------------------------------------

    @classmethod
    def top_companies(
        cls,
        holdings: pd.DataFrame,
        n: int = 20
    ) -> pd.DataFrame:

        return (
            cls.company_exposure(
                holdings
            )
            .head(n)
        )

    # -------------------------------------------------------------------------
    # Concentration
    # -------------------------------------------------------------------------

    @classmethod
    def concentration(
        cls,
        holdings: pd.DataFrame,
        top: int = 10
    ) -> float:

        exposure = cls.company_exposure(
            holdings
        )

        if exposure.empty:
            return 0.0

        total = exposure["investment_value"].sum()

        if total == 0:
            return 0.0

        top_value = (
            exposure
            .head(top)
            ["investment_value"]
            .sum()
        )

        return round(
            top_value / total * 100,
            2
        )

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    @classmethod
    def summary(
        cls,
        holdings: pd.DataFrame
    ) -> dict:

        exposure = cls.company_exposure(
            holdings
        )

        duplicates = cls.duplicate_companies(
            holdings
        )

        return {

            "companies": len(exposure),

            "duplicate_companies": len(duplicates),

            "diversification_score":
                cls.diversification_score(
                    holdings
                ),

            "top10_concentration":
                cls.concentration(
                    holdings,
                    top=10
                )

        }