# =============================================================================
# File Name : repositories/base_repository.py
# Project   : Investment Portfolio App V2
# Module    : Repository Layer
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Base Repository
#
# Parent class for every repository in the application.
#
# Responsibilities
# ----------------
# ✓ Generic CRUD operations
# ✓ Database abstraction
# ✓ Transaction safety
# ✓ DataFrame loading
# ✓ Exists checks
# ✓ Count
# ✓ Delete
# ✓ Update
#
# NOTE
# ----
# Do NOT write business logic here.
#
# Business rules belong inside the Service layer.
#
# =============================================================================

from __future__ import annotations

from typing import Any

import pandas as pd

from database.manager import DatabaseManager


class BaseRepository:
    """
    Generic Repository

    Every repository should inherit this class.

    Example
    -------

    class InvestmentRepository(BaseRepository):

        TABLE_NAME = "investments"

    """

    TABLE_NAME: str = ""

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        if not self.TABLE_NAME:
            raise ValueError(
                "TABLE_NAME cannot be empty."
            )

    # -------------------------------------------------------------------------
    # Execute
    # -------------------------------------------------------------------------

    def execute(
        self,
        query: str,
        params: tuple | None = None
    ) -> None:

        DatabaseManager.execute(
            query=query,
            params=params
        )

    # -------------------------------------------------------------------------
    # Execute Many
    # -------------------------------------------------------------------------

    def execute_many(
        self,
        query: str,
        values: list
    ) -> None:

        DatabaseManager.execute_many(
            query=query,
            values=values
        )

    # -------------------------------------------------------------------------
    # Fetch One
    # -------------------------------------------------------------------------

    def fetch_one(
        self,
        query: str,
        params: tuple | None = None
    ) -> Any:

        return DatabaseManager.fetch_one(
            query=query,
            params=params
        )

    # -------------------------------------------------------------------------
    # Fetch All
    # -------------------------------------------------------------------------

    def fetch_all(
        self,
        query: str,
        params: tuple | None = None
    ) -> list:

        return DatabaseManager.fetch_all(
            query=query,
            params=params
        )

    # -------------------------------------------------------------------------
    # DataFrame
    # -------------------------------------------------------------------------

    def fetch_dataframe(
        self,
        query: str,
        params: tuple | None = None
    ) -> pd.DataFrame:

        return DatabaseManager.fetch_dataframe(
            query=query,
            params=params
        )

    # -------------------------------------------------------------------------
    # Find By ID
    # -------------------------------------------------------------------------

    def find_by_id(
        self,
        row_id: int
    ):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        WHERE id=%s

        """

        return self.fetch_one(
            query,
            (row_id,)
        )

    # -------------------------------------------------------------------------
    # Find All
    # -------------------------------------------------------------------------

    def find_all(self):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        """

        return self.fetch_all(query)

    # -------------------------------------------------------------------------
    # Find All DataFrame
    # -------------------------------------------------------------------------

    def find_all_dataframe(self):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        """

        return self.fetch_dataframe(query)

    # -------------------------------------------------------------------------
    # Count
    # -------------------------------------------------------------------------

    def count(self) -> int:

        query = f"""

        SELECT COUNT(*)

        FROM {self.TABLE_NAME}

        """

        result = self.fetch_one(query)

        return int(result[0])

    # -------------------------------------------------------------------------
    # Exists
    # -------------------------------------------------------------------------

    def exists(
        self,
        row_id: int
    ) -> bool:

        query = f"""

        SELECT EXISTS(

            SELECT 1

            FROM {self.TABLE_NAME}

            WHERE id=%s

        )

        """

        result = self.fetch_one(
            query,
            (row_id,)
        )

        return bool(result[0])

    # -------------------------------------------------------------------------
    # Delete
    # -------------------------------------------------------------------------

    def delete(
        self,
        row_id: int
    ) -> None:

        query = f"""

        DELETE

        FROM {self.TABLE_NAME}

        WHERE id=%s

        """

        self.execute(
            query,
            (row_id,)
        )

    # -------------------------------------------------------------------------
    # Delete All
    # -------------------------------------------------------------------------

    def delete_all(self) -> None:

        query = f"""

        DELETE

        FROM {self.TABLE_NAME}

        """

        self.execute(query)

    # -------------------------------------------------------------------------
    # Truncate
    # -------------------------------------------------------------------------

    def truncate(self) -> None:

        query = f"""

        TRUNCATE TABLE

        {self.TABLE_NAME}

        RESTART IDENTITY

        """

        self.execute(query)

    # -------------------------------------------------------------------------
    # Max ID
    # -------------------------------------------------------------------------

    def max_id(self):

        query = f"""

        SELECT MAX(id)

        FROM {self.TABLE_NAME}

        """

        row = self.fetch_one(query)

        return row[0]

    # -------------------------------------------------------------------------
    # Min ID
    # -------------------------------------------------------------------------

    def min_id(self):

        query = f"""

        SELECT MIN(id)

        FROM {self.TABLE_NAME}

        """

        row = self.fetch_one(query)

        return row[0]

    # -------------------------------------------------------------------------
    # Last Record
    # -------------------------------------------------------------------------

    def last_record(self):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        ORDER BY id DESC

        LIMIT 1

        """

        return self.fetch_one(query)

    # -------------------------------------------------------------------------
    # First Record
    # -------------------------------------------------------------------------

    def first_record(self):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        ORDER BY id

        LIMIT 1

        """

        return self.fetch_one(query)

    # -------------------------------------------------------------------------
    # Search Text
    # -------------------------------------------------------------------------

    def search(
        self,
        column: str,
        value: str
    ):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        WHERE {column} ILIKE %s

        """

        return self.fetch_all(
            query,
            (f"%{value}%",)
        )

    # -------------------------------------------------------------------------
    # Search Exact
    # -------------------------------------------------------------------------

    def search_exact(
        self,
        column: str,
        value: Any
    ):

        query = f"""

        SELECT *

        FROM {self.TABLE_NAME}

        WHERE {column}=%s

        """

        return self.fetch_all(
            query,
            (value,)
        )

    # -------------------------------------------------------------------------
    # Fetch Column
    # -------------------------------------------------------------------------

    def fetch_column(
        self,
        column: str
    ) -> list:

        query = f"""

        SELECT {column}

        FROM {self.TABLE_NAME}

        """

        rows = self.fetch_all(query)

        return [r[0] for r in rows]

    # -------------------------------------------------------------------------
    # Distinct Values
    # -------------------------------------------------------------------------

    def distinct(
        self,
        column: str
    ) -> list:

        query = f"""

        SELECT DISTINCT {column}

        FROM {self.TABLE_NAME}

        ORDER BY {column}

        """

        rows = self.fetch_all(query)

        return [r[0] for r in rows]

    # -------------------------------------------------------------------------
    # Execute Raw SQL
    # -------------------------------------------------------------------------

    def raw(
        self,
        sql: str,
        params: tuple | None = None
    ):

        return self.fetch_all(
            sql,
            params
        )

    # -------------------------------------------------------------------------
    # Table Exists
    # -------------------------------------------------------------------------

    @staticmethod
    def table_exists(
        table_name: str
    ) -> bool:

        return DatabaseManager.table_exists(
            table_name
        )

    # -------------------------------------------------------------------------
    # Row Count
    # -------------------------------------------------------------------------

    @staticmethod
    def row_count(
        table_name: str
    ) -> int:

        return DatabaseManager.row_count(
            table_name
        )

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    @staticmethod
    def database_alive() -> bool:

        return DatabaseManager.ping()

    # -------------------------------------------------------------------------
    # Database Version
    # -------------------------------------------------------------------------

    @staticmethod
    def database_version():

        return DatabaseManager.server_version()

    # -------------------------------------------------------------------------
    # Current User
    # -------------------------------------------------------------------------

    @staticmethod
    def current_user():

        return DatabaseManager.current_user()

    # -------------------------------------------------------------------------
    # Database Name
    # -------------------------------------------------------------------------

    @staticmethod
    def database_name():

        return DatabaseManager.database_name()

    # -------------------------------------------------------------------------
    # Server Time
    # -------------------------------------------------------------------------

    @staticmethod
    def server_time():

        return DatabaseManager.server_time()