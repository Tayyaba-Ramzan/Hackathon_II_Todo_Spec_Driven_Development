# Data Model: Beautiful & Professional Frontend UI Polish

## Entities Overview

This UI redesign doesn't introduce new data entities but focuses on the presentation layer of existing entities. The frontend will interact with the following backend entities:

## User Entity
- **Fields**:
  - id: string (unique identifier)
  - name: string (user's display name)
  - email: string (user's email address)
  - createdAt: datetime (account creation timestamp)
  - updatedAt: datetime (last update timestamp)
- **Relationships**: Owns multiple Task entities
- **Validation**: Email must be valid format, name must not be empty
- **State transitions**: Active, Inactive (based on account status)

## Task Entity
- **Fields**:
  - id: string (unique identifier)
  - title: string (task title, max 255 chars)
  - description: string (optional task description)
  - completed: boolean (completion status)
  - createdAt: datetime (task creation timestamp)
  - updatedAt: datetime (last update timestamp)
  - userId: string (foreign key to User)
- **Relationships**: Belongs to one User
- **Validation**: Title must not be empty, length constraints applied
- **State transitions**: Pending → Completed → Archived

## UI State Entities (Frontend Only)

### Theme State
- **Fields**:
  - mode: 'light' | 'dark' | 'system' (current theme mode)
  - isSystemPreferred: boolean (whether system preference is being used)
- **Validation**: Mode must be one of the allowed values
- **State transitions**: User can toggle between light/dark/system modes

### Responsive State
- **Fields**:
  - breakpoint: 'mobile' | 'tablet' | 'desktop' (current responsive breakpoint)
  - isMobile: boolean (is current view mobile-sized)
  - isTablet: boolean (is current view tablet-sized)
  - isDesktop: boolean (is current view desktop-sized)
- **Validation**: Only one breakpoint should be active at a time
- **State transitions**: Changes based on window resize events

### UI Component States
- **TaskForm State**:
  - isExpanded: boolean (whether form is expanded/collapsed)
  - currentValues: object (current form field values)
  - errors: object (validation errors)
- **TaskCard State**:
  - isHovered: boolean (whether card is being hovered)
  - isFocused: boolean (whether card has focus)
  - isAnimating: boolean (whether card is in animation state)
- **Loading State**:
  - isLoading: boolean (whether data is loading)
  - skeletonCount: number (number of skeleton placeholders to show)

## UI Design Tokens

### Color Tokens
- **Primary**: indigo-600 (main accent color)
- **Secondary**: gray-200/gray-800 (secondary elements, varies by theme)
- **Success**: green-500 (for completed tasks)
- **Warning**: amber-500 (for important tasks)
- **Error**: red-500 (for error states)
- **Background**: white/gray-900 (background color, varies by theme)
- **Surface**: white/gray-800 (card and surface color, varies by theme)
- **Text**: gray-900/gray-100 (text color, varies by theme)

### Spacing Tokens
- **Base unit**: 4px (foundational spacing unit)
- **Multipliers**: 4, 6, 8, 12, 16, 24, 32, 48, 64 (in multiples of base unit)
- **Usage**: p-4, p-6, p-8 for padding; m-4, m-6, m-8 for margins; gap-4, gap-6, gap-8 for gaps

### Typography Tokens
- **Page Title**: text-4xl (for main page headings)
- **Card Title**: text-2xl (for card headings)
- **Body Text**: text-base (for regular content)
- **Small Text**: text-sm (for secondary information)
- **Large Text**: text-lg (for emphasized content)

### Elevation Tokens
- **Base Shadow**: shadow-sm (for default card elevation)
- **Hover Shadow**: shadow-lg (for hover states)
- **Active Shadow**: shadow-xl (for focused/active states)

### Animation Tokens
- **Duration**: duration-200 (200ms for most transitions)
- **Timing**: ease-in-out (for smooth transitions)
- **Properties**: transition-all (for all animatable properties)