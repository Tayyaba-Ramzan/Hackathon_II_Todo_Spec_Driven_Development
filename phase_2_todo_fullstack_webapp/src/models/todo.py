"""
Todo model representing a single todo task in the system.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Todo:
    """
    Represents a single todo task in the system.
    
    Attributes:
        id: Unique identifier for the task
        title: Task title (required)
        description: Task description (optional, default: empty string)
        completed: Task completion status (default: False)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __post_init__(self):
        """Validate the Todo instance after initialization."""
        if not self.title:
            raise ValueError("Title cannot be empty")
        if not isinstance(self.completed, bool):
            raise ValueError("Completed must be a boolean value")