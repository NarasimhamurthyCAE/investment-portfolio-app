# =============================================================================
# File Name : assets/providers/mf_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Mutual Fund Provider
#
# Wrapper around MFAPIClient.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.providers.base_provider import BaseProvider
from api.mfapi_client import MFAPIClient


class MFProvider(BaseProvider):

    PROVIDER_NAME = "MFAPI"

    def __init__(self):

        self.client = MFAPIClient()

    # -------------------------------------------------------------------------
    # Search
    # -------------------------------------------------------------------------

    def search(
        self,
        keyword: str
    ) -> pd.DataFrame:

        return self.client.search(

            keyword

        )

    # -------------------------------------------------------------------------
    # Latest NAV
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        identifier: str
    ) -> float:

        return self.client.latest_nav(

            identifier

        )

    # -------------------------------------------------------------------------
    # Historical NAV
    # -------------------------------------------------------------------------

    def historical_data(
        self,
        identifier: str,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:

        data = self.client.historical_nav(identifier)

        return pd.DataFrame(data)

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate(
        self,
        identifier: str
    ) -> bool:

        return self.client.validate(

            identifier

        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        identifier: str
    ) -> dict:

        return self.client.metadata(

            identifier

        )