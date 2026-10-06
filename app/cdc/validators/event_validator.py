ALLOWED_OPERATIONS = {"c", "u", "d", "r"}

ALLOWED_TABLES = {
    "accounts",
    "ledger_transactions",
}


def validate_event(event):
    """
    Validate a Debezium CDC event.

    Returns:
        (True, None) for a valid event
        (False, reason) for an invalid event
    """

    if not isinstance(event, dict):
        return False, "Event must be a JSON object"

    payload = event.get("payload")

    if payload is None:
        return False, "Missing payload"

    source = payload.get("source")

    if not isinstance(source, dict):
        return False, "Missing source information"

    table = source.get("table")

    if table not in ALLOWED_TABLES:
        return False, f"Unsupported table: {table}"

    operation = payload.get("op")

    if operation not in ALLOWED_OPERATIONS:
        return False, f"Unsupported operation: {operation}"

    if operation in {"c", "u", "r"} and payload.get("after") is None:
        return False, "Missing after data"

    if operation == "d" and payload.get("before") is None:
        return False, "Missing before data"

    return True, None