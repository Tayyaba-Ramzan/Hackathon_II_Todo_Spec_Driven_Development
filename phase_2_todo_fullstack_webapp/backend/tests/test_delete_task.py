import pytest
from fastapi.testclient import TestClient
from main import app
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

def test_delete_task_success(client, valid_token):
    """Test successful task deletion."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Task to Delete", "description": "This will be deleted"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 204  # No content
    
    # Verify the task is gone by trying to get it
    get_response = client.get(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert get_response.status_code == 404

def test_delete_task_nonexistent(client, valid_token):
    """Test deletion of non-existent task."""
    response = client.delete(
        "/api/test_user_123/tasks/nonexistent_id",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 404  # Not found

def test_delete_task_unauthorized(client):
    """Test task deletion without valid token (should fail authentication)."""
    response = client.delete("/api/test_user_123/tasks/123")
    
    assert response.status_code == 401  # Unauthorized

def test_delete_task_invalid_token(client):
    """Test task deletion with invalid token (should fail authentication)."""
    response = client.delete(
        "/api/test_user_123/tasks/123",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_delete_task_user_id_mismatch(client, valid_token):
    """Test task deletion with mismatched user_id in path vs token."""
    # Token has user_id "test_user_123" but path has "different_user"
    response = client.delete(
        "/api/different_user/tasks/123",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 403  # Forbidden