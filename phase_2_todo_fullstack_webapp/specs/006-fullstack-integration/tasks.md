# Tasks: Full-stack Integration for Frontend and Backend Services

**Input**: Design documents from `/specs/006-fullstack-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/`, `root/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create/update .env file in root with BETTER_AUTH_SECRET, NEXT_PUBLIC_BETTER_AUTH_URL, DATABASE_URL, NEXT_PUBLIC_API_URL
- [X] T002 [P] Create/update .env.local file in frontend/ with BETTER_AUTH_SECRET, NEXT_PUBLIC_BETTER_AUTH_URL, NEXT_PUBLIC_API_URL
- [X] T003 [P] Create/update .env file in backend/ with BETTER_AUTH_SECRET, DATABASE_URL
- [X] T004 Update docker-compose.yml in root to include both frontend and backend services with proper environment variables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [P] Configure CORS middleware in backend/main.py to allow requests from http://localhost:3000
- [X] T006 [P] Update frontend API configuration to point to backend API at http://localhost:8000
- [X] T007 [P] Verify JWT authentication flow works with shared BETTER_AUTH_SECRET between frontend and backend
- [X] T008 [P] Update backend API endpoints to follow /api/{user_id}/tasks/* pattern with JWT validation
- [X] T009 Test basic connectivity between frontend and backend services

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Full Application (Priority: P1) 🎯 MVP

**Goal**: Enable frontend application to communicate seamlessly with backend API for all todo operations

**Independent Test**: The frontend application should load properly and be able to make API calls to the backend, retrieve data, and perform CRUD operations on todo items.

### Implementation for User Story 1

- [X] T010 [P] [US1] Update frontend API service to use NEXT_PUBLIC_API_URL for all backend calls
- [X] T011 [US1] Test frontend can successfully fetch tasks from backend API
- [X] T012 [US1] Test frontend can successfully create tasks via backend API
- [X] T013 [US1] Test frontend can successfully update tasks via backend API
- [X] T014 [US1] Test frontend can successfully delete tasks via backend API
- [X] T015 [US1] Verify all API responses are handled correctly in the frontend

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Authenticate and Maintain Session (Priority: P1)

**Goal**: Enable login through the frontend with JWT token validation by the backend for secure access to todo data

**Independent Test**: A user can log in through the frontend, receive a JWT token, and use that token to access backend resources with proper authentication and authorization.

### Implementation for User Story 2

- [X] T016 [P] [US2] Configure frontend authentication to use BETTER_AUTH_URL and shared BETTER_AUTH_SECRET
- [X] T017 [US2] Verify JWT token received from frontend login can be validated by backend
- [X] T018 [US2] Test that authenticated requests include proper Bearer token in Authorization header
- [X] T019 [US2] Verify backend properly validates JWT tokens using shared secret
- [X] T020 [US2] Test user data isolation - users can only access their own tasks via user_id validation
- [X] T021 [US2] Test expired token handling and refresh mechanism

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Run Application via Docker (Priority: P2)

**Goal**: Enable running the complete application stack using a single docker-compose command

**Independent Test**: Running `docker-compose up` should start both frontend and backend services with proper configuration and connectivity.

### Implementation for User Story 3

- [X] T022 [P] [US3] Update docker-compose.yml to properly configure frontend service on port 3000
- [X] T023 [P] [US3] Update docker-compose.yml to properly configure backend service on port 8000
- [X] T024 [US3] Configure docker-compose.yml to inject environment variables to both services
- [X] T025 [US3] Test that services can communicate when running in Docker
- [X] T026 [US3] Verify frontend can access backend API when both running in Docker
- [X] T027 [US3] Test complete user flow works when running via docker-compose

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Environment Configuration (Priority: P2)

**Goal**: Ensure proper environment configuration across all application layers for consistent behavior across different deployment environments

**Independent Test**: The application can be configured with environment variables that control API endpoints, authentication secrets, and database connections.

### Implementation for User Story 4

- [X] T028 [P] [US4] Verify environment variables are properly loaded in frontend application
- [X] T029 [P] [US4] Verify environment variables are properly loaded in backend application
- [X] T030 [US4] Test that changing environment variables affects application behavior correctly
- [X] T031 [US4] Verify BETTER_AUTH_SECRET is consistent across frontend and backend
- [X] T032 [US4] Test API endpoint configuration via NEXT_PUBLIC_API_URL
- [X] T033 [US4] Verify database connection using DATABASE_URL

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 7: User Story 5 - Cross-Origin Resource Sharing (Priority: P3)

**Goal**: Enable frontend to communicate with backend API without CORS issues in web browsers

**Independent Test**: API requests from the frontend origin are accepted by the backend without CORS errors.

### Implementation for User Story 5

- [X] T034 [P] [US5] Verify CORS configuration allows requests from http://localhost:3000
- [X] T035 [US5] Test that API requests from frontend don't trigger CORS errors
- [X] T036 [US5] Verify preflight OPTIONS requests are handled correctly
- [X] T037 [US5] Test various HTTP methods (GET, POST, PUT, DELETE) work without CORS issues
- [X] T038 [US5] Verify credentials and headers are properly allowed in CORS configuration

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T039 [P] Update README.md with integration instructions
- [X] T040 Update .env.example with all required environment variables
- [X] T041 Test complete end-to-end user flow from login to task operations
- [X] T042 Verify all security requirements are met (JWT validation, user isolation)
- [X] T043 Run quickstart.md validation to ensure all steps work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tasks for User Story 1 together:
Task: "Update frontend API service to use NEXT_PUBLIC_API_URL for all backend calls"
Task: "Test frontend can successfully fetch tasks from backend API"
Task: "Test frontend can successfully create tasks via backend API"
Task: "Test frontend can successfully update tasks via backend API"
Task: "Test frontend can successfully delete tasks via backend API"
Task: "Verify all API responses are handled correctly in the frontend"
```

---

## Implementation Strategy

### MVP First (User Stories 1 and 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence