import os
import psycopg2


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "pipeline_db"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    )


def test_accounts_table_structure():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'accounts'
            ORDER BY ordinal_position;
        """)

        columns = [row[0] for row in cursor.fetchall()]

        assert "account_id" in columns
        assert "account_number" in columns
        assert "balance" in columns
        assert "currency" in columns
        assert "status" in columns

    finally:
        connection.close()


def test_transactions_table_structure():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'ledger_transactions'
            ORDER BY ordinal_position;
        """)

        columns = [row[0] for row in cursor.fetchall()]

        assert "transaction_id" in columns
        assert "from_account_id" in columns
        assert "to_account_id" in columns
        assert "amount" in columns
        assert "currency" in columns
        assert "status" in columns

    finally:
        connection.close()