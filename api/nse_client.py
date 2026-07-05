# =============================================================================
# File Name : api/nse_client.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# NSE Client
#
# =============================================================================

from __future__ import annotations

import requests


class NSEClient:
    """
    Simple NSE client.
    """

    BASE_URL = "https://www.nseindia.com"

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/137.0 Safari/537.36"
                )
            }
        )

    # ---------------------------------------------------------------------

    def latest_price(
        self,
        symbol: str,
    ) -> float:

        raise NotImplementedError(
            "NSE latest_price() will be implemented later."
        )

    # ---------------------------------------------------------------------

    def metadata(
        self,
        symbol: str,
    ) -> dict:

        return {

            "symbol": symbol,

            "exchange": "NSE"

        }

    # ---------------------------------------------------------------------

    def historical_data(
        self,
        symbol: str,
    ):

        raise NotImplementedError(
            "NSE historical_data() will be implemented later."
        )

    # ---------------------------------------------------------------------

    def validate(
        self,
        symbol: str,
    ) -> bool:

        return True