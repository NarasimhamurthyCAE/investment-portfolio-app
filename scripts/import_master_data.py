# =============================================================================
# File Name : scripts/import_master_data.py
# Project    : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Import Master Data
#
# Developer Utility
#
# This script imports all master data into assets_master.
#
# =============================================================================

from __future__ import annotations


class MasterDataImporter:

    def import_stocks(self):

        print("Import Stocks...")

    def import_etfs(self):

        print("Import ETFs...")

    def import_mutual_funds(self):

        print("Import Mutual Funds...")

    def import_indices(self):

        print("Import Indices...")

    def import_gold(self):

        print("Import Gold...")

    def import_bonds(self):

        print("Import Bonds...")

    def import_all(self):

        self.import_stocks()

        self.import_etfs()

        self.import_mutual_funds()

        self.import_indices()

        self.import_gold()

        self.import_bonds()


if __name__ == "__main__":

    MasterDataImporter().import_all()