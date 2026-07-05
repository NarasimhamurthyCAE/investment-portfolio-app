# =============================================================================
# File Name : utilities/download_stock_master.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Downloads latest stock master files.
#
# =============================================================================

from __future__ import annotations

from pathlib import Path


RAW_FOLDER = Path("data/raw")


def main():

    RAW_FOLDER.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("=" * 70)
    print("Download Stock Master")
    print("=" * 70)

    print("Downloader will be implemented in next step.")


if __name__ == "__main__":

    main()