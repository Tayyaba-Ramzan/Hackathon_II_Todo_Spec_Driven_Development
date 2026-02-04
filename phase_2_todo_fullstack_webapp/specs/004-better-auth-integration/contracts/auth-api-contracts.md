# Authentication API Contracts

## User Signup
**Endpoint**: `POST /api/auth/signup`
**Description**: Creates a new user account and returns a JWT token
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Response (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_12345",
    "email": "user@example.com"
  }
}
```
**Response (400)**: Invalid input
**Response (409)**: User already exists

## User Login
**Endpoint**: `POST /api/auth/login`
**Description**: Authenticates a user and returns a JWT token
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```
**Response (200)**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user_12345",
    "email": "user@example.com"
  }
}
```
**Response (400)**: Invalid input
**Response (401)**: Invalid credentials

## User Logout
**Endpoint**: `POST /api/auth/logout`
**Description**: Invalidates the user's session/JWT token
**Headers**: 
- Authorization: Bearer {token}
**Response (200)**: 
```json
{
  "message": "Successfully logged out"
}
```

## Get Session
**Endpoint**: `GET /api/auth/session`
**Description**: Retrieves the current user's session information
**Headers**: 
- Authorization: Bearer {token}
**Response (200)**:
```json
{
  "user": {
    "id": "user_12345",
    "email": "user@example.com"
  },
  "expires_at": "2026-01-12T10:00:00Z"
}
```
**Response (401)**: Invalid or expired token

## API Client with JWT
**Description**: All API calls to user-specific endpoints must include the JWT token
**Headers for user-specific endpoints** (e.g., `/api/{user_id}/tasks/*`):
- Authorization: Bearer {token}
**Response (401)**: If token is missing, invalid, or expired