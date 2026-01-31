---

description: "Task list for In-Memory Todo CLI App implementation"
---

# Tasks: In-Memory Todo CLI App

**Input**: Design documents from `/specs/002-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/
- [X] T002 Initialize Python 3.13+ project with pyproject.toml dependencies
- [X] T003 [P] Create __init__.py files in all directories: src/__init__.py, src/cli/__init__.py, src/models/__init__.py, src/services/__init__.py, src/lib/__init__.py
- [X] T004 [P] Create test directory structure: tests/__init__.py, tests/unit/__init__.py, tests/integration/__init__.py, tests/contract/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T005 Create Todo model in src/models/todo.py
- [X] T006 [P] Create InMemoryStorage in src/lib/storage.py
- [X] T007 Create TodoService in src/services/todo_service.py
- [X] T008 Create CLI menu structure in src/cli/main.py
- [X] T009 [P] Create entry point in src/entry_point.py
- [X] T010 Update pyproject.toml with console script entry point

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Todo Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo tasks with title and description, storing them in memory with unique ID and default incomplete status

**Independent Test**: Can be fully tested by adding a new task with a title and description, and verifying it appears in the task list with a unique ID and incomplete status

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T011 [P] [US1] Unit test for Todo model in tests/unit/test_models.py
- [ ] T012 [P] [US1] Unit test for TodoService.add_task in tests/unit/test_services.py
- [ ] T013 [P] [US1] Contract test for add command in tests/contract/test_contracts.py

### Implementation for User Story 1

- [X] T014 [US1] Implement Todo model with id, title, description, completed fields in src/models/todo.py
- [X] T015 [US1] Implement add_task method in TodoService in src/services/todo_service.py
- [X] T016 [US1] Implement add command handler in CLI in src/cli/main.py
- [X] T017 [US1] Add validation for empty titles in TodoService
- [X] T018 [US1] Add CLI input validation for add command

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Todo Tasks (Priority: P1)

**Goal**: Enable users to view all their todo tasks with ID, title, description, and completion status

**Independent Test**: Can be fully tested by adding tasks and then viewing the complete list with all relevant information displayed clearly

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T019 [P] [US2] Unit test for TodoService.get_all_tasks in tests/unit/test_services.py
- [ ] T020 [P] [US2] Contract test for view command in tests/contract/test_contracts.py

### Implementation for User Story 2

- [X] T021 [US2] Implement get_all_tasks method in TodoService in src/services/todo_service.py
- [X] T022 [US2] Implement view command handler in CLI in src/cli/main.py
- [X] T023 [US2] Format output to show ID, title, description, and status in CLI
- [X] T024 [US2] Handle case when no tasks exist in CLI

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Existing Todo Task (Priority: P2)

**Goal**: Enable users to update the title and/or description of existing tasks by providing the task ID

**Independent Test**: Can be fully tested by updating a task's title and/or description and verifying the changes are reflected when viewing the task

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US3] Unit test for TodoService.update_task in tests/unit/test_services.py
- [ ] T026 [P] [US3] Contract test for update command in tests/contract/test_contracts.py

### Implementation for User Story 3

- [X] T027 [US3] Implement update_task method in TodoService in src/services/todo_service.py
- [X] T028 [US3] Implement update command handler in CLI in src/cli/main.py
- [X] T029 [US3] Add validation for updating non-existent tasks
- [X] T030 [US3] Add CLI input validation for update command

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Todo Task (Priority: P2)

**Goal**: Enable users to remove tasks by providing the task ID

**Independent Test**: Can be fully tested by deleting a task and verifying it no longer appears in the task list

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T031 [P] [US4] Unit test for TodoService.delete_task in tests/unit/test_services.py
- [ ] T032 [P] [US4] Contract test for delete command in tests/contract/test_contracts.py

### Implementation for User Story 4

- [X] T033 [US4] Implement delete_task method in TodoService in src/services/todo_service.py
- [X] T034 [US4] Implement delete command handler in CLI in src/cli/main.py
- [X] T035 [US4] Add validation for deleting non-existent tasks
- [X] T036 [US4] Add CLI input validation for delete command

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Enable users to mark tasks as complete or incomplete by providing the task ID

**Independent Test**: Can be fully tested by marking a task as complete/incomplete and verifying the status change is reflected in the task list

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US5] Unit test for TodoService.mark_task_complete in tests/unit/test_services.py
- [ ] T038 [P] [US5] Unit test for TodoService.mark_task_incomplete in tests/unit/test_services.py
- [ ] T039 [P] [US5] Contract test for complete command in tests/contract/test_contracts.py
- [ ] T040 [P] [US5] Contract test for incomplete command in tests/contract/test_contracts.py

### Implementation for User Story 5

- [X] T041 [US5] Implement mark_task_complete method in TodoService in src/services/todo_service.py
- [X] T042 [US5] Implement mark_task_incomplete method in TodoService in src/services/todo_service.py
- [X] T043 [US5] Implement complete command handler in CLI in src/cli/main.py
- [X] T044 [US5] Implement incomplete command handler in CLI in src/cli/main.py
- [X] T045 [US5] Add validation for marking non-existent tasks
- [X] T046 [US5] Add CLI input validation for complete/incomplete commands

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T047 [P] Documentation updates in README.md
- [X] T048 Code cleanup and refactoring
- [ ] T049 [P] Additional unit tests in tests/unit/
- [X] T050 Error handling and validation across all commands
- [X] T051 Run quickstart.md validation
- [ ] T052 Integration tests for end-to-end functionality in tests/integration/test_end_to_end.py

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
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3/US4 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Todo model in tests/unit/test_models.py"
Task: "Unit test for TodoService.add_task in tests/unit/test_services.py"
Task: "Contract test for add command in tests/contract/test_contracts.py"

# Launch all models for User Story 1 together:
Task: "Create Todo model in src/models/todo.py"
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