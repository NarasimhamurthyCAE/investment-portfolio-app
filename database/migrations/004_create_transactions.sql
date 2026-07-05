-- =============================================================================
-- Migration : 004_create_transactions.sql
-- Project   : Investment Portfolio App V2
--
-- Description
-- -----------------------------------------------------------------------------
-- Investment Transactions
--
-- One row = One financial transaction.
--
-- =============================================================================

CREATE TABLE IF NOT EXISTS transactions
(
    transaction_id      BIGSERIAL PRIMARY KEY,

    investment_id       BIGINT NOT NULL,

    transaction_type    VARCHAR(20) NOT NULL,

    transaction_date    DATE NOT NULL,

    units               NUMERIC(20,8) NOT NULL,

    price               NUMERIC(20,8) NOT NULL,

    amount              NUMERIC(20,2) NOT NULL,

    charges             NUMERIC(20,2) DEFAULT 0,

    taxes               NUMERIC(20,2) DEFAULT 0,

    currency            VARCHAR(10) DEFAULT 'INR',

    reference_number    VARCHAR(100),

    remarks             TEXT,

    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),

    updated_at          TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_transaction_investment
        FOREIGN KEY (investment_id)
        REFERENCES investments(investment_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_transaction_type
        CHECK (
            transaction_type IN
            (
                'BUY',
                'SELL',
                'SIP',
                'SWP',
                'STP',
                'DIVIDEND',
                'BONUS',
                'SPLIT'
            )
        )
);

-- -----------------------------------------------------------------------------
-- Indexes
-- -----------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_transactions_investment
ON transactions(investment_id);

CREATE INDEX IF NOT EXISTS idx_transactions_date
ON transactions(transaction_date);

CREATE INDEX IF NOT EXISTS idx_transactions_type
ON transactions(transaction_type);