import { getCurrentSession } from './session-utils';

// Define the Task type to match the backend model after normalization
// The API utility transforms snake_case fields to camelCase
export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  createdAt: string;       // camelCase version (normalized)
  updatedAt: string;       // camelCase version (normalized)
  user_id: string;
}

// Define types for task operations
export interface CreateTaskData {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
}

// API base URL - in production, this would be the backend server URL
// Note: This should be the base URL without the /api part, as that's added in the routes
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Helper function to get the current user ID from the session
async function getCurrentUserId(): Promise<string> {
  const session = await getCurrentSession();
  if (!session) {
    throw new Error('No active session found');
  }
  // Extract the user ID part from the token if needed
  // The user ID format from login is user_timestamp
  return session.user.id;
}

// Helper function to make API requests
// Note: Hugging Face deployed backend might not require authentication
async function makeAuthenticatedRequest(
  url: string,
  options: RequestInit = {}
): Promise<any> {
  try {
    console.log('Making API request to:', url); // Debug logging

    // For Hugging Face deployment, we might not need authentication
    // But we'll keep it in case the backend requires it
    const session = await getCurrentSession();

    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        // Only add authorization header if we have a session
        ...(session && { 'Authorization': `Bearer ${session.token}` }),
        ...options.headers,
      },
      // Add mode: 'cors' to handle cross-origin requests properly
      mode: 'cors',
    });

    console.log('Response status:', response.status); // Debug logging
    // Convert headers to an array in a way that's compatible with older ES targets
    const headersArray: [string, string][] = [];
    response.headers.forEach((value, key) => {
      headersArray.push([key, value]);
    });
    console.log('Response headers:', headersArray); // Debug logging

    // Handle different response status codes
    if (!response.ok) {
      if (response.status === 401) {
        // Unauthorized - token might be expired
        localStorage.removeItem('auth-token');

        // Only redirect to login if we're not already on the login page
        if (typeof window !== 'undefined' && !window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }

        throw new Error('Authentication required');
      } else if (response.status === 403) {
        throw new Error('Access forbidden - you do not have permission to perform this action');
      } else if (response.status === 404) {
        // For 404 errors, check if it's HTML or JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
        } else {
          // It's likely an HTML error page
          const textContent = await response.text();
          console.error('Received HTML 404 response:', textContent.substring(0, 200));
          throw new Error(`API endpoint not found. Please check the URL: ${url}`);
        }
      } else {
        // Try to get error message from response body
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json();
          throw new Error(errorData.detail || `API Error: ${response.status} ${response.statusText}`);
        } else {
          // It's likely an HTML error page
          const textContent = await response.text();
          console.error('Received HTML error response:', textContent.substring(0, 200));
          throw new Error(`Server error returned HTML instead of JSON: ${response.status} ${response.statusText}`);
        }
      }
    }

    // For DELETE requests, there's typically no response body
    if (response.status === 204) {
      return null;
    }

    // Check if the response is JSON before parsing
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();

      // Helper function to normalize task data
      const normalizeTask = (task: any) => {
        // If the task already has camelCase dates, return as is
        if (task.createdAt && task.updatedAt) {
          return task;
        }

        // If the task has snake_case dates, convert to camelCase
        if (task.created_at && task.updated_at) {
          return {
            ...task,
            createdAt: task.created_at,
            updatedAt: task.updated_at,
          };
        }

        // If neither format exists, return as is
        return task;
      };

      // Transform snake_case date fields to camelCase for consistency with frontend expectations
      if (data && typeof data === 'object') {
        // Handle single task response
        if (data.hasOwnProperty('id') && (data.hasOwnProperty('created_at') || data.hasOwnProperty('createdAt'))) {
          return normalizeTask(data);
        }

        // Handle array of tasks response
        if (Array.isArray(data)) {
          return data.map(normalizeTask);
        }
      }

      return data;
    } else {
      // If the response is not JSON, it might be HTML (e.g., error page)
      // Try to get the text content and create an appropriate error
      const textContent = await response.text();

      // Check if it's HTML content
      if (textContent.trim().startsWith('<!DOCTYPE') || textContent.trim().startsWith('<html')) {
        console.error('Received HTML response instead of JSON:', textContent.substring(0, 300)); // Log first 300 chars
        throw new Error(`Server returned an HTML page instead of JSON. This indicates a routing error or server issue. URL: ${url}. Status: ${response.status} ${response.statusText}`);
      }

      // If it's not HTML but also not JSON, try to parse it as JSON anyway
      // or throw an error with the text content
      try {
        return JSON.parse(textContent);
      } catch {
        throw new Error(`Server returned non-JSON content: ${textContent.substring(0, 200)}...`);
      }
    }
  } catch (error) {
    console.error('API request error:', error);
    // Check if this is a CORS or network error
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error or CORS issue. Please check that the backend is accessible and properly configured for cross-origin requests.');
    }
    throw error;
  }
}

// Task API functions
export const taskApi = {
  // Get all tasks for the current user
  getTasks: async (statusFilter: 'all' | 'pending' | 'completed' = 'all'): Promise<Task[]> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/`;

    return makeAuthenticatedRequest(url, {
      method: 'GET',
    });
  },

  // Create a new task
  createTask: async (taskData: CreateTaskData): Promise<Task> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/`;

    return makeAuthenticatedRequest(url, {
      method: 'POST',
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description || "",
        completed: taskData.completed || false
      }),
    });
  },

  // Get a specific task by ID
  getTask: async (taskId: string): Promise<Task> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}/`;  // Added trailing slash

    return makeAuthenticatedRequest(url, {
      method: 'GET',
    });
  },

  // Update a task completely
  updateTask: async (taskId: string, taskData: UpdateTaskData): Promise<Task> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}/`;  // Added trailing slash

    return makeAuthenticatedRequest(url, {
      method: 'PUT',
      body: JSON.stringify({
        title: taskData.title,
        description: taskData.description || "",
        completed: taskData.completed || false
      }),
    });
  },

  // Partially update a task
  patchTask: async (taskId: string, taskData: Partial<UpdateTaskData>): Promise<Task> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}/`;  // Using the same endpoint for PATCH

    return makeAuthenticatedRequest(url, {
      method: 'PATCH',
      body: JSON.stringify({
        completed: taskData.completed
      }),
    });
  },

  // Delete a task
  deleteTask: async (taskId: string): Promise<void> => {
    // Get the current user ID to construct the proper API endpoint
    const userId = await getCurrentUserId();
    const url = `${API_BASE_URL}/api/${userId}/tasks/${taskId}/`;  // Added trailing slash

    await makeAuthenticatedRequest(url, {
      method: 'DELETE',
    });
  },
};