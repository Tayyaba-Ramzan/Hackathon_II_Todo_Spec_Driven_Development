# Feature Specification: Full-stack Integration for Frontend and Backend Services

**Feature Branch**: `006-fullstack-integration`
**Created**: 2026-01-06
**Status**: Draft
**Input**: User description: "You are an Expert Full-Stack Integration Agent for the Hackathon Todo Phase II project. Frontend and backend are already built. Your only task is to make them work together as a complete full-stack application. Strictly follow the project documentation and .env values: - BETTER_AUTH_SECRET = Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk (same for both services) - Frontend BETTER_AUTH_URL = http://localhost:3000 - Backend DATABASE_URL = postgresql://neondb_owner:npg_PI27GCiafTWl@ep-divine-hall-a4exapdh-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require - Frontend API calls go to http://localhost:8000/api/... (local) or backend service in docker Tasks to complete integration: 1. Create or update .env files in root, frontend, and backend with correct variables 2. Update frontend/lib/api.ts or config to point to backend URL (use NEXT_PUBLIC_API_URL=http://localhost:8000 locally) 3. Add CORS middleware in backend/main.py to allow frontend origin[](http://localhost:3000) 4. Create docker-compose.yml in root to run both services: - frontend on port 3000 - backend on port 8000 - backend depends_on database if needed, but use Neon external - shared network, environment variables injected 5. Ensure JWT flow works: frontend login → gets token → sends Bearer → backend verifies with same secret 6. Test full user flow works end-to-end Output: - Updated or new .env files - Updated frontend config for API URL - Updated backend/main.py with CORS Do only integration and configuration — no new features or UI changes. Output clean, ready-to-use files with paths."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Full Application (Priority: P1)

As a user, I want to access the frontend application and have it communicate seamlessly with the backend API so that I can perform all todo operations without any connectivity issues.

**Why this priority**: This is the foundational requirement for the application to function as a complete product. Without proper frontend-backend communication, the entire application is unusable.

**Independent Test**: The frontend application should load properly and be able to make API calls to the backend, retrieve data, and perform CRUD operations on todo items.

**Acceptance Scenarios**:

1. **Given** the frontend and backend services are running, **When** a user accesses the frontend application, **Then** the application loads without errors and can communicate with the backend API
2. **Given** a user is on the frontend application, **When** they perform any todo operation (create, read, update, delete), **Then** the operation is successfully processed by the backend and reflected in the UI

---

### User Story 2 - Authenticate and Maintain Session (Priority: P1)

As a user, I want to log in through the frontend and have my authentication token properly validated by the backend so that I can securely access my todo data.

**Why this priority**: Authentication is critical for user data security and proper isolation between users. Without this, the application cannot provide secure access to user data.

**Independent Test**: A user can log in through the frontend, receive a JWT token, and use that token to access backend resources with proper authentication and authorization.

**Acceptance Scenarios**:

1. **Given** a user enters valid credentials, **When** they submit the login form, **Then** they receive a valid JWT token and gain access to their todo data
2. **Given** a user has a valid JWT token, **When** they make API requests to the backend, **Then** the backend validates the token and grants appropriate access to resources

---

### User Story 3 - Run Application via Docker (Priority: P2)

As a developer, I want to run the complete application stack using a single command so that I can easily set up the development environment and test the integrated system.

**Why this priority**: This enables consistent development and deployment environments, making it easier for team members to work on the integrated application.

**Independent Test**: Running `docker-compose up` should start both frontend and backend services with proper configuration and connectivity.

**Acceptance Scenarios**:

1. **Given** the docker-compose.yml file exists with proper configuration, **When** a developer runs `docker-compose up`, **Then** both frontend and backend services start successfully and can communicate with each other
2. **Given** the services are running in Docker, **When** a user accesses the frontend, **Then** the application functions as expected with backend API connectivity

---

### User Story 4 - Environment Configuration (Priority: P2)

As a developer, I want proper environment configuration across all application layers so that the application works consistently across different deployment environments.

**Why this priority**: Proper environment configuration is essential for the application to work correctly in different environments (development, staging, production).

**Independent Test**: The application can be configured with environment variables that control API endpoints, authentication secrets, and database connections.

**Acceptance Scenarios**:

1. **Given** environment variables are properly set, **When** the application starts, **Then** it connects to the correct backend API and database
2. **Given** the application is running, **When** environment variables change, **Then** the application behavior adapts accordingly (e.g., connecting to different API endpoints)

---

### User Story 5 - Cross-Origin Resource Sharing (Priority: P3)

As a user, I want the frontend to communicate with the backend API without CORS issues so that the application functions properly in web browsers.

**Why this priority**: While important for web functionality, this is a technical requirement that supports the primary user stories.

**Independent Test**: API requests from the frontend origin are accepted by the backend without CORS errors.

**Acceptance Scenarios**:

1. **Given** the frontend is running on http://localhost:3000, **When** it makes API requests to the backend, **Then** the requests are accepted without CORS errors
2. **Given** a user performs actions in the frontend, **When** those actions trigger API calls, **Then** the calls succeed without browser security errors

---

### Edge Cases

- What happens when the backend service is temporarily unavailable?
- How does the system handle expired JWT tokens during API requests?
- What occurs if environment variables are missing or incorrectly configured?
- How does the application behave when CORS configuration changes?

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
- **FR-009**: System MUST have environment configuration files (.env) in root, frontend, and backend directories with proper variables
- **FR-010**: System MUST configure frontend to point to backend API at http://localhost:8000
- **FR-011**: System MUST implement CORS middleware in backend to allow frontend origin at http://localhost:3000
- **FR-012**: System MUST include a docker-compose.yml file that runs both frontend and backend services
- **FR-013**: System MUST ensure JWT tokens issued by frontend auth are validated by backend with the same secret
- **FR-014**: System MUST allow end-to-end testing of complete user flow from login to task operations
- **FR-015**: System MUST maintain consistent BETTER_AUTH_SECRET across frontend and backend services
- **FR-016**: System MUST configure database connection using provided Neon PostgreSQL URL

### Key Entities *(include if feature involves data)*

- **[User]**: Represents an authenticated user with JWT-based access control
- **[Task]**: Represents a task entity with user ownership and CRUD operations
- **[JWT Token]**: Stateless authentication token with user identity and permissions
- **[Environment Configuration]**: Collection of variables that control API endpoints, authentication secrets, and database connections
- **[Docker Compose Service]**: Containerized service definition for running frontend and backend together

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully log in through the frontend and access backend API endpoints without CORS errors
- **SC-002**: The complete application stack (frontend + backend) can be started with a single docker-compose command
- **SC-003**: All API calls from frontend to backend complete successfully with proper JWT authentication
- **SC-004**: End-to-end user flow (login → view tasks → create/update/delete tasks) completes without connectivity or authentication errors