# =============================================================================
# File Name : analytics/cagr_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# CAGR Engine
#
# Calculates
# ----------
# ✓ Investment CAGR
# ✓ Portfolio CAGR
# ✓ Benchmark CAGR
# ✓ Annualized Return
#
# =============================================================================

from __future__ import annotations

from datetime import datetime


class CAGRCalculator:
    """
    Compound Annual Growth Rate Calculator
    """

    # -------------------------------------------------------------------------
    # CAGR
    # -------------------------------------------------------------------------

    @staticmethod
    def calculate(

        invested: float,

        current_value: float,

        years: float

    ) -> float:

        if invested <= 0:

            return 0.0

        if current_value <= 0:

            return 0.0

        if years <= 0:

            return 0.0

        return round(

            (

                (

                    current_value

                    / invested

                )

                **

                (

                    1 / years

                )

                -

                1

            )

            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Years
    # -------------------------------------------------------------------------

    @staticmethod
    def years(

        start_date: datetime,

        end_date: datetime

    ) -> float:

        if start_date is None:

            return 0

        if end_date is None:

            return 0

        days = (

            end_date

            - start_date

        ).days

        return round(

            days / 365.25,

            4

        )

    # -------------------------------------------------------------------------
    # Annualized Return
    # -------------------------------------------------------------------------

    @classmethod
    def annualized(

        cls,

        invested,

        current_value,

        start_date,

        end_date

    ):

        years = cls.years(

            start_date,

            end_date

        )

        return cls.calculate(

            invested,

            current_value,

            years

        )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    @staticmethod
    def validate(

        invested,

        current_value,

        years

    ):

        return (

            invested > 0

            and

            current_value > 0

            and

            years > 0

        )