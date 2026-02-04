from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import field_serializer

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """
    Task model representing a task entity with user ownership and CRUD operations.
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Removed foreign_key constraint for simplicity
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class TaskCreate(TaskBase):
    """
    Request model for creating new tasks.
    """
    pass

class TaskUpdate(SQLModel):
    """
    Request model for updating existing tasks.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None

class TaskResponse(TaskBase):
    """
    Response model for task operations.
    """
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

    @field_serializer('created_at')
    def serialize_created_at(self, value: datetime) -> str:
        """Serialize created_at datetime to ISO format string."""
        return value.isoformat()

    @field_serializer('updated_at')
    def serialize_updated_at(self, value: datetime) -> str:
        """Serialize updated_at datetime to ISO format string."""
        return value.isoformat()