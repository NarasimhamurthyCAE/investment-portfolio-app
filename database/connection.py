"""
Investment Portfolio App V2

Module:
Database Connection

Purpose
-------
Centralized PostgreSQL (Supabase) connection.
"""

from __future__ import annotations

import streamlit as st
import psycopg2
from psycopg2.extensions import connection


class DatabaseConnection:
    """
    Creates PostgreSQL connections.

    Usage
    -----
    from database.connection import DatabaseConnection

    conn = DatabaseConnection.get_connection()
    """

    @staticmethod
    def get_connection() -> connection:
        database_url = st.secrets["DATABASE_URL"]

        return psycopg2.connect(
            database_url,
            sslmode="require",
        )