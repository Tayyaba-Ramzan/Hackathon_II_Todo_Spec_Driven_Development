# Quickstart Guide: Backend Todo API Implementation

## Prerequisites

- Python 3.11+
- Poetry (for dependency management) or pip
- Access to Neon PostgreSQL database
- BETTER_AUTH_SECRET environment variable
- Docker and docker-compose (for containerized deployment)

## Environment Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
# If using Poetry
poetry install

# If using pip
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env to include your values
BETTER_AUTH_SECRET=your_secret_key_here
DATABASE_URL=your_neon_postgresql_connection_string
```

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── models.py            # SQLModel database models
├── db.py                # Database session and connection setup
├── auth.py              # JWT verification middleware and dependencies
├── routes/
│   └── tasks.py         # Task CRUD endpoints implementation
└── tests/
    ├── conftest.py      # Test configuration
    ├── test_auth.py     # Authentication tests
    └── test_tasks.py    # Task CRUD tests
```

## Key Dependencies

- FastAPI: Web framework
- SQLModel: Database ORM
- PyJWT: JWT token handling
- python-multipart: Form data handling
- uvicorn: ASGI server

## Running the Application

### Development
```bash
# Run with auto-reload for development
uvicorn main:app --reload
```

### Production
```bash
# Run with multiple workers for production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### With Docker
```bash
# Build and run with docker-compose
docker-compose up --build
```

## Implementation Steps

### 1. Database Models (`models.py`)
- Define the Task model with required fields (id, title, description, completed, user_id)
- Add validation rules for title (1-200 chars) and description (≤1000 chars)
- Set up relationships and indexes

### 2. Database Connection (`db.py`)
- Set up async SQLModel session
- Create get_db dependency for FastAPI
- Configure connection to Neon PostgreSQL

### 3. Authentication (`auth.py`)
- Create get_current_user dependency
- Implement JWT verification using PyJWT
- Extract user_id from token and validate against path parameter

### 4. Task Endpoints (`routes/tasks.py`)
- Implement all 6 required endpoints:
  - GET /api/{user_id}/tasks
  - POST /api/{user_id}/tasks
  - GET /api/{user_id}/tasks/{id}
  - PUT /api/{user_id}/tasks/{id}
  - PATCH /api/{user_id}/tasks/{id}
  - DELETE /api/{user_id}/tasks/{id}
- Apply authentication dependency to all endpoints
- Filter all database queries by authenticated user_id

### 5. Testing
- Write tests for all endpoints
- Verify user isolation (users can't access other users' tasks)
- Test validation rules
- Test JWT authentication

## API Usage Examples

### Creating a Task
```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description"}'
```

### Listing Tasks
```bash
curl -X GET "http://localhost:8000/api/user123/tasks?status=pending" \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

### Updating a Task
```bash
curl -X PUT "http://localhost:8000/api/user123/tasks/task-id-uuid" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "completed": true}'
```

## Important Security Notes

1. Always verify that the user_id in the JWT token matches the user_id in the path
2. Filter all database queries by the authenticated user_id to prevent cross-user access
3. Validate all input data according to the specified constraints
4. Use HTTPS in production to protect JWT tokens in transit