# Quickstart Guide: Better Auth Integration

## Prerequisites
- Node.js 18+ installed
- Next.js 16+ project set up
- Better Auth library installed
- Environment variables configured (BETTER_AUTH_SECRET)

## Setup Steps

1. **Install Dependencies**
   ```bash
   npm install better-auth
   ```

2. **Configure Better Auth**
   Create `frontend/src/auth/auth.ts` with JWT plugin configuration:
   ```typescript
   import { betterAuth } from "better-auth";
   import { jwt } from "better-auth/plugins";

   export const auth = betterAuth({
     secret: process.env.BETTER_AUTH_SECRET,
     plugins: [
       jwt({
         expiresIn: "7d", // Token expires after 7 days
       })
     ]
   });
   ```

3. **Set Environment Variables**
   Add to your `.env.local`:
   ```
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
   ```

4. **Create Auth Pages**
   - Create login page at `frontend/src/app/(auth)/login/page.tsx`
   - Create signup page at `frontend/src/app/(auth)/signup/page.tsx`

5. **Update API Client**
   Modify `frontend/src/lib/api.ts` to include JWT token in requests:
   ```typescript
   // Example wrapper function
   export async function authenticatedFetch(url: string, options: RequestInit = {}) {
     const token = await getAuthToken(); // Get token from cookies or storage
     return fetch(url, {
       ...options,
       headers: {
         ...options.headers,
         'Authorization': `Bearer ${token}`,
         'Content-Type': 'application/json',
       },
     });
   }
   ```

6. **Implement Protected Route Logic**
   Create a server component or middleware to check authentication status before rendering protected pages.

## Running the Application
1. Start the development server:
   ```bash
   npm run dev
   ```
2. Navigate to the signup page to create an account
3. Login with your credentials
4. Access protected routes to verify authentication is working

## Testing the Integration
1. Verify signup flow creates a new user and returns a JWT token
2. Verify login flow authenticates existing users and returns a JWT token
3. Verify protected routes redirect unauthenticated users to login
4. Verify API calls include the JWT token in the Authorization header
5. Verify session data (user_id, email) is available in server components