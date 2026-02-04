# Task API Contract

## Base Path
`/api/{user_id}/tasks`

## Authentication
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer <JWT_TOKEN>`

The user_id in the path must match the user_id in the JWT token for authorization.

## Endpoints

### GET /api/{user_id}/tasks
**Description**: List all tasks for the authenticated user with optional filtering

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id

**Query Parameters**:
- `status` (string, optional): Filter by completion status ("all", "pending", "completed"), default: "all"

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)

**Responses**:
- `200 OK`: Successfully retrieved tasks
  - Content-Type: application/json
  - Body: `{ "tasks": [TaskResponse], "total": integer }`
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id

### POST /api/{user_id}/tasks
**Description**: Create a new task for the authenticated user

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json` (required)

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, ≤1000 chars)"
}
```

**Responses**:
- `201 Created`: Task successfully created
  - Content-Type: application/json
  - Body: `TaskResponse`
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id
- `422 Unprocessable Entity`: Validation error (e.g., title too long)

### GET /api/{user_id}/tasks/{id}
**Description**: Get a specific task by ID

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id
- `id` (UUID): Task ID

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)

**Responses**:
- `200 OK`: Successfully retrieved task
  - Content-Type: application/json
  - Body: `TaskResponse`
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id
- `404 Not Found`: Task not found or doesn't belong to user

### PUT /api/{user_id}/tasks/{id}
**Description**: Update a specific task completely

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id
- `id` (UUID): Task ID

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json` (required)

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional, ≤1000 chars)",
  "completed": "boolean"
}
```

**Responses**:
- `200 OK`: Task successfully updated
  - Content-Type: application/json
  - Body: `TaskResponse`
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id
- `404 Not Found`: Task not found or doesn't belong to user
- `422 Unprocessable Entity`: Validation error

### PATCH /api/{user_id}/tasks/{id}
**Description**: Partially update a specific task

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id
- `id` (UUID): Task ID

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)
- `Content-Type: application/json` (required)

**Request Body** (at least one field required):
```json
{
  "title": "string (1-200 chars, optional)",
  "description": "string (≤1000 chars, optional)",
  "completed": "boolean (optional)"
}
```

**Responses**:
- `200 OK`: Task successfully updated
  - Content-Type: application/json
  - Body: `TaskResponse`
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id
- `404 Not Found`: Task not found or doesn't belong to user
- `422 Unprocessable Entity`: Validation error

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific task

**Path Parameters**:
- `user_id` (string): User ID from JWT token, must match token's user_id
- `id` (UUID): Task ID

**Headers**:
- `Authorization: Bearer <JWT_TOKEN>` (required)

**Responses**:
- `204 No Content`: Task successfully deleted
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: user_id in path doesn't match JWT user_id
- `404 Not Found`: Task not found or doesn't belong to user

## Data Models

### TaskResponse
```json
{
  "id": "UUID",
  "title": "string (1-200 chars)",
  "description": "string (≤1000 chars, optional)",
  "completed": "boolean",
  "user_id": "string",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### TaskCreateRequest
```json
{
  "title": "string (1-200 chars)",
  "description": "string (≤1000 chars, optional)"
}
```

### TaskUpdateRequest
```json
{
  "title": "string (1-200 chars, optional)",
  "description": "string (≤1000 chars, optional)",
  "completed": "boolean (optional)"
}
```

## Error Responses

All error responses follow the standard FastAPI/Pydantic format:
```json
{
  "detail": "Error message"
}
```

## Validation Rules

1. Title: 1-200 characters (inclusive)
2. Description: ≤1000 characters if provided
3. user_id in path must match user_id in JWT token
4. Task operations only allowed on tasks belonging to authenticated user