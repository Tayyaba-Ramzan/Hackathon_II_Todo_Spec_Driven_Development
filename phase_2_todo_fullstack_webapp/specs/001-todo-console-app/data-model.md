# Data Model: In-Memory Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-27

## Task Entity

### Fields
- **id** (integer): Unique identifier for the task, auto-generated
- **title** (string): Required title of the task, cannot be empty
- **description** (string): Optional description of the task, can be empty
- **completed** (boolean): Status of the task, defaults to False

### Relationships
- No relationships with other entities (standalone entity)

### Validation Rules
- `id`: Must be a positive integer, auto-incremented from 1
- `title`: Required field, must not be empty or contain only whitespace
- `description`: Optional field, can be empty
- `completed`: Boolean value, defaults to False when creating a new task

### State Transitions
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user marks task as incomplete

## In-Memory Storage Model

### Fields
- **tasks** (dict): Dictionary mapping task IDs to Task objects
- **next_id** (integer): Counter for generating unique IDs, starts at 1

### Operations
- `add_task(task)`: Adds a new task to storage, assigns unique ID
- `get_task(task_id)`: Retrieves a task by its ID
- `update_task(task_id, title, description, completed)`: Updates task fields
- `delete_task(task_id)`: Removes a task from storage
- `get_all_tasks()`: Returns all tasks in storage

## CLI Command Model

### Fields
- **command** (string): The operation to perform (add, view, update, delete, complete)
- **arguments** (list): Additional parameters for the command
- **options** (dict): Optional flags for the command

### Validation Rules
- `command`: Must be one of the supported commands (add, view, update, delete, complete, incomplete)
- `arguments`: Required arguments vary by command type
- `options`: Valid options depend on the specific command

## Application State Model

### Fields
- **storage** (InMemoryStorage): The in-memory storage instance
- **running** (boolean): Whether the application is currently running
- **exit_code** (integer): Code to return when application exits