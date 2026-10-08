from app.business.processor import TransactionBusinessProcessor


def create_accounts():
    return {
        1: {
            "account_id": 1,
            "balance": 1000.00,
            "currency": "USD",
            "status": "ACTIVE"
        },
        2: {
            "account_id": 2,
            "balance": 500.00,
            "currency": "USD",
            "status": "ACTIVE"
        }
    }


def test_valid_transaction():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 100.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is True
    assert result["reason"] is None


def test_same_account_transaction():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 1,
        "amount": 100.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "different" in result["reason"]


def test_negative_amount():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": -100.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "greater than zero" in result["reason"]


def test_missing_source_account():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 99,
        "to_account_id": 2,
        "amount": 100.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "does not exist" in result["reason"]


def test_inactive_account():
    processor = TransactionBusinessProcessor()

    accounts = create_accounts()
    accounts[1]["status"] = "BLOCKED"

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 100.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        accounts
    )

    assert result["valid"] is False
    assert "not active" in result["reason"]


def test_insufficient_balance():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 5000.00,
        "currency": "USD"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "Insufficient" in result["reason"]


def test_currency_mismatch():
    processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 100.00,
        "currency": "EUR"
    }

    result = processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "currency" in result["reason"]