from app.cdc.processors.event_processor import CDCEventProcessor


def test_valid_create_event():
    processor = CDCEventProcessor()

    event = {
        "payload": {
            "before": None,
            "after": {
                "account_id": 1,
                "account_number": "ACC100001"
            },
            "source": {
                "table": "accounts"
            },
            "op": "c"
        }
    }

    result = processor.process(event)

    assert result["valid"] is True
    assert result["reason"] is None


def test_invalid_json():
    processor = CDCEventProcessor()

    result = processor.process(
        '{"invalid-json":'
    )

    assert result["valid"] is False
    assert "Invalid JSON" in result["reason"]


def test_unsupported_table():
    processor = CDCEventProcessor()

    event = {
        "payload": {
            "after": {
                "id": 1
            },
            "source": {
                "table": "unknown_table"
            },
            "op": "c"
        }
    }

    result = processor.process(event)

    assert result["valid"] is False
    assert "Unsupported table" in result["reason"]


def test_delete_event():
    processor = CDCEventProcessor()

    event = {
        "payload": {
            "before": {
                "account_id": 1
            },
            "after": None,
            "source": {
                "table": "accounts"
            },
            "op": "d"
        }
    }

    result = processor.process(event)

    assert result["valid"] is True