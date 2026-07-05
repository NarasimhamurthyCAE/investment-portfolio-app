# =============================================================================
# File Name : ui/components/investment_history.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import streamlit as st

from ui.components.transaction_table import TransactionTable


class InvestmentHistory:
    """
    Expandable Investment History.

    One expander per investment.

    Example

    ▼ Infosys Ltd

        Summary

        Transaction History
    """

    @staticmethod
    def render(
        investments: dict,
    ):

        if not investments:

            return

        st.subheader("📂 Investment History")

        for investment in investments.values():

            title = (

                f"{investment['asset_name']} "

                f"({investment['symbol']})"

            )

            with st.expander(

                title,

                expanded=False,

            ):

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.metric(

                        "Shares Held",

                        f"{investment['shares_held']:,.4f}"

                    )

                with c2:

                    st.metric(

                        "Average Buy",

                        f"₹{investment['average_buy_price']:,.2f}"

                    )

                with c3:

                    st.metric(

                        "Invested",

                        f"₹{investment['invested']:,.2f}"

                    )

                with c4:

                    st.metric(

                        "Current Price",

                        f"₹{investment['current_price']:,.2f}"

                    )

                c5, c6, c7 = st.columns(3)

                with c5:

                    st.metric(

                        "Current Value",

                        f"₹{investment['current_value']:,.2f}"

                    )

                with c6:

                    st.metric(

                        "Gain",

                        f"₹{investment['gain']:,.2f}",

                        delta=f"{investment['return_percent']:.2f}%"

                    )

                with c7:

                    st.metric(

                        "Portfolio",

                        investment["portfolio_name"]

                    )

                st.divider()

                csv = investment["transactions"].to_csv(

                    index=False

                )

                st.download_button(

                    "📥 Export History",

                    csv,

                    file_name=f"{investment['symbol']}.csv",

                    mime="text/csv",

                    key=f"history_{investment['investment_id']}",

                )

                TransactionTable.render(

                    investment["transactions"],

                    export_key=f"tx_{investment['investment_id']}",

                )