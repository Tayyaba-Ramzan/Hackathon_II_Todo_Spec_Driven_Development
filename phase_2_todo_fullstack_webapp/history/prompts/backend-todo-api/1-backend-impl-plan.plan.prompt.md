---
id: 1
title: backend-impl-plan
stage: plan
date: 2026-01-06
model: Qwen
feature: backend-todo-api
branch: 005-backend-todo-api
user: USER
command: /sp.plan
labels: ["plan", "backend", "todo-api", "fastapi", "jwt", "sqlmodel"]
links:
  spec: specs/005-backend-todo-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-backend-todo-api/plan.md
  - specs/005-backend-todo-api/research.md
  - specs/005-backend-todo-api/data-model.md
  - specs/005-backend-todo-api/quickstart.md
  - specs/005-backend-todo-api/contracts/task-api-contract.md
tests: []
outcome: "Complete backend implementation plan created with all required artifacts"
evaluation: "Plan includes research, data models, API contracts, quickstart guide, and constitution compliance"
---

# Prompt

Complete Backend Implementation for Phase II Todo App
Create: Project structure, database models, session dependency, JWT verification middleware, task routes, error handling, and full integration with frontend
Decisions needing documentation:

JWT library: PyJWT vs python-jose (choose PyJWT for simplicity and wide adoption; trade-off: python-jose has better JOSE support but overkill for simple HS256)
Dependency injection: get_current_user as dependency vs manual check in each route (dependency for DRY code and consistency)
Route organization: single tasks.py file vs separate files per operation (single tasks.py for simplicity in small project)
Error responses: custom JSON format vs default HTTPException (default FastAPI format for consistency with frontend expectations)
Query param handling: status filter default "all" vs "pending" (default "all" to show everything on dashboard load)
Token validation: strict user_id matching vs permissive (strict matching required for security as per documentation)
Testing strategy: Validation checks based on success criteria
Manual testing: Use frontend to signup/login → copy JWT → test all endpoints in Postman/Insomnia with Bearer token
Positive cases: Create, list, get, update, toggle, delete own tasks → 200/201 success
Negative cases: Missing token → 401, invalid token → 401, wrong user_id in path → 401/403, access other user's task → 404 or empty list
Database verification: Check Neon DB directly that tasks have correct user_id foreign key
Integration: Full flow from frontend works without errors
Technical details:
Use PyJWT for JWT decoding/verification with BETTER_AUTH_SECRET from env
DATABASE_URL = NEON_DB_URL from env
SQLModel models: Task with user_id ForeignKey to users.id (string)
Indexes on tasks.user_id and tasks.completed
Async SQLModel session in db.py
get_db dependency yields session
get_current_user dependency: extract token, verify, return user_id, raise 401 if invalid
All routes depend on get_current_user and get_db
Filter Task.select().where(Task.user_id == current_user_id)
Validation: title str min_length=1 max_length=200, description optional max 1000
Organize by phases:
Project Structure & Dependencies (main.py, db.py, models.py)
Database Models & Session (SQLModel setup with Neon)
JWT Verification Middleware/Dependency
Task CRUD Routes Implementation (routes/tasks.py)
Error Handling & Validation
Integration Testing with Frontend JWT

# Response

Successfully created a comprehensive implementation plan for the Complete Backend Implementation for Phase II Todo App. The plan includes:

1. Updated implementation plan (plan.md) with technical context, constitution check, and project structure
2. Research document (research.md) covering key architectural decisions:
   - JWT library choice (PyJWT)
   - Dependency injection patterns
   - Route organization
   - Error response format
   - Query parameter defaults
   - Token validation strictness
3. Data model specification (data-model.md) defining User and Task entities
4. API contract (contracts/task-api-contract.md) detailing all 6 required endpoints
5. Quickstart guide (quickstart.md) for developers implementing the backend
6. Updated agent context to include the new technology stack

All constitution requirements have been verified and satisfied. The plan is ready for the task breakdown phase.