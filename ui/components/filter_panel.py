# =============================================================================
# File Name : ui/components/filter_panel.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Portfolio Filter Panel
#
# Supports:
#   ✓ Asset Type
#   ✓ AMC
#   ✓ Category
#   ✓ Date Range
#
# =============================================================================

from __future__ import annotations

from datetime import date

import streamlit as st


class FilterPanel:
    """
    Reusable filter panel.
    """

    @staticmethod
    def render():

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            asset_type = st.selectbox(

                "Asset Type",

                [

                    "All",

                    "Mutual Fund",

                    "ETF",

                    "Stock"

                ]

            )

        with col2:

            amc = st.text_input(

                "AMC"

            )

        with col3:

            category = st.text_input(

                "Category"

            )

        with col4:

            from_date = st.date_input(

                "From",

                value=date(2020, 1, 1)

            )

        return {

            "asset_type": asset_type,

            "amc": amc,

            "category": category,

            "from_date": from_date

        }