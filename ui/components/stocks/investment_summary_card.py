# =============================================================================
# File Name : ui/components/stocks/investment_summary_card.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Live Investment Summary Card
#
# Responsibilities
# ----------------
# ✓ Display calculated investment summary
# ✓ Pure UI component
#
# Does NOT
# --------
# ✗ Perform business logic
# ✗ Save to database
# ✗ Call controllers
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class InvestmentSummaryCard:
    """
    Live investment summary.

    Pure UI.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        transaction: dict,
    ) -> None:

        st.subheader("📊 Investment Summary")

        if not transaction:

            st.info(
                "Enter transaction details."
            )
            return

        units = float(
            transaction.get(
                "units",
                0,
            )
        )

        price = float(
            transaction.get(
                "price",
                0,
            )
        )

        gross_amount = float(
            transaction.get(
                "gross_amount",
                0,
            )
        )

        total_charges = float(
            transaction.get(
                "total_charges",
                0,
            )
        )

        net_amount = float(
            transaction.get(
                "net_amount",
                0,
            )
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Units",

                f"{units:,.4f}",

            )

            st.metric(

                "Price / Share",

                f"₹{price:,.2f}",

            )

        with c2:

            st.metric(

                "Gross Amount",

                f"₹{gross_amount:,.2f}",

            )

            st.metric(

                "Charges",

                f"₹{total_charges:,.2f}",

            )

        with c3:

            st.metric(

                "Net Investment",

                f"₹{net_amount:,.2f}",

            )

            if units > 0:

                average = net_amount / units

            else:

                average = 0.0

            st.metric(

                "Average Cost",

                f"₹{average:,.2f}",

            )

        st.divider()

        st.success(

            f"Cash Flow : ₹{net_amount:,.2f}"

        )