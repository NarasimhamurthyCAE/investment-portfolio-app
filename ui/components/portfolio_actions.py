# =============================================================================
# File Name : ui/components/portfolio_actions.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Actions Component
#
# Displays action buttons for portfolio operations.
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class PortfolioActions:
    """
    Portfolio actions component.
    """

    @staticmethod
    def render(prefix: str = "portfolio"):

        st.subheader("⚡ Quick Actions")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            add = st.button(
                "➕ Add Investment",
                key=f"{prefix}_add_investment",
                use_container_width=True
            )

        with col2:

            refresh = st.button(
                "🔄 Refresh Prices",
                key=f"{prefix}_refresh_prices",
                use_container_width=True
            )

        with col3:

            rebalance = st.button(
                "⚖ Rebalance",
                key=f"{prefix}_rebalance",
                use_container_width=True
            )

        with col4:

            reports = st.button(
                "📄 Reports",
                key=f"{prefix}_reports",
                use_container_width=True
            )

        return {
            "add": add,
            "refresh": refresh,
            "rebalance": rebalance,
            "reports": reports
        }