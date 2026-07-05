# =============================================================================
# File Name : engines/fifo_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# FIFO Engine
#
# Responsibilities
# ----------------
# ✓ FIFO lot matching
# ✓ Remaining units
# ✓ Cost basis calculation
#
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Lot:

    transaction_date: datetime

    units: float

    nav: float

    amount: float


class FIFOEngine:
    """
    FIFO Lot Matching Engine
    """

    @staticmethod
    def consume(
        lots: list[Lot],
        units_to_sell: float
    ) -> list[Lot]:

        remaining = units_to_sell

        consumed = []

        for lot in lots:

            if remaining <= 0:
                break

            if lot.units <= remaining:

                consumed.append(
                    Lot(
                        transaction_date=lot.transaction_date,
                        units=lot.units,
                        nav=lot.nav,
                        amount=lot.amount
                    )
                )

                remaining -= lot.units

                lot.units = 0

            else:

                ratio = remaining / lot.units

                consumed.append(
                    Lot(
                        transaction_date=lot.transaction_date,
                        units=remaining,
                        nav=lot.nav,
                        amount=lot.amount * ratio
                    )
                )

                lot.units -= remaining
                remaining = 0

        return consumed

    @staticmethod
    def remaining(
        lots: list[Lot]
    ) -> list[Lot]:

        return [

            lot

            for lot in lots

            if lot.units > 0

        ]