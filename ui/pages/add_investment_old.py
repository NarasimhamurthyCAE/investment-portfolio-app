# =============================================================================
# File Name : ui/pages/add_investment.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Add Investment Page
#
# Supports:
#   ✓ Mutual Funds
#   ✓ ETFs
#   ✓ Stocks
#
# Workflow
# --------
# Search Asset
# ↓
# Select Asset
# ↓
# Fetch Metadata
# ↓
# Fetch Latest Price
# ↓
# Enter Amount
# ↓
# Live Unit Calculation
# ↓
# Save Investment
#
# =============================================================================

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from controllers.asset_controller import AssetController


class AddInvestmentPage:
    """
    Production Add Investment Page.
    """

    def __init__(self):

        self.controller = AssetController()

    # -------------------------------------------------------------------------
    # Session State
    # -------------------------------------------------------------------------

    def _initialize_session(self):

        defaults = {

            "asset_search_results": pd.DataFrame(),

            "selected_identifier": "",

            "selected_asset_name": "",

            "selected_metadata": {},

            "latest_price": 0.0,

            "search_keyword": "",

            "asset_confirmed": False,

        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    def render(self):

        self._initialize_session()

        st.title("➕ Add Investment")

        st.caption(
            "Create a new Mutual Fund, ETF or Stock investment."
        )

        st.divider()

        self._asset_search_section()

        st.divider()

        self._investment_form()

    # -------------------------------------------------------------------------
    # Asset Search Section
    # -------------------------------------------------------------------------

    def _asset_search_section(self):

        st.subheader("Step 1 : Select Asset")

        col1, col2 = st.columns([1, 2])

        with col1:

            asset_type = st.selectbox(

                "Asset Type",

                self.controller.supported_assets(),

                key="asset_type"

            )

        with col2:

            keyword = st.text_input(

                "Search",

                placeholder="Example: Parag, NIFTY, INFY...",

                key="search_keyword"

            )

        col1, col2 = st.columns([1, 5])

        with col1:

            search_clicked = st.button(

                "Search",

                use_container_width=True

            )

        if search_clicked:

            try:

                results = self.controller.search_market(

                    asset_type,

                    keyword

                )

                if results is None:

                    results = pd.DataFrame()

                st.session_state.asset_search_results = results

            except Exception as ex:

                st.error(str(ex))

                st.session_state.asset_search_results = pd.DataFrame()

        results = st.session_state.asset_search_results

        if not results.empty:

            st.success(

                f"{len(results)} asset(s) found."

            )

            st.dataframe(

                results,

                use_container_width=True,

                hide_index=True

            )

            if "name" in results.columns:

                display_column = "name"

            elif "scheme_name" in results.columns:

                display_column = "scheme_name"

            elif "company_name" in results.columns:

                display_column = "company_name"

            else:

                display_column = results.columns[0]

            selected_name = st.selectbox(
                "Select Asset",
                results[display_column].tolist(),
                key="selected_asset_dropdown"
            )

            if st.button(
                "✅ Select Asset",
                key="confirm_selected_asset",
                use_container_width=True,
            ):

                selected_row = results[
                    results[display_column] == selected_name
                ].iloc[0]

                st.session_state.selected_asset_name = selected_name

                if "scheme_code" in selected_row.index:

                    identifier = str(selected_row["scheme_code"])

                elif "symbol" in selected_row.index:

                    identifier = str(selected_row["symbol"])

                else:

                    identifier = str(selected_row.iloc[0])

                st.session_state.selected_identifier = identifier

                # IMPORTANT
                st.session_state.identifier = identifier

                st.session_state.asset_confirmed = True

                st.success(f"Selected : {selected_name}")

                st.rerun()

        else:

            st.info(

                "Search for an asset to continue."

            )

    # -------------------------------------------------------------------------
    # Investment Form
    # -------------------------------------------------------------------------

    def _investment_form(self):

        st.subheader("Step 2 : Investment Details")

        if not st.session_state.asset_confirmed:

            st.info("Please search and click '✅ Select Asset' first.")

            return

        identifier = st.text_input(

            "Scheme Code / Stock Symbol",

            key="identifier"

        )

        col1, col2 = st.columns([3, 1])

        with col1:

            investment_date = st.date_input(

                "Investment Date",

                value=date.today()

            )

        with col2:

            fetch_price = st.button(

                "Fetch Price",

                use_container_width=True

            )

        # -----------------------------------------------------------------
        # Metadata
        # -----------------------------------------------------------------

        metadata = {}

        if identifier:

            try:

                metadata = self.controller.metadata(

                    st.session_state.asset_type,

                    identifier

                )

            except Exception:

                metadata = {}

        st.session_state.selected_metadata = metadata

        if metadata:

            with st.expander(

                "Asset Information",

                expanded=True

            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(

                        "**Name**",

                        metadata.get(

                            "name",

                            "-"

                        )

                    )

                    st.write(

                        "**Category**",

                        metadata.get(

                            "category",

                            "-"

                        )

                    )

                    st.write(

                        "**AMC**",

                        metadata.get(

                            "amc",

                            "-"

                        )

                    )

                with col2:

                    st.write(

                        "**Symbol**",

                        metadata.get(

                            "symbol",

                            "-"

                        )

                    )

                    st.write(

                        "**Exchange**",

                        metadata.get(

                            "exchange",

                            "-"

                        )

                    )

                    st.write(

                        "**ISIN**",

                        metadata.get(

                            "isin",

                            "-"

                        )

                    )

        # -----------------------------------------------------------------
        # Latest Price
        # -----------------------------------------------------------------

        if fetch_price:

            try:

                latest_price = self.controller.latest_price(

                    st.session_state.asset_type,

                    identifier

                )

                st.session_state.latest_price = latest_price

            except Exception as ex:

                st.error(

                    str(ex)

                )

        price = st.number_input(

            "NAV / Price",

            min_value=0.0,

            format="%.4f",

            value=float(

                st.session_state.latest_price

            )

        )

        amount = st.number_input(

            "Investment Amount",

            min_value=0.0,

            step=500.0,

            format="%.2f"

        )

        charges = st.number_input(

            "Charges",

            min_value=0.0,

            step=1.0,

            format="%.2f"

        )

        remarks = st.text_area(

            "Remarks",

            placeholder="Optional..."

        )

        # -----------------------------------------------------------------
        # Live Units
        # -----------------------------------------------------------------

        units = 0.0

        if price > 0:

            units = (

                amount

                - charges

            ) / price

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Estimated Units",

                f"{units:.6f}"

            )

        with col2:

            st.metric(

                "Price",

                f"{price:.4f}"

            )

        with col3:

            st.metric(

                "Investment",

                f"₹{amount:,.2f}"

            )

        st.divider()

        save = st.button(

            "💾 Save Investment",

            type="primary",

            use_container_width=True

        )

        if save:

            self._save_investment(

                identifier,

                investment_date,

                amount,

                price,

                charges,

                remarks

            )

    # -------------------------------------------------------------------------
    # Save Investment
    # -------------------------------------------------------------------------

    def _save_investment(
        self,
        identifier: str,
        investment_date,
        amount: float,
        price: float,
        charges: float,
        remarks: str,
    ):

        # -------------------------------------------------------------
        # Validation
        # -------------------------------------------------------------

        if not identifier:

            st.error(
                "Please select an asset."
            )

            return

        if amount <= 0:

            st.error(
                "Investment amount must be greater than zero."
            )

            return

        if price <= 0:

            st.error(
                "Price / NAV must be greater than zero."
            )

            return

        asset_type = st.session_state.asset_type

        try:

            with st.spinner(
                "Saving investment..."
            ):

                investment_id = self.controller.add_investment(

                    user_id=1,

                    asset_type=asset_type,

                    identifier=identifier,

                    investment_date=investment_date,

                    amount=amount,

                    price=price,

                    charges=charges,

                    remarks=remarks,

                )

            units = (amount - charges) / price

            st.success(
                "Investment created successfully."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Investment ID",
                    investment_id
                )

                st.metric(
                    "Units Purchased",
                    f"{units:.6f}"
                )

            with col2:

                st.metric(
                    "Amount",
                    f"₹{amount:,.2f}"
                )

                st.metric(
                    "NAV / Price",
                    f"{price:.4f}"
                )

            metadata = st.session_state.selected_metadata

            if metadata:

                st.divider()

                st.subheader(
                    "Investment Summary"
                )

                summary = {

                    "Asset Type": asset_type,

                    "Identifier": identifier,

                    "Name": metadata.get(
                        "name",
                        "-"
                    ),

                    "Category": metadata.get(
                        "category",
                        "-"
                    ),

                    "AMC": metadata.get(
                        "amc",
                        "-"
                    ),

                    "Units": round(
                        units,
                        6
                    ),

                    "Investment": round(
                        amount,
                        2
                    ),

                    "Latest Price": round(
                        price,
                        4
                    ),

                }

                st.json(summary)

            # ---------------------------------------------------------
            # Clear Session
            # ---------------------------------------------------------

            st.session_state.asset_search_results = pd.DataFrame()

            st.session_state.selected_identifier = ""

            st.session_state.selected_asset_name = ""

            st.session_state.selected_metadata = {}

            st.session_state.latest_price = 0.0

            st.session_state.search_keyword = ""

            st.session_state.asset_confirmed = False

            # Clear the identifier text box
            st.session_state.identifier = ""

            st.info(
                "You can now add another investment."
            )

            st.rerun()

        except Exception as ex:

            st.error(
                str(ex)
            )


# =============================================================================
# Standalone Execution
# =============================================================================

def render():

    page = AddInvestmentPage()

    page.render()


if __name__ == "__main__":

    render()