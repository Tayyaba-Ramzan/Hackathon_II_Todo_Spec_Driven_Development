"""
Integration tests for the Todo Console Application
"""
import sys
from io import StringIO
from unittest.mock import patch
from src.cli.main import TodoCLI


def test_full_workflow():
    """Test the complete workflow of the todo application."""
    cli = TodoCLI()
    
    # Add a task
    cli.run(["add", "Test Task", "Test Description"])
    
    # View tasks - capture output
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "Test Task" in output
    assert "Test Description" in output
    assert "○" in output  # Should be incomplete
    
    # Update the task
    cli.run(["update", "1", "--title", "Updated Task", "--description", "Updated Description"])
    
    # View tasks again
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "Updated Task" in output
    assert "Updated Description" in output
    
    # Mark as complete
    cli.run(["complete", "1"])
    
    # View tasks again
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "Updated Task" in output
    assert "✓" in output  # Should now be complete
    
    # Delete the task
    cli.run(["delete", "1"])
    
    # View tasks - should be empty now
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "No tasks found" in output


def test_multiple_tasks_workflow():
    """Test workflow with multiple tasks."""
    cli = TodoCLI()
    
    # Add multiple tasks
    cli.run(["add", "First Task", "Description 1"])
    cli.run(["add", "Second Task", "Description 2"])
    cli.run(["add", "Third Task", "Description 3"])
    
    # View all tasks
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "First Task" in output
    assert "Second Task" in output
    assert "Third Task" in output
    
    # Mark second task as complete
    cli.run(["complete", "2"])
    
    # View tasks and verify second is complete
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    # Count how many completed and incomplete tasks are shown
    completed_count = output.count("✓")
    incomplete_count = output.count("○")
    
    assert completed_count == 1  # One task should be marked complete
    assert incomplete_count == 2  # Two tasks should be marked incomplete
    
    # Update the third task
    cli.run(["update", "3", "--title", "Updated Third Task"])
    
    # Delete the first task
    cli.run(["delete", "1"])
    
    # View tasks - should have 2 tasks now (second and third)
    captured_output = StringIO()
    sys.stdout = captured_output
    cli.run(["view"])
    sys.stdout = sys.__stdout__  # Reset stdout
    
    output = captured_output.getvalue()
    assert "First Task" not in output  # Should be deleted
    assert "Second Task" in output  # Should still exist
    assert "Updated Third Task" in output  # Should be updated
    assert output.count("ID:") == 2  # Should have 2 tasks


def test_error_handling():
    """Test error handling for invalid operations."""
    cli = TodoCLI()
    
    # Try to update a non-existent task
    try:
        cli.run(["update", "999", "--title", "New Title"])
    except SystemExit:
        pass  # Expected to exit with error
    
    # Try to delete a non-existent task
    try:
        cli.run(["delete", "999"])
    except SystemExit:
        pass  # Expected to exit with error
    
    # Try to mark complete a non-existent task
    try:
        cli.run(["complete", "999"])
    except SystemExit:
        pass  # Expected to exit with error
    
    # Try to mark incomplete a non-existent task
    try:
        cli.run(["incomplete", "999"])
    except SystemExit:
        pass  # Expected to exit with error