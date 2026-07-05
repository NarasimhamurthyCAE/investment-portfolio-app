# =============================================================================
# File Name : controllers/asset_controller.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Asset Controller
#
# Controller layer between UI and Asset Engine.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.engines.asset_engine import AssetEngine


class AssetController:
    """
    Asset Controller

    UI should communicate only with this controller.
    """

    def __init__(self):

        self.engine = AssetEngine()

    # -------------------------------------------------------------------------
    # Supported Assets
    # -------------------------------------------------------------------------

    def supported_assets(self) -> list[str]:

        return self.engine.supported_assets()

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int = 1
    ) -> pd.DataFrame:

        return self.engine.portfolio(user_id)

    # -------------------------------------------------------------------------
    # Portfolio Summary
    # -------------------------------------------------------------------------

    def summary(
        self,
        user_id: int = 1
    ) -> dict:

        return self.engine.summary(user_id)

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search_market(
        self,
        asset_type: str,
        keyword: str
    ) -> pd.DataFrame:

        return self.engine.search_market(
            asset_type,
            keyword
        )

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        asset_type: str,
        identifier: str
    ) -> float:

        return self.engine.latest_price(
            asset_type,
            identifier
        )

    # -------------------------------------------------------------------------
    # Historical Data
    # -------------------------------------------------------------------------

    def historical_data(
        self,
        asset_type: str,
        identifier: str,
        start_date=None,
        end_date=None
    ):

        return self.engine.historical_data(
            asset_type,
            identifier,
            start_date,
            end_date
        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        asset_type: str,
        identifier: str
    ) -> dict:

        return self.engine.metadata(
            asset_type,
            identifier
        )

    # -------------------------------------------------------------------------
    # Validate Asset
    # -------------------------------------------------------------------------

    def validate(
        self,
        asset_type: str,
        identifier: str
    ) -> bool:

        return self.engine.asset_service.validate(
            asset_type,
            identifier
        )

    # -------------------------------------------------------------------------
    # Add Investment
    # -------------------------------------------------------------------------

    def add_investment(
        self,
        **kwargs
    ) -> int:

        return self.engine.add_investment(
            **kwargs
        )