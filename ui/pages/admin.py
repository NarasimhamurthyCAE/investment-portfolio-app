# =============================================================================
# File Name : ui/pages/admin.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Administration Page
#
# =============================================================================

from __future__ import annotations

import streamlit as st


class AdminPage:

    def render(self):

        st.title("⚙ Administration")

        st.divider()

        # ==========================================================
        # Master Data
        # ==========================================================

        st.subheader("Master Data")

        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button(
                "📈 Update Stocks",
                use_container_width=True,
                key="update_stocks"
            ):

                st.info(
                    "Stock Importer will be connected next."
                )

        with col2:

            if st.button(
                "📊 Update ETFs",
                use_container_width=True,
                key="update_etfs"
            ):

                st.info(
                    "ETF Importer coming soon."
                )

        with col3:

            if st.button(
                "💰 Update Mutual Funds",
                use_container_width=True,
                key="update_mf"
            ):

                st.info(
                    "MF Importer coming soon."
                )

        st.divider()

        # ==========================================================
        # Database
        # ==========================================================

        st.subheader("Database")

        col1, col2 = st.columns(2)

        with col1:

            st.button(
                "💾 Backup Database",
                use_container_width=True,
                key="backup_db"
            )

        with col2:

            st.button(
                "♻ Restore Database",
                use_container_width=True,
                key="restore_db"
            )

        st.divider()

        # ==========================================================
        # System
        # ==========================================================

        st.subheader("System Status")

        st.success("Database : Connected")

        st.success("Application : Running")

        st.info("Master Data : Ready")


def render():

    AdminPage().render()