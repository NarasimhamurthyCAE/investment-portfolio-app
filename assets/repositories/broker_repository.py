# =============================================================================
# File Name : assets/repositories/broker_repository.py
# =============================================================================

from __future__ import annotations

import pandas as pd

from repositories.base_repository import BaseRepository


class BrokerRepository(BaseRepository):

    TABLE_NAME = "brokers"

    # -------------------------------------------------------------------------
    # Active Brokers
    # -------------------------------------------------------------------------

    def active(self) -> pd.DataFrame:

        query = """
        SELECT

            broker_id,

            broker_name

        FROM brokers

        WHERE is_active = TRUE

        ORDER BY broker_name
        """

        return self.fetch_dataframe(query)

    # -------------------------------------------------------------------------
    # Broker Names
    # -------------------------------------------------------------------------

    def names(self) -> list[str]:

        df = self.active()

        if df.empty:

            return []

        return df["broker_name"].tolist()