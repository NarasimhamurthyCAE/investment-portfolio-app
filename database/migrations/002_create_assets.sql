-- =============================================================================
-- Migration : 002_create_assets.sql
-- Project   : Investment Portfolio App V2
--
-- Description
-- -----------------------------------------------------------------------------
-- Master Asset Table
--
-- One row per asset.
--
-- Supports:
--   ✓ Mutual Funds
--   ✓ ETFs
--   ✓ Stocks
--   ✓ Gold ETFs
--   ✓ Silver ETFs
--   ✓ Bonds
--   ✓ REITs
--   ✓ InvITs
--   ✓ International ETFs
--   ✓ Future asset classes
--
-- =============================================================================

CREATE TABLE IF NOT EXISTS assets
(
    asset_id            BIGSERIAL PRIMARY KEY,

    asset_type          VARCHAR(30) NOT NULL,

    asset_name          VARCHAR(300) NOT NULL,

    symbol              VARCHAR(50),

    isin                VARCHAR(30),

    scheme_code         VARCHAR(50),

    amc                 VARCHAR(200),

    category            VARCHAR(100),

    subcategory         VARCHAR(100),

    exchange            VARCHAR(50),

    country             VARCHAR(50) DEFAULT 'India',

    currency            VARCHAR(10) DEFAULT 'INR',

    sector              VARCHAR(100),

    industry            VARCHAR(100),

    expense_ratio       NUMERIC(8,4),

    launch_date         DATE,

    is_active           BOOLEAN DEFAULT TRUE,

    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at          TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT uq_asset UNIQUE
    (
        asset_type,
        asset_name,
        symbol,
        scheme_code
    )
);

-- -------------------------------------------------------------------------
-- Indexes
-- -------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_assets_type
ON assets(asset_type);

CREATE INDEX IF NOT EXISTS idx_assets_symbol
ON assets(symbol);

CREATE INDEX IF NOT EXISTS idx_assets_name
ON assets(asset_name);

CREATE INDEX IF NOT EXISTS idx_assets_scheme
ON assets(scheme_code);

CREATE INDEX IF NOT EXISTS idx_assets_isin
ON assets(isin);