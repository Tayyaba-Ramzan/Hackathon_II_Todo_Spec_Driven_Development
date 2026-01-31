import pytest
from fastapi.testclient import TestClient
from main import app
import jwt
from settings import settings

@pytest.fixture
def user1_token():
    """Create a valid JWT token for user 1."""
    return jwt.encode(
        {"user_id": "user1", "exp": 9999999999},  # Far future expiration
        settings.better_auth_secret,
        algorithm="HS256"
    )

@pytest.fixture
def user2_token():
    """Create a valid JWT token for user 2."""
    return jwt.encode(
        {"user_id": "user2", "exp": 9999999999},  # Far future expiration
        settings.better_auth_secret,
        algorithm="HS256"
    )

def test_cross_user_access_get_task_list(client, user1_token, user2_token):
    """Test that user1 cannot access user2's task list."""
    # User2 creates a task
    create_response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 tries to access user2's task list
    response = client.get(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    
    # Should get 403 because user_id in token doesn't match path
    assert response.status_code == 403

def test_cross_user_access_get_specific_task(client, user1_token, user2_token):
    """Test that user1 cannot access user2's specific task."""
    # User2 creates a task
    create_response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 tries to access user2's specific task
    response = client.get(
        f"/api/user2/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    
    # Should get 403 because user_id in token doesn't match path
    assert response.status_code == 403

def test_cross_user_access_update_task(client, user1_token, user2_token):
    """Test that user1 cannot update user2's task."""
    # User2 creates a task
    create_response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 tries to update user2's task
    response = client.put(
        f"/api/user2/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "Hacked Task", "completed": True}
    )
    
    # Should get 403 because user_id in token doesn't match path
    assert response.status_code == 403

def test_cross_user_access_patch_task(client, user1_token, user2_token):
    """Test that user1 cannot partially update user2's task."""
    # User2 creates a task
    create_response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 tries to partially update user2's task
    response = client.patch(
        f"/api/user2/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "Hacked Task"}
    )
    
    # Should get 403 because user_id in token doesn't match path
    assert response.status_code == 403

def test_cross_user_access_delete_task(client, user1_token, user2_token):
    """Test that user1 cannot delete user2's task."""
    # User2 creates a task
    create_response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User2's Task", "description": "This belongs to user2"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 tries to delete user2's task
    response = client.delete(
        f"/api/user2/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    
    # Should get 403 because user_id in token doesn't match path
    assert response.status_code == 403

def test_same_user_access_success(client, user1_token):
    """Test that a user can access their own tasks."""
    # User1 creates a task
    create_response = client.post(
        "/api/user1/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "User1's Task", "description": "This belongs to user1"}
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # User1 accesses their own task list
    response = client.get(
        "/api/user1/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

    # User1 accesses their own specific task
    response = client.get(
        f"/api/user1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "User1's Task"

    # User1 updates their own task
    response = client.put(
        f"/api/user1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "Updated User1's Task", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated User1's Task"
    assert data["completed"] is True

    # User1 deletes their own task
    response = client.delete(
        f"/api/user1/tasks/{task_id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 204

def test_user_id_path_mismatch(client, user1_token):
    """Test that user_id in token must match user_id in path."""
    # Try to access /api/user2/tasks/ with a token for user1
    response = client.get(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert response.status_code == 403  # Forbidden

    # Try to create task for user2 with token for user1
    response = client.post(
        "/api/user2/tasks/",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "Wrong User Task"}
    )
    assert response.status_code == 403  # Forbidden