# API Contracts: Beautiful & Professional Frontend UI Polish

## Overview
This document defines the API contracts that support the UI redesign for the Todo application. The UI polish doesn't introduce new backend functionality but enhances the frontend presentation and user experience.

## Authentication Endpoints

### POST /api/auth/signup
**Purpose**: User registration
**Request**:
- Content-Type: application/json
- Body: {name: string, email: string, password: string}
**Response**:
- 200: {user: User, token: string}
- 400: Validation error
- 409: User already exists

### POST /api/auth/login
**Purpose**: User authentication
**Request**:
- Content-Type: application/json
- Body: {email: string, password: string}
**Response**:
- 200: {user: User, token: string}
- 400: Invalid credentials
- 401: Authentication failed

### POST /api/auth/logout
**Purpose**: User logout
**Request**:
- Headers: Authorization: Bearer {token}
**Response**:
- 200: {message: string}
- 401: Unauthorized

## User-Specific Task Endpoints

### GET /api/{user_id}/tasks
**Purpose**: Retrieve user's tasks
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT)
**Response**:
- 200: {tasks: Task[]}
- 401: Unauthorized
- 403: Access denied (user_id mismatch)

### POST /api/{user_id}/tasks
**Purpose**: Create a new task
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT)
- Body: {title: string, description?: string}
**Response**:
- 201: {task: Task}
- 400: Validation error
- 401: Unauthorized
- 403: Access denied (user_id mismatch)

### PUT /api/{user_id}/tasks/{task_id}
**Purpose**: Update a task
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT), task_id
- Body: {title?: string, description?: string, completed?: boolean}
**Response**:
- 200: {task: Task}
- 400: Validation error
- 401: Unauthorized
- 403: Access denied (user_id mismatch)
- 404: Task not found

### DELETE /api/{user_id}/tasks/{task_id}
**Purpose**: Delete a task
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT), task_id
**Response**:
- 200: {message: string}
- 401: Unauthorized
- 403: Access denied (user_id mismatch)
- 404: Task not found

## UI-Specific Endpoints

### GET /api/{user_id}/theme
**Purpose**: Retrieve user's theme preference
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT)
**Response**:
- 200: {theme: 'light' | 'dark' | 'system'}
- 401: Unauthorized
- 403: Access denied (user_id mismatch)

### PUT /api/{user_id}/theme
**Purpose**: Update user's theme preference
**Request**:
- Headers: Authorization: Bearer {token}
- Path: user_id (from JWT)
- Body: {theme: 'light' | 'dark' | 'system'}
**Response**:
- 200: {theme: 'light' | 'dark' | 'system'}
- 400: Validation error
- 401: Unauthorized
- 403: Access denied (user_id mismatch)

## Frontend State Management

### Client-Side State Schema
The following state schemas are managed on the frontend to support UI features:

#### Theme State
```json
{
  "mode": "light" | "dark" | "system",
  "isSystemPreferred": boolean,
  "lastUpdated": string
}
```

#### Responsive State
```json
{
  "breakpoint": "mobile" | "tablet" | "desktop",
  "isMobile": boolean,
  "isTablet": boolean,
  "isDesktop": boolean
}
```

#### Task Form State
```json
{
  "isExpanded": boolean,
  "currentValues": {
    "title": string,
    "description": string
  },
  "errors": {
    "title"?: string,
    "description"?: string
  }
}
```

#### Task Card State
```json
{
  "isHovered": boolean,
  "isFocused": boolean,
  "isAnimating": boolean
}
```

#### Loading State
```json
{
  "isLoading": boolean,
  "skeletonCount": number
}
```

## UI Component Contracts

### TaskCard Component
**Props**:
- task: Task
- onToggleComplete: (task: Task) => void
- onEdit: (task: Task) => void
- onDelete: (taskId: string) => void
- isHovered?: boolean
- isFocused?: boolean

### TaskForm Component
**Props**:
- onSubmit: (taskData: {title: string, description?: string}) => void
- onCancel?: () => void
- initialData?: {title: string, description?: string}
- isExpanded?: boolean

### ThemeToggle Component
**Props**:
- currentTheme: 'light' | 'dark' | 'system'
- onThemeChange: (theme: 'light' | 'dark' | 'system') => void

### ResponsiveGrid Component
**Props**:
- children: ReactNode[]
- minColumnWidth?: string
- gap?: string
- className?: string

## Error Handling

### HTTP Error Responses
- 400: Client error (validation, malformed request)
- 401: Unauthorized (invalid/expired JWT)
- 403: Forbidden (user trying to access another user's data)
- 404: Not found (resource doesn't exist)
- 409: Conflict (duplicate resource)
- 500: Server error (internal server error)

### UI Error States
- Form validation errors: Displayed inline below relevant fields
- API errors: Displayed in toast notifications
- Loading states: Skeleton components during data fetch
- Empty states: Friendly messages when no data available
- Network errors: Offline indicators and retry options

## Accessibility Contracts

### ARIA Attributes
- All interactive elements must have appropriate ARIA roles
- Form elements must have associated labels
- Loading states must announce to screen readers
- Focus management for keyboard navigation

### Keyboard Navigation
- Tab order follows visual hierarchy
- Focus indicators visible on all interactive elements
- Escape key closes modals and dropdowns
- Enter/Space activates buttons and links

## Performance Requirements

### Response Times
- API calls: <200ms p95
- Initial page load: <2s on 3G connection
- Interactive response: <100ms
- Animation frames: 60fps

### Bundle Size
- Main bundle: <300KB
- Vendor bundle: <500KB
- Individual components: <50KB