# =============================================================================
# File Name : database/transaction_manager.py
# Project   : Investment Portfolio App V2
#
# Description
# -----------------------------------------------------------------------------
# Database Transaction Manager
#
# Handles:
#   ✓ BEGIN
#   ✓ COMMIT
#   ✓ ROLLBACK
#
# =============================================================================

from __future__ import annotations

from contextlib import contextmanager

from database.connection import DatabaseConnection


class TransactionManager:
    """
    Transaction manager for database operations.
    """

    @staticmethod
    @contextmanager
    def transaction():

        connection = DatabaseConnection().connection

        try:

            yield connection

            connection.commit()

        except Exception:

            connection.rollback()

            raise

        finally:

            connection.close()