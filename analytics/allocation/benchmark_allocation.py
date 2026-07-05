# =============================================================================
# File Name : analytics/allocation/benchmark_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Benchmark Allocation Engine
#
# Examples
# --------
# NIFTY 50 TRI
# NIFTY 500 TRI
# NIFTY Midcap 150 TRI
# NASDAQ 100
# S&P 500
#
# =============================================================================

from __future__ import annotations

from analytics.allocation.base_allocation import BaseAllocationEngine


class BenchmarkAllocationEngine(BaseAllocationEngine):
    """
    Benchmark Allocation
    """

    GROUP_COLUMN = "benchmark"