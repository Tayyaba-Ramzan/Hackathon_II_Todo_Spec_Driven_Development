# Data Model: Better Auth Integration

## User Entity

**Fields:**
- `id` (string): Unique identifier for the user
- `email` (string): User's email address, used for authentication
- `password` (string): Hashed password for authentication
- `name` (string, optional): User's display name
- `created_at` (datetime): Timestamp when the user account was created
- `updated_at` (datetime): Timestamp when the user account was last updated

**Validation Rules:**
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (8+ characters)
- Email and password are required for signup

**Relationships:**
- One-to-Many: A user can have many tasks
- Each task belongs to exactly one user

## JWT Token Entity

**Fields:**
- `token` (string): The JWT token string
- `user_id` (string): Reference to the user who owns this token
- `expires_at` (datetime): Expiration timestamp (7 days from creation)
- `created_at` (datetime): Timestamp when the token was issued

**Validation Rules:**
- Token must be properly formatted JWT
- Token must be signed with the correct BETTER_AUTH_SECRET
- Token must not be expired at the time of validation
- User referenced by user_id must exist and be active

**State Transitions:**
- Active → Expired: When current time exceeds expires_at
- Active → Revoked: When user logs out or token is invalidated

## Session Data Entity

**Fields:**
- `user_id` (string): Reference to the authenticated user
- `email` (string): User's email for display purposes
- `expires_at` (datetime): Session expiration time
- `created_at` (datetime): When the session was established

**Validation Rules:**
- Session must be associated with a valid, active user
- Session must not be expired
- Session data must match the JWT token claims

**Relationships:**
- One-to-One: Each session is tied to one JWT token
- One-to-One: Each session represents one user's authentication state