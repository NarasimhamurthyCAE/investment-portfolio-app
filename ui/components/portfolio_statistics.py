# =============================================================================
# File Name : ui/components/portfolio_statistics.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Statistics Component
#
# Displays key portfolio statistics.
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class PortfolioStatistics:
    """
    Portfolio statistics component.
    """

    @staticmethod
    def render(summary: dict):

        st.subheader("📈 Portfolio Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Total Holdings",

                summary.get("total_holdings", 0)

            )

        with col2:

            st.metric(

                "Mutual Funds",

                summary.get("mutual_funds", 0)

            )

        with col3:

            st.metric(

                "ETFs",

                summary.get("etfs", 0)

            )

        with col4:

            st.metric(

                "Stocks",

                summary.get("stocks", 0)

            )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Largest Holding",

                summary.get(

                    "largest_holding",

                    "-"

                )

            )

        with col2:

            st.metric(

                "Best Performer",

                summary.get(

                    "best_performer",

                    "-"

                )

            )