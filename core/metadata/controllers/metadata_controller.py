# =============================================================================
# File Name : core/metadata/controllers/metadata_controller.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Metadata Controller
#
# Public entry point for metadata operations.
#
# =============================================================================

from __future__ import annotations

from core.metadata.models.metadata import Metadata
from core.metadata.services.metadata_service import (
    MetadataService,
)


class MetadataController:
    """
    Metadata Controller

    Responsibilities
    ----------------
    ✓ Refresh metadata
    ✓ Validate symbols
    ✓ Check metadata availability

    Never
    -----
    ✗ SQL
    ✗ Yahoo API
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.service = MetadataService()

    # -------------------------------------------------------------------------
    # Refresh
    # -------------------------------------------------------------------------

    def refresh(
        self,
        symbol: str,
        asset_type: str = "STOCK",
    ) -> Metadata:

        return self.service.refresh(

            symbol=symbol,

            asset_type=asset_type,

        )

    # -------------------------------------------------------------------------
    # Refresh If Required
    # -------------------------------------------------------------------------

    def refresh_if_required(
        self,
        symbol: str,
        asset_type: str = "STOCK",
    ) -> Metadata:

        return self.service.refresh_if_required(

            symbol=symbol,

            asset_type=asset_type,

        )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    def validate(
        self,
        symbol: str,
    ) -> bool:

        return self.service.validate(

            symbol

        )

    # -------------------------------------------------------------------------
    # Exists
    # -------------------------------------------------------------------------

    def exists(
        self,
        symbol: str,
    ) -> bool:

        return self.service.exists(

            symbol

        )