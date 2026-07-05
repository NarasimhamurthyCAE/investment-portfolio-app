# =============================================================================
# File Name : ui/pages/portfolio.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Page
#
# Displays portfolio across Mutual Funds, ETFs and Stocks.
#
# =============================================================================

from __future__ import annotations

import streamlit as st

from controllers.portfolio_controller import PortfolioController

from ui.components.summary_cards import SummaryCards
from ui.components.portfolio_toolbar import PortfolioToolbar
from ui.components.search_bar import SearchBar
from ui.components.filter_panel import FilterPanel
from ui.components.portfolio_table import PortfolioTable
from ui.components.portfolio_statistics import PortfolioStatistics
from ui.components.portfolio_charts import PortfolioCharts
from ui.components.portfolio_export import PortfolioExport
from ui.components.portfolio_footer import PortfolioFooter
from ui.components.portfolio_actions import PortfolioActions


class PortfolioPage:
    """
    Portfolio Page
    """

    def __init__(self):

        self.controller = PortfolioController()

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(
        self,
        user_id: int = 1
    ):

        st.title("📊 Portfolio")

        # -------------------------------------------------------------
        # Summary
        # -------------------------------------------------------------

        summary = self.controller.summary(user_id)

        SummaryCards.render(summary)

        st.divider()

        # -------------------------------------------------------------
        # Toolbar
        # -------------------------------------------------------------

        toolbar = PortfolioToolbar.render()

        st.divider()

        # -------------------------------------------------------------
        # Search
        # -------------------------------------------------------------

        keyword = SearchBar.render(

            key="portfolio_search",

            placeholder="Search investments..."

        )

        # -------------------------------------------------------------
        # Filters
        # -------------------------------------------------------------

        filters = FilterPanel.render()

        st.divider()

        # -------------------------------------------------------------
        # Load Portfolio
        # -------------------------------------------------------------

        portfolio = self.controller.portfolio(user_id)

        # -------------------------------------------------------------
        # Search
        # -------------------------------------------------------------

        if keyword:

            keyword = keyword.lower()

            portfolio = portfolio[

                portfolio.astype(str)

                .apply(

                    lambda row:

                    row.str.lower().str.contains(keyword)

                )

                .any(axis=1)

            ]

        # -------------------------------------------------------------
        # Asset Type Filter
        # -------------------------------------------------------------

        asset_type = filters["asset_type"]

        if (

            asset_type != "All"

            and

            "asset_type" in portfolio.columns

        ):

            portfolio = portfolio[

                portfolio["asset_type"] == asset_type

            ]

        # -------------------------------------------------------------
        # Table
        # -------------------------------------------------------------

        PortfolioTable.render(

            portfolio

        )

        # -------------------------------------------------------------
        # Statistics
        # -------------------------------------------------------------

        PortfolioStatistics.render(

            summary

        )

        # -------------------------------------------------------------
        # Charts
        # -------------------------------------------------------------

        PortfolioCharts.render(

            portfolio

        )

        # -------------------------------------------------------------
        # Export
        # -------------------------------------------------------------

        PortfolioExport.render(

            portfolio

        )

        # -------------------------------------------------------------
        # Actions
        # -------------------------------------------------------------

        actions = PortfolioActions.render()

        if actions["refresh"]:

            st.info(

                "Portfolio refresh will be implemented."

            )

        if actions["add"]:

            st.info(

                "Navigate to Add Investment page."

            )

        if actions["reports"]:

            st.info(

                "Reports module will be opened."

            )

        if actions["rebalance"]:

            st.info(

                "Portfolio rebalance module will be added."

            )

        # -------------------------------------------------------------
        # Footer
        # -------------------------------------------------------------

        PortfolioFooter.render(

            len(portfolio)

        )


# =============================================================================
# Standalone Execution
# =============================================================================

def render():

    PortfolioPage().render()


if __name__ == "__main__":

    render()