# =============================================================================
# File Name : ui/components/portfolio_toolbar.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Toolbar
#
# Provides common actions for the Portfolio page.
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class PortfolioToolbar:
    """
    Portfolio toolbar component.
    """

    @staticmethod
    def render():
        """
        Render the portfolio toolbar.

        Returns
        -------
        dict
            Selected actions.
        """

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            refresh = st.button(
                "🔄 Refresh",
                use_container_width=True
            )

        with col2:
            add = st.button(
                "➕ Add",
                use_container_width=True
            )

        with col3:
            export = st.button(
                "📥 Export",
                use_container_width=True
            )

        with col4:
            rebalance = st.button(
                "⚖ Rebalance",
                use_container_width=True
            )

        with col5:
            analytics = st.button(
                "📊 Analytics",
                use_container_width=True
            )

        return {
            "refresh": refresh,
            "add": add,
            "export": export,
            "rebalance": rebalance,
            "analytics": analytics,
        }