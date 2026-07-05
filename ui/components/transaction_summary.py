# =============================================================================
# File Name : ui/components/transaction_summary.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import streamlit as st


class TransactionSummary:
    """
    Transaction Dashboard Summary.

    Displays high-level portfolio statistics for the
    Transactions page.

    No calculations are performed here.
    """

    @staticmethod
    def render(summary: dict):

        if not summary:

            st.info("No summary available.")

            return

        st.subheader("📊 Investment Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "💰 Invested",

                f"₹{summary.get('cash_invested',0):,.2f}"

            )

        with col2:

            st.metric(

                "📈 Current Value",

                f"₹{summary.get('current_value',0):,.2f}"

            )

        with col3:

            gain = summary.get("gain",0)

            st.metric(

                "📊 Gain / Loss",

                f"₹{gain:,.2f}",

                delta=f"{summary.get('return_percent',0):.2f}%"

            )

        with col4:

            st.metric(

                "💸 Cash Withdrawn",

                f"₹{summary.get('cash_withdrawn',0):,.2f}"

            )

        st.divider()

        col5, col6, col7, col8 = st.columns(4)

        with col5:

            st.metric(

                "Transactions",

                summary.get("total_transactions",0)

            )

        with col6:

            st.metric(

                "Investments",

                summary.get("total_investments",0)

            )

        with col7:

            st.metric(

                "Charges",

                f"₹{summary.get('charges',0):,.2f}"

            )

        with col8:

            st.metric(

                "Taxes",

                f"₹{summary.get('taxes',0):,.2f}"

            )

        st.divider()

        col9, col10 = st.columns(2)

        with col9:

            st.metric(

                "Net Cash Flow",

                f"₹{summary.get('net_cash_flow',0):,.2f}"

            )

        with col10:

            st.metric(

                "XIRR",

                "Coming Soon"

            )