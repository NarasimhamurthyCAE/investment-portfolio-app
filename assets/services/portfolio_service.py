# =============================================================================
# File Name : assets/services/portfolio_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Service
#
# High-level coordinator for portfolio operations.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.repositories.asset_repository import AssetRepository
from assets.services.valuation_service import ValuationService


class PortfolioService:
    """
    Portfolio Service

    High-level portfolio operations.
    """

    def __init__(self):

        self.repository = AssetRepository()

        self.valuation = ValuationService()

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int
    ) -> pd.DataFrame:

        return self.repository.portfolio(user_id)

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    def summary(
        self,
        user_id: int
    ) -> dict:

        portfolio = self.portfolio(user_id)

        return self.valuation.portfolio_summary(

            portfolio

        )

    # -------------------------------------------------------------------------
    # Asset Type
    # -------------------------------------------------------------------------

    def asset_type(
        self,
        user_id: int,
        asset_type: str
    ) -> pd.DataFrame:

        return self.repository.by_asset_type(

            user_id,

            asset_type

        )

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        user_id: int,
        keyword: str
    ) -> pd.DataFrame:

        return self.repository.search(

            user_id,

            keyword

        )

    # -------------------------------------------------------------------------
    # Top Holdings
    # -------------------------------------------------------------------------

    def top_holdings(
        self,
        user_id: int,
        limit: int = 10
    ) -> pd.DataFrame:

        portfolio = self.portfolio(

            user_id

        )

        if portfolio.empty:

            return portfolio

        return (

            portfolio

            .sort_values(

                "current_value",

                ascending=False

            )

            .head(limit)

            .reset_index(drop=True)

        )

    # -------------------------------------------------------------------------
    # Asset Types
    # -------------------------------------------------------------------------

    def asset_types(self):

        return self.repository.asset_types()