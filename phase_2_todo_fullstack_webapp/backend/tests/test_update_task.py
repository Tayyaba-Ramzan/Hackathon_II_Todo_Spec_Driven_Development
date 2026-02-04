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

def test_update_task_put_success(client, valid_token):
    """Test successful task update with PUT request."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Original Title", "description": "Original Description"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Update the task with PUT
    response = client.put(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

def test_update_task_patch_success(client, valid_token):
    """Test successful partial task update with PATCH request."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Original Title", "description": "Original Description"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Partially update the task with PATCH
    response = client.patch(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Partially Updated Title"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Partially Updated Title"
    assert data["description"] == "Original Description"  # Should remain unchanged
    assert data["completed"] is False  # Should remain unchanged

def test_update_task_put_validation_error(client, valid_token):
    """Test task update with PUT request fails validation."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Original Title"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Try to update with title that's too long
    response = client.put(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "x" * 201,  # Too long
            "description": "Updated Description",
            "completed": True
        }
    )
    
    assert response.status_code == 422  # Validation error

def test_update_task_patch_validation_error(client, valid_token):
    """Test task update with PATCH request fails validation."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Original Title"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Try to update with title that's too long
    response = client.patch(
        f"/api/test_user_123/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "x" * 201}  # Too long
    )
    
    assert response.status_code == 422  # Validation error

def test_update_task_put_unauthorized(client):
    """Test task update with PUT request without valid token (should fail authentication)."""
    response = client.put(
        "/api/test_user_123/tasks/123",
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_update_task_patch_unauthorized(client):
    """Test task update with PATCH request without valid token (should fail authentication)."""
    response = client.patch(
        "/api/test_user_123/tasks/123",
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_update_task_put_invalid_token(client):
    """Test task update with PUT request with invalid token (should fail authentication)."""
    response = client.put(
        "/api/test_user_123/tasks/123",
        headers={"Authorization": "Bearer invalid_token"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_update_task_patch_invalid_token(client):
    """Test task update with PATCH request with invalid token (should fail authentication)."""
    response = client.patch(
        "/api/test_user_123/tasks/123",
        headers={"Authorization": "Bearer invalid_token"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_update_task_put_user_id_mismatch(client, valid_token):
    """Test task update with PUT request with mismatched user_id in path vs token."""
    # Token has user_id "test_user_123" but path has "different_user"
    response = client.put(
        "/api/different_user/tasks/123",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 403  # Forbidden

def test_update_task_patch_user_id_mismatch(client, valid_token):
    """Test task update with PATCH request with mismatched user_id in path vs token."""
    # Token has user_id "test_user_123" but path has "different_user"
    response = client.patch(
        "/api/different_user/tasks/123",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 403  # Forbidden

def test_update_task_put_nonexistent_task(client, valid_token):
    """Test task update with PUT request for non-existent task."""
    response = client.put(
        "/api/test_user_123/tasks/nonexistent_id",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 404  # Not found

def test_update_task_patch_nonexistent_task(client, valid_token):
    """Test task update with PATCH request for non-existent task."""
    response = client.patch(
        "/api/test_user_123/tasks/nonexistent_id",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Updated Title"}
    )
    
    assert response.status_code == 404  # Not found