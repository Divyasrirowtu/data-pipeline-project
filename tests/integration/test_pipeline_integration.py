from app.cdc.processors.event_processor import CDCEventProcessor
from app.business.processor import TransactionBusinessProcessor


def create_accounts():
    return {
        1: {
            "account_id": 1,
            "account_number": "ACC100001",
            "balance": 1000.00,
            "currency": "USD",
            "status": "ACTIVE"
        },
        2: {
            "account_id": 2,
            "account_number": "ACC100002",
            "balance": 500.00,
            "currency": "USD",
            "status": "ACTIVE"
        }
    }


def test_cdc_to_business_pipeline():
    cdc_processor = CDCEventProcessor()
    business_processor = TransactionBusinessProcessor()

    cdc_event = {
        "payload": {
            "before": None,
            "after": {
                "transaction_id": 1,
                "from_account_id": 1,
                "to_account_id": 2,
                "amount": 100.00,
                "currency": "USD"
            },
            "source": {
                "table": "ledger_transactions"
            },
            "op": "c"
        }
    }

    cdc_result = cdc_processor.process(cdc_event)

    assert cdc_result["valid"] is True

    transaction = cdc_result["event"]["payload"]["after"]

    business_result = business_processor.process(
        transaction,
        create_accounts()
    )

    assert business_result["valid"] is True
    assert business_result["reason"] is None


def test_invalid_cdc_event_does_not_pass():
    cdc_processor = CDCEventProcessor()

    invalid_event = {
        "payload": {
            "after": {
                "transaction_id": 1
            },
            "source": {
                "table": "unknown_table"
            },
            "op": "c"
        }
    }

    result = cdc_processor.process(invalid_event)

    assert result["valid"] is False


def test_invalid_business_transaction_does_not_pass():
    business_processor = TransactionBusinessProcessor()

    transaction = {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 5000.00,
        "currency": "USD"
    }

    result = business_processor.process(
        transaction,
        create_accounts()
    )

    assert result["valid"] is False
    assert "Insufficient" in result["reason"]


def test_delete_cdc_event():
    cdc_processor = CDCEventProcessor()

    delete_event = {
        "payload": {
            "before": {
                "transaction_id": 1
            },
            "after": None,
            "source": {
                "table": "ledger_transactions"
            },
            "op": "d"
        }
    }

    result = cdc_processor.process(delete_event)

    assert result["valid"] is True