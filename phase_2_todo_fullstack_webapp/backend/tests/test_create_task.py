import pytest
from fastapi.testclient import TestClient
from main import app
from models import Task
import jwt
from settings import settings

@pytest.fixture
def valid_token():
    """Create a valid JWT token for testing."""
    return jwt.encode(
        {"user_id": "test_user_123", "exp": 9999999999},  # Far future expiration
        settings.better_auth_secret,
        algorithm="HS256"
    )

def test_create_task_success(client, valid_token):
    """Test successful task creation with valid data."""
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert "id" in data
    assert data["user_id"] == "test_user_123"

def test_create_task_minimal_data(client, valid_token):
    """Test task creation with minimal required data."""
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Minimal Task"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["description"] is None
    assert data["completed"] is False

def test_create_task_missing_title(client, valid_token):
    """Test task creation with missing title (should fail validation)."""
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"description": "Missing title task"}
    )
    
    assert response.status_code == 422  # Validation error

def test_create_task_empty_title(client, valid_token):
    """Test task creation with empty title (should fail validation)."""
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "", "description": "Empty title task"}
    )
    
    assert response.status_code == 422  # Validation error

def test_create_task_title_too_long(client, valid_token):
    """Test task creation with title exceeding 200 characters (should fail validation)."""
    long_title = "x" * 201  # 201 characters, exceeding the limit
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": long_title, "description": "Long title task"}
    )
    
    assert response.status_code == 422  # Validation error

def test_create_task_description_too_long(client, valid_token):
    """Test task creation with description exceeding 1000 characters (should fail validation)."""
    long_description = "x" * 1001  # 1001 characters, exceeding the limit
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Valid Title", "description": long_description}
    )
    
    assert response.status_code == 422  # Validation error

def test_create_task_unauthorized(client):
    """Test task creation without valid token (should fail authentication)."""
    response = client.post(
        "/api/test_user_123/tasks/",
        json={"title": "Unauthorized Task", "description": "Should fail"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_create_task_invalid_token(client):
    """Test task creation with invalid token (should fail authentication)."""
    response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": "Bearer invalid_token"},
        json={"title": "Invalid Token Task", "description": "Should fail"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_create_task_user_id_mismatch(client, valid_token):
    """Test task creation with mismatched user_id in path vs token."""
    # Token has user_id "test_user_123" but path has "different_user"
    response = client.post(
        "/api/different_user/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Mismatch Task", "description": "Should fail"}
    )
    
    assert response.status_code == 403  # Forbidden