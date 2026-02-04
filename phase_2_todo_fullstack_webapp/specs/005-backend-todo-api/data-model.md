# Data Model: Backend Todo API

## Entity: User
**Description**: Represents an authenticated user with JWT-based access control

**Fields**:
- `id` (string): Unique identifier for the user, matches the user_id in JWT tokens
- `email` (string, optional): User's email address
- `created_at` (datetime): Timestamp when the user account was created
- `updated_at` (datetime): Timestamp when the user account was last updated

## Entity: Task
**Description**: Represents a task entity with user ownership and CRUD operations

**Fields**:
- `id` (UUID, primary key): Unique identifier for the task
- `title` (string): Task title, 1-200 characters
- `description` (string, optional): Task description, max 1000 characters
- `completed` (boolean): Whether the task is completed, default false
- `user_id` (string): Foreign key to User.id, ensures user isolation
- `created_at` (datetime): Timestamp when the task was created
- `updated_at` (datetime): Timestamp when the task was last updated

**Relationships**:
- `user_id` → `User.id` (many-to-one relationship)

**Validation Rules**:
- `title` must be between 1-200 characters (inclusive)
- `description` must be ≤1000 characters if provided
- `completed` defaults to false
- `user_id` must match the authenticated user's ID for all operations

**State Transitions**:
- `completed` field can transition from `false` to `true` (completed) or `true` to `false` (incomplete)

## API Request/Response Models

### TaskCreate
**Purpose**: Request model for creating new tasks
**Fields**:
- `title` (string): Required, 1-200 characters
- `description` (string, optional): Optional, ≤1000 characters

### TaskUpdate
**Purpose**: Request model for updating existing tasks
**Fields**:
- `title` (string, optional): Optional, 1-200 characters if provided
- `description` (string, optional): Optional, ≤1000 characters if provided
- `completed` (boolean, optional): Optional, updates completion status

### TaskResponse
**Purpose**: Response model for task operations
**Fields**:
- `id` (UUID): Task identifier
- `title` (string): Task title
- `description` (string, optional): Task description
- `completed` (boolean): Completion status
- `user_id` (string): Owner's user ID
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### TaskListResponse
**Purpose**: Response model for listing tasks
**Fields**:
- `tasks` (array of TaskResponse): List of tasks matching query parameters
- `total` (integer): Total number of tasks matching query (before pagination if implemented)