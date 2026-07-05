# =============================================================================
# File Name : ui/components/metric_card.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Reusable Metric Card Component
#
# Used by:
#   ✓ Dashboard
#   ✓ Portfolio
#   ✓ Analytics
#   ✓ Advisor
#   ✓ Reports
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class MetricCard:
    """
    Reusable metric card.
    """

    @staticmethod
    def render(
        title: str,
        value,
        delta=None,
        help_text: str | None = None
    ):
        """
        Render a Streamlit metric.

        Parameters
        ----------
        title : str
            Metric title.
        value : Any
            Metric value.
        delta : Any, optional
            Delta value.
        help_text : str, optional
            Tooltip.
        """

        st.metric(

            label=title,

            value=value,

            delta=delta,

            help=help_text

        )