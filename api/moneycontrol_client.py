# =============================================================================
# File Name : api/moneycontrol_client.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# MoneyControl Client
#
# =============================================================================

from __future__ import annotations

import requests


class MoneyControlClient:
    """
    MoneyControl API/Web Client.
    """

    BASE_URL = "https://www.moneycontrol.com"

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            }
        )

    # -------------------------------------------------------------------------

    def latest_price(
        self,
        symbol: str,
    ) -> float:

        raise NotImplementedError(
            "MoneyControl latest_price() will be implemented later."
        )

    # -------------------------------------------------------------------------

    def metadata(
        self,
        symbol: str,
    ) -> dict:

        return {

            "symbol": symbol,

            "source": "MoneyControl"

        }

    # -------------------------------------------------------------------------

    def historical_data(
        self,
        symbol: str,
    ):

        raise NotImplementedError(
            "MoneyControl historical_data() will be implemented later."
        )

    # -------------------------------------------------------------------------

    def validate(
        self,
        symbol: str,
    ) -> bool:

        return True