from decimal import Decimal


def validate_transaction(transaction, accounts):
    """
    Validate a ledger transaction against business rules.

    transaction:
        Dictionary containing transaction details.

    accounts:
        Dictionary containing account information.
    """

    if not isinstance(transaction, dict):
        return False, "Transaction must be a JSON object"

    required_fields = [
        "from_account_id",
        "to_account_id",
        "amount",
        "currency",
    ]

    for field in required_fields:
        if field not in transaction:
            return False, f"Missing required field: {field}"

    from_account_id = transaction["from_account_id"]
    to_account_id = transaction["to_account_id"]

    # Rule 1: Source and destination must be different
    if from_account_id == to_account_id:
        return False, "Source and destination accounts must be different"

    # Rule 2: Amount must be positive
    try:
        amount = Decimal(str(transaction["amount"]))
    except Exception:
        return False, "Invalid transaction amount"

    if amount <= 0:
        return False, "Transaction amount must be greater than zero"

    # Rule 3: Source account must exist
    if from_account_id not in accounts:
        return False, "Source account does not exist"

    # Rule 4: Destination account must exist
    if to_account_id not in accounts:
        return False, "Destination account does not exist"

    source_account = accounts[from_account_id]
    destination_account = accounts[to_account_id]

    # Rule 5: Both accounts must be active
    if source_account.get("status") != "ACTIVE":
        return False, "Source account is not active"

    if destination_account.get("status") != "ACTIVE":
        return False, "Destination account is not active"

    # Rule 6: Currency must match
    transaction_currency = transaction["currency"]

    if source_account.get("currency") != transaction_currency:
        return False, "Transaction currency does not match source account"

    if destination_account.get("currency") != transaction_currency:
        return False, "Transaction currency does not match destination account"

    # Rule 7: Source account must have sufficient balance
    source_balance = Decimal(str(source_account.get("balance", 0)))

    if source_balance < amount:
        return False, "Insufficient account balance"

    return True, None