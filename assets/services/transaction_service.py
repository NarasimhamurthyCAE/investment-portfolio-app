# =============================================================================
# File Name : assets/services/transaction_service.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Transaction Service
#
# Handles investment transactions for:
#   ✓ Mutual Funds
#   ✓ ETFs
#   ✓ Stocks
#
# Responsibilities
# ----------------
# • Buy
# • Sell
# • SIP
# • STP
# • SWP
# • Average Cost
# • Remaining Units
#
# =============================================================================

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

import pandas as pd

from assets.repositories.asset_repository import AssetRepository
from core.exceptions import ValidationError


class TransactionService:
    """
    Transaction business logic.
    """

    def __init__(self):

        self.repository = AssetRepository()

    # -------------------------------------------------------------------------
    # BUY
    # -------------------------------------------------------------------------

    def buy(
        self,
        investment_id: int,
        trade_date: datetime,
        amount: float,
        price: float,
        charges: float = 0.0
    ) -> dict:

        if amount <= 0:

            raise ValidationError(

                "Investment amount must be greater than zero."

            )

        if price <= 0:

            raise ValidationError(

                "Price must be greater than zero."

            )

        net_amount = Decimal(str(amount)) - Decimal(str(charges))

        units = net_amount / Decimal(str(price))

        return {

            "investment_id": investment_id,

            "transaction_type": "BUY",

            "trade_date": trade_date,

            "amount": float(amount),

            "price": float(price),

            "charges": float(charges),

            "units": round(float(units), 6)

        }

    # -------------------------------------------------------------------------
    # SELL
    # -------------------------------------------------------------------------

    def sell(
        self,
        investment_id: int,
        trade_date: datetime,
        units: float,
        price: float,
        charges: float = 0.0
    ) -> dict:

        if units <= 0:

            raise ValidationError(

                "Units must be greater than zero."

            )

        if price <= 0:

            raise ValidationError(

                "Price must be greater than zero."

            )

        gross_amount = Decimal(str(units)) * Decimal(str(price))

        net_amount = gross_amount - Decimal(str(charges))

        return {

            "investment_id": investment_id,

            "transaction_type": "SELL",

            "trade_date": trade_date,

            "units": round(units, 6),

            "price": float(price),

            "charges": float(charges),

            "amount": round(float(net_amount), 2)

        }

    # -------------------------------------------------------------------------
    # Average Purchase Price
    # -------------------------------------------------------------------------

    @staticmethod
    def average_price(
        transactions: pd.DataFrame
    ) -> float:

        if transactions.empty:

            return 0.0

        buys = transactions[
            transactions["transaction_type"] == "BUY"
        ]

        if buys.empty:

            return 0.0

        total_units = buys["units"].sum()

        if total_units == 0:

            return 0.0

        total_cost = buys["amount"].sum()

        return round(

            total_cost / total_units,

            4

        )

    # -------------------------------------------------------------------------
    # Remaining Units
    # -------------------------------------------------------------------------

    @staticmethod
    def remaining_units(
        transactions: pd.DataFrame
    ) -> float:

        if transactions.empty:

            return 0.0

        bought = transactions.loc[
            transactions["transaction_type"] == "BUY",
            "units"
        ].sum()

        sold = transactions.loc[
            transactions["transaction_type"] == "SELL",
            "units"
        ].sum()

        return round(

            bought - sold,

            6

        )

    # -------------------------------------------------------------------------
    # Current Investment Value
    # -------------------------------------------------------------------------

    @staticmethod
    def current_value(
        transactions: pd.DataFrame,
        latest_price: float
    ) -> float:

        units = TransactionService.remaining_units(

            transactions

        )

        return round(

            units * latest_price,

            2

        )

    # -------------------------------------------------------------------------
    # Create Transaction
    # -------------------------------------------------------------------------

    def create(
        self,
        investment_id: int,
        transaction_type: str,
        transaction_date,
        units: float,
        price: float,
        charges: float = 0.0,
        taxes: float = 0.0,
        currency: str = "INR",
        reference_number: str | None = None,
        remarks: str | None = None,
    ) -> int:

        if units <= 0:

            raise ValidationError(
                "Units must be greater than zero."
            )

        if price <= 0:

            raise ValidationError(
                "Price must be greater than zero."
            )

        amount = (units * price) + charges + taxes

        from assets.repositories.transaction_write_repository import (
            TransactionWriteRepository,
        )

        repository = TransactionWriteRepository()

        return repository.create(
            investment_id=investment_id,
            transaction_type=transaction_type,
            transaction_date=transaction_date,
            units=units,
            price=price,
            amount=amount,
            charges=charges,
            taxes=taxes,
            currency=currency,
            reference_number=reference_number,
            remarks=remarks,
        )