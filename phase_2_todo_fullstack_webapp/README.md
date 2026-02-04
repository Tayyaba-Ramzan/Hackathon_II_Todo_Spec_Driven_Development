# Full-Stack Todo Application

A complete full-stack application for managing todo tasks with frontend, backend, and database integration.

## Features

- Full-stack web application with Next.js frontend and FastAPI backend
- User authentication and authorization with JWT tokens
- CRUD operations for todo tasks
- User isolation - users can only access their own tasks
- Environment configuration for different deployment environments

## Architecture

The application follows a modern full-stack architecture:

- `frontend/`: Next.js 16+ frontend with App Router
- `backend/`: FastAPI backend with SQLModel and JWT authentication
- `specs/`: Specification files for the project

## Running the Application

### Local Development
1. Terminal 1 - Start the backend:
   ```bash
   cd backend
   pip install poetry
   poetry install
   poetry run uvicorn main:app --reload --port 8000
   ```

2. Terminal 2 - Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The frontend will be available at http://localhost:3000
The backend API will be available at http://localhost:8000

## API Communication
- Frontend makes API requests to `http://localhost:8000/api/{user_id}/tasks`
- Requests must include a valid JWT token in the Authorization header: `Bearer {token}`
- Backend validates JWT tokens using the shared BETTER_AUTH_SECRET

## Authentication Flow
1. User logs in through the frontend
2. Frontend receives JWT token from authentication service
3. Frontend stores token and includes it in API requests to backend
4. Backend verifies JWT token and processes requests based on user identity
5. Backend ensures users can only access their own data through user_id validation

## Development

This project was generated using Spec-Driven Development methodology with the Spec-Kit Plus framework.