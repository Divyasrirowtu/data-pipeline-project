from app.business.transaction_validator import validate_transaction


class TransactionBusinessProcessor:

    def process(self, transaction, accounts):
        valid, reason = validate_transaction(
            transaction,
            accounts
        )

        if not valid:
            return {
                "valid": False,
                "transaction": transaction,
                "reason": reason
            }

        return {
            "valid": True,
            "transaction": transaction,
            "reason": None
        }