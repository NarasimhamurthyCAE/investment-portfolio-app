# =============================================================================
# File Name : ui/components/holding_card.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import streamlit as st


class HoldingCard:
    """
    Displays one investment holding.

    Pure UI.

    No calculations.
    """

    @staticmethod
    def render(
        holding: dict,
    ):

        title = holding.get("asset_name", "Unknown")

        symbol = holding.get("symbol", "")

        with st.expander(

            f"📈 {title} ({symbol})",

            expanded=False,

        ):

            # ---------------------------------------------------------
            # Row 1
            # ---------------------------------------------------------

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(

                    "Shares Held",

                    f"{holding.get('shares_held',0):,.4f}"

                )

            with c2:

                st.metric(

                    "Average Buy",

                    f"₹{holding.get('average_buy_price',0):,.2f}"

                )

            with c3:

                st.metric(

                    "Current Price",

                    f"₹{holding.get('current_price',0):,.2f}"

                )

            with c4:

                st.metric(

                    "Current Value",

                    f"₹{holding.get('current_value',0):,.2f}"

                )

            # ---------------------------------------------------------
            # Row 2
            # ---------------------------------------------------------

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.metric(

                    "Invested",

                    f"₹{holding.get('invested',0):,.2f}"

                )

            with c2:

                st.metric(

                    "Gain",

                    f"₹{holding.get('gain',0):,.2f}",

                    delta=f"{holding.get('return_percent',0):.2f}%"

                )

            with c3:

                st.metric(

                    "Industry",

                    holding.get("industry","-")

                )

            with c4:

                st.metric(

                    "Sector",

                    holding.get("sector","-")

                )

            st.divider()

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                st.button(

                    "➕ Buy",

                    key=f"buy_{holding['investment_id']}",

                    use_container_width=True,

                )

            with c2:

                st.button(

                    "➖ Sell",

                    key=f"sell_{holding['investment_id']}",

                    use_container_width=True,

                )

            with c3:

                st.button(

                    "✏ Edit",

                    key=f"edit_{holding['investment_id']}",

                    use_container_width=True,

                )

            with c4:

                st.button(

                    "🗑 Delete",

                    key=f"delete_{holding['investment_id']}",

                    use_container_width=True,

                )

            st.divider()

            st.subheader("Transaction History")

            from ui.components.transaction_table import TransactionTable

            TransactionTable.render(

                holding["transactions"]

            )