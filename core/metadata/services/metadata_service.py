# =============================================================================
# File Name : core/metadata/services/metadata_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Metadata Service
#
# Responsibilities
# ----------------
# ✓ Download metadata from provider
# ✓ Normalize metadata
# ✓ Synchronize database
# ✓ Return Metadata object
#
# =============================================================================

from __future__ import annotations

from core.metadata.models.metadata import Metadata
from core.metadata.providers.yahoo_metadata_provider import (
    YahooMetadataProvider,
)
from core.metadata.repositories.metadata_repository import (
    MetadataRepository,
)


class MetadataService:
    """
    Metadata Business Service.

    This is the only business layer that should know
    how metadata is downloaded and synchronized.
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.provider = YahooMetadataProvider()

        self.repository = MetadataRepository()

    # -------------------------------------------------------------------------
    # Refresh Metadata
    # -------------------------------------------------------------------------

    def refresh(
        self,
        symbol: str,
        asset_type: str = "STOCK",
    ) -> Metadata:
        """
        Download latest metadata and synchronize
        local database.
        """

        metadata = self.provider.metadata(

            symbol=symbol,

            asset_type=asset_type,

        )

        self.repository.synchronize(

            metadata

        )

        return metadata

    # -------------------------------------------------------------------------
    # Metadata Exists
    # -------------------------------------------------------------------------

    def exists(
        self,
        symbol: str,
    ) -> bool:

        return self.repository.metadata_exists(

            symbol

        )

    # -------------------------------------------------------------------------
    # Validate Symbol
    # -------------------------------------------------------------------------

    def validate(
        self,
        symbol: str,
    ) -> bool:

        return self.provider.exists(

            symbol

        )

    # -------------------------------------------------------------------------
    # Refresh If Required
    # -------------------------------------------------------------------------

    def refresh_if_required(
        self,
        symbol: str,
        asset_type: str = "STOCK",
    ) -> Metadata:
        """
        Future implementation:

        • Check last refresh date.
        • Refresh only if stale.

        Current implementation:
        Always refresh.
        """

        return self.refresh(

            symbol=symbol,

            asset_type=asset_type,

        )