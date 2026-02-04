"""
In-memory storage implementation for the todo application.
"""
from typing import Dict, List, Optional
from src.models.todo import Todo


class InMemoryStorage:
    """
    In-memory storage for todo items.
    This class provides methods for storing, retrieving, updating, and deleting todos.
    """

    def __init__(self):
        """Initialize the storage with an empty dictionary and ID counter."""
        self.todos: Dict[int, Todo] = {}
        self.next_id = 1

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new todo.

        Returns:
            The next available ID
        """
        current_id = self.next_id
        self.next_id += 1
        return current_id

    def add_todo(self, todo: Todo) -> None:
        """
        Add a new todo to storage.

        Args:
            todo: The Todo object to add
        """
        self.todos[todo.id] = todo

    def get_todo(self, todo_id: int) -> Optional[Todo]:
        """
        Get a todo by its ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        return self.todos.get(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos from storage.

        Returns:
            A list of all Todo objects
        """
        return list(self.todos.values())

    def update_todo(self, todo: Todo) -> bool:
        """
        Update an existing todo in storage.

        Args:
            todo: The updated Todo object

        Returns:
            True if the todo was updated, False if it didn't exist
        """
        if todo.id in self.todos:
            self.todos[todo.id] = todo
            return True
        return False

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo from storage.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if the todo was deleted, False if it didn't exist
        """
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False