# =============================================================================
# File Name : database/manager.py
# Project   : Investment Portfolio App V2
# Module    : Database
# Author    : Narasimhamurthy Shivanna
#
# Description
# -----------------------------------------------------------------------------
# Centralized Database Manager
#
# Responsibilities
#
# ✓ Create PostgreSQL connection
# ✓ Connection Pool
# ✓ Transaction handling
# ✓ Cursor management
# ✓ Retry mechanism
# ✓ Automatic rollback
# ✓ Logging
# ✓ Context Manager
#
# NO SQL BUSINESS LOGIC HERE.
#
# Repositories should use this class.
# =============================================================================

from __future__ import annotations

import logging
import time

from contextlib import contextmanager

import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection
from psycopg2.extensions import cursor
from psycopg2.extras import RealDictCursor

import streamlit as st

from config.database_config import SUPABASE_CONFIG

LOGGER = logging.getLogger(__name__)


class DatabaseManager:
    """
    Enterprise Database Manager

    Singleton Connection Pool
    """

    _pool: SimpleConnectionPool | None = None

    _initialized = False

    # -------------------------------------------------------------------------
    # Initialize
    # -------------------------------------------------------------------------

    @classmethod
    def initialize(cls) -> None:

        if cls._initialized:
            return

        database_url = st.secrets["DATABASE_URL"]

        cls._pool = SimpleConnectionPool(

            minconn=1,

            maxconn=SUPABASE_CONFIG.CONNECTION_POOL_SIZE,

            dsn=database_url,

            sslmode="require",

            connect_timeout=SUPABASE_CONFIG.CONNECTION_TIMEOUT

        )

        cls._initialized = True

        LOGGER.info("Database connection pool initialized.")

    # -------------------------------------------------------------------------
    # Get Connection
    # -------------------------------------------------------------------------

    @classmethod
    def get_connection(cls) -> connection:

        if not cls._initialized:
            cls.initialize()

        return cls._pool.getconn()

    # -------------------------------------------------------------------------
    # Return Connection
    # -------------------------------------------------------------------------

    @classmethod
    def return_connection(
        cls,
        conn: connection
    ) -> None:

        if cls._pool is not None:

            cls._pool.putconn(conn)

    # -------------------------------------------------------------------------
    # Close Pool
    # -------------------------------------------------------------------------

    @classmethod
    def close_pool(cls) -> None:

        if cls._pool:

            cls._pool.closeall()

            LOGGER.info("Database pool closed.")

    # -------------------------------------------------------------------------
    # Cursor Context
    # -------------------------------------------------------------------------

    @classmethod
    @contextmanager
    def cursor(cls):

        conn = cls.get_connection()

        cur = conn.cursor(
            cursor_factory=RealDictCursor
        )

        try:

            yield cur

            conn.commit()

        except Exception:

            conn.rollback()

            raise

        finally:

            cur.close()

        cls.return_connection(conn)

    # -------------------------------------------------------------------------
    # Connection Context
    # -------------------------------------------------------------------------

    @classmethod
    @contextmanager
    def connection(cls):

        conn = cls.get_connection()

        try:

            yield conn

            conn.commit()

        except Exception:

            conn.rollback()

            raise

        finally:

            cls.return_connection(conn)

    # -------------------------------------------------------------------------
    # Execute Query
    # -------------------------------------------------------------------------

    @classmethod
    def execute(
        cls,
        query: str,
        params=None
    ) -> None:

        retries = SUPABASE_CONFIG.MAX_RETRIES

        for attempt in range(retries):

            try:

                with cls.cursor() as cur:

                    cur.execute(query, params)

                return

            except psycopg2.Error as exc:

                LOGGER.exception(exc)

                if attempt + 1 == retries:
                    raise

                time.sleep(
                    SUPABASE_CONFIG.RETRY_DELAY_SECONDS
                )

    # -------------------------------------------------------------------------
    # Fetch One
    # -------------------------------------------------------------------------

    @classmethod
    def fetch_one(
        cls,
        query: str,
        params=None
    ):

        retries = SUPABASE_CONFIG.MAX_RETRIES

        for attempt in range(retries):

            try:

                with cls.cursor() as cur:

                    cur.execute(query, params)

                    return cur.fetchone()

            except psycopg2.Error as exc:

                LOGGER.exception(exc)

                if attempt + 1 == retries:
                    raise

                time.sleep(
                    SUPABASE_CONFIG.RETRY_DELAY_SECONDS
                )

    # -------------------------------------------------------------------------
    # Fetch All
    # -------------------------------------------------------------------------

    @classmethod
    def fetch_all(
        cls,
        query: str,
        params=None
    ):

        retries = SUPABASE_CONFIG.MAX_RETRIES

        for attempt in range(retries):

            try:

                with cls.cursor() as cur:

                    cur.execute(query, params)

                    return cur.fetchall()

            except psycopg2.Error as exc:

                LOGGER.exception(exc)

                if attempt + 1 == retries:
                    raise

                time.sleep(
                    SUPABASE_CONFIG.RETRY_DELAY_SECONDS
                )

    # -------------------------------------------------------------------------
    # Fetch DataFrame
    # -------------------------------------------------------------------------

    @classmethod
    def fetch_dataframe(
        cls,
        query: str,
        params=None
    ):

        import pandas as pd

        with cls.connection() as conn:

            return pd.read_sql(
                query,
                conn,
                params=params
            )

    # -------------------------------------------------------------------------
    # Execute Many
    # -------------------------------------------------------------------------

    @classmethod
    def execute_many(
        cls,
        query: str,
        values: list
    ) -> None:

        with cls.cursor() as cur:

            cur.executemany(
                query,
                values
            )

    # -------------------------------------------------------------------------
    # Execute Batch
    # -------------------------------------------------------------------------

    @classmethod
    def execute_batch(
        cls,
        queries: list[tuple[str, tuple]]
    ) -> None:

        with cls.connection() as conn:

            cur = conn.cursor()

            try:

                for query, params in queries:

                    cur.execute(
                        query,
                        params
                    )

                conn.commit()

            except Exception:

                conn.rollback()

                raise

            finally:

                cur.close()

    # -------------------------------------------------------------------------
    # Health Check
    # -------------------------------------------------------------------------

    @classmethod
    def ping(cls) -> bool:

        try:

            result = cls.fetch_one(
                "SELECT 1"
            )

            return result[0] == 1

        except Exception:

            return False

    # -------------------------------------------------------------------------
    # Server Version
    # -------------------------------------------------------------------------

    @classmethod
    def server_version(cls) -> str:

        row = cls.fetch_one(
            "SELECT version();"
        )

        return row[0]

    # -------------------------------------------------------------------------
    # Current Database
    # -------------------------------------------------------------------------

    @classmethod
    def database_name(cls) -> str:

        row = cls.fetch_one(
            "SELECT current_database();"
        )

        return row[0]

    # -------------------------------------------------------------------------
    # Current User
    # -------------------------------------------------------------------------

    @classmethod
    def current_user(cls) -> str:

        row = cls.fetch_one(
            "SELECT current_user;"
        )

        return row[0]

    # -------------------------------------------------------------------------
    # PostgreSQL Time
    # -------------------------------------------------------------------------

    @classmethod
    def server_time(cls):

        row = cls.fetch_one(
            "SELECT NOW();"
        )

        return row[0]

    # -------------------------------------------------------------------------
    # Table Exists
    # -------------------------------------------------------------------------

    @classmethod
    def table_exists(
        cls,
        table_name: str
    ) -> bool:

        query = """

        SELECT EXISTS(

            SELECT 1

            FROM information_schema.tables

            WHERE table_name=%s

        )

        """

        row = cls.fetch_one(
            query,
            (table_name,)
        )

        return bool(row[0])

    # -------------------------------------------------------------------------
    # Count Rows
    # -------------------------------------------------------------------------

    @classmethod
    def row_count(
        cls,
        table_name: str
    ) -> int:

        query = f"SELECT COUNT(*) FROM {table_name}"

        row = cls.fetch_one(query)

        return int(row[0])

    # -------------------------------------------------------------------------
    # Vacuum Analyze
    # -------------------------------------------------------------------------

    @classmethod
    def vacuum(cls):

        with cls.connection() as conn:

            conn.set_session(
                autocommit=True
            )

            cur = conn.cursor()

            cur.execute("VACUUM ANALYZE;")

            cur.close()

    # -------------------------------------------------------------------------
    # Explain Query
    # -------------------------------------------------------------------------

    @classmethod
    def explain(
        cls,
        query: str
    ):

        return cls.fetch_all(
            "EXPLAIN " + query
        )

    # -------------------------------------------------------------------------
    # Shutdown
    # -------------------------------------------------------------------------

    @classmethod
    def shutdown(cls):

        cls.close_pool()