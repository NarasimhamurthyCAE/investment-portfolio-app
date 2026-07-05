# =============================================================================
# File Name : analytics/allocation/marketcap_allocation.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Market Cap Allocation Engine
#
# Examples
# --------
# Large Cap
# Mid Cap
# Small Cap
# Micro Cap
#
# =============================================================================

from __future__ import annotations

from analytics.allocation.base_allocation import BaseAllocationEngine


class MarketCapAllocationEngine(BaseAllocationEngine):
    """
    Market Capitalization Allocation
    """

    GROUP_COLUMN = "market_cap"