from config.database_config import (
    SQLITE_CONFIG,
    SUPABASE_CONFIG,
    BACKUP_CONFIG,
    DATABASE_CONFIG,
)

print("=" * 60)
print("Database Configuration Test")
print("=" * 60)

print("Default Database :", DATABASE_CONFIG.DEFAULT_DATABASE)
print("SQLite Database  :", SQLITE_CONFIG.DATABASE_NAME)
print("Timeout          :", SQLITE_CONFIG.CONNECTION_TIMEOUT)
print("Supabase Enabled :", SUPABASE_CONFIG.ENABLED)
print("Backup Enabled   :", BACKUP_CONFIG.ENABLE_AUTO_BACKUP)

print("\nSUCCESS: Database configuration loaded.")