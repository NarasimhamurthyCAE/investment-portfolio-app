# =============================================================================
# File Name : ui/pages/add_stock.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Production Add Stock Page
#
# Workflow
#
# Search
# ↓
# Select Stock
# ↓
# Auto Metadata Refresh (if required)
# ↓
# Stock Information
# ↓
# Transaction Details
# ↓
# Investment Summary
# ↓
# Save
#
# =============================================================================

from __future__ import annotations

import pandas as pd
import streamlit as st

from controllers.stock_master_controller import (
    StockMasterController,
)

from controllers.investment_controller import (
    InvestmentController,
)

from assets.services.broker_service import (
    BrokerService,
)

from ui.components.stocks.stock_search import (
    StockSearch,
)

from ui.components.stocks.stock_info_card import (
    StockInfoCard,
)

from ui.components.stocks.stock_transaction_form import (
    StockTransactionForm,
)

from ui.components.stocks.investment_summary_card import (
    InvestmentSummaryCard,
)


class AddStockPage:
    """
    Production Add Stock Page.

    Responsibilities
    ----------------
    ✓ Search stock
    ✓ Display metadata
    ✓ Collect transaction details
    ✓ Create investment
    ✓ Keep UI free from business logic
    """

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.master_controller = StockMasterController()

        self.investment_controller = InvestmentController()

        self.broker_service = BrokerService()

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(self):

        st.title("📈 Add Stock")

        st.divider()

        # ==========================================================
        # STEP 1 : SEARCH
        # ==========================================================

        st.subheader("Step 1 : Search")

        keyword = st.text_input(

            "Company Name / Symbol",

            placeholder="INFY, TCS, RELIANCE ...",

            key="stock_keyword",

        )

        results = pd.DataFrame()

        if keyword.strip():

            results = self.master_controller.search(

                keyword

            )

        # ----------------------------------------------------------
        # Search Component
        #
        # Automatically refreshes metadata if sector / industry
        # is missing and returns the latest stock information.
        # ----------------------------------------------------------

        selected_stock = StockSearch.render(

            results,

            controller=self.master_controller,

            key="stock",

        )

        # ----------------------------------------------------------
        # Preserve selection during reruns
        # ----------------------------------------------------------

        if selected_stock is None:

            selected_stock = st.session_state.get(

                "selected_stock_data",

                None,

            )

        # ==========================================================
        # STEP 2 : STOCK INFORMATION
        # ==========================================================

        StockInfoCard.render(

            selected_stock,

        )

        st.divider()

        # ==========================================================
        # STEP 3 : TRANSACTION DETAILS
        # ==========================================================

        brokers = self.broker_service.broker_names()

        portfolios = [

            "Default",

        ]

        accounts = [

            "Primary",

        ]

        transaction = None

        if selected_stock:

            transaction = StockTransactionForm.render(

                brokers=brokers,

                portfolios=portfolios,

                accounts=accounts,

            )

        else:

            st.info(

                "Select a stock to continue."

            )

        # ==========================================================
        # STEP 4 : LIVE INVESTMENT SUMMARY
        # ==========================================================

        if transaction:

            InvestmentSummaryCard.render(

                transaction

            )

        st.divider()

        # ==========================================================
        # STEP 5 : ACTION BUTTONS
        # ==========================================================

        col1, col2, col3 = st.columns(

            [

                1,

                1,

                2,

            ]

        )

        with col1:

            save = st.button(

                "💾 Save Investment",

                use_container_width=True,

                type="primary",

                disabled=(

                    selected_stock is None

                    or

                    transaction is None

                ),

            )

        with col2:

            clear = st.button(

                "🧹 Clear",

                use_container_width=True,

            )

        # ----------------------------------------------------------
        # Clear Screen
        # ----------------------------------------------------------

        if clear:

            st.session_state.pop(

                "selected_stock_data",

                None,

            )

            st.rerun()

        # ----------------------------------------------------------
        # Wait until Save is clicked
        # ----------------------------------------------------------

        if not save:

            return

        # ==========================================================
        # STEP 6 : VALIDATION
        # ==========================================================

        errors = []

        if transaction["units"] <= 0:

            errors.append(

                "Quantity must be greater than zero."

            )

        if transaction["price"] <= 0:

            errors.append(

                "Price must be greater than zero."

            )

        if errors:

            for error in errors:

                st.error(

                    error

                )

            return

        st.divider()

        # ==========================================================
        # STEP 7 : CREATE INVESTMENT
        # ==========================================================

        try:

            investment_id = (

                self.investment_controller.create_stock_investment(

                    user_id=1,

                    stock=selected_stock,

                    investment_date=transaction["transaction_date"],

                    units=transaction["units"],

                    price=transaction["price"],

                    broker=transaction["broker"],

                    account_name=transaction["account_name"],

                    portfolio_name=transaction["portfolio_name"],

                    charges=transaction["total_charges"],

                    reference_number=transaction["reference_number"],

                    notes=transaction["notes"],

                )

            )

        except Exception as ex:

            st.exception(

                ex

            )

            return

        # ==========================================================
        # STEP 8 : SUCCESS
        # ==========================================================

        st.success(

            f"""

Investment created successfully.

Investment ID : {investment_id}

"""

        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(

                "➕ Add Another",

                use_container_width=True,

                key="add_another_stock",

            ):

                # Clear current selection

                st.session_state.pop(

                    "selected_stock_data",

                    None,

                )

                st.rerun()

        with c2:

            if st.button(

                "📂 View Portfolio",

                use_container_width=True,

                key="view_portfolio_after_save",

            ):

                st.info(

                    "Portfolio navigation will be connected in a later phase."

                )

        # ==========================================================
        # CLEAR SESSION AFTER SAVE
        # ==========================================================

        st.session_state.pop(

            "selected_stock_data",

            None,

        )

        st.rerun()


# -----------------------------------------------------------------------------
# Render Shortcut
# -----------------------------------------------------------------------------

def render():

    AddStockPage().render()