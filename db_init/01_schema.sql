-- ============================================================
-- V1 DATABASE SCHEMA
-- Ledger Data Pipeline
-- ============================================================

-- ============================================================
-- ACCOUNTS
-- ============================================================

CREATE TABLE IF NOT EXISTS accounts (
    account_id BIGSERIAL PRIMARY KEY,
    account_number VARCHAR(50) NOT NULL UNIQUE,
    account_name VARCHAR(150) NOT NULL,
    balance NUMERIC(18, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT accounts_balance_non_negative
        CHECK (balance >= 0),

    CONSTRAINT accounts_currency_valid
        CHECK (char_length(currency) = 3),

    CONSTRAINT accounts_status_valid
        CHECK (status IN ('ACTIVE', 'INACTIVE', 'BLOCKED'))
);


-- ============================================================
-- LEDGER TRANSACTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS ledger_transactions (
    transaction_id BIGSERIAL PRIMARY KEY,

    from_account_id BIGINT NOT NULL,
    to_account_id BIGINT NOT NULL,

    amount NUMERIC(18, 2) NOT NULL,

    currency VARCHAR(3) NOT NULL DEFAULT 'USD',

    transaction_type VARCHAR(30) NOT NULL DEFAULT 'TRANSFER',

    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',

    reference_id VARCHAR(100) UNIQUE,

    description TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT ledger_transactions_amount_positive
        CHECK (amount > 0),

    CONSTRAINT ledger_transactions_different_accounts
        CHECK (from_account_id <> to_account_id),

    CONSTRAINT ledger_transactions_currency_valid
        CHECK (char_length(currency) = 3),

    CONSTRAINT ledger_transactions_type_valid
        CHECK (
            transaction_type IN (
                'TRANSFER',
                'DEPOSIT',
                'WITHDRAWAL'
            )
        ),

    CONSTRAINT ledger_transactions_status_valid
        CHECK (
            status IN (
                'PENDING',
                'COMPLETED',
                'FAILED',
                'CANCELLED'
            )
        ),

    CONSTRAINT ledger_transactions_from_account_fk
        FOREIGN KEY (from_account_id)
        REFERENCES accounts(account_id),

    CONSTRAINT ledger_transactions_to_account_fk
        FOREIGN KEY (to_account_id)
        REFERENCES accounts(account_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_accounts_account_number
    ON accounts(account_number);

CREATE INDEX IF NOT EXISTS idx_accounts_status
    ON accounts(status);

CREATE INDEX IF NOT EXISTS idx_transactions_from_account
    ON ledger_transactions(from_account_id);

CREATE INDEX IF NOT EXISTS idx_transactions_to_account
    ON ledger_transactions(to_account_id);

CREATE INDEX IF NOT EXISTS idx_transactions_created_at
    ON ledger_transactions(created_at);

CREATE INDEX IF NOT EXISTS idx_transactions_status
    ON ledger_transactions(status);


-- ============================================================
-- SAMPLE DATA FOR VALIDATION
-- ============================================================

INSERT INTO accounts (
    account_number,
    account_name,
    balance,
    currency,
    status
)
VALUES
    ('ACC100001', 'Alice Account', 1000.00, 'USD', 'ACTIVE'),
    ('ACC100002', 'Bob Account', 500.00, 'USD', 'ACTIVE')
ON CONFLICT (account_number) DO NOTHING;