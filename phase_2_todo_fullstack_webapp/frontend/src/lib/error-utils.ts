// Error handling utilities for authentication

export interface AuthError {
  message: string;
  status?: number;
}

export interface ValidationError {
  message: string;
}

export const handleAuthError = (error: any): AuthError => {
  if (error.status === 401) {
    return { message: 'Invalid credentials. Please check your email and password.' };
  } else if (error.status === 400) {
    return { message: error.message || 'Bad request. Please check your input.' };
  } else if (error.status === 404) {
    return { message: 'Authentication endpoint not found.' };
  } else if (error.status === 500) {
    return { message: 'Server error. Please try again later.' };
  } else if (error.message) {
    return { message: error.message };
  } else {
    return { message: 'An unexpected error occurred during authentication.' };
  }
};

export const validateAuthForm = (
  email: string, 
  password: string, 
  confirmPassword?: string
): ValidationError | null => {
  // Validate email format
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email || !emailRegex.test(email)) {
    return { message: 'Please enter a valid email address.' };
  }

  // Validate password length
  if (!password || password.length < 6) {
    return { message: 'Password must be at least 6 characters long.' };
  }

  // If confirmPassword is provided, validate that it matches password
  if (confirmPassword !== undefined) {
    if (!confirmPassword) {
      return { message: 'Please confirm your password.' };
    }
    if (password !== confirmPassword) {
      return { message: 'Passwords do not match.' };
    }
  }

  return null;
};