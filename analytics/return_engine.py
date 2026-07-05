# =============================================================================
# File Name : analytics/return_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Return Calculation Engine
#
# Calculates
#
# ✓ Investment
# ✓ Current Value
# ✓ Profit
# ✓ Profit %
# ✓ Annualized Return
#
# =============================================================================

from __future__ import annotations


class ReturnEngine:

    """
    Basic Return Calculations
    """

    # -------------------------------------------------------------------------
    # Current Value
    # -------------------------------------------------------------------------

    @staticmethod
    def current_value(

        units: float,

        latest_nav: float

    ) -> float:

        return round(

            units * latest_nav,

            2

        )

    # -------------------------------------------------------------------------
    # Profit
    # -------------------------------------------------------------------------

    @staticmethod
    def profit(

        invested: float,

        current_value: float

    ) -> float:

        return round(

            current_value

            - invested,

            2

        )

    # -------------------------------------------------------------------------
    # Return %
    # -------------------------------------------------------------------------

    @staticmethod
    def return_percent(

        invested: float,

        current_value: float

    ) -> float:

        if invested <= 0:

            return 0

        return round(

            (

                current_value

                - invested

            )

            / invested

            * 100,

            2

        )

    # -------------------------------------------------------------------------
    # Annualized Return
    # -------------------------------------------------------------------------

    @staticmethod
    def annualized_return(

        invested: float,

        current_value: float,

        years: float

    ) -> float:

        if invested <= 0:

            return 0

        if years <= 0:

            return 0

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
    # Wealth Multiple
    # -------------------------------------------------------------------------

    @staticmethod
    def wealth_multiple(

        invested,

        current_value

    ):

        if invested <= 0:

            return 0

        return round(

            current_value

            / invested,

            3

        )