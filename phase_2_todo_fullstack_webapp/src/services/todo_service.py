"""
Todo service for business logic operations.
"""
from typing import List, Optional
from src.models.todo import Todo
from src.lib.storage import InMemoryStorage


class TodoService:
    """
    Service class for handling business logic related to todos.
    
    This class provides methods for creating, reading, updating, and deleting
    todo items, as well as managing their completion status.
    """
    
    def __init__(self, storage: InMemoryStorage):
        """Initialize the service with a storage instance."""
        self.storage = storage
    
    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task with the given title and description.
        
        Args:
            title: The title of the task
            description: The description of the task (optional)
            
        Returns:
            The ID of the newly created task
        """
        if not title:
            raise ValueError("Title cannot be empty")
        
        new_id = self.storage.get_next_id()
        todo = Todo(id=new_id, title=title, description=description, completed=False)
        self.storage.add_todo(todo)
        return new_id
    
    def get_all_tasks(self) -> List[Todo]:
        """
        Get all tasks.
        
        Returns:
            A list of all Todo items
        """
        return self.storage.get_all_todos()
    
    def update_task(self, task_id: int, new_title: Optional[str] = None, 
                    new_description: Optional[str] = None) -> bool:
        """
        Update a task with new title and/or description.
        
        Args:
            task_id: The ID of the task to update
            new_title: The new title (optional)
            new_description: The new description (optional)
            
        Returns:
            True if the task was updated, False if the task doesn't exist
        """
        existing_todo = self.storage.get_todo(task_id)
        if not existing_todo:
            return False
        
        # Use existing values if new values are not provided
        updated_title = new_title if new_title is not None else existing_todo.title
        updated_description = new_description if new_description is not None else existing_todo.description
        
        # Create updated todo
        updated_todo = Todo(
            id=existing_todo.id,
            title=updated_title,
            description=updated_description,
            completed=existing_todo.completed
        )
        
        return self.storage.update_todo(updated_todo)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was deleted, False if the task doesn't exist
        """
        return self.storage.delete_todo(task_id)
    
    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.
        
        Args:
            task_id: The ID of the task to mark complete
            
        Returns:
            True if the task was marked complete, False if the task doesn't exist
        """
        existing_todo = self.storage.get_todo(task_id)
        if not existing_todo:
            return False
        
        updated_todo = Todo(
            id=existing_todo.id,
            title=existing_todo.title,
            description=existing_todo.description,
            completed=True
        )
        
        return self.storage.update_todo(updated_todo)
    
    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.
        
        Args:
            task_id: The ID of the task to mark incomplete
            
        Returns:
            True if the task was marked incomplete, False if the task doesn't exist
        """
        existing_todo = self.storage.get_todo(task_id)
        if not existing_todo:
            return False
        
        updated_todo = Todo(
            id=existing_todo.id,
            title=existing_todo.title,
            description=existing_todo.description,
            completed=False
        )
        
        return self.storage.update_todo(updated_todo)