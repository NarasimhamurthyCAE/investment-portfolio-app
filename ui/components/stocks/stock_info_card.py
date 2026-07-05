# =============================================================================
# File Name : ui/components/stocks/stock_info_card.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Stock Information Card
#
# Responsibilities
# ----------------
# ✓ Display selected stock information
# ✓ Read-only information card
#
# Does NOT
# --------
# ✗ Query database
# ✗ Call controllers
# ✗ Save anything
# ✗ Perform calculations
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class StockInfoCard:
    """
    Displays selected stock information.

    Pure UI component.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        stock: dict | None,
    ) -> None:

        st.subheader("📄 Selected Stock")

        if not stock:

            st.info(
                "No stock selected."
            )
            return

        st.success(
            f"{stock.get('company_name', '')}"
        )

        left, right = st.columns(2)

        # -------------------------------------------------------------
        # LEFT
        # -------------------------------------------------------------

        with left:

            st.text_input(
                "Company",
                value=stock.get(
                    "company_name",
                    "",
                ),
                disabled=True,
            )

            st.text_input(
                "Symbol",
                value=stock.get(
                    "symbol",
                    "",
                ),
                disabled=True,
            )

            st.text_input(
                "Exchange",
                value=stock.get(
                    "exchange",
                    "",
                ),
                disabled=True,
            )

        # -------------------------------------------------------------
        # RIGHT
        # -------------------------------------------------------------

        with right:

            st.text_input(
                "Sector",
                value=stock.get(
                    "sector",
                    "",
                ),
                disabled=True,
            )

            st.text_input(
                "Industry",
                value=stock.get(
                    "industry",
                    "",
                ),
                disabled=True,
            )

            st.text_input(
                "Currency",
                value=stock.get(
                    "currency",
                    "INR",
                ),
                disabled=True,
            )

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Country",

                stock.get(

                    "country",

                    "-",

                ),

            )

        with c2:

            st.metric(

                "Market Cap",

                stock.get(

                    "market_cap",

                    "-",

                ),

            )

        with c3:

            st.metric(

                "Status",

                stock.get(

                    "listing_status",

                    "ACTIVE",

                ),

            )