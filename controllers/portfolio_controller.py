# =============================================================================
# File Name : controllers/portfolio_controller.py
# =============================================================================

from __future__ import annotations

import pandas as pd

from portfolio.services.portfolio_service import PortfolioService
from assets.services.portfolio_filter_service import PortfolioFilterService


class PortfolioController:

    def __init__(self):

        self.service = PortfolioService()

        self.filter_service = PortfolioFilterService()

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return self.service.portfolio(user_id)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def summary(
        self,
        user_id: int = 1
    ) -> dict:

        return self.service.summary(user_id)

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        portfolio: pd.DataFrame,
        keyword: str
    ) -> pd.DataFrame:

        return self.filter_service.search(
            portfolio,
            keyword
        )

    # -------------------------------------------------------------------------
    # Filter by Asset Type
    # -------------------------------------------------------------------------

    def asset_type(
        self,
        portfolio: pd.DataFrame,
        asset_type: str
    ) -> pd.DataFrame:

        return self.filter_service.asset_type(
            portfolio,
            asset_type
        )

    # -------------------------------------------------------------------------
    # Sort
    # -------------------------------------------------------------------------

    def sort(
        self,
        portfolio: pd.DataFrame,
        column: str,
        ascending: bool = True
    ) -> pd.DataFrame:

        return self.filter_service.sort(
            portfolio,
            column,
            ascending
        )

    # -------------------------------------------------------------------------
    # Pagination
    # -------------------------------------------------------------------------

    def paginate(
        self,
        portfolio: pd.DataFrame,
        page: int,
        page_size: int
    ) -> pd.DataFrame:

        return self.filter_service.paginate(
            portfolio,
            page,
            page_size
        )

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(
        self,
        user_id: int = 1,
        limit: int = 10
    ) -> pd.DataFrame:

        return self.service.top_holdings(
            user_id,
            limit
        )

    # -------------------------------------------------------------------------
    # Temporary Dashboard Methods
    # -------------------------------------------------------------------------

    def asset_allocation(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return pd.DataFrame(
            columns=[
                "asset_type",
                "allocation"
            ]
        )

    def sector_allocation(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return pd.DataFrame(
            columns=[
                "sector",
                "allocation"
            ]
        )

    def industry_allocation(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return pd.DataFrame(
            columns=[
                "industry",
                "allocation"
            ]
        )

    def country_allocation(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return pd.DataFrame(
            columns=[
                "country",
                "allocation"
            ]
        )