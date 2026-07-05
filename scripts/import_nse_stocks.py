# =============================================================================
# File Name : scripts/import_nse_stocks.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Import NSE Stocks into stocks_master
#
# =============================================================================

from __future__ import annotations

import pandas as pd

from assets.services.stock_master_service import StockMasterService


class NSEStockImporter:

    def __init__(self):

        self.service = StockMasterService()

    # -------------------------------------------------------------------------
    # Import CSV
    # -------------------------------------------------------------------------

    def import_csv(
        self,
        csv_file: str,
    ):

        df = pd.read_csv(csv_file)

        print(f"\nLoaded {len(df)} records.")

        # -------------------------------------------------------------
        # Rename CSV columns to database columns
        # -------------------------------------------------------------

        column_map = {

            "SYMBOL": "symbol",

            "NAME OF COMPANY": "company_name",

            "ISIN NUMBER": "isin",

        }

        df = df.rename(columns=column_map)

        # -------------------------------------------------------------
        # Add default columns
        # -------------------------------------------------------------

        df["exchange"] = "NSE"

        df["currency"] = "INR"

        df["listing_status"] = "ACTIVE"

        df["yahoo_symbol"] = df["symbol"] + ".NS"

        # -------------------------------------------------------------
        # Keep only required columns
        # -------------------------------------------------------------

        df = df[

            [

                "symbol",

                "yahoo_symbol",

                "company_name",

                "isin",

                "exchange",

                "currency",

                "listing_status",

            ]

        ]

        print(df.head())

        self.service.bulk_import(df)

        print("\nImport Completed Successfully.")


if __name__ == "__main__":

    importer = NSEStockImporter()

    importer.import_csv(

        "master_data/stocks/nse_stocks.csv"

    )