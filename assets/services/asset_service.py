# =============================================================================
# File Name : assets/services/asset_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Asset Service
#
# Coordinates asset-related operations.
#
# Supported Assets
# ----------------
# ✓ Mutual Funds
# ✓ ETFs
# ✓ Stocks
#
# =============================================================================

# =============================================================================
# File Name : assets/services/asset_service.py
# =============================================================================

from __future__ import annotations

from datetime import datetime

import pandas as pd

from assets.providers.provider_factory import ProviderFactory
from assets.repositories.asset_repository import AssetRepository
from assets.repositories.investment_write_repository import InvestmentWriteRepository
from assets.repositories.transaction_write_repository import TransactionWriteRepository
from assets.services.transaction_service import TransactionService
from core.exceptions import ValidationError
from database.transaction_manager import TransactionManager


class AssetService:
    """
    Asset Service

    High-level coordinator for asset operations.
    """

    def __init__(self):

        self.repository = AssetRepository()

        self.investment_writer = InvestmentWriteRepository()

        self.transaction_writer = TransactionWriteRepository()

        self.transaction_service = TransactionService()

        self.asset_repository = AssetRepository()

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    def portfolio(
        self,
        user_id: int
    ) -> pd.DataFrame:

        return self.repository.portfolio(user_id)

    # -------------------------------------------------------------------------
    # Asset Type
    # -------------------------------------------------------------------------

    def assets(
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

    def search_market(
        self,
        asset_type: str,
        keyword: str
    ) -> pd.DataFrame:

        provider = ProviderFactory.get(asset_type)

        return provider.search(keyword)

    # -------------------------------------------------------------------------
    # Latest Price
    # -------------------------------------------------------------------------

    def latest_price(
        self,
        asset_type: str,
        identifier: str
    ) -> float:

        provider = ProviderFactory.get(asset_type)

        return provider.latest_price(identifier)

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

        provider = ProviderFactory.get(asset_type)

        return provider.historical_data(

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

        provider = ProviderFactory.get(asset_type)

        return provider.metadata(identifier)

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def validate(
        self,
        asset_type: str,
        identifier: str
    ) -> bool:

        provider = ProviderFactory.get(asset_type)

        return provider.validate(identifier)

    # -------------------------------------------------------------------------
    # Supported Assets
    # -------------------------------------------------------------------------

    @staticmethod
    def supported_assets():

        return ProviderFactory.supported_assets()

    # -------------------------------------------------------------------------
    # Add Investment
    # -------------------------------------------------------------------------

    def add_investment(
        self,
        *,
        user_id: int,
        asset_type: str,
        identifier: str,
        investment_date: datetime,
        amount: float,
        price: float,
        charges: float = 0.0,
        remarks: str = "",
    ) -> int:
        """
        Creates an investment together with its initial BUY transaction.

        Returns
        -------
        int
            Newly created investment ID.
        """

        if amount <= 0:

            raise ValidationError(
                "Investment amount must be greater than zero."
            )

        if price <= 0:

            raise ValidationError(
                "Price must be greater than zero."
            )

        provider = ProviderFactory.get(asset_type)

        existing = self.repository.find_existing(
            user_id=user_id,
            asset_type=asset_type,
            identifier=identifier,
        )

        if existing:

            raise ValidationError(

                "Investment already exists. Please use a BUY transaction instead."

            )

        if not provider.validate(identifier):

            raise ValidationError(

                f"Invalid {asset_type}: {identifier}"

            )

        metadata = provider.metadata(identifier)

        # ------------------------------------------------------------------
        # Build Asset Dictionary
        # ------------------------------------------------------------------

        asset = {

            "asset_type": asset_type,

            "asset_name": metadata.get(
                "name",
                identifier
            ),

            "symbol": metadata.get(
                "symbol"
            ),

            "scheme_code": metadata.get(
                "scheme_code"
            ),

            "exchange": metadata.get(
                "exchange"
            ),

            "currency": metadata.get(
                "currency"
            ),

            "sector": metadata.get(
                "sector"
            ),

            "industry": metadata.get(
                "industry"
            ),

            "isin": metadata.get(
                "isin"
            ),

            "provider": provider.PROVIDER_NAME,

            "provider_symbol": identifier,

        }

        asset_id = self.asset_repository.find_or_create(
            asset
        )

        transaction = self.transaction_service.buy(

            investment_id=0,

            trade_date=investment_date,

            amount=amount,

            price=price,

            charges=charges,

        )

        investment = {

            "user_id": user_id,

            "asset_type": asset_type,

            "asset_id": asset_id,

            "investment_date": investment_date,

            "amount": amount,

            "units": transaction["units"],

            "latest_nav": price,

            "current_value": amount,

        }

        with TransactionManager.transaction():

            investment_id = self.investment_writer.create(

                investment

            )

            transaction["investment_id"] = investment_id

            transaction["remarks"] = remarks

            self.transaction_writer.create(

                transaction

            )

        return investment_id


    