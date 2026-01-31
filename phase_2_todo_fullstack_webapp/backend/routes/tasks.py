from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# Import fix for Hugging Face deployment - ensuring correct module path
from models import Task, TaskCreate, TaskUpdate, TaskResponse  # This is the correct import

from sqlmodel import Session, select
from auth import get_current_user, verify_user_id_match
from db import get_db
from exceptions import TaskNotFoundException, UserMismatchException, ValidationErrorException
from uuid import UUID

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task: TaskCreate
):
    """
    Create a new task for the authenticated user.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Validate title length
    if len(task.title) < 1 or len(task.title) > 200:
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Create the task with the user_id
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    status_filter: str = "all"  # all, pending, completed
):
    """
    Retrieve tasks for the authenticated user with optional filtering.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Build the query with user_id filter
    query = select(Task).where(Task.user_id == user_id)

    # Add status filter if specified
    if status_filter == "pending":
        query = query.where(Task.completed == False)
    elif status_filter == "completed":
        query = query.where(Task.completed == True)
    # If status_filter is "all", no additional filter is needed

    tasks = db.exec(query).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Get a specific task by ID.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    task = db.get(Task, uuid_task_id)

    if not task:
        raise TaskNotFoundException(task_id)

    # Ensure the task belongs to the authenticated user
    if task.user_id != user_id:
        raise TaskNotFoundException(task_id)

    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Update a specific task completely.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    db_task = db.get(Task, uuid_task_id)

    if not db_task:
        raise TaskNotFoundException(task_id)

    # Ensure the task belongs to the authenticated user
    if db_task.user_id != user_id:
        raise TaskNotFoundException(task_id)

    # Validate title length if provided
    if task.title is not None and (len(task.title) < 1 or len(task.title) > 200):
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description is not None and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Update the task fields
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_partial(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str,
    task: TaskUpdate
):
    """
    Partially update a specific task.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    db_task = db.get(Task, uuid_task_id)

    if not db_task:
        raise TaskNotFoundException(task_id)

    # Ensure the task belongs to the authenticated user
    if db_task.user_id != user_id:
        raise TaskNotFoundException(task_id)

    # Validate title length if provided
    if task.title is not None and (len(task.title) < 1 or len(task.title) > 200):
        raise ValidationErrorException("Title must be between 1 and 200 characters")

    # Validate description length if provided
    if task.description is not None and len(task.description) > 1000:
        raise ValidationErrorException("Description must be less than 1000 characters")

    # Update only the fields that were provided
    if task.title is not None:
        db_task.title = task.title
    if task.description is not None:
        db_task.description = task.description
    if task.completed is not None:
        db_task.completed = task.completed

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    *,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user),
    user_id: str,
    task_id: str
):
    """
    Delete a specific task.
    """
    # Verify that the user_id in the JWT matches the user_id in the path
    verify_user_id_match(current_user_id, user_id)

    # Convert task_id string to UUID
    try:
        uuid_task_id = UUID(task_id)
    except ValueError:
        raise TaskNotFoundException(task_id)

    task = db.get(Task, uuid_task_id)

    if not task:
        raise TaskNotFoundException(task_id)

    # Ensure the task belongs to the authenticated user
    if task.user_id != user_id:
        raise TaskNotFoundException(task_id)

    db.delete(task)
    db.commit()

    return