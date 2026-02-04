// Custom authentication API route compatible with the backend API
import { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { sign, verify } from 'jsonwebtoken';
import { cookies } from 'next/headers';

// Simple user database (in a real app, this would be a real database)
const users = new Map([
  ['admin@example.com', { id: 'user_123', email: 'admin@example.com', password: 'password123' }],
  ['user@example.com', { id: 'user_456', email: 'user@example.com', password: 'password123' }]
]);

// Secret for JWT signing (should match the backend secret)
const JWT_SECRET = process.env.BETTER_AUTH_SECRET || "Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, password, request: authRequest } = body;

    if (authRequest === 'signIn') {
      // Find user by email
      const user = users.get(email);

      if (!user || user.password !== password) {
        return NextResponse.json(
          { error: 'Invalid credentials' },
          { status: 401 }
        );
      }

      // Create JWT token with user info
      const token = sign(
        {
          user_id: user.id,
          email: user.email,
          exp: Math.floor(Date.now() / 1000) + 7 * 24 * 60 * 60 // 7 days expiry
        },
        JWT_SECRET,
        { algorithm: 'HS256' }
      );

      // Return token and user info
      return NextResponse.json({
        token,
        user: {
          id: user.id,
          email: user.email
        }
      });
    } else if (authRequest === 'signUp') {
      // Check if user already exists
      if (users.has(email)) {
        return NextResponse.json(
          { error: 'User already exists' },
          { status: 409 }
        );
      }

      // Create new user
      const newUser = {
        id: `user_${Date.now()}`, // Simple ID generation
        email,
        password
      };

      users.set(email, newUser);

      // Create JWT token
      const token = sign(
        {
          user_id: newUser.id,
          email: newUser.email,
          exp: Math.floor(Date.now() / 1000) + 7 * 24 * 60 * 60 // 7 days expiry
        },
        JWT_SECRET,
        { algorithm: 'HS256' }
      );

      return NextResponse.json({
        token,
        user: {
          id: newUser.id,
          email: newUser.email
        }
      });
    } else if (authRequest === 'signOut') {
      // For sign out, we just need to clear the token on the frontend
      // The backend doesn't need to maintain server-side sessions
      return NextResponse.json({ message: 'Signed out successfully' });
    } else if (authRequest === 'getSession') {
      // Verify the token and return session info
      const authHeader = request.headers.get('authorization');
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return NextResponse.json(
          { error: 'Authorization header missing or invalid' },
          { status: 401 }
        );
      }

      const token = authHeader.substring(7);

      try {
        const decoded = verify(token, JWT_SECRET) as any;
        return NextResponse.json({
          user: {
            id: decoded.user_id,
            email: decoded.email
          }
        });
      } catch (error) {
        return NextResponse.json(
          { error: 'Invalid or expired token' },
          { status: 401 }
        );
      }
    } else {
      return NextResponse.json(
        { error: 'Invalid request type' },
        { status: 400 }
      );
    }
  } catch (error) {
    console.error('Auth API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// GET handler for session validation (if needed)
export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { error: 'Authorization header missing or invalid' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);
    const JWT_SECRET = process.env.BETTER_AUTH_SECRET || "Xp2Pai0rYqduM32JBoNYaqWYVQjZEIWk";

    try {
      const decoded = verify(token, JWT_SECRET) as any;
      return NextResponse.json({
        user: {
          id: decoded.user_id,
          email: decoded.email
        }
      });
    } catch (error) {
      return NextResponse.json(
        { error: 'Invalid or expired token' },
        { status: 401 }
      );
    }
  } catch (error) {
    console.error('Auth API GET error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}