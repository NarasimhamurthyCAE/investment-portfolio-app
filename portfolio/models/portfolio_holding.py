# =============================================================================
# File Name : portfolio/models/portfolio_holding.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class PortfolioHolding:
    """
    Represents one portfolio holding after all transactions
    have been processed.

    This is a pure business model.

    It contains NO:
        - SQL
        - Streamlit
        - Pandas
        - Database code
    """

    # ---------------------------------------------------------
    # Asset Information
    # ---------------------------------------------------------

    asset_id: int

    investment_id: int

    asset_name: str

    asset_type: str

    symbol: str

    category: str | None = None

    subcategory: str | None = None

    portfolio_name: str | None = None

    account_name: str | None = None

    broker: str | None = None

    # ---------------------------------------------------------
    # Holdings
    # ---------------------------------------------------------

    units: float = 0.0

    average_cost: float = 0.0

    invested_value: float = 0.0

    # ---------------------------------------------------------
    # Market
    # ---------------------------------------------------------

    current_price: float = 0.0

    current_value: float = 0.0

    # ---------------------------------------------------------
    # Returns
    # ---------------------------------------------------------

    profit_loss: float = 0.0

    profit_loss_percent: float = 0.0

    # ---------------------------------------------------------
    # Future Extensions
    # ---------------------------------------------------------

    realized_gain: float = 0.0

    unrealized_gain: float = 0.0

    dividend: float = 0.0

    xirr: float = 0.0

    allocation_percent: float = 0.0