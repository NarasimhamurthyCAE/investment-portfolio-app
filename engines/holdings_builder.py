# =============================================================================
# File Name : engines/holdings_builder.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Holdings Builder
#
# Converts investment records into a unified holdings DataFrame.
#
# NOTE
# ----
# This class will later merge:
#
# • Mutual Fund portfolio files
# • ETF portfolio files
# • Direct stocks
# • Gold ETFs
#
# =============================================================================

from __future__ import annotations

import pandas as pd


class HoldingsBuilder:

    """
    Unified Holdings Builder
    """

    def build(

        self,

        portfolio: pd.DataFrame

    ) -> pd.DataFrame:

        if portfolio.empty:

            return pd.DataFrame()

        columns = [

            "company",

            "sector",

            "country",

            "market_cap",

            "weight",

            "investment_value",

            "source"

        ]

        return pd.DataFrame(

            columns=columns

        )

    # -----------------------------------------------------------------

    def normalize_company(

        self,

        name: str

    ) -> str:

        if name is None:

            return ""

        return (

            str(name)

            .strip()

            .upper()

        )

    # -----------------------------------------------------------------

    def merge_duplicates(

        self,

        holdings: pd.DataFrame

    ) -> pd.DataFrame:

        if holdings.empty:

            return holdings

        return (

            holdings

            .groupby(

                [

                    "company",

                    "sector",

                    "country",

                    "market_cap"

                ],

                dropna=False

            )

            .agg(

                {

                    "weight": "sum",

                    "investment_value": "sum"

                }

            )

            .reset_index()

        )