# =============================================================================
# File : ui/pages/add_investment.py
# =============================================================================

from __future__ import annotations

import streamlit as st

from ui.pages.add_stock import AddStockPage
# from ui.pages.add_etf import AddETFPage
# from ui.pages.add_mutual_fund import AddMutualFundPage


class AddInvestmentPage:

    def render(self):

        st.title("➕ Add Investment")

        st.markdown(
            """
Choose the asset type you want to invest in.
"""
        )

        asset = st.radio(

            "Asset Type",

            [

                "📈 Stock",

                "📊 ETF",

                "💰 Mutual Fund",

            ]

        )

        st.divider()

        if asset == "📈 Stock":

            AddStockPage().render()

        elif asset == "📊 ETF":

            st.info(

                "ETF Module is under development."

            )

        elif asset == "💰 Mutual Fund":

            st.info(

                "Mutual Fund Module is under development."

            )


def render():

    AddInvestmentPage().render()