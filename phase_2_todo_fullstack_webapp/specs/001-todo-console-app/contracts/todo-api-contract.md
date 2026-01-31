# Todo API Contract

**Feature**: 001-todo-console-app
**Date**: 2025-12-27

## Overview
This document defines the contract for the Todo Console Application API. Since this is a CLI application, the "API" refers to the command-line interface and its expected behavior.

## Command Structure
```
python src/cli/main.py <command> [arguments] [options]
```

## Commands

### 1. Add Task
**Command**: `add`
**Description**: Add a new task with a title and optional description
**Arguments**:
- `title` (required): The title of the task
- `description` (optional): Additional details about the task
**Options**: None
**Example**:
```bash
python src/cli/main.py add "Buy groceries" "Milk, eggs, bread"
```
**Success Response**: 
- Output: "Task added successfully with ID: {id}"
- Exit Code: 0
**Error Response**:
- Output: "Error: Title cannot be empty" (if title is empty)
- Exit Code: 1

### 2. View Tasks
**Command**: `view`
**Description**: Display all tasks with their details
**Arguments**: None
**Options**: None
**Example**:
```bash
python src/cli/main.py view
```
**Success Response**:
- Output: Formatted list of all tasks with ID, title, description, and completion status
- Exit Code: 0
**Error Response**: 
- Output: "No tasks found" (if no tasks exist)
- Exit Code: 0

### 3. Update Task
**Command**: `update`
**Description**: Update an existing task's title and/or description
**Arguments**:
- `id` (required): The ID of the task to update
- `title` (optional): The new title for the task
- `description` (optional): The new description for the task
**Options**: None
**Example**:
```bash
python src/cli/main.py update 1 "Updated title" "Updated description"
```
**Success Response**:
- Output: "Task {id} updated successfully"
- Exit Code: 0
**Error Response**:
- Output: "Error: Task with ID {id} does not exist"
- Exit Code: 1

### 4. Delete Task
**Command**: `delete`
**Description**: Remove a task by its ID
**Arguments**:
- `id` (required): The ID of the task to delete
**Options**: None
**Example**:
```bash
python src/cli/main.py delete 1
```
**Success Response**:
- Output: "Task {id} deleted successfully"
- Exit Code: 0
**Error Response**:
- Output: "Error: Task with ID {id} does not exist"
- Exit Code: 1

### 5. Mark Task Complete
**Command**: `complete`
**Description**: Mark a task as complete
**Arguments**:
- `id` (required): The ID of the task to mark as complete
**Options**: None
**Example**:
```bash
python src/cli/main.py complete 1
```
**Success Response**:
- Output: "Task {id} marked as complete"
- Exit Code: 0
**Error Response**:
- Output: "Error: Task with ID {id} does not exist"
- Exit Code: 1

### 6. Mark Task Incomplete
**Command**: `incomplete`
**Description**: Mark a task as incomplete
**Arguments**:
- `id` (required): The ID of the task to mark as incomplete
**Options**: None
**Example**:
```bash
python src/cli/main.py incomplete 1
```
**Success Response**:
- Output: "Task {id} marked as incomplete"
- Exit Code: 0
**Error Response**:
- Output: "Error: Task with ID {id} does not exist"
- Exit Code: 1

## Data Models

### Task
```
{
  "id": integer,
  "title": string,
  "description": string,
  "completed": boolean
}
```

## Error Handling
All commands follow a consistent error handling approach:
- Invalid arguments result in error messages to stderr
- Non-existent tasks result in appropriate error messages
- Commands return exit code 1 for errors, 0 for success

## Validation Rules
- Task titles must not be empty
- Task IDs must be positive integers
- Update operations only affect specified fields
- Delete operations are idempotent (no error if task doesn't exist)