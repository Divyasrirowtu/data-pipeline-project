import json
import urllib.request


CONNECT_URL = "http://connect:8083"


def get_connectors():
    with urllib.request.urlopen(
        f"{CONNECT_URL}/connectors",
        timeout=10
    ) as response:
        return json.loads(response.read().decode())


def get_connector_status():
    with urllib.request.urlopen(
        f"{CONNECT_URL}/connectors/ledger-postgres-connector/status",
        timeout=10
    ) as response:
        return json.loads(response.read().decode())


def test_debezium_connector_exists():
    connectors = get_connectors()

    assert "ledger-postgres-connector" in connectors


def test_debezium_connector_running():
    status = get_connector_status()

    assert status["connector"]["state"] == "RUNNING"
    assert status["tasks"][0]["state"] == "RUNNING"