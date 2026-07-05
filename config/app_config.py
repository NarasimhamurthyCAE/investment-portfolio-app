"""
===============================================================================
File Name   : app_config.py
Module      : Configuration
Project     : Investment Portfolio App V2
Author      : Narasimhamurthy Shivanna
Architecture: Version 2.0

Description
-----------
This module contains the global application configuration.

It is the single source of truth for application-wide settings.

Do NOT place:
    - Database configuration
    - API Keys
    - Business Logic
    - Streamlit Code

inside this file.

Copyright (c) 2026
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final


# =============================================================================
# Project Paths
# =============================================================================

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

DATA_FOLDER: Final[Path] = PROJECT_ROOT / "data"
CACHE_FOLDER: Final[Path] = PROJECT_ROOT / "cache"
ASSETS_FOLDER: Final[Path] = PROJECT_ROOT / "assets"
REPORTS_FOLDER: Final[Path] = PROJECT_ROOT / "reports"
LOGS_FOLDER: Final[Path] = PROJECT_ROOT / "logs"


# =============================================================================
# Application Configuration
# =============================================================================

@dataclass(slots=True, frozen=True)
class AppConfig:
    """
    Global application configuration.

    This class should only contain application-level settings.
    """

    # -------------------------------------------------------------------------
    # Application Information
    # -------------------------------------------------------------------------

    APP_NAME: str = "Investment Portfolio App"

    APP_VERSION: str = "2.0.0"

    APP_AUTHOR: str = "Narasimhamurthy Shivanna"

    APP_DESCRIPTION: str = (
        "Personal Investment Decision System "
        "for Mutual Funds, ETFs and Stocks."
    )

    # -------------------------------------------------------------------------
    # Localization
    # -------------------------------------------------------------------------

    DEFAULT_LANGUAGE: str = "en"

    DEFAULT_CURRENCY: str = "INR"

    COUNTRY: str = "India"

    TIMEZONE: str = "Asia/Kolkata"

    DATE_FORMAT: str = "%d-%m-%Y"

    # -------------------------------------------------------------------------
    # Portfolio
    # -------------------------------------------------------------------------

    DEFAULT_BENCHMARK: str = "NIFTY 500 TRI"

    DEFAULT_RISK_PROFILE: str = "Moderate"

    DEFAULT_MARKET: str = "India"

    # -------------------------------------------------------------------------
    # Display
    # -------------------------------------------------------------------------

    DECIMAL_PLACES: int = 2

    PERCENTAGE_DECIMALS: int = 2

    ENABLE_DARK_THEME: bool = False

    SHOW_DEBUG_INFORMATION: bool = False

    # -------------------------------------------------------------------------
    # Supported Asset Types
    # -------------------------------------------------------------------------

    SUPPORTED_ASSET_TYPES: tuple[str, ...] = (
        "Mutual Fund",
        "ETF",
        "Stock",
        "Gold",
        "Silver",
        "Bond",
        "REIT",
        "Commodity",
        "Cash",
    )

    # -------------------------------------------------------------------------
    # Feature Flags
    # -------------------------------------------------------------------------

    ENABLE_MUTUAL_FUNDS: bool = True

    ENABLE_ETFS: bool = True

    ENABLE_STOCKS: bool = True

    ENABLE_ANALYTICS: bool = True

    ENABLE_ADVISOR: bool = True

    ENABLE_STRATEGY_LAB: bool = False

    ENABLE_AI: bool = False

    # -------------------------------------------------------------------------
    # Project Folders
    # -------------------------------------------------------------------------

    DATA_DIRECTORY: Path = field(default=DATA_FOLDER)

    CACHE_DIRECTORY: Path = field(default=CACHE_FOLDER)

    REPORT_DIRECTORY: Path = field(default=REPORTS_FOLDER)

    LOG_DIRECTORY: Path = field(default=LOGS_FOLDER)

    ASSET_DIRECTORY: Path = field(default=ASSETS_FOLDER)


# =============================================================================
# Singleton Configuration Object
# =============================================================================

APP_CONFIG = AppConfig()