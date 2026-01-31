import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_user_id():
    """Provide a sample user ID for testing."""
    return "test_user_123"