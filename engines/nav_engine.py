# =============================================================================
# File Name : engines/nav_engine.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# NAV Engine
#
# Responsibilities
# ----------------
# ✓ Latest NAV update
# ✓ Historical NAV
# ✓ Batch NAV refresh
# ✓ Portfolio refresh
# ✓ Cache integration
# ✓ MarketDataService integration
#
# =============================================================================

from __future__ import annotations

from datetime import datetime

import pandas as pd

from data.orchestrator.market_data_service import market_data

from repositories.investment_repository import InvestmentRepository
from repositories.investment_query_repository import (
    InvestmentQueryRepository,
)

from analytics.return_engine import ReturnEngine


class NAVEngine:
    """
    NAV Update Engine
    """

    def __init__(self):

        self.repository = InvestmentRepository()

        self.query = InvestmentQueryRepository()

    # -------------------------------------------------------------------------
    # Latest NAV
    # -------------------------------------------------------------------------

    def latest_nav(
        self,
        scheme_code: str
    ) -> float:

        return market_data.latest_price(

            "Mutual Fund",

            scheme_code

        )

    # -------------------------------------------------------------------------
    # NAV History
    # -------------------------------------------------------------------------

    def history(
        self,
        scheme_code: str,
        start_date=None,
        end_date=None
    ) -> pd.DataFrame:

        return market_data.historical_data(

            "Mutual Fund",

            scheme_code,

            start_date,

            end_date

        )

    # -------------------------------------------------------------------------
    # Refresh Single Investment
    # -------------------------------------------------------------------------

    def refresh_investment(
        self,
        investment
    ):

        latest_nav = self.latest_nav(

            investment.scheme_code

        )

        investment.latest_nav = latest_nav

        investment.current_value = (

            ReturnEngine.current_value(

                investment.units,

                latest_nav

            )

        )

        investment.gain_loss = (

            ReturnEngine.profit(

                investment.amount,

                investment.current_value

            )

        )

        investment.gain_loss_percent = (

            ReturnEngine.return_percent(

                investment.amount,

                investment.current_value

            )

        )

        self.repository.update(

            investment

        )

        return investment

    # -------------------------------------------------------------------------
    # Refresh Portfolio
    # -------------------------------------------------------------------------

    def refresh_portfolio(
        self,
        user_id: int = 1
    ):

        portfolio = self.query.load_portfolio(

            user_id

        )

        updated = 0

        failed = 0

        for _, row in portfolio.iterrows():

            try:

                latest = self.latest_nav(

                    str(row["scheme_code"])

                )

                current_value = (

                    ReturnEngine.current_value(

                        row["units"],

                        latest

                    )

                )

                gain = (

                    ReturnEngine.profit(

                        row["amount"],

                        current_value

                    )

                )

                gain_percent = (

                    ReturnEngine.return_percent(

                        row["amount"],

                        current_value

                    )

                )

                query = """

                UPDATE investments

                SET

                    latest_nav=%s,

                    nav_date=%s,

                    current_value=%s,

                    gain_loss=%s,

                    gain_loss_percent=%s

                WHERE id=%s

                """

                self.repository.execute(

                    query,

                    (

                        latest,

                        datetime.today(),

                        current_value,

                        gain,

                        gain_percent,

                        row["id"]

                    )

                )

                updated += 1

            except Exception:

                failed += 1

        return {

            "updated": updated,

            "failed": failed

        }

    # -------------------------------------------------------------------------
    # Refresh One Scheme
    # -------------------------------------------------------------------------

    def refresh_scheme(
        self,
        scheme_code: str,
        user_id: int = 1
    ):

        portfolio = self.query.search_exact(

            "scheme_code",

            scheme_code

        )

        for row in portfolio:

            self.refresh_investment(

                row

            )

    # -------------------------------------------------------------------------
    # Validate Scheme
    # -------------------------------------------------------------------------

    def validate(
        self,
        scheme_code: str
    ) -> bool:

        return market_data.validate(

            "Mutual Fund",

            scheme_code

        )

    # -------------------------------------------------------------------------
    # Provider Health
    # -------------------------------------------------------------------------

    def provider_status(self):

        return market_data.health()