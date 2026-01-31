# Research: In-Memory Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-27

## Research Summary

This document captures the research and decisions made during the planning phase for the In-Memory Todo Console Application.

## Data Structure Decision

### Decision: 
Use a Python dictionary with integer keys for task IDs and Task objects as values.

### Rationale:
- Dictionary provides O(1) lookup time for retrieving tasks by ID
- Simple to implement and maintain
- Python's built-in dict type is efficient and well-tested
- Allows for easy iteration over tasks when viewing all tasks

### Alternatives considered:
1. List of Task objects - would require O(n) search time to find a specific task by ID
2. Set of Task objects - doesn't support indexing by ID
3. Custom data structure - unnecessary complexity for this use case

## ID Generation Method

### Decision:
Use an auto-incrementing integer starting from 1.

### Rationale:
- Simple to implement and understand
- Guarantees unique IDs within a session
- Follows common conventions for ID generation
- Memory efficient (single integer counter)

### Alternatives considered:
1. UUIDs - would work but are overkill for in-memory application and use more memory
2. Random integers - risk of collisions
3. Timestamp-based IDs - could have collisions with rapid task creation

## CLI Style Decision

### Decision:
Use command-line arguments approach (e.g., `todo add "Buy milk"`).

### Rationale:
- Simpler to implement than interactive menu system
- Follows Unix/Linux command-line conventions
- Easier to test and automate
- More efficient for users familiar with command-line tools

### Alternatives considered:
1. Interactive menu system - more complex to implement and test
2. Mixed approach (menu + commands) - unnecessary complexity

## Task Model Design

### Decision:
Create a Task class with id, title, description, and completed attributes.

### Rationale:
- Encapsulates task data in a clean, organized way
- Makes it easy to extend with additional fields if needed
- Provides clear interface for task operations
- Follows object-oriented design principles

### Task Class Definition:
```python
class Task:
    def __init__(self, id, title, description="", completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
```

## Error Handling Approach

### Decision:
Provide clear, user-friendly error messages for invalid operations.

### Rationale:
- Improves user experience when mistakes are made
- Makes the application more robust
- Follows good CLI application practices

### Examples:
- "Error: Task with ID 5 does not exist"
- "Error: Title cannot be empty"
- "Usage: todo add <title> [description]"

## Storage Implementation

### Decision:
Use a Python dictionary for task storage and a class to manage the storage.

### Rationale:
- Dictionary provides efficient lookup by ID
- Class encapsulates storage operations
- Maintains clean separation of concerns
- In-memory only as required by specifications

### Storage Class Definition:
```python
class InMemoryStorage:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1
    
    def add_task(self, task):
        task.id = self.next_id
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task.id
    
    def get_task(self, task_id):
        return self.tasks.get(task_id)
    
    def update_task(self, task_id, title=None, description=None, completed=None):
        task = self.tasks.get(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed
            return task
        return None
    
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def get_all_tasks(self):
        return list(self.tasks.values())
```