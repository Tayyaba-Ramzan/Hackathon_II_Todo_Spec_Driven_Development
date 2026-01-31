# Implementation Plan: Full-stack Integration for Frontend and Backend Services

**Branch**: `006-fullstack-integration` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-fullstack-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the integration of frontend and backend services to create a complete full-stack application. The primary requirement is to connect the existing frontend (Next.js) and backend (FastAPI) applications with proper environment configuration, API communication, CORS setup, and JWT authentication flow. The technical approach involves updating environment files, configuring API endpoints, implementing CORS middleware, creating a docker-compose file, and ensuring the JWT flow works correctly between services.

## Technical Context

**Language/Version**: Python 3.11 (Backend/FastAPI), TypeScript/JavaScript (Frontend/Next.js 16+)
**Primary Dependencies**: Next.js 16+ App Router, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, JWT
**Storage**: Neon PostgreSQL database with external connection
**Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Web application (Linux/Mac/Windows compatible)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <200ms API response time, <3s frontend load time
**Constraints**: JWT-based authentication, CORS configuration for localhost:3000 to localhost:8000, shared BETTER_AUTH_SECRET
**Scale/Scope**: Single application with frontend and backend components, multi-user support with data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-driven: All work starts and ends with /specs/
- [x] No manual coding: Only AI agents (Qwen CLI) edit code
- [x] Strict user isolation via JWT + DB filtering
- [x] Stateless JWT auth with shared BETTER_AUTH_SECRET
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── models/
│   ├── __init__.py
│   └── user_task.py
├── api/
│   ├── __init__.py
│   └── tasks.py
├── auth/
│   └── jwt.py
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── lib/
├── next.config.js
├── package.json
└── .env.local

specs/
└── 006-fullstack-integration/
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    ├── contracts/
    └── tasks.md

root/
├── .env
├── .env.example
├── docker-compose.yml
└── README.md
```

**Structure Decision**: Web application structure with separate frontend and backend services, following the monorepo pattern required by the constitution. The integration work will focus on environment configuration, API communication, and authentication flow between the two services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
