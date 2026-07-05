# =============================================================================
# File Name : core/metadata/repositories/metadata_repository.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Metadata Repository
#
# Responsibilities
# ----------------
# ✓ Update stocks_master metadata
# ✓ Update assets metadata
# ✓ Check metadata availability
#
# Never
# -----
# ✗ Business Logic
# ✗ Yahoo API
# ✗ Streamlit
#
# =============================================================================

from __future__ import annotations

from repositories.base_repository import BaseRepository

from core.metadata.models.metadata import Metadata


class MetadataRepository(BaseRepository):
    """
    Repository responsible for synchronizing metadata
    between master tables.
    """

    TABLE_NAME = "stocks_master"

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        super().__init__()

    # -------------------------------------------------------------------------
    # Update Stocks Master
    # -------------------------------------------------------------------------

    def update_stock_master(
        self,
        metadata: Metadata,
    ) -> None:

        query = """
        UPDATE stocks_master
        SET

            company_name=%s,

            exchange=%s,

            currency=%s,

            country=%s,

            sector=%s,

            industry=%s,

            isin=%s,

            market_cap=%s,

            listing_status=%s,

            last_metadata_refresh=%s,

            metadata_provider=%s,

            metadata_version=%s,

            updated_at=CURRENT_TIMESTAMP

        WHERE symbol=%s
        """

        self.execute(

            query,

            (

                metadata.company_name,

                metadata.exchange,

                metadata.currency,

                metadata.country,

                metadata.sector,

                metadata.industry,

                metadata.isin,

                metadata.market_cap,

                metadata.listing_status,

                metadata.last_refresh,

                metadata.provider,

                metadata.metadata_version,

                metadata.symbol,

            ),

        )

    # -------------------------------------------------------------------------
    # Update Assets
    # -------------------------------------------------------------------------

    def update_assets(
        self,
        metadata: Metadata,
    ) -> None:

        query = """
        UPDATE assets
        SET

            asset_name=%s,

            exchange=%s,

            currency=%s,

            country=%s,

            sector=%s,

            industry=%s,

            isin=%s,

            provider=%s,

            provider_symbol=%s,

            last_metadata_refresh=%s,

            updated_at=CURRENT_TIMESTAMP

        WHERE symbol=%s
        """

        self.execute(

            query,

            (

                metadata.company_name,

                metadata.exchange,

                metadata.currency,

                metadata.country,

                metadata.sector,

                metadata.industry,

                metadata.isin,

                metadata.provider,

                metadata.provider_symbol,

                metadata.last_refresh,

                metadata.symbol,

            ),

        )

    # -------------------------------------------------------------------------
    # Synchronize
    # -------------------------------------------------------------------------

    def synchronize(
        self,
        metadata: Metadata,
    ) -> None:
        """
        Synchronize metadata across all tables.
        """

        self.update_stock_master(

            metadata

        )

        self.update_assets(

            metadata

        )

    # -------------------------------------------------------------------------
    # Metadata Exists
    # -------------------------------------------------------------------------

    def metadata_exists(
        self,
        symbol: str,
    ) -> bool:

        query = """
        SELECT 1
        FROM stocks_master
        WHERE symbol=%s
        LIMIT 1
        """

        row = self.fetch_one(

            query,

            (

                symbol,

            ),

        )

        return row is not None

    # -------------------------------------------------------------------------
    # Last Refresh
    # -------------------------------------------------------------------------

    def last_refresh(
        self,
        symbol: str,
    ):

        query = """
        SELECT last_metadata_refresh
        FROM stocks_master
        WHERE symbol=%s
        """

        row = self.fetch_one(

            query,

            (

                symbol,

            ),

        )

        if row is None:

            return None

        return row["last_metadata_refresh"]