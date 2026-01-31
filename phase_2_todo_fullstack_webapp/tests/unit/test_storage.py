"""
Unit tests for storage operations
"""
import pytest
from src.models.task import Task
from src.lib.storage import InMemoryStorage


def test_get_all_tasks():
    """Test that all tasks can be retrieved from storage."""
    storage = InMemoryStorage()
    
    # Add some tasks directly to storage
    task1 = Task(id=0, title="First Task", description="Description 1")
    task2 = Task(id=0, title="Second Task", description="Description 2")
    
    storage.add_task(task1)
    storage.add_task(task2)
    
    # Get all tasks
    tasks = storage.get_all_tasks()
    
    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[0].title == "First Task"
    assert tasks[0].description == "Description 1"
    assert tasks[1].id == 2
    assert tasks[1].title == "Second Task"
    assert tasks[1].description == "Description 2"


def test_get_all_tasks_empty():
    """Test that get_all_tasks returns an empty list when no tasks exist."""
    storage = InMemoryStorage()
    
    tasks = storage.get_all_tasks()
    
    assert len(tasks) == 0


def test_add_task_assigns_id():
    """Test that adding a task assigns it a unique ID."""
    storage = InMemoryStorage()
    
    task = Task(id=0, title="Test Task")
    assigned_id = storage.add_task(task)
    
    assert assigned_id == 1
    assert task.id == 1


def test_add_multiple_tasks_sequential_ids():
    """Test that multiple tasks get sequential IDs."""
    storage = InMemoryStorage()

    task1 = Task(id=0, title="First Task")
    task2 = Task(id=0, title="Second Task")

    id1 = storage.add_task(task1)
    id2 = storage.add_task(task2)

    assert id1 == 1
    assert id2 == 2
    assert task1.id == 1
    assert task2.id == 2


def test_update_task_title():
    """Test that a task's title can be updated."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Old Title", description="Old Description")
    task_id = storage.add_task(task)

    # Update the task's title
    updated_task = storage.update_task(task_id, title="New Title")

    assert updated_task is not None
    assert updated_task.title == "New Title"
    assert updated_task.description == "Old Description"


def test_update_task_description():
    """Test that a task's description can be updated."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Title", description="Old Description")
    task_id = storage.add_task(task)

    # Update the task's description
    updated_task = storage.update_task(task_id, description="New Description")

    assert updated_task is not None
    assert updated_task.title == "Title"
    assert updated_task.description == "New Description"


def test_update_task_completed_status():
    """Test that a task's completed status can be updated."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Title", completed=False)
    task_id = storage.add_task(task)

    # Update the task's completed status
    updated_task = storage.update_task(task_id, completed=True)

    assert updated_task is not None
    assert updated_task.completed is True


def test_update_task_all_fields():
    """Test that all fields of a task can be updated."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Old Title", description="Old Description", completed=False)
    task_id = storage.add_task(task)

    # Update all fields
    updated_task = storage.update_task(task_id, title="New Title", description="New Description", completed=True)

    assert updated_task is not None
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    assert updated_task.completed is True


def test_update_nonexistent_task():
    """Test that updating a non-existent task returns None."""
    storage = InMemoryStorage()

    # Try to update a non-existent task
    result = storage.update_task(999, title="New Title")

    assert result is None


def test_delete_task():
    """Test that a task can be deleted."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Task to Delete", description="Description")
    task_id = storage.add_task(task)

    # Verify task exists
    tasks = storage.get_all_tasks()
    assert len(tasks) == 1

    # Delete the task
    success = storage.delete_task(task_id)

    assert success is True

    # Verify task is gone
    tasks = storage.get_all_tasks()
    assert len(tasks) == 0


def test_delete_nonexistent_task():
    """Test that deleting a non-existent task returns False."""
    storage = InMemoryStorage()

    # Try to delete a non-existent task
    success = storage.delete_task(999)

    assert success is False


def test_delete_task_leaves_others():
    """Test that deleting one task doesn't affect others."""
    storage = InMemoryStorage()

    # Add multiple tasks
    task1 = Task(id=0, title="First Task", description="Description 1")
    task2 = Task(id=0, title="Second Task", description="Description 2")
    task3 = Task(id=0, title="Third Task", description="Description 3")

    id1 = storage.add_task(task1)
    id2 = storage.add_task(task2)
    id3 = storage.add_task(task3)

    # Verify all tasks exist
    tasks = storage.get_all_tasks()
    assert len(tasks) == 3

    # Delete the second task
    success = storage.delete_task(id2)

    assert success is True

    # Verify only the second task is gone
    tasks = storage.get_all_tasks()
    assert len(tasks) == 2
    task_ids = [task.id for task in tasks]
    assert id1 in task_ids
    assert id2 not in task_ids
    assert id3 in task_ids


def test_update_task_status():
    """Test that a task's completion status can be updated."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Test Task", completed=False)
    task_id = storage.add_task(task)

    # Verify it starts as incomplete
    task = storage.get_task(task_id)
    assert task is not None
    assert task.completed is False

    # Update the completion status to True
    updated_task = storage.update_task(task_id, completed=True)

    assert updated_task is not None
    assert updated_task.completed is True

    # Verify the change is persistent
    retrieved_task = storage.get_task(task_id)
    assert retrieved_task is not None
    assert retrieved_task.completed is True


def test_update_task_status_multiple_times():
    """Test that a task's completion status can be updated multiple times."""
    storage = InMemoryStorage()

    # Add a task
    task = Task(id=0, title="Test Task", completed=False)
    task_id = storage.add_task(task)

    # Toggle the status a few times
    # Start: False
    assert storage.get_task(task_id).completed is False

    # Set to True
    storage.update_task(task_id, completed=True)
    assert storage.get_task(task_id).completed is True

    # Set back to False
    storage.update_task(task_id, completed=False)
    assert storage.get_task(task_id).completed is False

    # Set to True again
    storage.update_task(task_id, completed=True)
    assert storage.get_task(task_id).completed is True