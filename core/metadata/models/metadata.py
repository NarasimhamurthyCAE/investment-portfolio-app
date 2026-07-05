# =============================================================================
# File Name : core/metadata/models/metadata.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Canonical Metadata Model
#
# Used by:
#   ✓ Stocks
#   ✓ ETFs
#   ✓ REITs
#   ✓ INVITs
#   ✓ Mutual Funds (future)
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Metadata:
    """
    Canonical metadata object shared across the application.
    """

    # -------------------------------------------------------------
    # Asset
    # -------------------------------------------------------------

    asset_type: str

    symbol: str

    provider_symbol: str

    company_name: str

    # -------------------------------------------------------------
    # Exchange
    # -------------------------------------------------------------

    exchange: str | None = None

    currency: str | None = "INR"

    country: str | None = "India"

    # -------------------------------------------------------------
    # Classification
    # -------------------------------------------------------------

    sector: str | None = None

    industry: str | None = None

    category: str | None = None

    subcategory: str | None = None

    # -------------------------------------------------------------
    # Security
    # -------------------------------------------------------------

    isin: str | None = None

    listing_status: str = "ACTIVE"

    market_cap: float | None = None

    # -------------------------------------------------------------
    # Provider
    # -------------------------------------------------------------

    provider: str = "YAHOO"

    # -------------------------------------------------------------
    # Synchronization
    # -------------------------------------------------------------

    last_refresh: datetime | None = None

    metadata_version: int = 1