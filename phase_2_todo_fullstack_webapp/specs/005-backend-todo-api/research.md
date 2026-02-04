# Research Summary: Complete Backend Implementation for Phase II Todo App

## Decision: JWT Library Choice
**Rationale**: Selected PyJWT over python-jose for its simplicity and wide adoption in the Python community. While python-jose has better JOSE support, it's overkill for our simple HS256 token verification needs.
**Alternatives considered**: python-jose (more comprehensive but more complex), Authlib (more features but overkill for simple JWT verification)

## Decision: Dependency Injection Pattern
**Rationale**: Using get_current_user as a dependency rather than manual checks in each route ensures DRY code and consistency across all endpoints. This approach leverages FastAPI's built-in dependency injection system.
**Alternatives considered**: Manual JWT verification in each route handler (repetitive and error-prone), Custom middleware (more complex for this use case)

## Decision: Route Organization
**Rationale**: Using a single tasks.py file for all task-related routes keeps the implementation simple for this small project. As the application grows, routes can be split into separate files.
**Alternatives considered**: Separate files per operation (tasks_create.py, tasks_update.py, etc.) (overkill for this small project), Single file per resource (current approach)

## Decision: Error Response Format
**Rationale**: Using FastAPI's default HTTPException responses maintains consistency with frontend expectations and follows standard REST API practices. Custom error formats would require additional frontend handling.
**Alternatives considered**: Custom JSON error format (would require frontend changes), Standard HTTP error codes with custom messages (current approach)

## Decision: Query Parameter Default
**Rationale**: Setting the status filter default to "all" ensures that when users visit the dashboard, they see all their tasks rather than only pending ones. This provides a more complete view of their task list.
**Alternatives considered**: Default to "pending" (would hide completed tasks), Require explicit status parameter (would break expected functionality)

## Decision: Token Validation Strictness
**Rationale**: Implementing strict user_id matching between JWT claims and path parameters is required for security as specified in the feature requirements. This prevents users from accessing other users' data by manipulating the URL.
**Alternatives considered**: Permissive matching (would violate security requirements), No matching required (would violate security requirements)

## Technical Implementation Details

### JWT Token Handling
- Use PyJWT for JWT decoding/verification with BETTER_AUTH_SECRET from environment
- Extract user_id from token payload and compare with path parameter
- Raise HTTP 401 if token is invalid or expired

### Database Configuration
- DATABASE_URL from NEON_DB_URL environment variable
- SQLModel models with Task entity containing user_id ForeignKey to users.id (string)
- Indexes on tasks.user_id and tasks.completed for performance
- Async SQLModel sessions in db.py with get_db dependency

### Authentication Dependency
- get_current_user dependency extracts token from Authorization header
- Verifies token using PyJWT and BETTER_AUTH_SECRET
- Returns user_id if valid, raises HTTP 401 if invalid
- All routes depend on get_current_user and get_db

### Data Filtering
- All database queries filtered by authenticated user_id: Task.select().where(Task.user_id == current_user_id)
- Prevents cross-user data access as required

### Validation Requirements
- Title: string, min_length=1, max_length=200
- Description: optional string, max_length=1000
- Implemented using Pydantic models for request/response validation

## Testing Strategy

### Validation Checks
Based on success criteria from feature specification:
- All 6 REST API endpoints implemented: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{id}
- JWT middleware correctly verifies tokens and extracts user_id
- Database queries filtered by authenticated user_id with zero cross-user access
- Proper validation and error handling implemented
- Query parameters supported on list endpoint
- Frontend JWT tokens accepted successfully

### Manual Testing Approach
1. Use frontend to signup/login → copy JWT → test all endpoints in Postman/Insomnia with Bearer token
2. Positive cases: Create, list, get, update, toggle, delete own tasks → 200/201 success
3. Negative cases: Missing token → 401, invalid token → 401, wrong user_id in path → 401/403, access other user's task → 404
4. Database verification: Check Neon DB directly that tasks have correct user_id foreign key
5. Integration: Full flow from frontend works without errors