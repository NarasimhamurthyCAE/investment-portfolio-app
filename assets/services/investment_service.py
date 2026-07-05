# =============================================================================
# File Name : assets/services/investment_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Investment Service
#
# Handles creation of Investments and BUY transactions.
#
# =============================================================================

from __future__ import annotations

from assets.repositories.asset_repository import AssetRepository
from assets.repositories.investment_write_repository import (
    InvestmentWriteRepository,
)

from assets.services.transaction_service import (
    TransactionService,
)

from core.metadata.services.metadata_service import (
    MetadataService,
)


class InvestmentService:
    """
    Investment Business Service.
    """

    def __init__(self):

        self.asset_repository = AssetRepository()

        self.investment_repository = InvestmentWriteRepository()

        self.transaction_service = TransactionService()

        self.metadata_service = MetadataService()

    # -------------------------------------------------------------------------
    # Create Stock Investment
    # -------------------------------------------------------------------------

    def create_stock_investment(
        self,
        *,
        user_id: int,
        stock: dict,
        investment_date,
        units: float,
        price: float,
        charges: float = 0.0,
        broker: str | None = None,
        account_name: str | None = None,
        portfolio_name: str = "Default",
        reference_number: str | None = None,
        notes: str | None = None,
    ) -> int:

        # ---------------------------------------------------------------------
        # Refresh Metadata
        # ---------------------------------------------------------------------

        metadata = None

        try:

            metadata = self.metadata_service.refresh_if_required(

                symbol=stock["symbol"],

                asset_type="STOCK",

            )

        except Exception as ex:

            print("=" * 80)
            print("METADATA REFRESH FAILED")
            print(stock["symbol"])
            print(ex)
            print("=" * 80)

        # ---------------------------------------------------------------------
        # Step 1 : Find or Create Asset
        # ---------------------------------------------------------------------

        print("=" * 80)
        print("STOCK RECEIVED")
        print(stock)
        print("=" * 80)

        asset = {

            "asset_type": "STOCK",

            "asset_name": (

                metadata.company_name

                if metadata

                else stock["company_name"]

            ),

            "symbol": stock["symbol"],

            "scheme_code": None,

            "exchange": (

                metadata.exchange

                if metadata

                else stock.get("exchange")

            ),

            "currency": (

                metadata.currency

                if metadata

                else "INR"

            ),

            "sector": (

                metadata.sector

                if metadata

                else stock.get("sector")

            ),

            "industry": (

                metadata.industry

                if metadata

                else stock.get("industry")

            ),

            "isin": (

                metadata.isin

                if metadata

                else stock.get("isin")

            ),

            "provider": "YAHOO",

            "provider_symbol": stock["symbol"],

            "last_metadata_refresh": (
                metadata.last_refresh
                if metadata
                else None
            ),

        }

        print("SERVICE START")

        asset_id = self.asset_repository.find_or_create(asset)

        # ---------------------------------------------------------------------
        # Step 2 : Find Existing Investment
        # ---------------------------------------------------------------------

        existing = self.investment_repository.find_existing(
            user_id=user_id,
            asset_id=asset_id,
            portfolio_name=portfolio_name,
        )

        if existing:

            investment_id = existing["investment_id"]

        else:

            investment_id = self.investment_repository.create(
                user_id=user_id,
                asset_id=asset_id,
                broker=broker,
                account_name=account_name,
                portfolio_name=portfolio_name,
                notes=notes,
            )

            print("ASSET CREATED", asset_id)

        # ---------------------------------------------------------------------
        # Step 3 : Create BUY Transaction
        # ---------------------------------------------------------------------


        self.transaction_service.create(
            investment_id=investment_id,
            transaction_type="BUY",
            transaction_date=investment_date,
            units=units,
            price=price,
            charges=charges,
            taxes=0.0,
            currency="INR",
            reference_number=reference_number,
            remarks=notes,
        )

        print("SERVICE END")

        print("INVESTMENT CREATED", investment_id)

        return investment_id