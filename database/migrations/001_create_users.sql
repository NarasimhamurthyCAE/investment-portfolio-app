-- =============================================================================
-- Migration : 001_create_users.sql
-- Project   : Investment Portfolio App V2
-- Description:
-- Creates the users table.
-- =============================================================================

CREATE TABLE IF NOT EXISTS users
(
    user_id          BIGSERIAL PRIMARY KEY,

    username         VARCHAR(100) NOT NULL UNIQUE,

    full_name        VARCHAR(200),

    email            VARCHAR(255) UNIQUE,

    password_hash    TEXT,

    base_currency    VARCHAR(10) DEFAULT 'INR',

    timezone         VARCHAR(50) DEFAULT 'Asia/Kolkata',

    is_active        BOOLEAN DEFAULT TRUE,

    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);