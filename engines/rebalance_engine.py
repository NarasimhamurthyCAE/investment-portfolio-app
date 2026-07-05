# =============================================================================
# File Name : engines/rebalance_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Rebalance Engine
#
# Calculates buy/sell recommendations based on
# current allocation and target allocation.
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from analytics.allocation.asset_allocation import AssetAllocationEngine
from domain.target_allocation import TargetAllocation


class RebalanceEngine:
    """
    Portfolio Rebalance Engine
    """

    @staticmethod
    def calculate(
        portfolio: pd.DataFrame,
        target: TargetAllocation
    ) -> pd.DataFrame:

        current = AssetAllocationEngine.calculate(portfolio)

        if current.empty:
            return pd.DataFrame()

        total_value = current["current_value"].sum()

        rows = []

        for _, row in current.iterrows():

            asset = row["asset_type"]

            current_pct = float(row["allocation_percent"])

            target_pct = target.target_for(asset)

            current_value = float(row["current_value"])

            target_value = (

                total_value

                * target_pct

                / 100

            )

            difference = target_value - current_value

            action = "HOLD"

            if difference > 1:

                action = "BUY"

            elif difference < -1:

                action = "SELL"

            rows.append({

                "asset_type": asset,

                "current_percent": round(current_pct, 2),

                "target_percent": round(target_pct, 2),

                "difference_percent": round(

                    target_pct - current_pct,

                    2

                ),

                "current_value": round(current_value, 2),

                "target_value": round(target_value, 2),

                "buy_sell_amount": round(difference, 2),

                "action": action

            })

        return pd.DataFrame(rows)