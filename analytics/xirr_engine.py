# =============================================================================
# File Name : analytics/xirr_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# XIRR Calculation Engine
#
# Supports
# --------
# ✓ Single Investment
# ✓ SIP
# ✓ STP
# ✓ SWP
# ✓ Portfolio XIRR
# ✓ Benchmark XIRR
#
# =============================================================================

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import numpy as np


class XIRREngine:
    """
    Extended Internal Rate of Return (XIRR)
    """

    MAX_ITERATIONS = 100

    TOLERANCE = 1e-7

    INITIAL_GUESS = 0.10

    # -------------------------------------------------------------------------
    # Net Present Value
    # -------------------------------------------------------------------------

    @staticmethod
    def _xnpv(
        rate: float,
        cashflows: Iterable[tuple[datetime, float]]
    ) -> float:

        cashflows = list(cashflows)

        if not cashflows:
            return 0.0

        first_date = cashflows[0][0]

        total = 0.0

        for date, value in cashflows:

            years = (

                date - first_date

            ).days / 365.25

            total += value / ((1 + rate) ** years)

        return total

    # -------------------------------------------------------------------------
    # Derivative
    # -------------------------------------------------------------------------

    @staticmethod
    def _derivative(
        rate: float,
        cashflows: Iterable[tuple[datetime, float]]
    ) -> float:

        cashflows = list(cashflows)

        first_date = cashflows[0][0]

        total = 0.0

        for date, value in cashflows:

            years = (

                date - first_date

            ).days / 365.25

            total -= (

                years

                * value

            ) / (

                (1 + rate)

                **

                (years + 1)

            )

        return total

    # -------------------------------------------------------------------------
    # Calculate
    # -------------------------------------------------------------------------

    @classmethod
    def calculate(
        cls,
        cashflows: Iterable[tuple[datetime, float]],
        guess: float = INITIAL_GUESS
    ) -> float:

        cashflows = sorted(

            cashflows,

            key=lambda x: x[0]

        )

        rate = guess

        for _ in range(

            cls.MAX_ITERATIONS

        ):

            value = cls._xnpv(

                rate,

                cashflows

            )

            derivative = cls._derivative(

                rate,

                cashflows

            )

            if abs(

                derivative

            ) < cls.TOLERANCE:

                break

            new_rate = (

                rate

                -

                value

                / derivative

            )

            if abs(

                new_rate

                - rate

            ) < cls.TOLERANCE:

                return round(

                    new_rate * 100,

                    2

                )

            rate = new_rate

        raise ValueError(

            "XIRR failed to converge."

        )

    # -------------------------------------------------------------------------
    # Validate
    # -------------------------------------------------------------------------

    @staticmethod
    def validate(
        cashflows
    ) -> bool:

        positives = any(

            amount > 0

            for _, amount

            in cashflows

        )

        negatives = any(

            amount < 0

            for _, amount

            in cashflows

        )

        return (

            positives

            and negatives

        )

    # -------------------------------------------------------------------------
    # Portfolio XIRR
    # -------------------------------------------------------------------------

    @classmethod
    def portfolio_xirr(
        cls,
        cashflows
    ) -> float:

        if not cls.validate(

            cashflows

        ):

            return 0.0

        return cls.calculate(

            cashflows

        )

    # -------------------------------------------------------------------------
    # Benchmark XIRR
    # -------------------------------------------------------------------------

    @classmethod
    def benchmark_xirr(
        cls,
        benchmark_cashflows
    ) -> float:

        return cls.portfolio_xirr(

            benchmark_cashflows

        )