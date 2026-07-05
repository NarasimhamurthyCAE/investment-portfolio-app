# =============================================================================
# File Name : ui/components/stocks/stock_transaction_form.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Reusable Stock / ETF / REIT / INVIT Transaction Form
#
# Responsibilities
# ----------------
# ✓ Render transaction input controls
# ✓ Capture user input
# ✓ Return entered values
#
# Does NOT
# --------
# ✗ Save to database
# ✗ Call controllers
# ✗ Perform business calculations
# ✗ Execute SQL
#
# =============================================================================

from __future__ import annotations

from datetime import date

import streamlit as st


class StockTransactionForm:
    """
    Reusable transaction form.

    This component can be reused by:

        • Add Stock
        • Add ETF
        • Add REIT
        • Add INVIT
    """

    # -------------------------------------------------------------------------
    # Render
    # -------------------------------------------------------------------------

    @classmethod
    def render(
        cls,
        *,
        brokers: list[str],
        portfolios: list[str] | None = None,
        accounts: list[str] | None = None,
    ) -> dict:

        if portfolios is None:

            portfolios = ["Default"]

        if accounts is None:

            accounts = ["Primary"]

        st.subheader("💳 Transaction Details")

        left, right = st.columns(2)

        # ===============================================================
        # LEFT COLUMN
        # ===============================================================

        with left:

            transaction_date = st.date_input(

                "Investment Date",

                value=date.today(),

                key="stock_transaction_date",

            )

            transaction_type = st.selectbox(

                "Transaction Type",

                [

                    "BUY",

                    "SELL",

                ],

                key="stock_transaction_type",

            )

            units = st.number_input(

                "Quantity",

                min_value=0.0,

                value=0.0,

                step=1.0,

                format="%.6f",

                key="stock_units",

            )

            price = st.number_input(

                "Price / Share",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_price",

            )

        # ===============================================================
        # RIGHT COLUMN
        # ===============================================================

        with right:

            portfolio_name = st.selectbox(

                "Portfolio",

                portfolios,

                key="stock_portfolio",

            )

            broker = st.selectbox(

                "Broker",

                brokers if brokers else ["Default"],

                key="stock_broker",

            )

            account_name = st.selectbox(

                "Account",

                accounts,

                key="stock_account",

            )

            reference_number = st.text_input(

                "Reference Number",

                key="stock_reference",

            )

        st.divider()

        st.subheader("💰 Charges")

        # ===============================================================
        # CHARGES
        # ===============================================================

        charge_left, charge_right = st.columns(2)

        with charge_left:

            brokerage = st.number_input(

                "Brokerage",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_brokerage",

            )

            stt = st.number_input(

                "STT",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_stt",

            )

            exchange_charge = st.number_input(

                "Exchange Charges",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_exchange_charge",

            )

            sebi_charge = st.number_input(

                "SEBI Charges",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_sebi_charge",

            )

        with charge_right:

            stamp_duty = st.number_input(

                "Stamp Duty",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_stamp_duty",

            )

            gst = st.number_input(

                "GST",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_gst",

            )

            other_charges = st.number_input(

                "Other Charges",

                min_value=0.0,

                value=0.0,

                step=0.01,

                format="%.2f",

                key="stock_other_charges",

            )

        st.divider()

        # ===============================================================
        # NOTES
        # ===============================================================

        notes = st.text_area(

            "Notes",

            height=100,

            key="stock_notes",

        )

        # ===============================================================
        # LIVE INVESTMENT SUMMARY
        # ===============================================================

        gross_amount = units * price

        total_charges = (

            brokerage

            + stt

            + exchange_charge

            + sebi_charge

            + stamp_duty

            + gst

            + other_charges

        )

        if transaction_type == "BUY":

            net_amount = gross_amount + total_charges

        else:

            net_amount = gross_amount - total_charges

        st.divider()

        st.subheader("📊 Investment Summary")

        s1, s2, s3, s4 = st.columns(4)

        with s1:

            st.metric(

                "Units",

                f"{units:,.4f}",

            )

        with s2:

            st.metric(

                "Price",

                f"₹{price:,.2f}",

            )

        with s3:

            st.metric(

                "Gross Amount",

                f"₹{gross_amount:,.2f}",

            )

        with s4:

            st.metric(

                "Total Charges",

                f"₹{total_charges:,.2f}",

            )

        st.metric(

            "Net Cash Flow",

            f"₹{net_amount:,.2f}",

        )

        st.divider()

        # ===============================================================
        # RETURN FORM DATA
        # ===============================================================

        return {

            # ----------------------------------------------------------
            # Transaction
            # ----------------------------------------------------------

            "transaction_date": transaction_date,

            "transaction_type": transaction_type,

            # ----------------------------------------------------------
            # Quantity
            # ----------------------------------------------------------

            "units": units,

            "price": price,

            # ----------------------------------------------------------
            # Portfolio
            # ----------------------------------------------------------

            "portfolio_name": portfolio_name,

            "broker": broker,

            "account_name": account_name,

            # ----------------------------------------------------------
            # Charges
            # ----------------------------------------------------------

            "brokerage": brokerage,

            "stt": stt,

            "exchange_charge": exchange_charge,

            "sebi_charge": sebi_charge,

            "stamp_duty": stamp_duty,

            "gst": gst,

            "other_charges": other_charges,

            # ----------------------------------------------------------
            # Calculated Values
            # ----------------------------------------------------------

            "gross_amount": gross_amount,

            "total_charges": total_charges,

            "net_amount": net_amount,

            # ----------------------------------------------------------
            # Additional Information
            # ----------------------------------------------------------

            "reference_number": reference_number,

            "notes": notes,

        }