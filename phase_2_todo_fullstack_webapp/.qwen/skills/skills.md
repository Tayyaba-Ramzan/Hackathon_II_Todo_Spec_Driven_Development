# Project Skills Catalog

---
name: task-crud-implementation  
description: Implement full Task CRUD operations across frontend and backend with proper user isolation and JWT authentication.  
---
# Task CRUD Implementation Skill
## When to Use
- User wants to add create/read/update/delete/mark-complete functionality
- Implementing core todo features in the web app
- Ensuring tasks are tied to authenticated user only

## How to Execute
1. Read @specs/features/task-crud.md and @specs/api/rest-endpoints.md
2. Use Backend Tasks CRUD Agent to implement all 6 REST endpoints
3. Use Frontend Main Agent + UI Agent to build TaskList, TaskCard, TaskForm
4. Ensure every operation filters by authenticated user_id from JWT
5. Add basic validation (title required, length limits)

## Output Format
- Updated backend/routes/tasks.py with all endpoints
- Updated frontend/components/TaskList.tsx, TaskCard.tsx, TaskForm.tsx
- Working dashboard page showing only user's tasks
- Confirmation that user isolation is enforced

---
name: better-auth-jwt-setup  
description: Set up Better Auth with JWT plugin on frontend and JWT verification middleware on backend using shared secret.  
---
# Better Auth + JWT Setup Skill
## When to Use
- Starting authentication implementation
- Need stateless auth between Next.js and FastAPI
- Multi-user isolation is required

## How to Execute
1. Read @specs/features/authentication.md
2. Configure Better Auth in frontend/auth.ts with JWT plugin and BETTER_AUTH_SECRET
3. Implement JWT verification middleware in backend (dependencies.py + get_current_user)
4. Ensure frontend API client attaches Bearer token automatically
5. Test login → token issued → API calls succeed

## Output Format
- frontend/auth.ts with JWT plugin enabled
- backend/dependencies.py with get_current_user dependency
- Updated /lib/api.ts to attach Authorization header
- Working login flow with protected routes

---
name: database-schema-management  
description: Manage database models, schema updates, and migrations for users and tasks tables.  
---
# Database Schema Management Skill
## When to Use
- Adding new fields to tasks (e.g., due_date)
- Defining relationships and indexes
- Syncing SQLModel models with Neon PostgreSQL

## How to Execute
1. Read @specs/database/schema.md
2. Update models.py with SQLModel classes (User, Task)
3. Add foreign key user_id → users.id
4. Define indexes on user_id and completed
5. Update schema.md documentation

## Output Format
- Updated backend/models.py
- Updated @specs/database/schema.md
- Proper indexes and defaults (created_at, updated_at)

---
name: frontend-ui-polish  
description: Build and refine responsive, beautiful UI components using Tailwind CSS.  
---
# Frontend UI Polish Skill
## When to Use
- Components look basic or inconsistent
- Need mobile-responsive design
- Adding loading states, modals, or toast notifications

## How to Execute
1. Read @specs/ui/components.md and @frontend/QWEN.md
2. Use Frontend UI Agent
3. Implement reusable components with Tailwind
4. Add loading skeletons and error messages
5. Ensure mobile-first and accessible

## Output Format
- Polished TaskCard, TaskForm, Header components
- Responsive grid/list views
- Loading and error states
- Consistent Tailwind styling across app

---
name: api-client-centralization  
description: Create and maintain a single typed API client for all backend calls with JWT handling.  
---
# API Client Centralization Skill
## When to Use
- Multiple pages/components making direct fetch calls
- JWT not being attached consistently
- Need typed functions for all endpoints

## How to Execute
1. Read @specs/api/rest-endpoints.md
2. Implement /lib/api.ts with fetchWithAuth wrapper
3. Add typed methods for all 6 task endpoints
4. Handle 401 errors gracefully

## Output Format
- Complete frontend/lib/api.ts
- All pages/components importing from api
- Automatic JWT attachment and error handling

---
name: integration-testing  
description: Write integration and E2E tests to verify full-stack behavior, especially auth and user isolation.  
---
# Integration Testing Skill
## When to Use
- After major features (auth, CRUD)
- Need confidence that frontend + backend work together
- Preventing regressions in user data isolation

## How to Execute
1. Use Integration Main Agent + sub-agents
2. Write pytest integration tests for API with real JWT
3. Write Playwright E2E tests for browser flows
4. Include negative tests (accessing other user's tasks)

## Output Format
- tests/integration/test_tasks_crud.py
- tests/e2e/dashboard.spec.ts
- Tests covering auth flow, CRUD, and security isolation
- Passing test report

---
name: protected-route-handling  
description: Implement route protection and redirects for authenticated vs unauthenticated users.  
---
# Protected Route Handling Skill
## When to Use
- Users can access dashboard without login
- Need proper redirects (unauth → login, auth → dashboard)

## How to Execute
1. Use Better Auth session in server components
2. Check session in layout or page
3. Redirect accordingly using Next.js redirect()
4. Optionally add middleware.ts for global protection

## Output Format
- Protected /dashboard route
- Auto-redirect from / to /dashboard if logged in
- Auto-redirect to /login if not authenticated

---
name: full-phase2-deployment-ready  
description: Bring the entire Phase II app to a production-ready state with auth, CRUD, UI, and tests.  
---
# Full Phase 2 Deployment Ready Skill
## When to Use
- End of Phase II
- Preparing for demo or Phase III (chatbot)
- Need complete, working, secure full-stack todo app

## How to Execute
1. Run all previous skills in order
2. Verify docker-compose up works (frontend + backend)
3. Test full user journey: signup → login → create tasks → logout
4. Confirm user isolation and JWT security
5. Run all integration tests

## Output Format
- Complete working monorepo
- Clean, responsive UI
- Secure multi-user backend
- Passing test suite
- Ready for deployment (Vercel + Render/Fly.io)