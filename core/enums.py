from __future__ import annotations

from enum import Enum


class TransactionType(str, Enum):

    BUY = "BUY"

    SELL = "SELL"

    SIP = "SIP"

    SWP = "SWP"

    STP = "STP"

    SWITCH = "SWITCH"

    DIVIDEND = "DIVIDEND"

    BONUS = "BONUS"

    SPLIT = "SPLIT"

    TRANSFER = "TRANSFER"


class AssetType(str, Enum):

    MUTUAL_FUND = "Mutual Fund"

    ETF = "ETF"

    STOCK = "Stock"

    GOLD = "Gold"

    SILVER = "Silver"

    BOND = "Bond"

    REIT = "REIT"

    CASH = "Cash"

    CRYPTO = "Crypto"


class RiskProfile(str, Enum):

    LOW = "Low"

    MODERATE = "Moderate"

    HIGH = "High"


class Market(str, Enum):

    INDIA = "India"

    USA = "USA"

    GLOBAL = "Global"


class Benchmark(str, Enum):

    NIFTY50 = "NIFTY 50 TRI"

    NIFTY500 = "NIFTY 500 TRI"

    MIDCAP150 = "NIFTY Midcap 150 TRI"

    SMALLCAP250 = "NIFTY Smallcap 250 TRI"

    NASDAQ100 = "NASDAQ 100"

    GOLD = "Gold"

    SILVER = "Silver"