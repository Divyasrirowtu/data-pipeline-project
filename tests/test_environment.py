import os


def test_environment_variables_exist():
    assert os.getenv("POSTGRES_DB") is not None
    assert os.getenv("POSTGRES_USER") is not None
    assert os.getenv("POSTGRES_PASSWORD") is not None