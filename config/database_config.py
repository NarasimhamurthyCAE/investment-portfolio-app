"""
===============================================================================
File Name   : database_config.py
Module      : Configuration
Project     : Investment Portfolio App V2
Author      : Narasimhamurthy Shivanna
Architecture: Version 2.0

Description
-----------
Database configuration for the application.

This file only stores database settings.

Do NOT write database logic here.
===============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class SQLiteConfig:
    """
    SQLite configuration.

    SQLite is used for:
        - Local development
        - Local cache
        - Offline mode
        - Backup database
    """

    DATABASE_NAME: str = "portfolio.db"

    DATABASE_FOLDER: Path = Path("database")

    CONNECTION_TIMEOUT: int = 30

    ENABLE_FOREIGN_KEYS: bool = True

    ENABLE_WAL_MODE: bool = True

    AUTO_VACUUM: bool = True


@dataclass(slots=True, frozen=True)
class SupabaseConfig:
    """
    Supabase PostgreSQL configuration.

    Credentials are stored inside:

        .streamlit/secrets.toml

    Never store passwords here.
    """

    ENABLED: bool = True

    CONNECTION_TIMEOUT: int = 30

    MAX_RETRIES: int = 3

    RETRY_DELAY_SECONDS: int = 5

    CONNECTION_POOL_SIZE: int = 10


@dataclass(slots=True, frozen=True)
class BackupConfig:
    """
    Database backup configuration.
    """

    ENABLE_AUTO_BACKUP: bool = True

    BACKUP_FOLDER: Path = Path("data/backup")

    KEEP_LAST_BACKUPS: int = 30

    COMPRESS_BACKUPS: bool = True


@dataclass(slots=True, frozen=True)
class DatabaseConfig:
    """
    Main database configuration.
    """

    DEFAULT_DATABASE: str = "Supabase"

    ENABLE_SQLITE_FALLBACK: bool = True

    ENABLE_QUERY_LOGGING: bool = False

    ENABLE_PERFORMANCE_LOGGING: bool = False


# =============================================================================
# Singleton Objects
# =============================================================================

SQLITE_CONFIG = SQLiteConfig()

SUPABASE_CONFIG = SupabaseConfig()

BACKUP_CONFIG = BackupConfig()

DATABASE_CONFIG = DatabaseConfig()