# Data Model: Full-stack Integration for Frontend and Backend Services

## Overview
This document describes the key data entities involved in the full-stack integration of the Todo application. Since the integration primarily involves configuration and communication between existing services, the data model focuses on the entities that are already defined in the existing application.

## Key Entities

### User
Represents an authenticated user with JWT-based access control.

**Fields**:
- id: UUID (Primary Key)
- email: String (Unique, Required)
- name: String (Optional)
- created_at: DateTime
- updated_at: DateTime

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Name, if provided, must be between 1 and 100 characters

**Relationships**:
- One-to-Many: User has many Tasks

### Task
Represents a task entity with user ownership and CRUD operations.

**Fields**:
- id: UUID (Primary Key)
- title: String (Required)
- description: Text (Optional)
- completed: Boolean (Default: false)
- user_id: UUID (Foreign Key to User)
- created_at: DateTime
- updated_at: DateTime

**Validation Rules**:
- Title must be between 1 and 200 characters
- User_id must reference an existing User
- Only the owner can modify their tasks

**Relationships**:
- Many-to-One: Task belongs to a User

### JWT Token
Stateless authentication token with user identity and permissions.

**Fields**:
- sub: String (Subject - user ID)
- exp: Integer (Expiration timestamp)
- iat: Integer (Issued at timestamp)
- permissions: Array (Optional permissions)

**Validation Rules**:
- Token must not be expired
- User referenced in token must exist
- Token must be signed with the correct secret

### Environment Configuration
Collection of variables that control API endpoints, authentication secrets, and database connections.

**Fields**:
- BETTER_AUTH_SECRET: String (Required, Shared secret)
- BETTER_AUTH_URL: String (Frontend auth URL)
- DATABASE_URL: String (Backend database connection)
- NEXT_PUBLIC_API_URL: String (Frontend API endpoint)

**Validation Rules**:
- BETTER_AUTH_SECRET must be consistent across services
- URLs must be valid and accessible
- DATABASE_URL must allow successful connection

### Docker Compose Service
Containerized service definition for running frontend and backend together.

**Fields**:
- service_name: String (frontend or backend)
- image: String (Docker image)
- ports: Array (Port mappings)
- environment: Object (Environment variables)
- depends_on: Array (Service dependencies)

**Validation Rules**:
- Port mappings must not conflict
- Environment variables must be properly formatted
- Dependencies must be resolvable