# =============================================================================
# File Name : ui/components/portfolio_charts.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Charts Component
#
# =============================================================================

from __future__ import annotations

import pandas as pd
import streamlit as st


class PortfolioCharts:
    """
    Portfolio chart component.
    """

    @staticmethod
    def render(
        portfolio: pd.DataFrame
    ):

        if portfolio.empty:

            return

        st.subheader("📊 Portfolio Allocation")

        if "asset_type" in portfolio.columns:

            allocation = (

                portfolio

                .groupby("asset_type")["current_value"]

                .sum()

            )

            st.bar_chart(

                allocation

            )

        if "current_value" in portfolio.columns:

            top = (

                portfolio

                .sort_values(

                    "current_value",

                    ascending=False

                )

                .head(10)

            )

            if "scheme_name" in top.columns:

                chart = top.set_index(

                    "scheme_name"

                )["current_value"]

            elif "symbol" in top.columns:

                chart = top.set_index(

                    "symbol"

                )["current_value"]

            else:

                chart = top["current_value"]

            st.subheader(

                "🏆 Top Holdings"

            )

            st.bar_chart(

                chart

            )