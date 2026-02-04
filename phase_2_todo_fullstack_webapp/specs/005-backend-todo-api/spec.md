# Feature Specification: Complete Backend Implementation for Phase II Todo App

**Feature Branch**: `005-backend-todo-api`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "Complete Backend Implementation for Phase II Todo App Target audience: Developers building the backend in the Hackathon Todo monorepo using Qwen CLI and agentic workflow Focus: Build a fully functional FastAPI backend with SQLModel, Neon PostgreSQL integration, JWT verification middleware, and complete task CRUD API that enforces user isolation and integrates seamlessly with the frontend Success criteria: All 6 REST API endpoints implemented exactly as specified: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{id} JWT middleware correctly verifies tokens using BETTER_AUTH_SECRET, extracts user_id, and matches it with path {user_id} All database queries filtered by authenticated user_id — zero possibility of cross-user data access Database connection using DATABASE_URL from environment (Neon PostgreSQL) with SQLModel sessions Proper Pydantic request/response models, validation (title 1-200 chars, description ≤1000), and HTTPException error handling Support query params on list endpoint (status: all/pending/completed) Full integration test: Frontend JWT token accepted, tasks created/viewed/updated/deleted only for authenticated user Backend runs with uvicorn main:app --reload and works with docker-compose Constraints: Use Python FastAPI, SQLModel ORM only Project structure: backend/main.py, models.py, db.py, routes/ folder Environment variables: BETTER_AUTH_SECRET (same as frontend), DATABASE_URL from NEON_DB_URL JWT verification using PyJWT or python-jose, shared secret only — no database sessions All routes under /api/, async where possible Reference @backend/QWEN.md (or CLAUDE.md), @specs/api/rest-endpoints.md, @specs/database/schema.md Implement via Backend Agent iterations only — no manual coding Not building: Frontend changes (auth pages, UI) Advanced features (due dates, sorting beyond status, pagination) Admin panel or user management endpoints Email verification or password reset flows"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create New Task (Priority: P1)

As an authenticated user, I want to create new tasks in my personal task list so that I can track my work and responsibilities.

**Why this priority**: This is the foundational functionality that enables users to add items to their task list, which is the core value of the application.

**Independent Test**: Can be fully tested by authenticating with a JWT token, sending a POST request to /api/{user_id}/tasks with valid task data, and verifying that the task is created and returned with a 201 status code.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends POST request to /api/{user_id}/tasks with valid task data, **Then** a new task is created and returned with 201 status code
2. **Given** user is authenticated with a valid JWT token, **When** user sends POST request with invalid task data (title too long or missing), **Then** appropriate error response is returned with 422 status code

---

### User Story 2 - View User's Tasks (Priority: P1)

As an authenticated user, I want to view all my tasks so that I can see what I need to do and track my progress.

**Why this priority**: This is essential functionality that allows users to see their tasks, which is the primary purpose of the application.

**Independent Test**: Can be fully tested by authenticating with a JWT token, sending a GET request to /api/{user_id}/tasks, and verifying that only tasks belonging to the authenticated user are returned.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends GET request to /api/{user_id}/tasks, **Then** all tasks belonging to that user are returned with 200 status code
2. **Given** user is authenticated with a valid JWT token, **When** user sends GET request with status query parameter, **Then** only tasks with the specified status are returned

---

### User Story 3 - Update Task Details (Priority: P2)

As an authenticated user, I want to update my tasks (title, description, status) so that I can keep my task list current and reflect changes in my work.

**Why this priority**: This allows users to modify existing tasks, which is important for maintaining an accurate task list.

**Independent Test**: Can be fully tested by authenticating with a JWT token, sending a PUT or PATCH request to /api/{user_id}/tasks/{id}, and verifying that the task is updated correctly.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token and owns the task, **When** user sends PUT request to /api/{user_id}/tasks/{id} with updated data, **Then** the task is updated and returned with 200 status code
2. **Given** user is authenticated with a valid JWT token and owns the task, **When** user sends PATCH request to update specific fields, **Then** only those fields are updated

---

### User Story 4 - Delete Task (Priority: P2)

As an authenticated user, I want to delete tasks that I no longer need so that I can keep my task list clean and relevant.

**Why this priority**: This allows users to remove completed or irrelevant tasks, which is important for maintaining an organized task list.

**Independent Test**: Can be fully tested by authenticating with a JWT token, sending a DELETE request to /api/{user_id}/tasks/{id}, and verifying that the task is removed.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token and owns the task, **When** user sends DELETE request to /api/{user_id}/tasks/{id}, **Then** the task is deleted and 204 status code is returned
2. **Given** user is authenticated with a valid JWT token but doesn't own the task, **When** user sends DELETE request to /api/{user_id}/tasks/{id}, **Then** 404 status code is returned

---

### User Story 5 - Secure Task Access (Priority: P1)

As a security-conscious user, I want to ensure that I can only access my own tasks and not other users' tasks so that my data remains private.

**Why this priority**: This is critical for data privacy and security, ensuring that users cannot access each other's tasks.

**Independent Test**: Can be fully tested by attempting to access tasks with different user JWT tokens and verifying that users can only access their own tasks.

**Acceptance Scenarios**:

1. **Given** user is authenticated with a valid JWT token, **When** user sends GET request to /api/{user_id}/tasks where {user_id} doesn't match the JWT's user_id, **Then** 403 status code is returned
2. **Given** user is authenticated with a valid JWT token, **When** user attempts to access another user's specific task, **Then** 404 status code is returned

---

### Edge Cases

- What happens when a user attempts to create a task with a title longer than 200 characters?
- How does the system handle requests with invalid or expired JWT tokens?
- What happens when a user attempts to access a task that doesn't exist?
- How does the system handle database connection failures during API requests?
- What happens when a user attempts to access tasks with a malformed user_id?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST follow spec-driven development (all work starts and ends with /specs/)
- **FR-002**: System MUST be implemented using only AI agents (Qwen CLI) - no manual coding
- **FR-003**: System MUST implement strict user isolation via JWT + DB filtering
- **FR-004**: System MUST use stateless JWT auth with shared BETTER_AUTH_SECRET
- **FR-005**: System MUST use the specified tech stack: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- **FR-006**: System MUST follow monorepo structure: .spec-kit/, specs/, frontend/, backend/
- **FR-007**: System MUST implement all API endpoints as /api/{user_id}/tasks/* with JWT validation
- **FR-008**: System MUST ensure users can only access their own data (no cross-user access)
- **FR-009**: System MUST implement 6 REST API endpoints: GET/POST /api/{user_id}/tasks and GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{id}
- **FR-010**: System MUST verify JWT tokens using BETTER_AUTH_SECRET and extract user_id
- **FR-011**: System MUST match JWT user_id with path {user_id} parameter for authorization
- **FR-012**: System MUST filter all database queries by authenticated user_id to prevent cross-user data access
- **FR-013**: System MUST connect to database using DATABASE_URL from environment (Neon PostgreSQL)
- **FR-014**: System MUST use SQLModel for database operations and sessions
- **FR-015**: System MUST implement proper Pydantic request/response models with validation
- **FR-016**: System MUST validate task title length between 1-200 characters
- **FR-017**: System MUST validate task description length ≤1000 characters
- **FR-018**: System MUST implement HTTPException error handling for invalid requests
- **FR-019**: System MUST support query parameters on list endpoint (status: all/pending/completed)
- **FR-020**: System MUST accept frontend JWT tokens and work with integration tests
- **FR-021**: System MUST run with uvicorn main:app --reload and work with docker-compose
- **FR-022**: System MUST use JWT verification with PyJWT or python-jose, shared secret only
- **FR-023**: System MUST implement all routes under /api/ and use async where possible
- **FR-024**: System MUST NOT implement database sessions, using shared secret only
- **FR-025**: System MUST NOT make frontend changes (auth pages, UI)
- **FR-026**: System MUST NOT implement advanced features (due dates, sorting beyond status, pagination)
- **FR-027**: System MUST NOT implement admin panel or user management endpoints
- **FR-028**: System MUST NOT implement email verification or password reset flows

### Key Entities *(include if feature involves data)*

- **[User]**: Represents an authenticated user with JWT-based access control
- **[Task]**: Represents a task entity with user ownership and CRUD operations
- **[JWT Token]**: Stateless authentication token with user identity and permissions
- **[Database]**: Neon PostgreSQL database storing user tasks with SQLModel ORM
- **[API Endpoint]**: RESTful endpoints for task management with user isolation

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 6 REST API endpoints implemented exactly as specified: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{id}
- **SC-002**: JWT middleware correctly verifies tokens using BETTER_AUTH_SECRET, extracts user_id, and matches it with path {user_id} parameter
- **SC-003**: 100% of database queries filtered by authenticated user_id with zero possibility of cross-user data access
- **SC-004**: All API endpoints pass validation with proper Pydantic models, field validation (title 1-200 chars, description ≤1000), and HTTPException error handling
- **SC-005**: List endpoint supports query parameters for filtering by status (all/pending/completed)
- **SC-006**: Frontend JWT tokens are accepted and validated successfully by the backend
- **SC-007**: Tasks can be created, viewed, updated, and deleted only for authenticated user with proper isolation
- **SC-008**: Backend runs successfully with uvicorn main:app --reload and integrates with docker-compose
- **SC-009**: All integration tests pass demonstrating proper user isolation and JWT validation
- **SC-010**: API response times are under 500ms for standard operations under normal load
