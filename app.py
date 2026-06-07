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
import plotly.graph_objects as go

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

    # ==========================================
    # INVESTMENTS TABLE
    # ==========================================

    cursor.execute("""
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

        created_at TIMESTAMP DEFAULT NOW()
    )
    """)

    # ==========================================
    # BENCHMARK MAPPING TABLE
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_mapping (

        fund_name TEXT PRIMARY KEY,

        benchmark TEXT

    )
    """)

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


    for i, item in enumerate(nav_data[:5]):
        print(
            i,
            item["date"],
            item["nav"]
        )

    target_date = datetime.strptime(
        invest_date,
        "%d/%m/%Y"
    )


    purchase_nav = None
    nav_date_used = None

    # MFAPI already returns newest -> oldest

    for item in nav_data:

        nav_date = datetime.strptime(
            item["date"],
            "%d-%m-%Y"
        )

        if nav_date <= target_date:

            purchase_nav = float(
                item["nav"]
            )

            nav_date_used = item["date"]

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

# =====================================================
# LOAD BENCHMARK MAPPING
# =====================================================

def load_benchmark_mapping():

    conn = get_connection()

    query = """
    SELECT
        fund_name,
        benchmark
    FROM benchmark_mapping
    """

    try:

        df = pd.read_sql(
            query,
            conn
        )

        conn.close()

        return dict(
            zip(
                df["fund_name"],
                df["benchmark"]
            )
        )

    except:

        conn.close()

        return {}


# =====================================================
# SAVE BENCHMARK MAPPING
# =====================================================

def save_benchmark_mapping(
    fund_name,
    benchmark
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO benchmark_mapping
        (
            fund_name,
            benchmark
        )

        VALUES
        (
            %s,
            %s
        )

        ON CONFLICT (fund_name)

        DO UPDATE SET

        benchmark =
        EXCLUDED.benchmark
        """,

        (
            fund_name,
            benchmark
        )
    )

    conn.commit()

    cursor.close()

    conn.close()


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
    new_amount = st.number_input(
        "Investment Amount (₹)",
        min_value=1.0,
        value=float(row["Amount"]),
        step=100.0,
        key=f"edit_amount_{row['ID']}"
    )

    new_date = st.date_input(
        "Investment Date",
        value=parsed_date,
        format="DD/MM/YYYY",
        key=f"edit_date_{row['ID']}"
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

            if purchase_nav is None:

                st.error(
                    f"NAV not found for {fund_name} "
                    f"on {invest_date_str}"
                )

                st.stop()

            if purchase_nav is None:

                st.error(
                    f"No NAV available for {fund_name}"
                )

                st.stop()

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


def parse_portfolio_date(x):

    if pd.isna(x):
        return pd.NaT

    if isinstance(
        x,
        (pd.Timestamp, datetime)
    ):
        return pd.Timestamp(x)

    x = str(x).strip()

    formats = [
        "%d/%m/%Y",
        "%d/%b/%Y",
        "%d/%B/%Y"
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(
                x,
                format=fmt
            )
        except:
            pass

    return pd.NaT

# =====================================================
# BENCHMARK SIP XIRR CALCULATION
# =====================================================
def calculate_benchmark_xirr(
    fund_data,
    benchmark_df
):

    fund_data = fund_data.copy()

    fund_data["Date"] = (
        fund_data["Date"]
        .apply(parse_portfolio_date)
    )

    fund_data = (
        fund_data
        .sort_values("Date")
    )

    try:

        benchmark_df = benchmark_df.copy()

        benchmark_df["Date"] = pd.to_datetime(
            benchmark_df["Date"],
            errors="coerce"
        )

        benchmark_df["Close"] = pd.to_numeric(
            benchmark_df["Close"],
            errors="coerce"
        )

        benchmark_df = (
            benchmark_df
            .dropna(subset=["Date", "Close"])
            .sort_values("Date")
        )


        if benchmark_df.empty:
            return None

        latest_close = float(
            benchmark_df.loc[
                benchmark_df["Date"].idxmax(),
                "Close"
            ]
        )

        total_units = 0.0

        cashflows = []

        for _, sip in fund_data.iterrows():
            

            sip_date = sip["Date"]

            if pd.isna(sip_date):
                continue

            sip_amount = float(
                sip["Amount"]
            )

            rows = benchmark_df[
                benchmark_df["Date"] <= sip_date
            ]


            if rows.empty:
                st.error(
                    f"No benchmark data for {sip_date}"
                )
                continue

            benchmark_close = float(
                rows.iloc[-1]["Close"]
            )

            units = (
                sip_amount
                / benchmark_close
            )

            total_units += units

            cashflows.append(
                (
                    sip_date,
                    -sip_amount
                )
            )



        if total_units == 0:
            return None

        benchmark_value = (
            total_units
            * latest_close
        )

        cashflows.append(
            (
                datetime.today(),
                benchmark_value
            )
        )

        benchmark_xirr = (
            xirr(cashflows)
            * 100
        )

        return {
            "xirr": round(
                benchmark_xirr,
                2
            ),
            "value": round(
                benchmark_value,
                2
            )
        }

    except Exception as e:

        st.error(
            f"Benchmark XIRR Error: {e}"
        )

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

    "ICICI PRUDENTIAL MULTI ASSET":
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




#CATEGORY_MAP

CATEGORY_MAP = {

    # EQUITY
    "Large Cap": "Equity",
    "Mid Cap": "Equity",
    "Small Cap": "Equity",
    "Flexi Cap": "Equity",
    "Multi Cap": "Equity",
    "Focused Fund": "Equity",
    "Value Fund": "Equity",
    "Contra Fund": "Equity",
    "ELSS": "Equity",
    "Index Fund": "Equity",
    "Sectoral/Thematic": "Equity",

    # HYBRID
    "Aggressive Hybrid": "Hybrid",
    "Balanced Advantage": "Hybrid",
    "Multi Asset Allocation": "Hybrid",
    "Equity Savings": "Hybrid",
    "Arbitrage Fund": "Hybrid",
    "Dynamic Asset Allocation": "Hybrid",
    "Conservative Hybrid": "Hybrid",

    # DEBT
    "Liquid Fund": "Debt",
    "Ultra Short Duration": "Debt",
    "Low Duration": "Debt",
    "Short Duration": "Debt",
    "Corporate Bond": "Debt",
    "Banking & PSU Debt": "Debt",
    "Money Market": "Debt",
    "Gilt Fund": "Debt",
    "Dynamic Bond": "Debt",

    # COMMODITY
    "Gold Fund": "Commodity",
    "Silver Fund": "Commodity",

    # GLOBAL
    "International Fund": "Global",
    "US Equity": "Global",
    "Global Equity": "Global",
    "FoF Overseas": "Global"
}


# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================
st.markdown("---")


portfolio_df = load_portfolio(
    user_id=1
)


portfolio_df["Category"] = (
    portfolio_df["Fund Type"]
    .map(CATEGORY_MAP)
    .fillna("Unknown")
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
        ["Category", "Fund Type"],
        as_index=False
    )
    .agg(
        {
            "Amount": "sum",
            "Current Value": "sum",
            "Gain/Loss": "sum"
        }
    )
)

# Rename for display
type_summary.rename(
    columns={
        "Category": "Fund Category"
    },
    inplace=True
)

category_order = {
    "Equity": 1,
    "Hybrid": 2,
    "Debt": 3,
    "Commodity": 4,
    "Global": 5
}

type_summary["SortOrder"] = (
    type_summary["Fund Category"]
    .map(category_order)
)

type_summary = (
    type_summary
    .sort_values(
        [
            "SortOrder",
            "Fund Type"
        ]
    )
    .drop(
        columns="SortOrder"
    )
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

for fund_type in type_summary["Fund Type"]:

    category_df = portfolio_df[
        portfolio_df["Fund Type"] == fund_type
    ]

    oldest_date = (
        category_df["Date"]
        .apply(parse_portfolio_date)
        .min()
    )

    holding_days = (
        pd.Timestamp.today() - oldest_date
    ).days

    if holding_days < 30:
        category_xirr = None
    else:
        category_xirr = calculate_portfolio_xirr(
            category_df
        )

    category_xirr_list.append(
        category_xirr
    )

# CREATE COLUMN
xirr_values = []
xirr_comments = []

for fund_type in type_summary["Fund Type"]:

    category_df = portfolio_df[
        portfolio_df["Fund Type"] == fund_type
    ]

    oldest_date = (
        category_df["Date"]
        .apply(parse_portfolio_date)
        .min()
    )

    holding_days = (
        pd.Timestamp.today() - oldest_date
    ).days

    if holding_days < 30:

        xirr_values.append(None)

        xirr_comments.append(
            f"Only {holding_days} days"
        )

    else:

        xirr_values.append(
            calculate_portfolio_xirr(category_df)
        )

        xirr_comments.append("OK")

type_summary["XIRR %"] = xirr_values
type_summary["Remarks"] = xirr_comments

# ROUND
type_summary["XIRR %"] = (
    type_summary["XIRR %"]
    .round(2)
)

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

    st.markdown("---")

    col_a, col_b = st.columns([1,4])




# ======================================================
# MUTUAL FUND TYPE SUMMARY
# ======================================================

with st.expander(
    "📊 Mutual Fund Type Summary",
    expanded=False
):

    category_order = [
        "Equity",
        "Hybrid",
        "Debt",
        "Commodity",
        "Global"
    ]

    for category in category_order:

        category_table = (
            type_summary[
                type_summary["Fund Category"]
                == category
            ]
        )

        if category_table.empty:
            continue

        with st.expander(
            f"📂 {category}",
            expanded=False
        ):

            display_table = category_table.copy()

            display_table["XIRR Display"] = np.where(
                display_table["Remarks"] == "OK",
                display_table["XIRR %"].astype(str) + "%",
                display_table["Remarks"]
            )

            display_table = display_table[
                [
                    "Fund Type",
                    "Amount",
                    "Current Value",
                    "Gain/Loss",
                    "Allocation %",
                    "XIRR Display"
                ]
            ]

            st.dataframe(
                display_table,
                use_container_width=True,
                hide_index=True,
                height=min(
                    35 * (len(display_table) + 1),
                    250
                )
            )


# =====================================================
# BENCHMARK MAPPING STORAGE
# =====================================================

if "benchmark_mapping" not in st.session_state:

    st.session_state.benchmark_mapping = (
        load_benchmark_mapping()
    )

# =====================================================
# BENCHMARK ANALYSIS
# =====================================================

BENCHMARK_FILES = {
    "None": None,
    "NIFTY50_TRI": "NIFTY_50_TRI.csv",
    "NIFTY500_TRI": "NIFTY_500_TRI.csv"
}

# =====================================================
# LOAD BENCHMARK FILE
# =====================================================

@st.cache_data
def load_benchmark_file(file_name):

    try:

        df = pd.read_csv(file_name)

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # =====================================
        # TRI FILE SUPPORT
        # =====================================

        if "Net Total Return Index" in df.columns:

            df.rename(
                columns={
                    "Net Total Return Index": "Close"
                },
                inplace=True
            )

        elif "Total Returns Index" in df.columns:

            df.rename(
                columns={
                    "Total Returns Index": "Close"
                },
                inplace=True
            )

        # =====================================
        # DATE FORMAT
        # =====================================

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d-%b-%y",
            errors="coerce"
        )

        df["Close"] = pd.to_numeric(
            df["Close"],
            errors="coerce"
        )

        df = (
            df
            .dropna(subset=["Date", "Close"])
            .sort_values("Date")
            .reset_index(drop=True)
        )

        return df

    except Exception as e:

        st.error(
            f"Benchmark load error: {e}"
        )

        return pd.DataFrame()




if st.button("🔄 Reload Benchmark Files"):
    st.cache_data.clear()
    st.success("Benchmark files reloaded")
    st.rerun()
# =====================================================
# BENCHMARK ANALYSIS
# =====================================================

with st.expander(
    "📈 Benchmark Analysis",
    expanded=False
):

    # =====================================================
    # BENCHMARK MAPPING
    # =====================================================

    st.subheader("Benchmark Selection")

    benchmark_options = [
        "None",
        "NIFTY50_TRI",
        "NIFTY500_TRI"
    ]

    if "benchmark_mapping" not in st.session_state:
        st.session_state.benchmark_mapping = {}

    mapping_rows = []

    for fund_name in sorted(
        portfolio_df["Fund Name"].unique()
    ):

        fund_type = portfolio_df[
            portfolio_df["Fund Name"] == fund_name
        ]["Fund Type"].iloc[0]

        mapping_rows.append({

            "Fund Type": fund_type,

            "Fund Name": fund_name,

            "Benchmark":
            st.session_state.benchmark_mapping.get(
                fund_name,
                "None"
            )
        })

    mapping_df = pd.DataFrame(
        mapping_rows
    )

    edited_mapping = st.data_editor(

        mapping_df,

        hide_index=True,

        use_container_width=True,

        key="benchmark_mapping_editor",

        column_config={

            "Benchmark":
            st.column_config.SelectboxColumn(

                "Benchmark",

                options=benchmark_options,

                required=True
            )
        },

        disabled=[
            "Fund Type",
            "Fund Name"
        ]
    )

    for _, row in edited_mapping.iterrows():

        st.session_state.benchmark_mapping[
            row["Fund Name"]
        ] = row["Benchmark"]

    if st.button(
        "💾 Save Benchmark Mapping"
    ):

        for _, row in edited_mapping.iterrows():

            fund_name = row["Fund Name"]

            benchmark = row["Benchmark"]

            st.session_state.benchmark_mapping[
                fund_name
            ] = benchmark

            save_benchmark_mapping(
                fund_name,
                benchmark
            )

        st.success(
            "Benchmark mapping saved"
        )

    # =====================================================
    # BENCHMARK COMPARISON RESULTS
    # =====================================================

    st.subheader("Benchmark Comparison Results")

    comparison_rows = []

    for fund_name in sorted(
        portfolio_df["Fund Name"].unique()
    ):

        fund_data = portfolio_df[
            portfolio_df["Fund Name"] == fund_name
        ]

 

        fund_type = fund_data[
            "Fund Type"
        ].iloc[0]

        invested = round(
            fund_data["Amount"].sum(),
            2
        )

        current_value = round(
            fund_data["Current Value"].sum(),
            2
        )

        fund_xirr = calculate_fund_xirr(
            fund_data
        )

        benchmark_name = (
            st.session_state.benchmark_mapping.get(
                fund_name,
                "None"
            )
        )

        benchmark_xirr = None
        benchmark_value = None
        alpha = None
        status = "N/A"

        if benchmark_name != "None":


            benchmark_file = BENCHMARK_FILES.get(
                benchmark_name
            )


            if benchmark_file:

                benchmark_df = load_benchmark_file(
                    benchmark_file
                )


                fund_dates = (
                    fund_data["Date"]
                    .apply(parse_portfolio_date)
                )

                oldest_date = fund_dates.min()


                result = calculate_benchmark_xirr(
                    fund_data,
                    benchmark_df
                )

                if result:

                    benchmark_xirr = result["xirr"]

                    benchmark_value = result["value"]

                    alpha = round(
                        fund_xirr -
                        benchmark_xirr,
                        2
                    )

                    if alpha >= 5:
                        status = "🟢 Strong Outperformance"

                    elif alpha > 0:
                        status = "🟡 Outperforming"

                    elif alpha > -5:
                        status = "🟠 Slightly Behind"

                    else:
                        status = "🔴 Underperforming"

                else:

                    benchmark_xirr = None
                    benchmark_value = None
                    alpha = None
                    status = (
                        "No Benchmark Data"
                    )

        comparison_rows.append({

            "Fund Type":
            fund_type,

            "Fund Name":
            fund_name,

            "Benchmark":
            benchmark_name,

            "Invested":
            invested,

            "Current Value":
            current_value,

            "Fund XIRR %":
            round(fund_xirr, 2)
            if fund_xirr is not None
            else None,

            "Benchmark XIRR %":
            round(benchmark_xirr, 2)
            if benchmark_xirr is not None
            else None,

            "Benchmark Current Value ₹":
            round(benchmark_value, 2)
            if benchmark_value is not None
            else None,

            "Excess XIRR %":
            alpha,

            "Status":
            status
        })

    comparison_df = pd.DataFrame(
        comparison_rows
    )

    valid_alpha = comparison_df[
        "Excess XIRR %"
    ].dropna()

    if not valid_alpha.empty:

        avg_alpha = round(
            valid_alpha.mean(),
            2
        )

        st.metric(
            "Average Portfolio Alpha",
            f"{avg_alpha}%"
        )

    st.dataframe(

        comparison_df,

        hide_index=True,

        use_container_width=True
    )

# =====================================================
# INVESTMENT vs BENCHMARK TIMELINE
# =====================================================

st.markdown("---")
st.subheader("📅 Investment vs Benchmark Timeline")

for fund_name in sorted(portfolio_df["Fund Name"].unique()):

    benchmark_name = (
        st.session_state.benchmark_mapping.get(
            fund_name,
            "None"
        )
    )

    if benchmark_name == "None":
        continue

    fund_data = portfolio_df[
        portfolio_df["Fund Name"] == fund_name
    ].copy()

    if fund_data.empty:
        continue

    latest_nav = (
        fund_data["Latest NAV"]
        .iloc[0]
    )

    with st.expander(
        f"📈 {fund_name}",
        expanded=False
    ):

        st.caption(
            f"Default Benchmark: {benchmark_name}"
        )

        available_benchmarks = [
            "NIFTY50_TRI",
            "NIFTY500_TRI"
        ]

        default_selection = [benchmark_name]

        selected_benchmarks = st.multiselect(
            "Compare against benchmark(s)",
            options=available_benchmarks,
            default=default_selection,
            placeholder="Select benchmark(s)",
            key=f"timeline_benchmarks_{fund_name}"
        )

        if not selected_benchmarks:
            selected_benchmarks = default_selection

        timeline_rows = []

        for _, txn in fund_data.iterrows():

            sip_date = parse_portfolio_date(
                txn["Date"]
            )

            if pd.isna(sip_date):
                continue

            amount = float(txn["Amount"])

            purchase_nav = float(
                txn["Purchase NAV"]
            )

            fund_units = (
                amount / purchase_nav
            )

            fund_current_value = (
                fund_units * latest_nav
            )

            row = {

                "Investment Date":
                sip_date.strftime("%d-%b-%Y"),

                "Invested ₹":
                round(amount, 2),

                "Fund Value ₹":
                round(
                    fund_current_value,
                    2
                )
            }

            for bm_name in selected_benchmarks:

                bm_file = BENCHMARK_FILES.get(
                    bm_name
                )

                if bm_file is None:
                    continue

                bm_df = load_benchmark_file(
                    bm_file
                )

                bm_rows = bm_df[
                    bm_df["Date"] <= sip_date
                ]

                if bm_rows.empty:
                    continue

                purchase_index = float(
                    bm_rows.iloc[-1]["Close"]
                )

                latest_index = float(
                    bm_df["Close"].iloc[-1]
                )

                benchmark_value = (
                    amount
                    * latest_index
                    / purchase_index
                )

                row[f"{bm_name} ₹"] = round(
                    benchmark_value,
                    2
                )

                row[f"Alpha vs {bm_name} ₹"] = round(
                    fund_current_value
                    - benchmark_value,
                    2
                )

            timeline_rows.append(row)
        # ==========================================
        # CREATE DATAFRAME
        # ==========================================
        timeline_df = pd.DataFrame(
            timeline_rows
        )

        if timeline_df.empty:
            st.info("No data available")
            continue

        # ==========================================
        # REORDER COLUMNS
        # ==========================================

        display_cols = [
            "Investment Date",
            "Invested ₹",
            "Fund Value ₹"
        ]

        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"
            alpha_col = f"Alpha vs {bm_name} ₹"

            if bm_col in timeline_df.columns:
                display_cols.append(bm_col)

            if alpha_col in timeline_df.columns:
                display_cols.append(alpha_col)

        timeline_df = timeline_df[display_cols]


        # ==========================================
        # SORT TIMELINE - NEWEST DATE FIRST
        # ==========================================

        timeline_df["SortDate"] = pd.to_datetime(
            timeline_df["Investment Date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

        timeline_df = (
            timeline_df
            .sort_values(
                "SortDate",
                ascending=False
            )
            .drop(
                columns=["SortDate"]
            )
            .reset_index(drop=True)
        )

        # ==========================================
        # SHOW TABLE
        # ==========================================

        st.dataframe(
            timeline_df,
            use_container_width=False,
            hide_index=True,
            height=min(
                35 * (len(timeline_df) + 1),
                400
            )
        )

        # ==========================================
        # PERFORMANCE SUMMARY
        # ==========================================

        st.markdown("### 📊 Performance Summary")

        fund_total_value = (
            timeline_df["Fund Value ₹"]
            .sum()
        )

        col1, col2, col3 = st.columns([2,2,2])

        with col1:
            st.metric(
                "Fund Portfolio Value",
                f"₹{fund_total_value:,.2f}"
            )

        if len(selected_benchmarks) >= 1:

            bm1 = selected_benchmarks[0]

            bm1_total = (
                timeline_df[f"{bm1} ₹"]
                .sum()
            )

            bm1_alpha = (
                fund_total_value
                - bm1_total
            )

            with col2:

                st.metric(
                    f"{bm1} Value",
                    f"₹{bm1_total:,.2f}"
                )

                st.caption(
                    f"Alpha ₹{bm1_alpha:,.2f}"
                )

        if len(selected_benchmarks) >= 2:

            bm2 = selected_benchmarks[1]

            bm2_total = (
                timeline_df[f"{bm2} ₹"]
                .sum()
            )

            bm2_alpha = (
                fund_total_value
                - bm2_total
            )

            with col3:

                st.metric(
                    f"{bm2} Value",
                    f"₹{bm2_total:,.2f}"
                )

                st.caption(
                    f"Alpha ₹{bm2_alpha:,.2f}"
                )

        # ==========================================
        # SIP-WISE PERFORMANCE COMPARISON
        # ==========================================

        st.markdown("### 📈 SIP-wise Performance Comparison")

        chart_df = timeline_df.copy()

        chart_df["Investment Date"] = pd.to_datetime(
            chart_df["Investment Date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

        chart_df = chart_df.sort_values(
            "Investment Date",
            ascending=True
        )

        # --------------------------------------------------
        # Create custom hover data
        # --------------------------------------------------

        hover_fields = []

        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col in chart_df.columns:
                hover_fields.append(bm_col)

            alpha_col = f"Alpha vs {bm_name} ₹"

            if alpha_col in chart_df.columns:
                hover_fields.append(alpha_col)

        # --------------------------------------------------
        # Plot columns
        # --------------------------------------------------

        plot_columns = ["Fund Value ₹"]

        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col in chart_df.columns:
                plot_columns.append(bm_col)

        plot_columns = list(dict.fromkeys(plot_columns))

        # --------------------------------------------------
        # Figure
        # --------------------------------------------------

        fig = go.Figure()

        for col in plot_columns:

            customdata = chart_df[
                hover_fields
            ].values

            hover_text = (
                "<b>Date:</b> %{x}<br>"
                "<b>Fund Value:</b> ₹%{customdata[0]:,.2f}<br>"
            )

            idx = 1

            for bm_name in selected_benchmarks:

                bm_col = f"{bm_name} ₹"

                alpha_col = f"Alpha vs {bm_name} ₹"

                if bm_col in chart_df.columns:

                    hover_text += (
                        f"<b>{bm_name}:</b> "
                        f"₹%{{customdata[{idx}]:,.2f}}<br>"
                    )

                    idx += 1

                if alpha_col in chart_df.columns:

                    hover_text += (
                        f"<b>Alpha vs {bm_name}:</b> "
                        f"₹%{{customdata[{idx}]:,.2f}}<br>"
                    )

                    idx += 1

            hover_text += "<extra></extra>"

            fig.add_trace(

                go.Scatter(

                    x=chart_df["Investment Date"],

                    y=chart_df[col],

                    mode="lines+markers",

                    name=col,

                    customdata=np.column_stack(

                        [
                            chart_df["Fund Value ₹"]
                        ]

                        +

                        [
                            chart_df[c]
                            for c in hover_fields
                        ]
                    ),

                    hovertemplate=hover_text
                )
            )

        # --------------------------------------------------
        # Layout
        # --------------------------------------------------

        fig.update_layout(

            height=420,

            hovermode="x unified",

            xaxis_title="Investment Date",

            yaxis_title="Value (₹)",

            legend_title="",

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ==========================================
        # SIP-WISE BAR CHART
        # ==========================================

        st.markdown(
            "### 📊 SIP-wise Value Comparison (Bar Chart)"
        )

        bar_df = chart_df.copy()

        # Convert dates to categorical labels
        bar_df["Investment Date Label"] = (
            bar_df["Investment Date"]
            .dt.strftime("%d-%b-%Y")
        )

        fig_bar = go.Figure()

        # Fund bars
        fig_bar.add_trace(
            go.Bar(
                x=bar_df["Investment Date Label"],
                y=bar_df["Fund Value ₹"],
                name="Fund Value ₹"
            )
        )

        # Benchmark bars
        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col in bar_df.columns:

                fig_bar.add_trace(
                    go.Bar(
                        x=bar_df["Investment Date Label"],
                        y=bar_df[bm_col],
                        name=bm_col
                    )
                )

        fig_bar.update_layout(

            barmode="group",

            height=500,

            xaxis_title="Investment Date",

            yaxis_title="Value (₹)",

            legend_title="",

            hovermode="x unified",

            margin=dict(
                l=20,
                r=20,
                t=20,
                b=80
            )
        )

        fig_bar.update_xaxes(
            tickangle=-45
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )
        # ==========================================
        # ALPHA SUMMARY
        # ==========================================

        st.markdown(
            "### 🎯 Alpha Summary"
        )

        summary_items = []

        fund_total_value = (
            timeline_df["Fund Value ₹"].sum()
        )

        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col not in timeline_df.columns:
                continue

            benchmark_total = (
                timeline_df[bm_col].sum()
            )

            alpha_total = (
                fund_total_value
                - benchmark_total
            )

            summary_items.append(
                (
                    f"Alpha vs {bm_name}",
                    alpha_total
                )
            )

        cols = st.columns(
            max(1, len(summary_items))
        )

        for col, (label, value) in zip(
            cols,
            summary_items
        ):

            col.metric(
                label,
                f"₹{value:,.2f}"
            )


        # ==========================================
        # PREPARE CUMULATIVE DATA
        # ==========================================

        cumulative_df = timeline_df.copy()

        cumulative_df["Investment Date"] = pd.to_datetime(
            cumulative_df["Investment Date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

        cumulative_df = cumulative_df.sort_values(
            "Investment Date",
            ascending=True
        )

        # Fund cumulative growth
        cumulative_df["Fund Cumulative ₹"] = (
            cumulative_df["Fund Value ₹"]
            .cumsum()
        )

        # Benchmark cumulative growth
        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col not in cumulative_df.columns:
                continue

            cumulative_df[
                f"{bm_name} Cumulative ₹"
            ] = (
                cumulative_df[bm_col]
                .cumsum()
            )

            cumulative_df[
                f"Alpha vs {bm_name} Cumulative ₹"
            ] = (
                cumulative_df["Fund Cumulative ₹"]
                -
                cumulative_df[
                    f"{bm_name} Cumulative ₹"
                ]
            )



        # ==========================================
        # CUMULATIVE PORTFOLIO GROWTH
        # ==========================================

        st.markdown("### 📊 Cumulative Portfolio Growth vs Benchmark")

        cumulative_df = timeline_df.copy()

        cumulative_df["Investment Date"] = pd.to_datetime(
            cumulative_df["Investment Date"],
            format="%d-%b-%Y",
            errors="coerce"
        )

        cumulative_df = cumulative_df.sort_values(
            "Investment Date",
            ascending=True
        )

        # ------------------------------------------
        # Fund cumulative growth
        # ------------------------------------------

        cumulative_df["Fund Cumulative ₹"] = (
            cumulative_df["Fund Value ₹"]
            .cumsum()
        )

        # ------------------------------------------
        # Benchmark cumulative growth
        # ------------------------------------------

        for bm_name in selected_benchmarks:

            bm_col = f"{bm_name} ₹"

            if bm_col not in cumulative_df.columns:
                continue

            cumulative_df[
                f"{bm_name} Cumulative ₹"
            ] = (
                cumulative_df[bm_col]
                .cumsum()
            )

            cumulative_df[
                f"Alpha vs {bm_name} Cumulative ₹"
            ] = (
                cumulative_df["Fund Cumulative ₹"]
                -
                cumulative_df[
                    f"{bm_name} Cumulative ₹"
                ]
            )

        # ------------------------------------------
        # Cumulative Growth Chart
        # ------------------------------------------

        plot_columns = [
            "Fund Cumulative ₹"
        ]

        for bm_name in selected_benchmarks:

            col_name = (
                f"{bm_name} Cumulative ₹"
            )

            if col_name in cumulative_df.columns:

                plot_columns.append(
                    col_name
                )

        chart_cumulative = (
            cumulative_df
            .set_index("Investment Date")
        )

        fig_cum = go.Figure()

        for col in plot_columns:

            fig_cum.add_trace(
                go.Scatter(
                    x=chart_cumulative.index,
                    y=chart_cumulative[col],
                    mode="lines+markers",
                    name=col,
                    hovertemplate=
                    "<b>Date:</b> %{x}<br>" +
                    f"<b>{col}:</b> ₹%{{y:,.2f}}" +
                    "<extra></extra>"
                )
            )

        fig_cum.update_layout(
            height=350,
            hovermode="x unified",
            xaxis_title="Investment Date",
            yaxis_title="Cumulative Value (₹)"
        )

        st.plotly_chart(
            fig_cum,
            use_container_width=True
        )

        # ==========================================
        # CUMULATIVE ALPHA CHART
        # ==========================================

        st.markdown(
            "### 📈 Cumulative Alpha Growth"
        )

        alpha_columns = []

        for bm_name in selected_benchmarks:

            alpha_col = (
                f"Alpha vs {bm_name} Cumulative ₹"
            )

            if alpha_col in cumulative_df.columns:

                alpha_columns.append(
                    alpha_col
                )

        if alpha_columns:

            alpha_chart_df = (
                cumulative_df
                .set_index("Investment Date")
            )

            fig_alpha = go.Figure()

            for col in alpha_columns:

                fig_alpha.add_trace(
                    go.Scatter(
                        x=alpha_chart_df.index,
                        y=alpha_chart_df[col],
                        mode="lines+markers",
                        name=col,
                        hovertemplate=
                        "<b>Date:</b> %{x}<br>" +
                        f"<b>{col}:</b> ₹%{{y:,.2f}}" +
                        "<extra></extra>"
                    )
                )

            fig_alpha.update_layout(
                height=350,
                hovermode="x unified",
                xaxis_title="Investment Date",
                yaxis_title="Alpha (₹)"
            )

            st.plotly_chart(
                fig_alpha,
                use_container_width=True
            )


# ==========================================================
# INDUSTRY DISTRIBUTION ANALYSIS
# ==========================================================

fund_list = sorted(
    portfolio_df["Fund Name"].unique()
)

with st.expander(
    "📊 Industry Distribution Analysis",
    expanded=False
):

    industry_funds = st.multiselect(
        "Select Mutual Fund(s)",
        fund_list,
        key="industry_distribution_funds"
    )

    if len(industry_funds) == 0:

        st.info(
            "Select at least 1 mutual fund."
        )

    else:

        industry_df = (
            calculate_industry_distribution(
                industry_funds
            )
        )

        if industry_df.empty:

            st.warning(
                "No holdings data available."
            )

        else:

            st.dataframe(
                industry_df.round(1),
                use_container_width=True
            )

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
                xaxis_tickangle=-45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ==========================================================
# MUTUAL FUND OVERLAP ANALYSIS
# ==========================================================

with st.expander(
    "🔄 Mutual Fund Overlap Analysis",
    expanded=False
):

    overlap_funds = st.multiselect(
        "Select Mutual Funds (2-6)",
        fund_list,
        max_selections=6,
        key="overlap_analysis_funds"
    )

    if len(overlap_funds) < 2:

        st.info(
            "Select at least 2 mutual funds."
        )

    else:

        overlap_df = (
            calculate_multi_fund_overlap(
                overlap_funds
            )
        )

        repeated_stocks = (
            overlap_df[
                overlap_df["Fund Count"] > 1
            ]
        )

        fund_cols = [

            fund

            for fund in overlap_funds

            if fund in overlap_df.columns
        ]

        avg_overlap = 0

        if not repeated_stocks.empty:

            avg_overlap = round(
                repeated_stocks[
                    "Total Exposure"
                ].mean(),
                1
            )

        overall_overlap = round(

            overlap_df[
                overlap_df["Fund Count"] > 1
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

        # ======================================
        # OVERLAP MATRIX
        # ======================================

        with st.expander(
            "📊 Overlap Matrix",
            expanded=False
        ):

            matrix_df = (
                calculate_overlap_matrix(
                    overlap_funds
                )
            )

            styled_matrix = (
                matrix_df.style
                .format("{:.1f}")
                .map(color_overlap)
            )

            st.dataframe(
                styled_matrix,
                use_container_width=True
            )

        # ======================================
        # INDUSTRY EXPOSURE COMPARISON
        # ======================================

        with st.expander(
            "🏭 Industry Exposure Comparison",
            expanded=False
        ):

            industry_df = (
                calculate_industry_distribution(
                    overlap_funds
                )
            )

            if industry_df.empty:

                st.warning(
                    "No industry data available."
                )

            else:

                industry_table = (
                    industry_df
                    .reset_index()
                )

                available_funds = [

                    fund

                    for fund in overlap_funds

                    if fund in industry_table.columns
                ]

                industry_table["Total"] = (

                    industry_table[
                        available_funds
                    ]
                    .sum(axis=1)
                )

                industry_table = (

                    industry_table
                    .sort_values(
                        "Total",
                        ascending=False
                    )
                    .drop(
                        columns="Total"
                    )
                )

                st.dataframe(
                    industry_table.round(1),
                    use_container_width=True,
                    hide_index=True
                )

        # ======================================
        # COMMON STOCKS
        # ======================================

        with st.expander(
            "🔁 Common Stocks Across Funds",
            expanded=False
        ):

            common_stocks = (

                overlap_df[
                    overlap_df[
                        "Fund Count"
                    ] > 1
                ]
                .copy()
            )

            if common_stocks.empty:

                st.info(
                    "No common stocks found."
                )

            else:

                st.dataframe(
                    common_stocks,
                    use_container_width=True,
                    hide_index=True
                )


# ======================================================
# CATEGORY -> TYPE -> FUND
# ======================================================

category_order = [
    "Equity",
    "Hybrid",
    "Debt",
    "Commodity",
    "Global"
]

for category in category_order:

    category_df = portfolio_df[
        portfolio_df["Category"] == category
    ]

    if category_df.empty:
        continue

    with st.expander(
        f"📂 {category}",
        expanded=False
    ):

        fund_types = sorted(
            category_df["Fund Type"].unique()
        )

        for ft in fund_types:

            type_df = category_df[
                category_df["Fund Type"] == ft
            ]

            if type_df.empty:
                continue

            with st.expander(
                f"📁 {ft}",
                expanded=False
            ):

                fund_summary = (
                    type_df
                    .groupby(
                        "Fund Name",
                        as_index=False
                    )
                    .agg(
                        {
                            "Amount": "sum",
                            "Current Value": "sum",
                            "Gain/Loss": "sum"
                        }
                    )
                )

                # ======================================
                # FUND XIRR
                # ======================================

                fund_xirr_list = []
                remarks = []

                for fund_name in fund_summary["Fund Name"]:

                    temp_df = type_df[
                        type_df["Fund Name"] == fund_name
                    ]

                    oldest_date = (
                        temp_df["Date"]
                        .apply(parse_portfolio_date)
                        .min()
                    )

                    holding_days = (
                        pd.Timestamp.today() - oldest_date
                    ).days

                    if holding_days < 30:

                        fund_xirr_list.append(None)

                        remarks.append(
                            f"Only {holding_days} days"
                        )

                    else:

                        fund_xirr_list.append(
                            calculate_fund_xirr(temp_df)
                        )

                        remarks.append("OK")

                # ======================================
                # XIRR DISPLAY COLUMN
                # ======================================

                fund_summary["XIRR %"] = [

                    f"{x:.2f}%"
                    if x is not None
                    else remarks[i]

                    for i, x in enumerate(fund_xirr_list)
                ]

                # ======================================
                # ALLOCATION %
                # ======================================

                total_type_value = (
                    fund_summary["Current Value"]
                    .sum()
                )

                fund_summary["Allocation %"] = (

                    fund_summary["Current Value"]
                    / total_type_value
                    * 100

                ).round(2)

                # ======================================
                # SORT
                # ======================================

                fund_summary = (
                    fund_summary
                    .sort_values(
                        by="Current Value",
                        ascending=False
                    )
                )

                # ======================================
                # DISPLAY ONLY REQUIRED COLUMNS
                # ======================================

                display_fund_summary = fund_summary[
                    [
                        "Fund Name",
                        "Amount",
                        "Current Value",
                        "Gain/Loss",
                        "XIRR %",
                        "Allocation %"
                    ]
                ]

                st.dataframe(
                    display_fund_summary,
                    use_container_width=True,
                    hide_index=True
                )

                # ======================================
                # ALLOCATION %
                # WITHIN FUND TYPE
                # ======================================

                total_type_value = (
                    fund_summary[
                        "Current Value"
                    ]
                    .sum()
                )

                fund_summary["Allocation %"] = (
                    fund_summary[
                        "Current Value"
                    ]
                    / total_type_value
                    * 100
                ).round(2)

                # ======================================
                # SORT LARGEST FIRST
                # ======================================

                fund_summary = (
                    fund_summary
                    .sort_values(
                        by="Current Value",
                        ascending=False
                    )
                )

                # ======================================
                # DISPLAY COLUMNS
                # ======================================

                for fund in fund_summary["Fund Name"]:

                    fund_df_detail = type_df[
                        type_df["Fund Name"] == fund
                    ].copy()

                    fund_df_detail["SortDate"] = pd.to_datetime(
                        fund_df_detail["Date"],
                        dayfirst=True,
                        errors="coerce"
                    )

                    fund_df_detail = (
                        fund_df_detail
                        .sort_values(
                            by="SortDate",
                            ascending=False
                        )
                        .drop(columns="SortDate")
                    )

                    with st.expander(
                        f"📄 {fund}",
                        expanded=False
                    ):

                        header1, header2, header3, header4, header5, header6, header7, header8, header9 = st.columns(
                            [1.5, 1.5, 1.1, 1.1, 1.4, 1.4, 1.0, 0.9, 0.9]
                        )

                        header1.markdown("**Date**")
                        header2.markdown("**Amount**")
                        header3.markdown("**Purchase NAV**")
                        header4.markdown("**Latest NAV**")
                        header5.markdown("**Current Value**")
                        header6.markdown("**Gain/Loss**")
                        header7.markdown("**Return %**")
                        header8.markdown("**Edit**")
                        header9.markdown("**Delete**")



                        for idx, row in fund_df_detail.iterrows():

                            col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(
                                [1.5, 1.5, 1.1, 1.1, 1.4, 1.4, 1.0, 0.9, 0.9]
                            )

                            col1.write(row["Date"])

                            col2.write(
                                f"₹{row['Amount']:,.2f}"
                            )

                            col3.write(
                                f"{row['Purchase NAV']:.2f}"
                            )

                            col4.write(
                                f"{row['Latest NAV']:.2f}"
                            )

                            col5.write(
                                f"₹{row['Current Value']:,.2f}"
                            )

                            col6.write(
                                f"₹{row['Gain/Loss']:,.2f}"
                            )

                            return_pct = (
                                row["Gain/Loss"]
                                / row["Amount"]
                            ) * 100

                            col7.write(
                                f"{return_pct:.2f}%"
                            )

                            with col8:

                                if st.button(
                                    "✏️",
                                    key=f"edit_{row['ID']}",
                                    use_container_width=True
                                ):
                                    edit_investment_dialog(row)

                            with col9:

                                if st.button(
                                    "🗑️",
                                    key=f"delete_{row['ID']}",
                                    use_container_width=True
                                ):
                                    confirm_delete_dialog(
                                        row["ID"]
                                    )

# ======================================================
# FUND CATEGORY -> FUND TYPE MAPPING
# ======================================================

CATEGORY_TYPES = {

    "Equity": [
        "Large Cap",
        "Mid Cap",
        "Small Cap",
        "Flexi Cap",
        "Multi Cap",
        "Focused Fund",
        "Value Fund",
        "Contra Fund",
        "ELSS",
        "Index Fund",
        "Sectoral/Thematic"
    ],

    "Hybrid": [
        "Aggressive Hybrid",
        "Balanced Advantage",
        "Multi Asset Allocation",
        "Equity Savings",
        "Arbitrage Fund",
        "Dynamic Asset Allocation",
        "Conservative Hybrid"
    ],

    "Debt": [
        "Liquid Fund",
        "Ultra Short Duration",
        "Low Duration",
        "Short Duration",
        "Corporate Bond",
        "Banking & PSU Debt",
        "Money Market",
        "Gilt Fund",
        "Dynamic Bond"
    ],

    "Commodity": [
        "Gold Fund",
        "Silver Fund"
    ],

    "Global": [
        "International Fund",
        "US Equity",
        "Global Equity",
        "FoF Overseas"
    ]
}


# ==========================================================
# INPUT SECTION
# ==========================================================
st.subheader(
    "Add Mutual Fund Investment"
)

col1, col2, col3, col4, col5 = st.columns(5)

investment_date = col1.date_input(
    "Investment Date",
    value=date.today(),
    format="DD/MM/YYYY"
)

fund_category = col2.selectbox(
    "Fund Category",
    list(CATEGORY_TYPES.keys())
)


mf_type = col3.selectbox(
    "Mutual Fund Type",
    CATEGORY_TYPES[
        fund_category
    ]
)

selected_fund = col4.selectbox(
    "Mutual Fund",
    options=fund_df["Fund Name"].tolist(),
    index=None,
    placeholder="Search mutual fund..."
)

investment_amount = col5.number_input(
    "Investment Amount (₹)",
    min_value=100,
    step=100
)

if st.button("Add Investment"):

    try:

        if not selected_fund:

            st.error(
                "Please select a mutual fund."
            )
            st.stop()

        scheme_match = fund_df[
            fund_df["Fund Name"]
            == selected_fund
        ]

        if scheme_match.empty:

            st.error(
                f"Fund not found: {selected_fund}"
            )
            st.stop()

        scheme_code = (
            scheme_match[
                "Scheme Code"
            ].iloc[0]
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

        gain_loss = (
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

        if holding_years > 0:

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

        else:

            cagr = 0

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
                gain_loss,
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
