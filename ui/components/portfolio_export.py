# =============================================================================
# File Name : ui/components/portfolio_export.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Export Component
#
# Export portfolio data.
#
# =============================================================================

from __future__ import annotations

import streamlit as st
import pandas as pd


class PortfolioExport:
    """
    Portfolio export component.
    """

    @staticmethod
    def render(
        portfolio: pd.DataFrame
    ):

        if portfolio.empty:

            return

        csv = portfolio.to_csv(

            index=False

        )

        st.download_button(

            label="📥 Download CSV",

            data=csv,

            file_name="portfolio.csv",

            mime="text/csv",

            use_container_width=True

        )