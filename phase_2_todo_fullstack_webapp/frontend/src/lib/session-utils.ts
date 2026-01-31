// Session management utilities

export interface SessionUser {
  id: string;
  email: string;
}

export interface SessionData {
  user: SessionUser;
  token: string;
}

// Helper function to decode JWT token (without verification)
function decodeJWT(token: string): any {
  try {
    // Split the token into its parts
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    // Decode the payload (second part)
    let payload = parts[1];

    // Replace URL-safe base64 characters
    payload = payload.replace(/-/g, '+').replace(/_/g, '/');

    // Add padding if needed
    while (payload.length % 4) {
      payload += '=';
    }

    // Decode the base64 payload
    const decodedPayload = atob(payload);
    const parsedPayload = JSON.parse(decodedPayload);

    // Log the payload for debugging purposes (will be removed in production)
    console.log('Decoded JWT payload:', parsedPayload);

    return parsedPayload;
  } catch (error) {
    console.error('Error decoding JWT:', error);
    throw error;
  }
}

// Get the current session from local storage
export const getCurrentSession = async (): Promise<SessionData | null> => {
  try {
    const token = localStorage.getItem('auth-token');

    if (!token) {
      return null;
    }

    // Decode the JWT token to get user info without making a network request
    try {
      const decodedToken = decodeJWT(token);

      // Check if token is expired
      if (decodedToken.exp && decodedToken.exp * 1000 < Date.now()) {
        localStorage.removeItem('auth-token');
        localStorage.removeItem('user-email');
        return null;
      }

      // Return session data from the token
      return {
        user: {
          id: decodedToken.user_id || decodedToken.sub || decodedToken.id || decodedToken.userId,
          email: decodedToken.email || localStorage.getItem('user-email') || ''
        },
        token
      };
    } catch (decodeError) {
      console.error('Error decoding token:', decodeError);
      // If token is invalid, remove it from storage
      localStorage.removeItem('auth-token');
      localStorage.removeItem('user-email');
      return null;
    }
  } catch (error) {
    console.error('Error getting current session:', error);
    return null;
  }
};

// Store the authentication token and user email
export const setAuthToken = (token: string, userEmail?: string): void => {
  try {
    localStorage.setItem('auth-token', token);
    if (userEmail) {
      localStorage.setItem('user-email', userEmail);
    }
  } catch (error) {
    console.error('Error setting auth token:', error);
  }
};

// Clear the authentication session
export const logout = async (): Promise<void> => {
  try {
    // Remove the token from local storage
    localStorage.removeItem('auth-token');
    localStorage.removeItem('user-email');

    // Redirect to login page
    window.location.href = '/login';
  } catch (error) {
    console.error('Error during logout:', error);
    // Still redirect even if there's an error clearing storage
    window.location.href = '/login';
  }
};