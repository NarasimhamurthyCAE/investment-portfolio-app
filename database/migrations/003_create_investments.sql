-- =============================================================================
-- Migration : 003_create_investments.sql
-- Project   : Investment Portfolio App V2
--
-- Description
-- -----------------------------------------------------------------------------
-- Portfolio Holdings
--
-- One row = One asset owned by one user.
--
-- Transaction details are stored separately.
--
-- =============================================================================

CREATE TABLE IF NOT EXISTS investments
(
    investment_id      BIGSERIAL PRIMARY KEY,

    user_id            BIGINT NOT NULL,

    asset_id           BIGINT NOT NULL,

    broker             VARCHAR(100),

    account_name       VARCHAR(100),

    portfolio_name     VARCHAR(100) DEFAULT 'Default',

    notes              TEXT,

    is_active          BOOLEAN DEFAULT TRUE,

    created_at         TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at         TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_investment_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_investment_asset
        FOREIGN KEY (asset_id)
        REFERENCES assets(asset_id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_user_asset
        UNIQUE(user_id, asset_id, portfolio_name)
);

-- -----------------------------------------------------------------------------
-- Indexes
-- -----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_investments_user
ON investments(user_id);

CREATE INDEX IF NOT EXISTS idx_investments_asset
ON investments(asset_id);

CREATE INDEX IF NOT EXISTS idx_investments_portfolio
ON investments(portfolio_name);

CREATE INDEX IF NOT EXISTS idx_investments_active
ON investments(is_active);