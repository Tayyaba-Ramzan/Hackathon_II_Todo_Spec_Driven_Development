# Quickstart Guide: In-Memory Todo Console Application

**Feature**: 001-todo-console-app
**Date**: 2025-12-27

## Overview
This guide provides instructions for setting up and using the In-Memory Todo Console Application. This application allows you to manage your tasks from the command line with all data stored in memory only.

## Prerequisites
- Python 3.13+ installed on your system
- UV package manager installed

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment using UV:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Application

To run the application, execute:
```bash
python src/cli/main.py
```

## Available Commands

### Add a Task
Add a new task with a title and optional description:
```bash
python src/cli/main.py add "Buy groceries" "Milk, eggs, bread"
```

### View All Tasks
List all tasks with their details:
```bash
python src/cli/main.py view
```

### Update a Task
Update an existing task's title or description:
```bash
python src/cli/main.py update 1 "Buy groceries and cook dinner" "Milk, eggs, bread, chicken"
```

### Delete a Task
Remove a task by its ID:
```bash
python src/cli/main.py delete 1
```

### Mark Task as Complete
Mark a task as completed:
```bash
python src/cli/main.py complete 1
```

### Mark Task as Incomplete
Mark a completed task as incomplete:
```bash
python src/cli/main.py incomplete 1
```

## Example Workflow

1. Add a task:
   ```bash
   python src/cli/main.py add "Learn Python" "Complete the tutorial"
   ```

2. View all tasks:
   ```bash
   python src/cli/main.py view
   ```

3. Mark the task as complete:
   ```bash
   python src/cli/main.py complete 1
   ```

4. Update the task:
   ```bash
   python src/cli/main.py update 1 "Master Python" "Complete all tutorials and build a project"
   ```

## Important Notes

- All data is stored in memory only and will be lost when the application exits
- Task IDs are auto-generated and unique within a session
- The application does not persist data to files or databases
- All commands must be run from the project root directory