# =============================================================================
# File Name : data/network/http_client.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Enterprise HTTP Client
#
# Responsibilities
# ----------------
# ✓ GET requests
# ✓ POST requests
# ✓ Session reuse
# ✓ Timeout handling
# ✓ Retry support (future)
# ✓ Rate limiter support (future)
# ✓ Logging
# ✓ JSON parsing
#
# Every provider must use this client.
#
# =============================================================================

from __future__ import annotations

from typing import Any
from typing import Optional

import requests

from core.logger import get_logger


LOGGER = get_logger(__name__)


class HTTPClient:

    """
    Enterprise HTTP Client
    """

    DEFAULT_TIMEOUT = 20

    USER_AGENT = (

        "InvestmentPortfolioApp/2.0"

    )

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(

        self,

        timeout: int | None = None

    ) -> None:

        self.timeout = (

            timeout

            or

            self.DEFAULT_TIMEOUT

        )

        self.session = requests.Session()

        self.session.headers.update(

            {

                "User-Agent": self.USER_AGENT,

                "Accept": "application/json",

                "Connection": "keep-alive"

            }

        )

    # -------------------------------------------------------------------------
    # GET
    # -------------------------------------------------------------------------

    def get(

        self,

        url: str,

        params: Optional[dict] = None,

        headers: Optional[dict] = None

    ) -> requests.Response:

        LOGGER.info(

            "GET %s",

            url

        )

        response = self.session.get(

            url,

            params=params,

            headers=headers,

            timeout=self.timeout

        )

        response.raise_for_status()

        return response

    # -------------------------------------------------------------------------
    # POST
    # -------------------------------------------------------------------------

    def post(

        self,

        url: str,

        data: Any = None,

        json: Any = None,

        headers: Optional[dict] = None

    ) -> requests.Response:

        LOGGER.info(

            "POST %s",

            url

        )

        response = self.session.post(

            url,

            data=data,

            json=json,

            headers=headers,

            timeout=self.timeout

        )

        response.raise_for_status()

        return response

    # -------------------------------------------------------------------------
    # JSON GET
    # -------------------------------------------------------------------------

    def get_json(

        self,

        url: str,

        params: Optional[dict] = None

    ) -> dict:

        response = self.get(

            url,

            params=params

        )

        return response.json()

    # -------------------------------------------------------------------------
    # TEXT GET
    # -------------------------------------------------------------------------

    def get_text(

        self,

        url: str

    ) -> str:

        response = self.get(url)

        return response.text

    # -------------------------------------------------------------------------
    # Download File
    # -------------------------------------------------------------------------

    def download(

        self,

        url: str,

        destination

    ) -> None:

        response = self.get(

            url

        )

        with open(

            destination,

            "wb"

        ) as file:

            file.write(

                response.content

            )

    # -------------------------------------------------------------------------
    # HEAD
    # -------------------------------------------------------------------------

    def head(

        self,

        url: str

    ):

        response = self.session.head(

            url,

            timeout=self.timeout

        )

        response.raise_for_status()

        return response

    # -------------------------------------------------------------------------
    # Health
    # -------------------------------------------------------------------------

    def ping(

        self,

        url: str

    ) -> bool:

        try:

            self.head(url)

            return True

        except Exception:

            return False

    # -------------------------------------------------------------------------
    # Close
    # -------------------------------------------------------------------------

    def close(self):

        self.session.close()