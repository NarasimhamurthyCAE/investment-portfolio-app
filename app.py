import streamlit as st
import pandas as pd
import requests
import psycopg2
import os
from datetime import datetime, date

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

    df.rename(
        columns={
            "schemeCode": "Scheme Code",
            "schemeName": "Fund Name"
        },
        inplace=True
    )

    # Filter Direct Growth only
    df["UPPER"] = (
        df["Fund Name"]
        .str.upper()
    )

    include = (
        df["UPPER"].str.contains(
            "DIRECT",
            na=False
        )
        &
        df["UPPER"].str.contains(
            "GROWTH",
            na=False
        )
    )

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

    df = df[
        include
        &
        ~exclude
    ]

    df = df.sort_values(
        "Fund Name"
    )

    df = df.reset_index(
        drop=True
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
# LOAD PORTFOLIO
# ==========================================================
def load_portfolio(user_id=1):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

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

selected_index = col3.selectbox(
    "Mutual Fund",
    fund_df.index,
    format_func=lambda x:
    fund_df.loc[
        x,
        "Fund Name"
    ]
)

investment_amount = col4.number_input(
    "Investment Amount (₹)",
    min_value=100,
    step=100
)

if st.button("Add Investment"):

    try:

        scheme_code = fund_df.loc[
            selected_index,
            "Scheme Code"
        ]

        fund_name = fund_df.loc[
            selected_index,
            "Fund Name"
        ]

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
                "%d/%B/%Y"
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

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

# ==========================================================
# PORTFOLIO SUMMARY
# ==========================================================
st.markdown("---")

st.header(
    "Portfolio Summary"
)

# Load saved investments
portfolio_df = load_portfolio(
    user_id=1
)

if not portfolio_df.empty:

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

    st.subheader(
        "Mutual Fund Type Summary"
    )

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

    type_summary[
        "Allocation %"
    ] = (
        type_summary["Amount"]
        / total_invested
        * 100
    ).round(2)

    st.dataframe(
        type_summary,
        use_container_width=True,
        hide_index=True
    )

    for ft in (
        portfolio_df[
            "Fund Type"
        ].unique()
    ):

        with st.expander(
            ft
        ):

            type_df = (
                portfolio_df[
                    portfolio_df[
                        "Fund Type"
                    ] == ft
                ]
            )

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

            st.dataframe(
                fund_summary,
                use_container_width=True,
                hide_index=True
            )

            for fund in (
                type_df[
                    "Fund Name"
                ].unique()
            ):

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
                    )

                    st.dataframe(
                        fund_df_detail,
                        use_container_width=True,
                        hide_index=True
                    )

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

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

else:

    st.info(
        "No investments added yet"
    )