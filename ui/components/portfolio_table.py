# =============================================================================
# File Name : ui/components/portfolio_table.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Table Component
#
# =============================================================================

from __future__ import annotations

import pandas as pd
import streamlit as st


class PortfolioTable:
    """
    Portfolio table renderer.
    """

    @staticmethod
    def render(
        portfolio: pd.DataFrame
    ):

        if portfolio.empty:

            st.info(

                "No investments found."

            )

            return

        st.dataframe(

            portfolio,

            use_container_width=True,

            hide_index=True

        )