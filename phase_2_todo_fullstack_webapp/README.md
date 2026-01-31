# TodoPro – Full-Stack Task Management Application 🚀

A professional full-stack web application to manage your tasks efficiently with modern frontend and backend technologies.

[Frontend Live Demo](https://your-frontend-url.vercel.app) | [Backend API](https://your-backend-url.railway.app)

---

## Features ✨

- Modern Full-Stack Architecture: Next.js 16+ frontend with FastAPI backend
- Secure User Authentication: JWT-based login and signup
- CRUD Operations: Create, Read, Update, Delete tasks
- Task Filters: View active, completed, and all tasks
- User Isolation: Each user can only access their own tasks
- Responsive & Dark Mode Compatible UI
- Environment Config for development and production

---

## Tech Stack 🛠

| Layer      | Technology |
|-----------|------------|
| Frontend  | Next.js 16+, React 18, TailwindCSS |
| Backend   | FastAPI, SQLModel, Python 3.11 |
| Database  | PostgreSQL (Railway Managed) |
| Auth      | JWT Tokens, Secure Password Hashing |
| Deployment| Vercel (Frontend), Railway (Backend & DB) |

---

## Getting Started – Local Development 💻

### Backend Setup

```bash
cd backend
pip install poetry
poetry install
poetry run uvicorn main:app --reload --port 8000

Backend API URL: http://localhost:8000
```
 Frontend Setup

```bash
cd frontend
npm install
npm run dev

Backend API URL: http://localhost:8000
````

API Communication 🔗

Frontend requests: GET/POST/PUT/DELETE http://localhost:8000/api/{user_id}/tasks

Include JWT token in Authorization header:
Authorization: Bearer {token}

Backend validates token and ensures user-specific access

Authentication Flow 🔐

User signs up or logs in via frontend

JWT token returned and stored securely

Token included in all API requests

Backend verifies token and grants access

Users can only access their own tasks

Deployment Guide 🚀

Frontend: Vercel

Connect GitHub repo → Auto-detect Next.js → Deploy

Backend: Railway

Connect GitHub repo → Auto-detect Python → Add environment variables:
BETTER_AUTH_SECRET, DATABASE_URL → Deploy

Database: Managed PostgreSQL (Railway)

Connect Frontend & Backend:
Set environment variable in Vercel:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app/api
```

Contributing 🤝

Fork the repository

Create a new branch: git checkout -b feature/awesome-feature

Make changes & commit: git commit -m "Add awesome feature"

Push to branch: git push origin feature/awesome-feature

Create a Pull Request







