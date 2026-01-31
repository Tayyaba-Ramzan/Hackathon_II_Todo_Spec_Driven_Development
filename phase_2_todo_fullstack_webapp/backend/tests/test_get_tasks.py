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

def test_get_tasks_success(client, valid_token):
    """Test successful retrieval of tasks for authenticated user."""
    # First create a task
    create_response = client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Then get the tasks
    response = client.get(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Find our test task in the response
    test_task = next((task for task in data if task["id"] == task_id), None)
    assert test_task is not None
    assert test_task["title"] == "Test Task"
    assert test_task["description"] == "Test Description"

def test_get_tasks_empty_list(client, valid_token):
    """Test retrieval of tasks when user has no tasks."""
    response = client.get(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_get_tasks_status_filter_all(client, valid_token):
    """Test retrieval of tasks with status filter 'all'."""
    # Create a completed task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Completed Task", "completed": True}
    )
    
    # Create a pending task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Pending Task", "completed": False}
    )
    
    # Get all tasks
    response = client.get(
        "/api/test_user_123/tasks/?status=all",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should include both completed and pending tasks
    assert len(data) >= 2

def test_get_tasks_status_filter_pending(client, valid_token):
    """Test retrieval of tasks with status filter 'pending'."""
    # Create a completed task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Completed Task", "completed": True}
    )
    
    # Create a pending task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Pending Task", "completed": False}
    )
    
    # Get pending tasks only
    response = client.get(
        "/api/test_user_123/tasks/?status=pending",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should only include pending tasks
    pending_tasks = [task for task in data if task["completed"] == False]
    assert len(data) == len(pending_tasks)

def test_get_tasks_status_filter_completed(client, valid_token):
    """Test retrieval of tasks with status filter 'completed'."""
    # Create a completed task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Completed Task", "completed": True}
    )
    
    # Create a pending task
    client.post(
        "/api/test_user_123/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Pending Task", "completed": False}
    )
    
    # Get completed tasks only
    response = client.get(
        "/api/test_user_123/tasks/?status=completed",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should only include completed tasks
    completed_tasks = [task for task in data if task["completed"] == True]
    assert len(data) == len(completed_tasks)

def test_get_tasks_unauthorized(client):
    """Test task retrieval without valid token (should fail authentication)."""
    response = client.get("/api/test_user_123/tasks/")
    
    assert response.status_code == 401  # Unauthorized

def test_get_tasks_invalid_token(client):
    """Test task retrieval with invalid token (should fail authentication)."""
    response = client.get(
        "/api/test_user_123/tasks/",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401  # Unauthorized

def test_get_tasks_user_id_mismatch(client, valid_token):
    """Test task retrieval with mismatched user_id in path vs token."""
    # Token has user_id "test_user_123" but path has "different_user"
    response = client.get(
        "/api/different_user/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    assert response.status_code == 403  # Forbidden