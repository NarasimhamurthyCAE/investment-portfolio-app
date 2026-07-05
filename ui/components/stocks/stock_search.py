# =============================================================================
# File Name : ui/components/stocks/stock_search.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Reusable Stock Search Component
#
# Responsibilities
# ----------------
# ✓ Display search results
# ✓ Allow stock selection
# ✓ Automatically refresh metadata (if missing)
# ✓ Return selected stock
#
# Business Rules
# --------------
# • Search results come from stocks_master
# • If Sector/Industry is missing:
#       -> Refresh metadata from Yahoo
#       -> Update database
#       -> Reload latest stock
#
# =============================================================================

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)


class StockSearch:
    """
    Reusable Stock Search Component.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        results: pd.DataFrame,
        *,
        controller,
        key: str = "stock_search",
    ) -> dict | None:

        st.subheader("🔍 Search Results")

        # ---------------------------------------------------------------------
        # No Results
        # ---------------------------------------------------------------------

        if results is None or results.empty:

            st.info(

                "Search a company name or symbol to begin."

            )

            return None

        # ---------------------------------------------------------------------
        # Sort
        # ---------------------------------------------------------------------

        results = (

            results

            .sort_values(

                by="company_name",

                ascending=True,

            )

            .reset_index(

                drop=True

            )

        )

        # ---------------------------------------------------------------------
        # Result Count
        # ---------------------------------------------------------------------

        st.caption(

            f"{len(results)} stock(s) found."

        )

        # ---------------------------------------------------------------------
        # Preview Table
        # ---------------------------------------------------------------------

        preview_columns = [

            c

            for c in [

                "company_name",

                "symbol",

                "exchange",

                "sector",

                "industry",

            ]

            if c in results.columns

        ]

        if preview_columns:

            st.dataframe(

                results[preview_columns],

                hide_index=True,

                use_container_width=True,

            )

        # ---------------------------------------------------------------------
        # Selection
        # ---------------------------------------------------------------------

        options = (

            results["company_name"]

            + " ("

            + results["symbol"]

            + ")"

        )

        selected = st.selectbox(

            "Select Stock",

            options,

            index=None,

            placeholder="Choose a stock...",

            key=f"{key}_select",

        )

        if selected is None:

            return None

        # ---------------------------------------------------------------------
        # Selected Row
        # ---------------------------------------------------------------------

        selected_row = results.loc[

            options == selected

        ].iloc[0]

        selected_stock = selected_row.to_dict()

        # ---------------------------------------------------------------------
        # Metadata Refresh
        # ---------------------------------------------------------------------

        needs_refresh = (

            not selected_stock.get("sector")

            or

            not selected_stock.get("industry")

        )

        if needs_refresh:

            with st.spinner(

                "Fetching latest company information..."

            ):

                try:

                    controller.refresh_metadata(

                        selected_stock["symbol"]

                    )

                    refreshed = controller.by_symbol(

                        selected_stock["symbol"]

                    )

                    if refreshed:

                        selected_stock = refreshed

                except Exception:

                    logger.exception(

                        "Metadata refresh failed."

                    )

                    st.info(

                        "Latest metadata could not be fetched. Existing information will be used."

                    )

        # ---------------------------------------------------------------------
        # Save Session
        # ---------------------------------------------------------------------

        st.session_state["selected_stock_data"] = selected_stock

        return selected_stock