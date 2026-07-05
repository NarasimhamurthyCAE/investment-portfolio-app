# =============================================================================
# File Name : utilities/import_sample_stocks.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Import Sample Stocks
# =============================================================================

from __future__ import annotations

import pandas as pd

from controllers.stock_master_controller import StockMasterController


CSV_FILE = "data/sample/stocks_master_sample.csv"


def main():

    print("=" * 70)
    print("Import Sample Stocks")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Read CSV
    # -------------------------------------------------------------------------

    try:

        dataframe = pd.read_csv(
            CSV_FILE,
            encoding="utf-8-sig",
        )

    except UnicodeDecodeError:

        dataframe = pd.read_csv(
            CSV_FILE,
            encoding="cp1252",
        )

    # -------------------------------------------------------------------------
    # Import
    # -------------------------------------------------------------------------

    controller = StockMasterController()

    controller.import_master(
        dataframe
    )

    print()

    print("Import Completed Successfully.")

    print("=" * 70)


if __name__ == "__main__":

    main()