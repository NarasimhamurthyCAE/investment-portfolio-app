# =============================================================================
# File Name : ui/components/portfolio_footer.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Footer Component
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class PortfolioFooter:

    @staticmethod
    def render(portfolio_size: int):

        st.divider()

        st.caption(

            f"Showing {portfolio_size:,} investment(s)."

        )

        st.caption(

            "Investment Portfolio App V2"

        )