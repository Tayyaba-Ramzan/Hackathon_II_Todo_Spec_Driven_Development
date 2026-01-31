# Quickstart Guide: In-Memory Todo CLI App

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -e .`

## Running the Application
- Execute: `python -m src.cli.main` or `todo` (if installed as a console script)

## Using the Application
1. The application will display a menu with numbered options
2. Enter the number corresponding to the action you want to perform
3. Follow the prompts to enter required information

## Available Commands
- Add Todo: Add a new task with title and optional description
- View Todos: Display all tasks with ID, title, description, and status
- Update Todo: Modify title and/or description of an existing task
- Delete Todo: Remove a task by ID
- Mark Complete: Mark a task as complete by ID
- Mark Incomplete: Mark a task as incomplete by ID
- Exit: Quit the application

## Example Usage
1. Select "Add Todo" and enter a title and description
2. Select "View Todos" to see your task list
3. Select "Mark Complete" and enter the task ID to mark it as done