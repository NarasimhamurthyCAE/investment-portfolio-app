# =============================================================================
# File Name : ui/components/transaction_table.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import pandas as pd
import streamlit as st


class TransactionTable:
    """
    Professional Transaction Table

    Responsibilities
    ----------------
    ✓ Format transaction data
    ✓ Currency formatting
    ✓ Date formatting
    ✓ Display transaction table
    ✓ Export CSV

    No calculations.
    """

    # -------------------------------------------------------------------------
    # Currency
    # -------------------------------------------------------------------------

    @staticmethod
    def currency(value):

        if pd.isna(value):

            return ""

        return f"₹{value:,.2f}"

    # -------------------------------------------------------------------------
    # Date
    # -------------------------------------------------------------------------

    @staticmethod
    def format_date(series):

        return pd.to_datetime(series).dt.strftime("%d-%b-%Y")

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        transactions: pd.DataFrame,
        export_key: str | None = None,
    ):

        if transactions.empty:

            st.info("No transactions found.")

            return

        df = transactions.copy()

        # -------------------------------------------------------------
        # Date
        # -------------------------------------------------------------

        if "transaction_date" in df.columns:

            df["transaction_date"] = cls.format_date(
                df["transaction_date"]
            )

        # -------------------------------------------------------------
        # BUY / SELL Badge
        # -------------------------------------------------------------

        if "transaction_type" in df.columns:

            df["transaction_type"] = df[
                "transaction_type"
            ].str.upper()

            df["transaction_type"] = df[
                "transaction_type"
            ].replace(
                {
                    "BUY": "🟢 BUY",
                    "SELL": "🔴 SELL",
                }
            )

        # -------------------------------------------------------------
        # Currency Formatting
        # -------------------------------------------------------------

        currency_columns = [

            "price",

            "amount",

            "charges",

            "taxes",

            "gross_outflow",

            "net_cash_flow",

        ]

        for col in currency_columns:

            if col in df.columns:

                df[col] = df[col].apply(
                    cls.currency
                )

        # -------------------------------------------------------------
        # Rename Columns
        # -------------------------------------------------------------

        rename = {

            "transaction_date": "Date",

            "asset_name": "Asset",

            "symbol": "Symbol",

            "industry": "Industry",

            "asset_type": "Type",

            "transaction_type": "BUY / SELL",

            "units": "Units",

            "price": "Price / Unit",

            "amount": "Gross Amount",

            "charges": "Charges",

            "taxes": "Taxes",

            "gross_outflow": "Gross Cash",

            "net_cash_flow": "Net Cash Flow",

            "portfolio_name": "Portfolio",

            "broker": "Broker",

        }

        df.rename(
            columns=rename,
            inplace=True,
        )

        # -------------------------------------------------------------
        # Visible Columns
        # -------------------------------------------------------------

        visible = [

            "Date",

            "Asset",

            "Symbol",

            "Industry",

            "Type",

            "BUY / SELL",

            "Units",

            "Price / Unit",

            "Gross Amount",

            "Charges",

            "Taxes",

            "Net Cash Flow",

            "Portfolio",

            "Broker",

        ]

        visible = [

            c

            for c in visible

            if c in df.columns

        ]

        st.subheader("📄 Transaction History")

        st.dataframe(

            df[visible],

            use_container_width=True,

            hide_index=True,

        )

        st.caption(

            f"{len(df)} transaction(s)"

        )

      