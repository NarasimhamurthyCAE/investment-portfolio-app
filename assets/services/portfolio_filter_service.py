# =============================================================================
# File Name : services/portfolio_filter_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Filter Service
#
# Centralized filtering for portfolio data.
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class PortfolioFilterService:
    """
    Portfolio filtering utilities.
    """

    @staticmethod
    def search(
        portfolio: pd.DataFrame,
        keyword: str,
    ) -> pd.DataFrame:

        if portfolio.empty:

            return portfolio

        if not keyword:

            return portfolio

        keyword = keyword.lower()

        return portfolio[

            portfolio.astype(str)

            .apply(

                lambda row:

                row.str.lower().str.contains(keyword)

            )

            .any(axis=1)

        ]

    @staticmethod
    def asset_type(
        portfolio: pd.DataFrame,
        asset_type: str,
    ) -> pd.DataFrame:

        if portfolio.empty:

            return portfolio

        if asset_type == "All":

            return portfolio

        if "asset_type" not in portfolio.columns:

            return portfolio

        return portfolio[

            portfolio["asset_type"] == asset_type

        ]

    @staticmethod
    def sort(
        portfolio: pd.DataFrame,
        column: str,
        ascending: bool = True,
    ) -> pd.DataFrame:

        if portfolio.empty:

            return portfolio

        if column not in portfolio.columns:

            return portfolio

        return portfolio.sort_values(

            by=column,

            ascending=ascending

        )

    @staticmethod
    def paginate(
        portfolio: pd.DataFrame,
        page: int,
        page_size: int,
    ) -> pd.DataFrame:

        start = page * page_size

        end = start + page_size

        return portfolio.iloc[start:end]