# =============================================================================
# File Name : engines/benchmark_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Benchmark Engine
#
# Responsibilities
# ----------------
# ✓ Benchmark Comparison
# ✓ Portfolio vs Benchmark
# ✓ Benchmark CAGR
# ✓ Benchmark XIRR
# ✓ Alpha
# ✓ Excess Return
#
# =============================================================================

from __future__ import annotations

from analytics.cagr_engine import CAGRCalculator
from analytics.return_engine import ReturnEngine
from analytics.xirr_engine import XIRREngine


class BenchmarkEngine:
    """
    Portfolio Benchmark Comparison Engine
    """

    # -------------------------------------------------------------------------
    # Absolute Difference
    # -------------------------------------------------------------------------

    @staticmethod
    def difference(
        portfolio_value: float,
        benchmark_value: float
    ) -> float:

        return round(

            portfolio_value

            - benchmark_value,

            2

        )

    # -------------------------------------------------------------------------
    # Excess Return
    # -------------------------------------------------------------------------

    @staticmethod
    def excess_return(
        portfolio_return: float,
        benchmark_return: float
    ) -> float:

        return round(

            portfolio_return

            - benchmark_return,

            2

        )

    # -------------------------------------------------------------------------
    # Alpha
    # -------------------------------------------------------------------------

    @staticmethod
    def alpha(
        portfolio_return: float,
        benchmark_return: float
    ) -> float:

        return round(

            portfolio_return

            - benchmark_return,

            2

        )

    # -------------------------------------------------------------------------
    # Portfolio CAGR
    # -------------------------------------------------------------------------

    @staticmethod
    def portfolio_cagr(
        invested: float,
        current_value: float,
        years: float
    ):

        return CAGRCalculator.calculate(

            invested,

            current_value,

            years

        )

    # -------------------------------------------------------------------------
    # Benchmark CAGR
    # -------------------------------------------------------------------------

    @staticmethod
    def benchmark_cagr(
        invested: float,
        benchmark_value: float,
        years: float
    ):

        return CAGRCalculator.calculate(

            invested,

            benchmark_value,

            years

        )

    # -------------------------------------------------------------------------
    # Portfolio XIRR
    # -------------------------------------------------------------------------

    @staticmethod
    def portfolio_xirr(
        cashflows
    ):

        return XIRREngine.portfolio_xirr(

            cashflows

        )

    # -------------------------------------------------------------------------
    # Benchmark XIRR
    # -------------------------------------------------------------------------

    @staticmethod
    def benchmark_xirr(
        cashflows
    ):

        return XIRREngine.benchmark_xirr(

            cashflows

        )

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------

    @classmethod
    def summary(
        cls,
        invested: float,
        portfolio_value: float,
        benchmark_value: float,
        years: float,
        portfolio_cashflows=None,
        benchmark_cashflows=None
    ) -> dict:

        portfolio_return = ReturnEngine.return_percent(

            invested,

            portfolio_value

        )

        benchmark_return = ReturnEngine.return_percent(

            invested,

            benchmark_value

        )

        return {

            "portfolio_value": portfolio_value,

            "benchmark_value": benchmark_value,

            "difference": cls.difference(

                portfolio_value,

                benchmark_value

            ),

            "portfolio_return": portfolio_return,

            "benchmark_return": benchmark_return,

            "excess_return": cls.excess_return(

                portfolio_return,

                benchmark_return

            ),

            "alpha": cls.alpha(

                portfolio_return,

                benchmark_return

            ),

            "portfolio_cagr": cls.portfolio_cagr(

                invested,

                portfolio_value,

                years

            ),

            "benchmark_cagr": cls.benchmark_cagr(

                invested,

                benchmark_value,

                years

            ),

            "portfolio_xirr":

                None if portfolio_cashflows is None

                else cls.portfolio_xirr(

                    portfolio_cashflows

                ),

            "benchmark_xirr":

                None if benchmark_cashflows is None

                else cls.benchmark_xirr(

                    benchmark_cashflows

                )

        }