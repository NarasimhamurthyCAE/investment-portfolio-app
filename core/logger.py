# =============================================================================
# File Name : core/logger.py
# Project   : Investment Portfolio App V2
# =============================================================================

from __future__ import annotations

import logging

from pathlib import Path

from config.app_config import LOGS_FOLDER


LOGS_FOLDER.mkdir(

    parents=True,

    exist_ok=True

)

LOG_FILE = LOGS_FOLDER / "application.log"


logging.basicConfig(

    level=logging.INFO,

    format=(

        "%(asctime)s | "

        "%(levelname)s | "

        "%(name)s | "

        "%(message)s"

    ),

    handlers=[

        logging.FileHandler(LOG_FILE),

        logging.StreamHandler()

    ]

)


def get_logger(name: str) -> logging.Logger:

    """
    Returns configured logger.

    Example
    -------

    logger = get_logger(__name__)

    """

    return logging.getLogger(name)