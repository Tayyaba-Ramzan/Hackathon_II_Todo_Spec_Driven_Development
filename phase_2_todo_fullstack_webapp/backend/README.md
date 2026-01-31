---
title: Todo Backend API
emoji: ✅
colorFrom: blue
colorTo: indigo
sdk: docker
sdk_version: "latest"
app_file: main.py
pinned: false
---

# Backend Todo API

This is the backend service for the Todo application, built with FastAPI and SQLModel. It provides a secure, user-isolated task management API with JWT authentication.

## Features

- JWT-based authentication and authorization
- User-isolated task management (users can only access their own tasks)
- Full CRUD operations for tasks
- Task filtering by status (all, pending, completed)
- Input validation for task titles and descriptions
- Comprehensive error handling

## API Endpoints

All endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <JWT_TOKEN>`

The user_id in the path must match the user_id in the JWT token for authorization.

### Task Management

- `GET /api/{user_id}/tasks` - List all tasks for the authenticated user with optional filtering
- `POST /api/{user_id}/tasks` - Create a new task for the authenticated user
- `GET /api/{user_id}/tasks/{id}` - Get a specific task by ID
- `PUT /api/{user_id}/tasks/{id}` - Update a specific task completely
- `PATCH /api/{user_id}/tasks/{id}` - Partially update a specific task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a specific task

### Health Check

- `GET /` - Welcome message
- `GET /health` - Health check endpoint

## Validation Rules

- Title: 1-200 characters (inclusive)
- Description: ≤1000 characters if provided
- user_id in path must match user_id in JWT token
- Task operations only allowed on tasks belonging to authenticated user

## Setup and Development

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env to include your values
   ```
4. Run the application:
   ```bash
   poetry run uvicorn backend.main:app --reload
   ```

### Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for JWT token signing/verification
- `DATABASE_URL`: Database connection string

## Testing

Run the tests using pytest:

```bash
poetry run pytest backend/tests/ -v
```

## Docker

To run the application with Docker:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Architecture

- **FastAPI**: Web framework with automatic API documentation
- **SQLModel**: Database ORM with support for SQLAlchemy and Pydantic
- **PyJWT**: JWT token handling
- **PostgreSQL**: Database for storing tasks and user data
- **Pydantic**: Data validation and settings management

## Security

- JWT tokens are verified using the `BETTER_AUTH_SECRET`
- All endpoints verify that the user_id in the JWT matches the user_id in the path
- Database queries are filtered by the authenticated user's ID to prevent cross-user access