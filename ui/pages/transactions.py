# =============================================================================
# File Name : ui/pages/transactions.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import streamlit as st

from transactions.controllers.transaction_controller import (
    TransactionController,
)

from ui.components.filter_panel import FilterPanel
from ui.components.investment_history import InvestmentHistory
from ui.components.search_bar import SearchBar
from ui.components.transaction_summary import TransactionSummary
from ui.components.transaction_table import TransactionTable


class TransactionsPage:
    """
    Professional Transactions Page

    Responsibilities
    ----------------
    ✓ Search
    ✓ Filters
    ✓ Dashboard
    ✓ Transaction Table
    ✓ Investment History

    No calculations.
    """

    def __init__(self):

        self.controller = TransactionController()

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(
        self,
        user_id: int = 1,
    ):

        st.title("💳 Transactions")

        # ---------------------------------------------------------
        # Search
        # ---------------------------------------------------------

        keyword = SearchBar.render(

            key="transaction_search",

            placeholder="Search Investment",

        )

        filters = FilterPanel.render()

        st.divider()

        # ---------------------------------------------------------
        # Dashboard
        # ---------------------------------------------------------

        dashboard = self.controller.dashboard(
            user_id
        )

        summary = dashboard["summary"]

        transactions = dashboard["transactions"]

        investments = dashboard["investments"]

        # ---------------------------------------------------------
        # Search
        # ---------------------------------------------------------

        if keyword:

            keyword = keyword.lower()

            transactions = transactions[

                transactions.astype(str)

                .apply(

                    lambda row:

                    row.str.lower().str.contains(keyword)

                )

                .any(axis=1)

            ]

        # ---------------------------------------------------------
        # Asset Filter
        # ---------------------------------------------------------

        asset_type = filters["asset_type"]

        if (

            asset_type != "All"

            and

            "asset_type" in transactions.columns

        ):

            transactions = transactions[

                transactions["asset_type"]

                == asset_type

            ]

        # ---------------------------------------------------------
        # Dashboard Summary
        # ---------------------------------------------------------

        TransactionSummary.render(

            summary

        )

        # ---------------------------------------------------------
        # Complete Transaction Table
        # ---------------------------------------------------------

        TransactionTable.render(
            transactions,
            export_key="all_transactions",
        )

        csv = transactions.to_csv(index=False)

        st.download_button(

            "📥 Export All Transactions",

            csv,

            file_name="transactions.csv",

            mime="text/csv",

            use_container_width=True,

            key="export_all_transactions",

        )

        st.divider()

        # ---------------------------------------------------------
        # Investment History
        # ---------------------------------------------------------

        InvestmentHistory.render(

            investments

        )

        st.divider()

        # ---------------------------------------------------------
        # Future Buttons
        # ---------------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            if st.button(

                "➕ Buy",

                use_container_width=True,

            ):

                st.info(

                    "Buy Transaction module coming next."

                )

        with c2:

            if st.button(

                "➖ Sell",

                use_container_width=True,

            ):

                st.info(

                    "Sell Transaction module coming next."

                )

        with c3:

            if st.button(

                "✏ Edit",

                use_container_width=True,

            ):

                st.info(

                    "Edit Transaction module coming next."

                )

        with c4:

            if st.button(

                "🗑 Delete",

                use_container_width=True,

            ):

                st.info(

                    "Delete Transaction module coming next."

                )