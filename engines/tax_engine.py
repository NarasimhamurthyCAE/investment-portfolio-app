# =============================================================================
# File Name : engines/tax_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Tax Engine
#
# Responsibilities
# ----------------
# ✓ STCG
# ✓ LTCG
# ✓ Holding Period
# ✓ Tax Summary
#
# =============================================================================

from __future__ import annotations

from datetime import datetime

from engines.fifo_engine import Lot


class TaxEngine:

    EQUITY_LTCG_DAYS = 365

    # -------------------------------------------------------------------------
    # Holding Period
    # -------------------------------------------------------------------------

    @staticmethod
    def holding_days(
        purchase_date: datetime,
        sale_date: datetime
    ) -> int:

        return (

            sale_date

            - purchase_date

        ).days

    # -------------------------------------------------------------------------
    # Long Term
    # -------------------------------------------------------------------------

    @classmethod
    def is_long_term(
        cls,
        purchase_date: datetime,
        sale_date: datetime
    ) -> bool:

        return (

            cls.holding_days(

                purchase_date,

                sale_date

            )

            >= cls.EQUITY_LTCG_DAYS

        )

    # -------------------------------------------------------------------------
    # Gain
    # -------------------------------------------------------------------------

    @staticmethod
    def capital_gain(
        purchase_amount: float,
        sale_amount: float
    ) -> float:

        return round(

            sale_amount

            - purchase_amount,

            2

        )

    # -------------------------------------------------------------------------
    # Tax Summary
    # -------------------------------------------------------------------------

    @classmethod
    def summarize(
        cls,
        consumed_lots: list[Lot],
        sale_date: datetime,
        sale_value: float
    ) -> dict:

        purchase = sum(

            lot.amount

            for lot in consumed_lots

        )

        gain = cls.capital_gain(

            purchase,

            sale_value

        )

        long_term = all(

            cls.is_long_term(

                lot.transaction_date,

                sale_date

            )

            for lot in consumed_lots

        )

        return {

            "purchase_value": purchase,

            "sale_value": sale_value,

            "capital_gain": gain,

            "tax_type": (

                "LTCG"

                if long_term

                else "STCG"

            )

        }