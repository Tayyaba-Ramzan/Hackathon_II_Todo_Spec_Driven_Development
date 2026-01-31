import pytest
from fastapi.testclient import TestClient
from main import app
import jwt
from settings import settings

@pytest.fixture
def valid_token():
    """Create a valid JWT token for testing."""
    return jwt.encode(
        {"user_id": "integration_test_user", "exp": 9999999999},  # Far future expiration
        settings.better_auth_secret,
        algorithm="HS256"
    )

def test_full_task_lifecycle(client, valid_token):
    """Test the complete lifecycle of a task: create, read, update, delete."""
    user_id = "integration_test_user"
    
    # 1. Create a task
    create_response = client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Integration Test Task",
            "description": "This is a test task for integration testing",
            "completed": False
        }
    )
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Integration Test Task"
    assert created_task["description"] == "This is a test task for integration testing"
    assert created_task["completed"] is False
    task_id = created_task["id"]
    
    # 2. Get the specific task
    get_specific_response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert get_specific_response.status_code == 200
    retrieved_task = get_specific_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Integration Test Task"
    
    # 3. List all tasks and verify the created task is there
    list_response = client.get(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert list_response.status_code == 200
    tasks_list = list_response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id
    
    # 4. Update the task
    update_response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={
            "title": "Updated Integration Test Task",
            "description": "This task has been updated",
            "completed": True
        }
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Integration Test Task"
    assert updated_task["description"] == "This task has been updated"
    assert updated_task["completed"] is True
    
    # 5. Partially update the task
    patch_response = client.patch(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Partially Updated Integration Test Task"}
    )
    assert patch_response.status_code == 200
    patched_task = patch_response.json()
    assert patched_task["title"] == "Partially Updated Integration Test Task"
    # Description and completed status should remain unchanged from the previous update
    assert patched_task["description"] == "This task has been updated"
    assert patched_task["completed"] is True
    
    # 6. Delete the task
    delete_response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert delete_response.status_code == 204
    
    # 7. Verify the task is deleted by trying to get it
    get_after_delete_response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert get_after_delete_response.status_code == 404

def test_status_filtering(client, valid_token):
    """Test the status filtering functionality."""
    user_id = "integration_test_user"
    
    # Create a pending task
    client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Pending Task", "completed": False}
    )
    
    # Create a completed task
    client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Completed Task", "completed": True}
    )
    
    # Get all tasks
    all_response = client.get(
        f"/api/{user_id}/tasks/?status=all",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert all_response.status_code == 200
    all_tasks = all_response.json()
    assert len(all_tasks) >= 2
    
    # Get only pending tasks
    pending_response = client.get(
        f"/api/{user_id}/tasks/?status=pending",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert pending_response.status_code == 200
    pending_tasks = pending_response.json()
    pending_count = len(pending_tasks)
    
    # Get only completed tasks
    completed_response = client.get(
        f"/api/{user_id}/tasks/?status=completed",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert completed_response.status_code == 200
    completed_tasks = completed_response.json()
    completed_count = len(completed_tasks)
    
    # Verify that filtering works correctly
    assert pending_count + completed_count == len(all_tasks)

def test_validation_rules(client, valid_token):
    """Test the validation rules for task creation and updates."""
    user_id = "integration_test_user"
    
    # Test title too short (empty)
    response = client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "", "description": "Valid description"}
    )
    assert response.status_code == 422
    
    # Test title too long (>200 chars)
    long_title = "x" * 201
    response = client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": long_title, "description": "Valid description"}
    )
    assert response.status_code == 422
    
    # Test description too long (>1000 chars)
    long_description = "x" * 1001
    response = client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Valid title", "description": long_description}
    )
    assert response.status_code == 422
    
    # Test valid creation
    response = client.post(
        f"/api/{user_id}/tasks/",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"title": "Valid task title", "description": "Valid description"}
    )
    assert response.status_code == 201

def test_user_isolation(client, valid_token):
    """Test that users can only access their own tasks."""
    user1_id = "user1_integration_test"
    user2_id = "user2_integration_test"
    
    # Create tokens for both users
    user1_token = jwt.encode(
        {"user_id": user1_id, "exp": 9999999999},
        settings.better_auth_secret,
        algorithm="HS256"
    )
    user2_token = jwt.encode(
        {"user_id": user2_id, "exp": 9999999999},
        settings.better_auth_secret,
        algorithm="HS256"
    )
    
    # User1 creates a task
    create_response = client.post(
        f"/api/{user1_id}/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "User1's Task", "description": "This belongs to user1"}
    )
    assert create_response.status_code == 201
    user1_task_id = create_response.json()["id"]
    
    # User2 creates a task
    create_response = client.post(
        f"/api/{user2_id}/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    user2_task_id = create_response.json()["id"]
    
    # User1 tries to access user2's task list (should fail with 403)
    response = client.get(
        f"/api/{user2_id}/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 403
    
    # User1 tries to access user2's specific task (should fail with 403)
    response = client.get(
        f"/api/{user2_id}/tasks/{user2_task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 403
    
    # User1 should only see their own tasks
    response = client.get(
        f"/api/{user1_id}/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200
    user1_tasks = response.json()
    # Should only contain user1's task
    user1_task_ids = [task["id"] for task in user1_tasks]
    assert user1_task_id in user1_task_ids
    assert user2_task_id not in user1_task_ids