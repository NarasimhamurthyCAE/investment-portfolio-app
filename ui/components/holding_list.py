# =============================================================================
# File Name : ui/components/holding_list.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import streamlit as st

from ui.components.holding_card import HoldingCard


class HoldingList:
    """
    Holding List Component.

    Responsibilities
    ----------------
    ✓ Render all holdings
    ✓ Sort holdings
    ✓ Handle empty portfolio

    No calculations.
    No database.
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @staticmethod
    def render(
        holdings: dict,
    ):

        st.subheader("📂 Holdings")

        if not holdings:

            st.info("No active holdings available.")

            return

        # ---------------------------------------------------------
        # Sort alphabetically
        # ---------------------------------------------------------

        ordered = sorted(

            holdings.values(),

            key=lambda h: h.get("asset_name", "").lower(),

        )

        for holding in ordered:

            HoldingCard.render(

                holding

            )