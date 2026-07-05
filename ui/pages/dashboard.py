# =============================================================================
# File Name : ui/pages/dashboard.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Dashboard Page
#
# =============================================================================

from __future__ import annotations

import streamlit as st

from controllers.portfolio_controller import PortfolioController


class DashboardPage:

    def __init__(self):

        self.controller = PortfolioController()

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(self):

        st.title("📈 Investment Portfolio Dashboard")

        summary = self.controller.summary()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Investment",

                f"₹{summary['investment']:,.2f}"

            )

        with col2:

            st.metric(

                "Current Value",

                f"₹{summary['current_value']:,.2f}"

            )

        with col3:

            st.metric(

                "Profit",

                f"₹{summary['profit']:,.2f}"

            )

        with col4:

            value = summary["return_percent"]

            st.metric(

                "Return",

                f"{value:.2f}%"

            )

        st.divider()

        st.subheader("Asset Allocation")

        st.dataframe(

            self.controller.asset_allocation(),

            use_container_width=True

        )

        st.subheader("Top Holdings")

        st.dataframe(

            self.controller.top_holdings(),

            use_container_width=True

        )