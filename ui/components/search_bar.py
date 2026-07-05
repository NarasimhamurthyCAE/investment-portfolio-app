# =============================================================================
# File Name : ui/components/search_bar.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Reusable Search Bar Component
#
# Used in:
#   ✓ Portfolio
#   ✓ Mutual Funds
#   ✓ ETFs
#   ✓ Stocks
#   ✓ Transactions
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class SearchBar:
    """
    Reusable search component.
    """

    @staticmethod
    def render(
        key: str = "search",
        label: str = "Search",
        placeholder: str = "Search..."
    ) -> str:

        return st.text_input(

            label,

            key=key,

            placeholder=placeholder

        )