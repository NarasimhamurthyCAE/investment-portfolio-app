# =============================================================================
# File Name : app.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Main Entry Point
#
# =============================================================================

from __future__ import annotations

import streamlit as st

from ui.pages.dashboard import DashboardPage
from ui.pages.portfolio import PortfolioPage
from ui.pages.add_investment import AddInvestmentPage
from ui.pages.transactions import TransactionsPage


class InvestmentPortfolioApp:

    def __init__(self):

        st.set_page_config(

            page_title="Investment Portfolio App",

            page_icon="📈",

            layout="wide",

            initial_sidebar_state="expanded"

        )

    # -------------------------------------------------------------------------

    def run(self):

        st.sidebar.title(

            "Investment Portfolio"

        )

        page = st.sidebar.radio(

            "Navigation",

            [

                "Dashboard",

                "Portfolio",

                "Add Investment",

                "Transactions"

            ]

        )

        if page == "Dashboard":

            DashboardPage().render()

        elif page == "Portfolio":

            PortfolioPage().render()

        elif page == "Add Investment":

            AddInvestmentPage().render()

        elif page == "Transactions":

            TransactionsPage().render()


# =============================================================================

if __name__ == "__main__":

    InvestmentPortfolioApp().run()