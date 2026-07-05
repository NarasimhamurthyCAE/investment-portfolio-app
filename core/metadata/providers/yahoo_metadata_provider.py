# =============================================================================
# File Name : core/metadata/providers/yahoo_metadata_provider.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Yahoo Metadata Provider
#
# Responsibilities
# ----------------
# ✓ Download metadata from Yahoo Finance
# ✓ Convert to Metadata model
# ✓ No database access
#
# =============================================================================

from __future__ import annotations

from datetime import datetime

from api.yahoo_client import YahooClient

from core.metadata.models.metadata import Metadata


class YahooMetadataProvider:
    """
    Yahoo Finance Metadata Provider

    Pure provider.

    Never:
        ✗ SQL
        ✗ Repository
        ✗ Streamlit
    """

    PROVIDER_NAME = "YAHOO"

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.client = YahooClient()

    # -------------------------------------------------------------------------
    # Get Metadata
    # -------------------------------------------------------------------------

    def metadata(
        self,
        symbol: str,
        asset_type: str = "STOCK",
    ) -> Metadata:
        """
        Download metadata from Yahoo and return
        canonical Metadata object.
        """

        data = self.client.metadata(symbol)

        return Metadata(

            asset_type=asset_type,

            symbol=symbol,

            provider_symbol=symbol,

            company_name=data.get(
                "name",
                symbol,
            ),

            exchange=self._normalize_exchange(
                data.get("exchange")
            ),

            currency=data.get(
                "currency",
                "INR",
            ),

            country=data.get(
                "country",
                "India",
            ),

            sector=data.get(
                "sector",
            ),

            industry=data.get(
                "industry",
            ),

            isin=data.get(
                "isin",
            ),

            market_cap=data.get(
                "marketCap",
            ),

            listing_status="ACTIVE",

            provider=self.PROVIDER_NAME,

            last_refresh=datetime.now(),

        )

    # -------------------------------------------------------------------------
    # Exists
    # -------------------------------------------------------------------------

    def exists(
        self,
        symbol: str,
    ) -> bool:
        """
        Returns True if Yahoo has data for the symbol.
        """

        return self.client.validate(symbol)

    def _normalize_exchange(
        self,
        exchange: str | None,
    ) -> str:

        mapping = {

            "NSI": "NSE",

            "BSE": "BSE",

            "NASDAQ": "NASDAQ",

            "NYQ": "NYSE",

        }

        if not exchange:

            return ""

        return mapping.get(exchange, exchange)