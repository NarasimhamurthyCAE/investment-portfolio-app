# =============================================================================
# File Name : ui/components/summary_cards.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Summary Cards
#
# Reusable dashboard metrics.
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class SummaryCards:

    @staticmethod
    def render(summary: dict):

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                "Investment",

                f"₹{summary['invested']:,.2f}"

            )

        with col2:

            st.metric(

                "Current Value",

                f"₹{summary['current_value']:,.2f}"

            )

        with col3:

            st.metric(

                "Profit",

                f"₹{summary['profit']:,.2f}"

            )

        with col4:

            st.metric(

                "Return",

                f"{summary['return_percent']:.2f}%"

            )