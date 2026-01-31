"""
Unit tests for Task model validation
"""
import pytest
from src.models.task import Task


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