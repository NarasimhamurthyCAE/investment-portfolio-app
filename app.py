import streamlit as st
import pandas as pd
import requests
import psycopg2
import os
import matplotlib.pyplot as plt
from datetime import datetime, date
from pyxirr import xirr
import numpy as np
from bs4 import BeautifulSoup
import io
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Mutual Fund Portfolio Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Mutual Fund Portfolio Analyzer")

st.write(
    "Track Direct Growth Mutual Funds with automatic NAV calculation"
)

# ==========================================================
# SUPABASE DATABASE
# ==========================================================
DATABASE_URL = st.secrets["DATABASE_URL"]


def get_connection():

    return psycopg2.connect(
        DATABASE_URL,
        sslmode="require"
    )


def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS investments (

            id BIGSERIAL PRIMARY KEY,

            user_id INTEGER DEFAULT 1,

            date TEXT,

            fund_type TEXT,

            fund_name TEXT,

            amount DOUBLE PRECISION,

            purchase_nav DOUBLE PRECISION,

            nav_date TEXT,

            latest_nav DOUBLE PRECISION,

            units DOUBLE PRECISION,

            current_value DOUBLE PRECISION,

            gain_loss DOUBLE PRECISION,

            holding_years DOUBLE PRECISION,

            cagr DOUBLE PRECISION,

            created_at TIMESTAMP
            DEFAULT NOW()
        )
        """
    )

    conn.commit()
    cursor.close()
    conn.close()


init_db()

# ==========================================================
# LOAD MUTUAL FUNDS
# ==========================================================
@st.cache_data
def load_mutual_funds():

    url = "https://api.mfapi.in/mf"

    response = requests.get(url)

    data = response.json()

    df = pd.DataFrame(data)

    # ======================================
    # MANUALLY ADD MISSING FUNDS
    # ======================================

    manual_funds = pd.DataFrame([

        {
            "schemeCode": 150518,
            "schemeName":
            "Motilal Oswal BSE Enhanced Value Index Fund Direct Growth"
        }

    ])

    df = pd.concat(
        [df, manual_funds],
        ignore_index=True
    )

    df.rename(
        columns={
            "schemeCode": "Scheme Code",
            "schemeName": "Fund Name"
        },
        inplace=True
    )

    # ======================================
    # CLEAN TEXT
    # ======================================
    df["UPPER"] = (
        df["Fund Name"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ======================================
    # INCLUDE DIRECT
    # ======================================
    direct_filter = (
        df["UPPER"]
        .str.contains(
            "DIRECT",
            na=False
        )
    )

    # ======================================
    # INCLUDE GROWTH
    # More flexible filter
    # ======================================
    growth_keywords = [

        "GROWTH",
        "GROWTH OPTION",
        "DIRECT GROWTH",
        "DIR GROWTH",
        "GROWTH PLAN",
        "PLAN GROWTH"
    ]

    growth_filter = False

    for word in growth_keywords:

        growth_filter |= (
            df["UPPER"]
            .str.contains(
                word,
                na=False
            )
        )

    # ======================================
    # EXCLUDE NON-GROWTH
    # ======================================
    exclude_words = [

        "IDCW",
        "DIVIDEND",
        "BONUS",
        "REINVESTMENT",
        "REGULAR",
        "FMP",
        "SERIES",
        "INTERVAL",
        "WEEKLY",
        "MONTHLY",
        "DAILY"
    ]

    exclude = False

    for word in exclude_words:

        exclude |= (
            df["UPPER"]
            .str.contains(
                word,
                na=False
            )
        )

    # ======================================
    # FINAL FILTER
    # ======================================
    df = df[
        direct_filter
        &
        growth_filter
        &
        ~exclude
    ]

    # ======================================
    # REMOVE DUPLICATES
    # ======================================
    df = (
        df
        .drop_duplicates(
            subset="Fund Name"
        )
        .sort_values(
            "Fund Name"
        )
        .reset_index(
            drop=True
        )
    )

    return df


fund_df = load_mutual_funds()


# ==========================================================
# NAV FUNCTION
# ==========================================================
def get_nav_data(
    scheme_code,
    invest_date
):

    url = (
        f"https://api.mfapi.in/mf/"
        f"{scheme_code}"
    )

    response = requests.get(url)
    data = response.json()

    nav_data = data["data"]

    target_date = datetime.strptime(
        invest_date,
        "%d/%m/%Y"
    )

    purchase_nav = None
    nav_date_used = None

    # oldest → latest
    nav_data = nav_data[::-1]

    for item in nav_data:

        nav_date = datetime.strptime(
            item["date"],
            "%d-%m-%Y"
        )

        # nearest available NAV
        if nav_date >= target_date:

            purchase_nav = float(
                item["nav"]
            )

            nav_date_used = (
                item["date"]
            )

            break

    latest_nav = float(
        data["data"][0]["nav"]
    )

    return (
        purchase_nav,
        latest_nav,
        nav_date_used
    )

# ==========================================================
# SAVE INVESTMENT
# ==========================================================
def save_investment(
    user_id,
    date,
    fund_type,
    fund_name,
    amount,
    purchase_nav,
    nav_date,
    latest_nav,
    units,
    current_value,
    gain_loss,
    holding_years,
    cagr
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO investments (

            user_id,
            date,
            fund_type,
            fund_name,
            amount,
            purchase_nav,
            nav_date,
            latest_nav,
            units,
            current_value,
            gain_loss,
            holding_years,
            cagr

        )

        VALUES (

            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s
        )
        """,

        (
            user_id,
            date,
            fund_type,
            fund_name,
            amount,
            purchase_nav,
            nav_date,
            latest_nav,
            units,
            current_value,
            gain_loss,
            holding_years,
            cagr
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

# ==========================================================
# DELETE INVESTMENT
# ==========================================================
def delete_investment(investment_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM investments
        WHERE id = %s
        """,
        (investment_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    
# ==========================================================
# LOAD PORTFOLIO
# ==========================================================
def load_portfolio(user_id=1):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            id,
            date,
            fund_type,
            fund_name,
            amount,
            purchase_nav,
            nav_date,
            latest_nav,
            units,
            current_value,
            gain_loss,
            holding_years,
            cagr

        FROM investments

        WHERE user_id = %s
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    columns = [
        "ID",
        "Date",
        "Fund Type",
        "Fund Name",
        "Amount",
        "Purchase NAV",
        "NAV Date",
        "Latest NAV",
        "Units",
        "Current Value",
        "Gain/Loss",
        "Holding Years",
        "CAGR %"
    ]

    portfolio_df = pd.DataFrame(
        rows,
        columns=columns
    )

    return portfolio_df


# ==========================================================
# DELETE CONFIRMATION DIALOG
# ==========================================================
@st.dialog("Delete Investment")
def confirm_delete_dialog(investment_id):

    st.warning(
        "Are you sure you want to delete this investment?"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):
            st.rerun()

    with col2:

        if st.button(
            "🗑 Yes, Delete",
            use_container_width=True
        ):

            delete_investment(
                investment_id
            )

            st.success(
                "Investment deleted successfully"
            )

            st.rerun()


# ==========================================================
# EDIT INVESTMENT DIALOG
# ==========================================================
@st.dialog("Edit Investment")
def edit_investment_dialog(row):

    st.write(
        "Update investment details"
    )

    # ==========================================
    # HANDLE MIXED DATE FORMATS
    # ==========================================
    try:

        parsed_date = datetime.strptime(
            row["Date"],
            "%d/%b/%Y"
        ).date()

    except ValueError:

        parsed_date = datetime.strptime(
            row["Date"],
            "%d/%m/%Y"
        ).date()

    # ==========================================
    # INPUTS
    # ==========================================
    new_date = st.date_input(
        "Investment Date",
        value=parsed_date,
        format="DD/MM/YYYY"
    )

    new_amount = st.number_input(
        "Investment Amount (₹)",
        min_value=1.0,
        value=float(
            row["Amount"]
        ),
        step=100.0
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "❌ Cancel",
            use_container_width=True
        ):
            st.rerun()

    with col2:

        if st.button(
            "💾 Save Changes",
            use_container_width=True
        ):

            # ==================================
            # FIND SCHEME CODE
            # ==================================
            scheme_code = (
                fund_df[
                    fund_df[
                        "Fund Name"
                    ] == row["Fund Name"]
                ]["Scheme Code"]
                .iloc[0]
            )

            # ==================================
            # RECALCULATE NAV
            # ==================================
            purchase_nav, latest_nav, nav_date_used = (
                get_nav_data(
                    scheme_code,
                    new_date.strftime(
                        "%d/%m/%Y"
                    )
                )
            )

            units = (
                new_amount
                / purchase_nav
            )

            current_value = (
                units
                * latest_nav
            )

            gain_loss = (
                current_value
                - new_amount
            )

            # ==================================
            # UPDATE DATABASE
            # ==================================
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE investments
                SET
                    date = %s,
                    amount = %s,
                    purchase_nav = %s,
                    nav_date = %s,
                    latest_nav = %s,
                    units = %s,
                    current_value = %s,
                    gain_loss = %s
                WHERE id = %s
                """,
                (
                    new_date.strftime(
                        "%d/%m/%Y"
                    ),
                    new_amount,
                    purchase_nav,
                    nav_date_used,
                    latest_nav,
                    units,
                    current_value,
                    gain_loss,
                    row["ID"]
                )
            )

            conn.commit()
            cursor.close()
            conn.close()

            st.success(
                "Investment updated successfully"
            )

            st.rerun()

# ==========================================================
# PORTFOLIO XIRR
# ==========================================================
def calculate_portfolio_xirr(df):

    if df.empty:
        return None

    cashflows = []

    for _, row in df.iterrows():

        try:

            investment_date = pd.to_datetime(
                row["Date"],
                dayfirst=True
            )

        except:

            continue

        cashflows.append(
            (
                investment_date,
                -float(row["Amount"])
            )
        )

    # add today's portfolio value
    current_value = (
        df["Current Value"]
        .sum()
    )

    cashflows.append(
        (
            pd.Timestamp.today(),
            current_value
        )
    )

    try:

        result = xirr(
            cashflows
        )

        return round(
            result * 100,
            2
        )

    except:

        return None

# ==========================================================
# FUND XIRR
# ==========================================================
def calculate_fund_xirr(fund_df):

    if fund_df.empty:
        return None

    cashflows = []

    for _, row in (
        fund_df
        .iterrows()
    ):

        try:

            investment_date = (
                pd.to_datetime(
                    row["Date"],
                    dayfirst=True
                )
            )

            cashflows.append(
                (
                    investment_date,
                    -float(
                        row["Amount"]
                    )
                )
            )

        except:

            continue

    current_value = (
        fund_df[
            "Current Value"
        ]
        .sum()
    )

    cashflows.append(
        (
            pd.Timestamp.today(),
            current_value
        )
    )

    try:

        result = xirr(
            cashflows
        )

        return round(
            result * 100,
            2
        )

    except:

        return None


# ======================================================
# HOLDINGS LAST UPDATE
# ======================================================
FUND_HOLDINGS_DATE = {

    "AXIS SMALL CAP":
        "May 2026",

    "BANDHAN":
        "May 2026",

    "HDFC FLEXI":
        "April 2026",

    "ICICI":
    "April 2026",

    "PARAG":
        "30/04/2026"
}

# ======================================
# GENERIC FUND EXCEL LOADER
# ======================================

def load_fund_excel(file_path):

    try:

        # Read Excel
        df = pd.read_excel(file_path)

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Keep required columns
        df = df[
            [
                "Stock",
                "Industry",
                "Weight"
            ]
        ].copy()

        # Remove blank rows
        df = df[
            df["Stock"].notna()
        ]

        # Clean text
        df["Stock"] = (
            df["Stock"]
            .astype(str)
            .str.strip()
        )

        df["Industry"] = (
            df["Industry"]
            .astype(str)
            .str.strip()
        )

        # ======================================
        # FIX WEIGHT FORMAT
        # ======================================

        # Convert weight to numeric
        df["Weight"] = pd.to_numeric(

            df["Weight"],

            errors="coerce"
        )

        # Remove invalid rows
        df = df[
            df["Weight"].notna()
        ]

        # Clean rounding
        df["Weight"] = (
            df["Weight"]
            .round(2)
        )

        return (
            df[
                [
                    "Stock",
                    "Industry",
                    "Weight"
                ]
            ]
            .reset_index(drop=True)
        )

    except Exception as e:

        st.error(
            f"Excel loading failed: {e}"
        )

        return pd.DataFrame()

# ======================================
# CLEAN STOCK NAMES
# ======================================
def normalize_stock_name(name):

    if pd.isna(name):
        return ""

    name = str(name).upper().strip()

    # remove common suffixes
    replacements = {

        " LIMITED": "",
        " LTD.": "",
        " LTD": "",
        " INC.": "",
        " INC": "",
        " PLC": "",
        " CORPORATION": " CORP",
        "&": "AND",

        "(INDIA)": "INDIA",
        "(INDIA) LIMITED": "INDIA",

        " COMPANY": "",
        " CO.": "",
        " PRIVATE": "",
        " PVT": "",

        ",": "",
        ".": ""
    }

    for old, new in replacements.items():

        name = name.replace(
            old,
            new
        )

    # remove extra spaces
    name = " ".join(
        name.split()
    )

    return name

# ==========================================================
# FUND OVERLAP CALCULATOR
# ==========================================================
def calculate_fund_overlap(
    fund1_df,
    fund2_df
):

    try:

        # ======================================
        # EMPTY CHECK
        # ======================================
        if (
            fund1_df.empty
            or
            fund2_df.empty
        ):

            return (
                0,
                pd.DataFrame()
            )

        # ======================================
        # NORMALIZE STOCK NAMES
        # ======================================

        fund1_df = (
            fund1_df.copy()
        )

        fund2_df = (
            fund2_df.copy()
        )

        fund1_df[
            "Stock_Normalized"
        ] = (
            fund1_df["Stock"]
            .apply(
                normalize_stock_name
            )
        )

        fund2_df[
            "Stock_Normalized"
        ] = (
            fund2_df["Stock"]
            .apply(
                normalize_stock_name
            )
        )

        # ======================================
        # MERGE USING NORMALIZED NAME
        # ======================================

        overlap_df = pd.merge(

            fund1_df,

            fund2_df,

            on="Stock_Normalized",

            how="outer",

            suffixes=(
                "_1",
                "_2"
            )
        )

        # ======================================
        # FIX STOCK NAME DISPLAY
        # ======================================

        overlap_df["Stock"] = (
            overlap_df["Stock_1"]
            .fillna(
                overlap_df["Stock_2"]
            )
        )


        # ======================================
        # FILL MISSING WEIGHTS
        # ======================================
        overlap_df[
            "Weight_1"
        ] = (
            overlap_df[
                "Weight_1"
            ]
            .fillna(0)
        )

        overlap_df[
            "Weight_2"
        ] = (
            overlap_df[
                "Weight_2"
            ]
            .fillna(0)
        )

        # ======================================
        # INDUSTRY FIX
        # ======================================

        # clean text values
        overlap_df[
            "Industry_1"
        ] = (
            overlap_df[
                "Industry_1"
            ]
            .astype(str)
            .str.strip()
        )

        overlap_df[
            "Industry_2"
        ] = (
            overlap_df[
                "Industry_2"
            ]
            .astype(str)
            .str.strip()
        )

        # replace bad values with NaN
        overlap_df[
            "Industry_1"
        ] = overlap_df[
            "Industry_1"
        ].replace(
            [
                "None",
                "none",
                "nan",
                "NaN",
                ""
            ],
            np.nan
        )

        overlap_df[
            "Industry_2"
        ] = overlap_df[
            "Industry_2"
        ].replace(
            [
                "None",
                "none",
                "nan",
                "NaN",
                ""
            ],
            np.nan
        )

        # combine industries
        overlap_df[
            "Industry"
        ] = (
            overlap_df[
                "Industry_1"
            ]
            .fillna(
                overlap_df[
                    "Industry_2"
                ]
            )
        )

        # final fallback
        overlap_df[
            "Industry"
        ] = (
            overlap_df[
                "Industry"
            ]
            .fillna(
                "Unknown"
            )
        )

        # ======================================
        # OVERLAP WEIGHT
        # ======================================
        overlap_df[
            "MinWeight"
        ] = overlap_df[
            [
                "Weight_1",
                "Weight_2"
            ]
        ].min(
            axis=1
        )

        # ======================================
        # OVERLAP %
        # ======================================
        overlap_pct = round(

            overlap_df[
                "MinWeight"
            ].sum(),

            2
        )

        return (
            overlap_pct,
            overlap_df
        )

    except Exception as e:

        st.error(
            f"Overlap calculation error: {e}"
        )

        return (
            0,
            pd.DataFrame()
        )

# ==========================================================
# MULTI FUND OVERLAP
# ==========================================================
def calculate_multi_fund_overlap(
    selected_funds
):

    all_holdings = []

    for fund in selected_funds:

        holdings = (
            get_fund_holdings(
                fund
            )
        )

        if holdings.empty:
            continue

        holdings = (
            holdings.copy()
        )

        holdings[
            "Stock_Normalized"
        ] = (
            holdings["Stock"]
            .apply(
                normalize_stock_name
            )
        )

        holdings[
            "Fund Name"
        ] = fund

        all_holdings.append(
            holdings
        )

    if not all_holdings:

        return pd.DataFrame()

    combined_df = pd.concat(
        all_holdings,
        ignore_index=True
    )

    # ======================================
    # PIVOT TABLE
    # ======================================
    pivot_df = (
        combined_df
        .pivot_table(

            index=[
                "Stock_Normalized"
            ],

            columns=
            "Fund Name",

            values=
            "Weight",

            aggfunc=
            "sum",

            fill_value=0
        )
        .reset_index()
    )

    # ======================================
    # STOCK NAME
    # ======================================
    stock_map = (
        combined_df
        .drop_duplicates(
            "Stock_Normalized"
        )
        [
            [
                "Stock_Normalized",
                "Stock",
                "Industry"
            ]
        ]
    )

    overlap_df = (
        pivot_df.merge(

            stock_map,

            on=
            "Stock_Normalized",

            how=
            "left"
        )
    )

    # ======================================
    # FUND COUNT
    # ======================================
    fund_cols = [
        x for x in overlap_df.columns
        if x in selected_funds
    ]

    overlap_df[
        "Fund Count"
    ] = (
        overlap_df[
            fund_cols
        ] > 0
    ).sum(
        axis=1
    )

    # ======================================
    # TOTAL EXPOSURE
    # ======================================
    overlap_df[
        "Total Exposure"
    ] = (
        overlap_df[
            fund_cols
        ]
        .sum(axis=1)
        .round(2)
    )

    # ======================================
    # SORT
    # ======================================
    overlap_df = (
        overlap_df
        .sort_values(

            by=[
                "Fund Count",
                "Total Exposure"
            ],

            ascending=False
        )
    )

    columns_to_show = [

        "Stock",

        "Industry",

        "Fund Count",

        "Total Exposure"

    ] + fund_cols

    return (
        overlap_df[
            columns_to_show
        ]
    )

# ==========================================================
# INDUSTRY DISTRIBUTION
# ==========================================================
def calculate_industry_distribution(
    selected_funds
):

    industry_data = []

    for fund in selected_funds:

        holdings = (
            get_fund_holdings(
                fund
            )
        )

        if holdings.empty:
            continue

        industry_df = (
            holdings
            .groupby(
                "Industry",
                as_index=False
            )["Weight"]
            .sum()
        )

        industry_df[
            "Fund"
        ] = fund

        industry_data.append(
            industry_df
        )

    if not industry_data:

        return pd.DataFrame()

    combined_df = pd.concat(

        industry_data,

        ignore_index=True
    )

    pivot_df = (
        combined_df
        .pivot_table(

            index="Industry",

            columns="Fund",

            values="Weight",

            fill_value=0
        )
    )

    return (
        pivot_df
        .round(1)
    )

# ==========================================================
# OVERLAP MATRIX COLORS
# ==========================================================
def color_overlap(val):

    if val == 100:
        return (
            "background-color: "
            "#2E8B57; color: white"
        )

    elif val < 10:
        return (
            "background-color: "
            "#1B5E20; color: white"
        )

    elif val < 25:
        return (
            "background-color: "
            "#F9A825; color: black"
        )

    elif val < 40:
        return (
            "background-color: "
            "#EF6C00; color: white"
        )

    else:
        return (
            "background-color: "
            "#C62828; color: white"
        )

# ==========================================================
# OVERLAP MATRIX
# ==========================================================
def calculate_overlap_matrix(
    selected_funds
):

    overlap_matrix = pd.DataFrame(

        index=selected_funds,

        columns=selected_funds,

        dtype=float
    )

    for i, fund1 in enumerate(selected_funds):

        for j, fund2 in enumerate(selected_funds):

            if i == j:

                overlap_matrix.loc[
                    fund1,
                    fund2
                ] = 100

            else:

                holdings_1 = (
                    get_fund_holdings(
                        fund1
                    )
                )

                holdings_2 = (
                    get_fund_holdings(
                        fund2
                    )
                )

                overlap_pct, _ = (
                    calculate_fund_overlap(
                        holdings_1,
                        holdings_2
                    )
                )

                overlap_matrix.loc[
                    fund1,
                    fund2
                ] = overlap_pct

    return (
        overlap_matrix
        .round(1)
    )


# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================
st.markdown("---")

portfolio_df = load_portfolio(
    user_id=1
)

st.header(
    "Portfolio Summary"
)

if not portfolio_df.empty:

    # ======================================================
    # TOTALS
    # ======================================================
    total_invested = (
        portfolio_df["Amount"]
        .sum()
    )

    total_current_value = (
        portfolio_df["Current Value"]
        .sum()
    )

    total_gain_loss = (
        portfolio_df["Gain/Loss"]
        .sum()
    )

    portfolio_xirr = (
        calculate_portfolio_xirr(
            portfolio_df
        )
    )

    # ======================================================
    # TOP METRICS
    # ======================================================
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Invested",
        f"₹{total_invested:,.2f}"
    )

    col2.metric(
        "Current Value",
        f"₹{total_current_value:,.2f}"
    )

    col3.metric(
        "Gain/Loss",
        f"₹{total_gain_loss:,.2f}"
    )

    col4.metric(
        "Portfolio XIRR",
        (
            f"{portfolio_xirr}%"
            if portfolio_xirr is not None
            else "N/A"
        )
    )

    st.markdown("---")

# ======================================================
# TYPE SUMMARY
# ======================================================
type_summary = (
    portfolio_df
    .groupby(
        "Fund Type",
        as_index=False
    )
    .agg({
        "Amount": "sum",
        "Current Value": "sum",
        "Gain/Loss": "sum"
    })
)

# ==========================================
# ALLOCATION %
# ==========================================
type_summary[
    "Allocation %"
] = (
    type_summary["Amount"]
    / total_invested
    * 100
).round(2)

# ==========================================
# CATEGORY XIRR %
# ==========================================
category_xirr_list = []

for fund_type in (
    type_summary[
        "Fund Type"
    ]
):

    category_df = (
        portfolio_df[
            portfolio_df[
                "Fund Type"
            ] == fund_type
        ]
    )

    category_xirr = (
        calculate_portfolio_xirr(
            category_df
        )
    )

    category_xirr_list.append(
        category_xirr
    )

type_summary[
    "XIRR %"
] = category_xirr_list

# ==========================================
# ROUND VALUES
# ==========================================
type_summary[
    "Current Value"
] = (
    type_summary[
        "Current Value"
    ].round(2)
)

type_summary[
    "Gain/Loss"
] = (
    type_summary[
        "Gain/Loss"
    ].round(2)
)

type_summary[
    "XIRR %"
] = (
    type_summary[
        "XIRR %"
    ].round(2)
)

# ======================================================
# CHARTS SECTION
# ======================================================
col_chart1, col_chart2 = st.columns(2)

# ======================================================
# PIE CHART
# ======================================================
with col_chart1:

    st.subheader(
        "Portfolio Allocation"
    )

    fig1, ax1 = plt.subplots(
        figsize=(4, 4)
    )

    ax1.pie(
        type_summary[
            "Amount"
        ],
        labels=type_summary[
            "Fund Type"
        ],
        autopct="%1.1f%%"
    )

    ax1.axis(
        "equal"
    )

    st.pyplot(
        fig1
    )

# ======================================================
# PORTFOLIO GROWTH
# ======================================================
with col_chart2:

    st.subheader(
        "Portfolio Growth"
    )

    growth_df = (
        portfolio_df.copy()
    )

    # ==========================================
    # ROBUST DATE PARSING
    # ==========================================
    def parse_mixed_date(x):

        if pd.isna(x):
            return pd.NaT

        x = str(x).strip()

        formats = [
            "%d/%m/%Y",   # 01/04/2026
            "%d/%b/%Y",   # 01/May/2023 short month
            "%d/%B/%Y"    # 01/May/2023 full month
        ]

        for fmt in formats:

            try:
                return pd.to_datetime(
                    x,
                    format=fmt
                )

            except:
                continue

        return pd.NaT


    growth_df[
        "SortDate"
    ] = (
        growth_df[
            "Date"
        ].apply(
            parse_mixed_date
        )
    )

    growth_df = (
        growth_df
        .sort_values(
            by="SortDate"
        )
    )


    # ==========================================
    # UNIQUE DATES
    # ==========================================
    unique_dates = sorted(
        pd.to_datetime(
            growth_df[
                "SortDate"
            ].dropna()
        )
    )

    growth_history = []

    # ==========================================
    # CALCULATE GROWTH OVER TIME
    # ==========================================
    for dt in unique_dates:

        temp_df = (
            growth_df[
                growth_df[
                    "SortDate"
                ] <= dt
            ]
        )

        growth_history.append(
            {
                "Date": dt,
                "Invested": temp_df[
                    "Amount"
                ].sum(),

                "CurrentValue": temp_df[
                    "Current Value"
                ].sum()
            }
        )

    chart_df = pd.DataFrame(
        growth_history
    )

    # ==========================================
    # CHART
    # ==========================================
    fig2, ax2 = plt.subplots(
        figsize=(5, 4)
    )


    ax2.plot(
        chart_df[
            "Date"
        ],
        chart_df[
            "Invested"
        ],
        label="Invested",
        linewidth=2
    )
        
    ax2.plot(
        chart_df[
            "Date"
        ],
        chart_df[
            "CurrentValue"
        ],
        label="Current Value",
        linewidth=2
    )

    ax2.set_ylabel(
        "₹"
    )

    ax2.legend()

    ax2.grid(
        True
    )

    st.pyplot(
        fig2
    )

# ======================================================
# MUTUAL FUND TYPE SUMMARY
# ======================================================
st.subheader(
    "Mutual Fund Type Summary"
)

st.dataframe(
    type_summary,
    use_container_width=True,
    hide_index=True
)


# ======================================
# FUND HOLDINGS DATABASE
# ======================================

def get_fund_holdings(fund_name):

    fund_upper = (
        fund_name.upper()
    )

    # BANDHAN SMALL CAP
    if "BANDHAN" in fund_upper:

        return load_fund_excel(
            "bandhan_small_cap_mar_2026.xlsx"
        )

    # HDFC FLEXI CAP
    elif "HDFC FLEXI" in fund_upper:

        return load_fund_excel(
            "hdfc_flexi_cap_apr_2026.xlsx"
        )

    # HDFC MID CAP
    elif "HDFC MID CAP" in fund_upper:

        return load_fund_excel(
            "hdfc_mid_cap_apr_2026.xlsx"
        )

    # ICICI_Prudential_Multi_Asset_Fund
    elif (
        "ICICI" in fund_upper
    ):

        return load_fund_excel(
            "ICICI_Prudential_Multi_Asset_Fund_apr_2026.xlsx"
        )

        # PARAG PARIKH FLEXI
    elif (
        "PARAG" in fund_upper
        or
        "PPFAS" in fund_upper
    ):

        return load_fund_excel(
            "parag_parikh_flexi_apr_2026.xlsx"
        )

    # MOTILAL OSWAL BSE ENHANCED VALUE INDEX FUND
    elif (
        "MOTILAL OSWAL BSE ENHANCED VALUE"
        in fund_upper
    ):

        return load_fund_excel(

            file_path=
            "Motilal_Oswal_BSE_Enhanced_Value_Index_Fund_apr_2026.xlsx"
        )

    return pd.DataFrame()

# ==========================================================
# MULTI FUND OVERLAP ANALYSIS
# ==========================================================

fund_list = sorted(
    portfolio_df[
        "Fund Name"
    ].unique()
)

if len(fund_list) >= 2:

    with st.expander(

        "📊 Mutual Fund Overlap Analysis",

        expanded=False
    ):

        selected_funds = st.multiselect(

            "Select Mutual Funds (2–6)",

            fund_list,

            default=fund_list[:2],

            max_selections=6
        )

        if len(selected_funds) == 0:

            st.warning(
                "Please select at least 1 fund."
            )

        else:

            overlap_df = (
                calculate_multi_fund_overlap(
                    selected_funds
                )
            )

            if not overlap_df.empty:

                # ==================================
                # OVERLAP ONLY (2+ FUNDS)
                # ==================================
                if len(selected_funds) >= 2:

                    repeated_stocks = (
                        overlap_df[
                            overlap_df[
                                "Fund Count"
                            ] > 1
                        ]
                    )

                    avg_overlap = round(

                        repeated_stocks[
                            "Total Exposure"
                        ].mean(),

                        1
                    )

                    fund_cols = selected_funds

                    overall_overlap = round(

                        overlap_df[
                            overlap_df[
                                "Fund Count"
                            ] > 1
                        ][fund_cols]
                        .min(axis=1)
                        .sum(),

                        1
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Repeated Stocks",
                        len(repeated_stocks)
                    )

                    col2.metric(
                        "Average Exposure",
                        f"{avg_overlap:.1f}%"
                    )

                    col3.metric(
                        "Portfolio Overlap",
                        f"{overall_overlap:.1f}%"
                    )

                    with st.expander(

                        "📊 Overlap Matrix",

                        expanded=False
                    ):

                        matrix_df = (
                            calculate_overlap_matrix(
                                selected_funds
                            )
                        )

                        styled_matrix = (
                            matrix_df.style
                            .format("{:.1f}")
                            .map(
                                color_overlap
                            )
                        )

                        st.dataframe(

                            styled_matrix,

                            use_container_width=True
                        )


                # ==================================
                # INDUSTRY DISTRIBUTION CHART
                # ==================================
                with st.expander(

                    "📈 Industry Distribution",

                    expanded=False
                ):

                    industry_df = (
                        calculate_industry_distribution(
                            selected_funds
                        )
                    )

                    if not industry_df.empty:

                        plot_df = (
                            industry_df
                            .reset_index()
                            .melt(

                                id_vars="Industry",

                                var_name="Fund",

                                value_name="Weight"
                            )
                        )

                        fig = px.bar(

                            plot_df,

                            x="Industry",

                            y="Weight",

                            color="Fund",

                            barmode="group",

                            title="Industry-wise Exposure"
                        )

                        fig.update_layout(

                            height=500,

                            xaxis_title="Industry",

                            yaxis_title="Weight (%)",

                            xaxis_tickangle=-45,

                            legend_title="Funds"
                        )

                        st.plotly_chart(

                            fig,

                            use_container_width=True
                        )

                # ==================================
                # INDUSTRY EXPOSURE TABLE
                # ==================================
                with st.expander(

                    "🏭 Industry Exposure Comparison",

                    expanded=False
                ):

                    industry_table = (
                        industry_df
                        .reset_index()
                    )

                    # sort by total exposure
                    industry_table["Total"] = (

                        industry_table[
                            selected_funds
                        ]
                        .sum(axis=1)
                    )

                    industry_table = (

                        industry_table
                        .sort_values(

                            by="Total",

                            ascending=False
                        )
                        .drop(
                            columns="Total"
                        )
                    )

                    industry_table = (
                        industry_table
                        .round(1)
                    )

                    st.dataframe(

                        industry_table,

                        use_container_width=True,

                        hide_index=True
                    )

                # ==================================
                # INDUSTRY STOCK BREAKDOWN
                # ==================================
                with st.expander(

                    "🏢 Industry Holdings Breakdown",

                    expanded=False
                ):

                    # ==================================
                    # SORT INDUSTRIES BY EXPOSURE
                    # ==================================
                    industry_order = (

                        overlap_df
                        .groupby(
                            "Industry",
                            as_index=False
                        )[
                            "Total Exposure"
                        ]
                        .sum()
                        .sort_values(

                            by="Total Exposure",

                            ascending=False
                        )
                    )

                    for industry in (
                        industry_order[
                            "Industry"
                        ]
                    ):

                        industry_stocks = (
                            overlap_df[
                                overlap_df[
                                    "Industry"
                                ] == industry
                            ]
                            .copy()
                        )

                        if industry_stocks.empty:
                            continue

                        industry_total = round(

                            industry_stocks[
                                "Total Exposure"
                            ].sum(),

                            1
                        )

                        with st.expander(

                            f"🏭 {industry} "
                            f"({industry_total:.1f}%)"
                        ):

                            display_cols = [

                                "Stock",

                                "Total Exposure"

                            ] + selected_funds

                            display_cols = [

                                col for col
                                in display_cols

                                if col
                                in industry_stocks.columns
                            ]

                            industry_stocks = (
                                industry_stocks
                                .sort_values(

                                    by="Total Exposure",

                                    ascending=False
                                )
                            )

                            st.dataframe(

                                industry_stocks[
                                    display_cols
                                ].round(1),

                                use_container_width=True,

                                hide_index=True
                            )

                # ==================================
                # COMMON STOCKS ACROSS FUNDS
                # ==================================
                with st.expander(

                    "🔁 Common Stocks Across Funds",

                    expanded=False
                ):

                    st.subheader(
                        "Common Stocks Across Funds"
                    )

                    # only repeated stocks
                    common_stocks = overlap_df[
                        overlap_df[
                            "Fund Count"
                        ] > 1
                    ].copy()

                    if not common_stocks.empty:

                        common_stock_rows = []

                        for _, row in (
                            common_stocks.iterrows()
                        ):

                            for fund in (
                                selected_funds
                            ):

                                weight = (
                                    row.get(
                                        fund,
                                        0
                                    )
                                )

                                if weight > 0:

                                    common_stock_rows.append({

                                        "Stock":
                                        row["Stock"],

                                        "Industry":
                                        row["Industry"],

                                        "Mutual Fund":
                                        fund,

                                        "Weight %":
                                        round(
                                            weight,
                                            1
                                        )
                                    })

                        common_stock_df = (
                            pd.DataFrame(
                                common_stock_rows
                            )
                        )

                        # ==========================
                        # SORT MOST COMMON FIRST
                        # ==========================
                        stock_count = (

                            common_stock_df
                            .groupby(
                                "Stock"
                            )[
                                "Mutual Fund"
                            ]
                            .nunique()
                            .reset_index(
                                name=
                                "Fund Count"
                            )
                        )

                        stock_total = (

                            common_stock_df
                            .groupby(
                                "Stock"
                            )[
                                "Weight %"
                            ]
                            .sum()
                            .reset_index(
                                name=
                                "Total Exposure"
                            )
                        )

                        common_stock_df = (

                            common_stock_df
                            .merge(
                                stock_count,
                                on="Stock",
                                how="left"
                            )
                            .merge(
                                stock_total,
                                on="Stock",
                                how="left"
                            )
                        )

                        common_stock_df = (

                            common_stock_df
                            .sort_values(

                                by=[

                                    "Fund Count",

                                    "Total Exposure",

                                    "Weight %"
                                ],

                                ascending=[

                                    False,

                                    False,

                                    False
                                ]
                            )
                        )

                        common_stock_df = (
                            common_stock_df.drop(

                                columns=[

                                    "Fund Count",

                                    "Total Exposure"
                                ]
                            )
                        )

                        st.dataframe(

                            common_stock_df,

                            use_container_width=True,

                            hide_index=True,

                            height=450
                        )

                    else:

                        st.info(
                            "No common stocks found."
                        )

else:

    st.info(
        "Add at least 2 mutual funds "
        "to use overlap analysis."
    )


# ======================================================
# FUND TYPE LOOP
# ======================================================
for ft in (
    portfolio_df[
        "Fund Type"
    ].unique()
):

    ft_key = f"ft_{ft}"


    with st.expander(
    ft,
    expanded=False
    ):

        # ==========================================
        # FILTER DATA
        # ==========================================
        type_df = (
            portfolio_df[
                portfolio_df[
                    "Fund Type"
                ] == ft
            ]
        )

        # ==========================================
        # FUND SUMMARY
        # ==========================================
        fund_summary = (
            type_df
            .groupby(
                "Fund Name",
                as_index=False
            )
            .agg({
                "Amount": "sum",
                "Current Value": "sum",
                "Gain/Loss": "sum"
            })
        )

        # ==========================================
        # ALLOCATION %
        # ==========================================
        type_total = (
            fund_summary[
                "Amount"
            ].sum()
        )

        fund_summary[
            "Allocation %"
        ] = (
            fund_summary[
                "Amount"
            ]
            / type_total
            * 100
        ).round(2)

        # ==========================================
        # FUND XIRR %
        # ==========================================
        fund_xirr_list = []

        for fund_name in (
            fund_summary[
                "Fund Name"
            ]
        ):

            fund_df_temp = (
                type_df[
                    type_df[
                        "Fund Name"
                    ] == fund_name
                ]
            )

            fund_xirr = (
                calculate_fund_xirr(
                    fund_df_temp
                )
            )

            fund_xirr_list.append(
                fund_xirr
            )

        fund_summary[
            "XIRR %"
        ] = fund_xirr_list

        # ==========================================
        # ROUND VALUES
        # ==========================================
        fund_summary[
            "Current Value"
        ] = (
            fund_summary[
                "Current Value"
            ].round(2)
        )

        fund_summary[
            "Gain/Loss"
        ] = (
            fund_summary[
                "Gain/Loss"
            ].round(2)
        )

        fund_summary[
            "XIRR %"
        ] = (
            fund_summary[
                "XIRR %"
            ].round(2)
        )

        st.dataframe(
            fund_summary,
            use_container_width=True,
            hide_index=True
        )



        # ==========================================
        # FUND LOOP
        # ==========================================
        for fund in (
            type_df[
                "Fund Name"
            ].unique()
        ):

            fund_key = (
                f"fund_{fund}"
            )

            with st.expander(
                fund,
                expanded=False
            ):

                fund_df_detail = (
                    type_df[
                        type_df[
                            "Fund Name"
                        ] == fund
                    ]
                ).copy()
                # ==================================
                # DATE CLEANUP
                # ==================================
                def parse_mixed_date(x):

                    try:
                        return pd.to_datetime(
                            x,
                            format="%d/%m/%Y"
                        )

                    except:

                        try:
                            return pd.to_datetime(
                                x,
                                format="%d/%b/%Y"
                            )

                        except:

                            try:
                                return pd.to_datetime(
                                    x,
                                    format="%d/%B/%Y"
                                )

                            except:
                                return pd.NaT


                fund_df_detail[
                    "SortDate"
                ] = (
                    fund_df_detail[
                        "Date"
                    ].apply(
                        parse_mixed_date
                    )
                )

                fund_df_detail = (
                    fund_df_detail
                    .sort_values(
                        by="SortDate",
                        ascending=False
                    )
                )

                fund_df_detail[
                    "Date"
                ] = (
                    fund_df_detail[
                        "SortDate"
                    ]
                    .dt.strftime(
                        "%d/%m/%Y"
                    )
                )

                # ==================================
                # TABLE HEADER
                # ==================================
                h1, h2, h3, h4, h5 = st.columns(
                    [2.2, 2, 2, 1.5, 1.1]
                )

                h1.markdown(
                    "**Date**"
                )
                h2.markdown(
                    "**Amount**"
                )
                h3.markdown(
                    "**Current Value**"
                )
                h4.markdown(
                    "**Gain/Loss**"
                )
                h5.markdown(
                    "**Actions**"
                )

                # ==================================
                # TRANSACTION ROWS
                # ==================================
                for _, row in (
                    fund_df_detail
                    .iterrows()
                ):

                    c1, c2, c3, c4, c5 = st.columns(
                        [2.2, 2, 2, 1.5, 1.1]
                    )

                    c1.markdown(
                        row["Date"]
                    )

                    c2.markdown(
                        f"₹{row['Amount']:.2f}"
                    )

                    c3.markdown(
                        f"₹{row['Current Value']:.2f}"
                    )

                    c4.markdown(
                        f"₹{row['Gain/Loss']:.2f}"
                    )

                    with c5:

                        edit_col, delete_col = st.columns(
                            [1, 1]
                        )

                        with edit_col:

                            if st.button(
                                "✏️",
                                key=f"edit_{row['ID']}"
                            ):

                                edit_investment_dialog(
                                    row
                                )

                        with delete_col:

                            if st.button(
                                "🗑",
                                key=f"delete_{row['ID']}"
                            ):

                                confirm_delete_dialog(
                                    row["ID"]
                                )


# ==========================================================
# INPUT SECTION
# ==========================================================
st.subheader(
    "Add Mutual Fund Investment"
)

col1, col2, col3, col4 = st.columns(4)

investment_date = col1.date_input(
    "Investment Date",
    value=date.today(),
    format="DD/MM/YYYY"
)

mutual_fund_types = [
    "Large Cap",
    "Flexi Cap",
    "Mid Cap",
    "Small Cap",
    "Hybrid",
    "Debt",
    "ELSS",
    "Index Fund",
    "Sectoral/Thematic"
]

mf_type = col2.selectbox(
    "Mutual Fund Type",
    mutual_fund_types
)

selected_fund = col3.selectbox(
    "Mutual Fund",

    options=fund_df["Fund Name"].tolist(),

    index=None,

    placeholder="Search mutual fund..."
)

investment_amount = col4.number_input(
    "Investment Amount (₹)",
    min_value=100,
    step=100
)

if st.button("Add Investment"):

    try:

        scheme_code = (
            fund_df[
                fund_df["Fund Name"]
                == selected_fund
            ]["Scheme Code"]
            .iloc[0]
        )

        fund_name = selected_fund

        invest_date_str = (
            investment_date.strftime(
                "%d/%m/%Y"
            )
        )

        (
            purchase_nav,
            latest_nav,
            nav_date_used
        ) = get_nav_data(
            scheme_code,
            invest_date_str
        )

        units = (
            investment_amount
            / purchase_nav
        )

        current_value = (
            units
            * latest_nav
        )

        gain = (
            current_value
            - investment_amount
        )

        holding_years = (
            (
                date.today()
                - investment_date
            ).days
            / 365.25
        )

        cagr = (
            (
                current_value
                / investment_amount
            )
            ** (
                1 / holding_years
            )
            - 1
        ) * 100

        save_investment(

            user_id=1,

            date=investment_date.strftime(
                "%d/%m/%Y"
            ),

            fund_type=mf_type,

            fund_name=fund_name,

            amount=investment_amount,

            purchase_nav=round(
                purchase_nav,
                2
            ),

            nav_date=nav_date_used,

            latest_nav=round(
                latest_nav,
                2
            ),

            units=round(
                units,
                4
            ),

            current_value=round(
                current_value,
                2
            ),

            gain_loss=round(
                gain,
                2
            ),

            holding_years=round(
                holding_years,
                2
            ),

            cagr=round(
                cagr,
                2
            )
        )

        st.success(
            "Investment added successfully"
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Error: {e}"
        )
