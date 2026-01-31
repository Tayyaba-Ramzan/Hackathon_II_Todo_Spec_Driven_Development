"""
Unit tests for Task model validation and TodoService operations
"""
import pytest
from src.models.task import Task
from src.services.todo_service import TodoService
from src.lib.storage import InMemoryStorage


def test_task_creation_with_valid_title():
    """Test that a task can be created with a valid title."""
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False


def test_task_creation_with_empty_title():
    """Test that creating a task with an empty title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
        Task(id=1, title="", description="Test Description", completed=False)


def test_task_creation_with_whitespace_only_title():
    """Test that creating a task with whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
        Task(id=1, title="   ", description="Test Description", completed=False)


def test_task_defaults():
    """Test that a task can be created with default values."""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.completed is False


def test_add_task():
    """Test that a task can be added successfully."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    task_id = service.add_task("Test Task", "Test Description")
    
    assert task_id == 1  # First task should get ID 1
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == "Test Description"
    assert tasks[0].completed is False


def test_add_task_without_description():
    """Test that a task can be added without a description."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    task_id = service.add_task("Test Task")
    
    assert task_id == 1
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"
    assert tasks[0].description == ""


def test_add_multiple_tasks():
    """Test that multiple tasks can be added with sequential IDs."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    id1 = service.add_task("First Task")
    id2 = service.add_task("Second Task")
    
    assert id1 == 1
    assert id2 == 2
    
    tasks = storage.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].title == "First Task"
    assert tasks[1].id == 2
    assert tasks[1].title == "Second Task"


def test_get_all_tasks():
    """Test that all tasks can be retrieved."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add some tasks
    service.add_task("First Task", "Description 1")
    service.add_task("Second Task", "Description 2")
    
    # Get all tasks
    tasks = service.get_all_tasks()
    
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].title == "First Task"
    assert tasks[0].description == "Description 1"
    assert tasks[0].completed is False
    assert tasks[1].id == 2
    assert tasks[1].title == "Second Task"
    assert tasks[1].description == "Description 2"
    assert tasks[1].completed is False


def test_get_all_tasks_empty():
    """Test that get_all_tasks returns an empty list when no tasks exist."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    tasks = service.get_all_tasks()
    
    assert len(tasks) == 0


def test_update_task_title():
    """Test that a task's title can be updated."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task
    task_id = service.add_task("Old Title", "Old Description")
    
    # Update the task's title
    success = service.update_task(task_id, title="New Title")
    
    assert success is True
    
    # Verify the update
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "New Title"
    assert tasks[0].description == "Old Description"


def test_update_task_description():
    """Test that a task's description can be updated."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task
    task_id = service.add_task("Title", "Old Description")
    
    # Update the task's description
    success = service.update_task(task_id, description="New Description")
    
    assert success is True
    
    # Verify the update
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Title"
    assert tasks[0].description == "New Description"


def test_update_task_both_fields():
    """Test that a task's title and description can be updated together."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task
    task_id = service.add_task("Old Title", "Old Description")
    
    # Update both fields
    success = service.update_task(task_id, title="New Title", description="New Description")
    
    assert success is True
    
    # Verify the update
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "New Title"
    assert tasks[0].description == "New Description"


def test_update_nonexistent_task():
    """Test that updating a non-existent task returns False."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Try to update a non-existent task
    success = service.update_task(999, title="New Title")
    
    assert success is False


def test_delete_task():
    """Test that a task can be deleted."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task
    task_id = service.add_task("Task to Delete", "Description")
    
    # Verify task exists
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    
    # Delete the task
    success = service.delete_task(task_id)
    
    assert success is True
    
    # Verify task is gone
    tasks = service.get_all_tasks()
    assert len(tasks) == 0


def test_delete_nonexistent_task():
    """Test that deleting a non-existent task returns False."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Try to delete a non-existent task
    success = service.delete_task(999)
    
    assert success is False


def test_delete_task_leaves_others():
    """Test that deleting one task doesn't affect others."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add multiple tasks
    id1 = service.add_task("First Task", "Description 1")
    id2 = service.add_task("Second Task", "Description 2")
    id3 = service.add_task("Third Task", "Description 3")
    
    # Verify all tasks exist
    tasks = service.get_all_tasks()
    assert len(tasks) == 3
    
    # Delete the second task
    success = service.delete_task(id2)
    
    assert success is True
    
    # Verify only the second task is gone
    tasks = service.get_all_tasks()
    assert len(tasks) == 2
    task_ids = [task.id for task in tasks]
    assert id1 in task_ids
    assert id2 not in task_ids
    assert id3 in task_ids


def test_mark_task_complete():
    """Test that a task can be marked as complete."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add an incomplete task
    task_id = service.add_task("Test Task", "Test Description")
    
    # Verify it starts as incomplete
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is False
    
    # Mark it as complete
    success = service.mark_task_complete(task_id)
    
    assert success is True
    
    # Verify it's now complete
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is True


def test_mark_task_incomplete():
    """Test that a task can be marked as incomplete."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task and mark it complete
    task_id = service.add_task("Test Task", "Test Description")
    service.mark_task_complete(task_id)
    
    # Verify it's complete
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is True
    
    # Mark it as incomplete
    success = service.mark_task_incomplete(task_id)
    
    assert success is True
    
    # Verify it's now incomplete
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].completed is False


def test_mark_nonexistent_task():
    """Test that marking a non-existent task returns False."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Try to mark a non-existent task
    success_complete = service.mark_task_complete(999)
    success_incomplete = service.mark_task_incomplete(999)
    
    assert success_complete is False
    assert success_incomplete is False


def test_mark_task_preserves_other_fields():
    """Test that marking a task doesn't change other fields."""
    storage = InMemoryStorage()
    service = TodoService(storage)
    
    # Add a task
    task_id = service.add_task("Original Title", "Original Description")
    
    # Mark it as complete
    success = service.mark_task_complete(task_id)
    
    assert success is True
    
    # Verify other fields are unchanged
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == task_id
    assert tasks[0].title == "Original Title"
    assert tasks[0].description == "Original Description"
    assert tasks[0].completed is True