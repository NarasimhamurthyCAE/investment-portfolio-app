# =============================================================================
# File Name : api/yahoo_client.py
# Project   : Investment Portfolio App V2
#
# =============================================================================

from __future__ import annotations

import yfinance as yf


class YahooClient:
    """
    Yahoo Finance Client
    """

    def latest_price(
        self,
        symbol: str,
    ) -> float:

        ticker = yf.Ticker(symbol)

        history = ticker.history(period="5d")

        if history.empty:

            raise ValueError(f"No price data found for {symbol}")

        return float(history["Close"].iloc[-1])

    def historical_data(
        self,
        symbol: str,
        period: str = "1y",
    ):

        ticker = yf.Ticker(symbol)

        return ticker.history(period=period)

    def metadata(
        self,
        symbol: str,
    ) -> dict:

        info = yf.Ticker(symbol).info

        return {
            "symbol": symbol,
            "name": info.get("longName", symbol),
            "exchange": info.get("exchange", ""),
            "currency": info.get("currency", ""),
            "sector": info.get("sector", ""),
            "industry": info.get("industry", ""),
        }

    def validate(
        self,
        symbol: str,
    ) -> bool:

        try:

            history = yf.Ticker(symbol).history(period="1d")

            return not history.empty

        except Exception:

            return False