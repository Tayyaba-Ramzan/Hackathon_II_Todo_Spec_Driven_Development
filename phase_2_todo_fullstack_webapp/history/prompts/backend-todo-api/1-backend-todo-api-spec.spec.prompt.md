---
id: 1
title: backend-todo-api-spec
stage: spec
date: 2026-01-06
model: Qwen
feature: backend-todo-api
branch: 005-backend-todo-api
user: USER
command: /sp.specify
labels: ["spec", "backend", "todo-api", "fastapi"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-backend-todo-api/spec.md
  - specs/005-backend-todo-api/checklists/requirements.md
tests: []
outcome: "Specification created successfully with all required sections"
evaluation: "Specification meets all quality criteria and is ready for planning phase"
---

# Prompt

Complete Backend Implementation for Phase II Todo App Target audience: Developers building the backend in the Hackathon Todo monorepo using Qwen CLI and agentic workflow Focus: Build a fully functional FastAPI backend with SQLModel, Neon PostgreSQL integration, JWT verification middleware, and complete task CRUD API that enforces user isolation and integrates seamlessly with the frontend Success criteria: All 6 REST API endpoints implemented exactly as specified: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE/PATCH /api/{user_id}/tasks/{id} JWT middleware correctly verifies tokens using BETTER_AUTH_SECRET, extracts user_id, and matches it with path {user_id} All database queries filtered by authenticated user_id — zero possibility of cross-user data access Database connection using DATABASE_URL from environment (Neon PostgreSQL) with SQLModel sessions Proper Pydantic request/response models, validation (title 1-200 chars, description ≤1000), and HTTPException error handling Support query params on list endpoint (status: all/pending/completed) Full integration test: Frontend JWT token accepted, tasks created/viewed/updated/deleted only for authenticated user Backend runs with uvicorn main:app --reload and works with docker-compose Constraints: Use Python FastAPI, SQLModel ORM only Project structure: backend/main.py, models.py, db.py, routes/ folder Environment variables: BETTER_AUTH_SECRET (same as frontend), DATABASE_URL from NEON_DB_URL JWT verification using PyJWT or python-jose, shared secret only — no database sessions All routes under /api/, async where possible Reference @backend/QWEN.md (or CLAUDE.md), @specs/api/rest-endpoints.md, @specs/database/schema.md Implement via Backend Agent iterations only — no manual coding Not building: Frontend changes (auth pages, UI) Advanced features (due dates, sorting beyond status, pagination) Admin panel or user management endpoints Email verification or password reset flows

# Response

Created a comprehensive feature specification for the backend todo API implementation with the following key elements:

1. User Scenarios & Testing:
   - Created 5 prioritized user stories covering task creation, viewing, updating, deletion, and secure access
   - Defined acceptance scenarios for each user story
   - Identified edge cases for error handling

2. Requirements:
   - 28 functional requirements covering all aspects of the backend implementation
   - Key entities identified (User, Task, JWT Token, Database, API Endpoint)

3. Success Criteria:
   - 10 measurable outcomes that can be verified without implementation details

4. Quality Validation:
   - Created a checklist to validate specification completeness
   - All quality criteria have been met

The specification is ready for the planning phase and follows the spec-driven development approach required for this project.