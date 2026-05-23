import streamlit as st
import pandas as pd
import requests
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
# SESSION STATE
# ==========================================================
if "transactions" not in st.session_state:
    st.session_state.transactions = []

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
            investment_date
            .strftime("%d/%m/%Y")
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
            ** (1 / holding_years)
            - 1
        ) * 100

        st.session_state.transactions.append({

            "Date":
            investment_date.strftime(
                "%d/%B/%Y"
            ),

            "Fund Type":
            mf_type,

            "Fund Name":
            fund_name,

            "Amount":
            investment_amount,

            "Purchase NAV":
            round(
                purchase_nav,
                2
            ),

            "NAV Date":
            nav_date_used,

            "Latest NAV":
            round(
                latest_nav,
                2
            ),

            "Units":
            round(
                units,
                4
            ),

            "Current Value":
            round(
                current_value,
                2
            ),

            "Gain/Loss":
            round(
                gain,
                2
            ),

            "Holding Years":
            round(
                holding_years,
                2
            ),

            "CAGR %":
            round(
                cagr,
                2
            )
        })

        st.success(
            "Investment added successfully"
        )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

# ==========================================================
# PORTFOLIO
# ==========================================================
if st.session_state.transactions:

    portfolio_df = pd.DataFrame(
        st.session_state.transactions
    )

    st.divider()

    st.header(
        "Portfolio Summary"
    )

    # ======================================================
    # TYPE SUMMARY
    # ======================================================
    st.subheader(
        "Mutual Fund Type Summary"
    )

    type_summary = (
        portfolio_df
        .groupby("Fund Type")
        .agg({
            "Amount": "sum",
            "Current Value": "sum",
            "Gain/Loss": "sum"
        })
        .reset_index()
    )

    total_portfolio = (
        type_summary[
            "Amount"
        ].sum()
    )

    type_summary[
        "Allocation %"
    ] = (
        type_summary[
            "Amount"
        ]
        / total_portfolio
        * 100
    ).round(2)

    type_summary = type_summary[
        [
            "Fund Type",
            "Amount",
            "Allocation %",
            "Current Value",
            "Gain/Loss"
        ]
    ]

    st.dataframe(
        type_summary,
        use_container_width=True,
        hide_index=True
    )

    # ======================================================
    # FUND DETAILS
    # ======================================================
    fund_type_order = [
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

    available_types = [
        ft for ft in fund_type_order
        if ft in portfolio_df[
            "Fund Type"
        ].unique()
    ]

    for fund_type in available_types:

        type_df = portfolio_df[
            portfolio_df[
                "Fund Type"
            ]
            == fund_type
        ]

        with st.expander(
            f"{fund_type}",
            expanded=False
        ):

            st.markdown(
                "### Fund Summary"
            )

            fund_summary = (
                type_df
                .groupby(
                    "Fund Name"
                )
                .agg({
                    "Amount": "sum",
                    "Current Value": "sum",
                    "Gain/Loss": "sum"
                })
                .reset_index()
            )

            total_type_amount = (
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
                / total_type_amount
                * 100
            ).round(2)

            fund_summary = fund_summary[
                [
                    "Fund Name",
                    "Amount",
                    "Allocation %",
                    "Current Value",
                    "Gain/Loss"
                ]
            ]

            st.dataframe(
                fund_summary,
                use_container_width=True,
                hide_index=True
            )

            # Transactions
            for fund in (
                type_df[
                    "Fund Name"
                ].unique()
            ):

                with st.expander(
                    fund,
                    expanded=False
                ):

                    fund_transactions = (
                        type_df[
                            type_df[
                                "Fund Name"
                            ]
                            == fund
                        ]
                    )

                    fund_transactions = (
                        fund_transactions
                        .drop(
                            columns=[
                                "Fund Type",
                                "Fund Name"
                            ]
                        )
                    )

                    st.dataframe(
                        fund_transactions,
                        use_container_width=True,
                        hide_index=True
                    )

    # ======================================================
    # OVERALL SUMMARY
    # ======================================================
    st.divider()

    total_invested = (
        portfolio_df[
            "Amount"
        ].sum()
    )

    total_current = (
        portfolio_df[
            "Current Value"
        ].sum()
    )

    total_gain = (
        portfolio_df[
            "Gain/Loss"
        ].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Invested",
        f"₹{total_invested:,.2f}"
    )

    col2.metric(
        "Current Value",
        f"₹{total_current:,.2f}"
    )

    col3.metric(
        "Gain/Loss",
        f"₹{total_gain:,.2f}"
    )

else:

    st.info(
        "No investments added yet"
    )