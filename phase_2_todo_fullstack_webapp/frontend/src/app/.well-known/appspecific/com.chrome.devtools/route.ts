import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

// Handle requests for Chrome DevTools configuration
export async function GET(request: NextRequest) {
  // Return an empty JSON response to prevent 404 errors
  return NextResponse.json({});
}