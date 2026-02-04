# Tasks: Better Auth Integration for Phase II Todo Frontend

**Input**: Design documents from `/specs/004-better-auth-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Install Better Auth library and JWT plugin dependencies in frontend
- [X] T002 [P] Create auth configuration file at frontend/src/auth/auth.ts with JWT plugin enabled
- [X] T003 [P] Set up BETTER_AUTH_SECRET environment variable in .env.local
- [X] T004 Create directory structure for auth pages: frontend/src/app/(auth)/login and frontend/src/app/(auth)/signup

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Configure Better Auth with JWT plugin and 7-day expiration in auth.ts
- [X] T006 [P] Create API client wrapper in frontend/src/lib/api.ts to handle JWT token attachment
- [X] T007 [P] Implement session management utilities for handling JWT tokens
- [X] T008 Create base UI components for auth forms with Tailwind styling
- [X] T009 Set up error handling utilities for auth operations
- [X] T010 Configure dark mode compatibility for auth UI components

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable new users to sign up and sign in to the Todo application with JWT-based authentication

**Independent Test**: A user can complete the signup flow and verify they can sign in with their credentials, with JWT tokens properly issued and stored.

### Implementation for User Story 1

- [X] T011 [P] [US1] Create signup page component at frontend/src/app/(auth)/signup/page.tsx
- [X] T012 [P] [US1] Create login page component at frontend/src/app/(auth)/login/page.tsx
- [X] T013 [US1] Implement signup form with email and password fields using Better Auth
- [X] T014 [US1] Implement login form with email and password fields using Better Auth
- [X] T015 [US1] Add form validation for email and password requirements
- [X] T016 [US1] Add error handling and user feedback for auth operations
- [X] T017 [US1] Implement redirect to dashboard after successful authentication
- [X] T018 [US1] Test signup flow: user enters credentials → account created → JWT token issued
- [X] T019 [US1] Test login flow: user enters credentials → authenticated → JWT token issued

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Secure API Access with JWT (Priority: P1)

**Goal**: Ensure authenticated users can make API calls that include their JWT token in the Authorization header

**Independent Test**: Can be tested by making API calls from the frontend and verifying that JWT tokens are automatically attached to requests and validated by the backend.

### Implementation for User Story 2

- [X] T020 [P] [US2] Update API client in frontend/src/lib/api.ts to include JWT token in headers
- [X] T021 [US2] Implement token retrieval from Better Auth session for API calls
- [X] T022 [US2] Add 401 error handling to redirect to login when token is invalid/expired
- [X] T023 [US2] Test API calls with valid JWT: authenticated user → token attached → request succeeds
- [X] T024 [US2] Test API calls with invalid JWT: invalid token → 401 response → redirect to login

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Protected Route Navigation (Priority: P2)

**Goal**: Automatically redirect unauthenticated users to the login page when attempting to access protected routes

**Independent Test**: Can be tested by attempting to access protected routes both when authenticated and unauthenticated, verifying correct redirection behavior.

### Implementation for User Story 3

- [X] T025 [P] [US3] Create server component to check authentication status in dashboard page
- [X] T026 [US3] Implement redirect logic to /login for unauthenticated users accessing protected routes
- [X] T027 [US3] Add session check using auth.api.getSession() in protected pages
- [X] T028 [US3] Test unauthenticated access: user not logged in → attempts to access dashboard → redirected to login
- [X] T029 [US3] Test authenticated access: user logged in → accesses dashboard → content displayed

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Session Data Availability (Priority: P2)

**Goal**: Make session data (user_id, email) available in server components for personalized content rendering

**Independent Test**: Can be tested by verifying that server components have access to user session data when a user is authenticated.

### Implementation for User Story 4

- [X] T030 [P] [US4] Update dashboard page to display user session data (user_id, email)
- [X] T031 [US4] Implement server-side session data retrieval using Better Auth
- [X] T032 [US4] Add graceful handling when session data is not available
- [X] T033 [US4] Test session data availability: authenticated user → session data displayed in header
- [X] T034 [US4] Test session handling: unauthenticated user → no session data displayed gracefully

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T035 [P] Add logout functionality with proper token cleanup
- [X] T036 [P] Ensure all auth pages have consistent Tailwind styling and dark mode support
- [X] T037 Add responsive design for auth pages on mobile devices
- [X] T038 Add smooth hover and focus effects for better UX
- [X] T039 [P] Implement proper error boundaries for auth components
- [X] T040 Run complete flow validation: Signup → Login → Dashboard → API Call → Logout
- [X] T041 Update documentation with auth implementation details

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
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
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
# Launch all components for User Story 1 together:
Task: "Create signup page component at frontend/src/app/(auth)/signup/page.tsx"
Task: "Create login page component at frontend/src/app/(auth)/login/page.tsx"
Task: "Implement signup form with email and password fields using Better Auth"
Task: "Implement login form with email and password fields using Better Auth"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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