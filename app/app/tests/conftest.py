import pytest

from tests import create_test_app


@pytest.fixture(scope="session")
def mock_client():
    return create_test_app().test_client()
