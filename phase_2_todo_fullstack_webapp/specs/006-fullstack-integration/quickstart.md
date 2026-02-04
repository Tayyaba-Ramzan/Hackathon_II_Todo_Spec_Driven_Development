# Quickstart Guide: Full-stack Integration for Frontend and Backend Services

## Overview
This guide provides instructions for setting up and running the integrated full-stack Todo application with proper environment configuration, API communication, and authentication flow.

## Prerequisites
- Docker and Docker Compose
- Node.js (for manual frontend execution)
- Python 3.11+ (for manual backend execution)
- Access to Neon PostgreSQL database

## Environment Configuration

### Root Directory (.env)
```env
BETTER_AUTH_SECRET=Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://neondb_owner:npg_PI27GCiafTWl@ep-divine-hall-a4exapdh-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Frontend Directory (frontend/.env.local)
```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk
```

### Backend Directory (backend/.env)
```env
BETTER_AUTH_SECRET=Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk
DATABASE_URL=postgresql://neondb_owner:npg_PI27GCiafTWl@ep-divine-hall-a4exapdh-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## Running the Application

### Using Docker Compose (Recommended)
1. Navigate to the project root directory
2. Run the following command:
   ```bash
   docker-compose up --build
   ```
3. The frontend will be available at http://localhost:3000
4. The backend API will be available at http://localhost:8000

### Manual Execution
1. Terminal 1 - Start the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. Terminal 2 - Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## API Communication
- Frontend makes API requests to `http://localhost:8000/api/{user_id}/tasks`
- Requests must include a valid JWT token in the Authorization header: `Bearer {token}`
- Backend validates JWT tokens using the shared BETTER_AUTH_SECRET

## Authentication Flow
1. User logs in through the frontend
2. Frontend receives JWT token from authentication service
3. Frontend stores token and includes it in API requests to backend
4. Backend verifies JWT token and processes requests based on user identity
5. Backend ensures users can only access their own data through user_id validation

## Testing the Integration
1. Start both services using Docker Compose or manually
2. Access the frontend at http://localhost:3000
3. Create an account or log in
4. Verify that you can create, read, update, and delete tasks
5. Confirm that API requests are being made to the backend
6. Verify that CORS is properly configured and no errors occur