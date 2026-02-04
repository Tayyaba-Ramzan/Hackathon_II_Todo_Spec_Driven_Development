# Data Model: In-Memory Todo CLI App

## Entity: Todo

**Description**: Represents a single todo task in the system

**Fields**:
- `id`: int (unique identifier, auto-generated)
- `title`: str (required, task title)
- `description`: str (optional, task description, default: empty string)
- `completed`: bool (task completion status, default: False)

**Validation Rules**:
- `id` must be unique within the system
- `title` must not be empty or None
- `completed` must be a boolean value

**State Transitions**:
- Default state: `completed = False`
- Can transition from `False` to `True` (mark complete)
- Can transition from `True` to `False` (mark incomplete)

## Entity: TodoList

**Description**: Collection of Todo items stored in memory

**Fields**:
- `tasks`: dict[int, Todo] (collection of Todo items indexed by ID)

**Operations**:
- Add a new Todo item
- Retrieve all Todo items
- Retrieve a specific Todo item by ID
- Update a Todo item by ID
- Delete a Todo item by ID
- Mark a Todo item as complete by ID
- Mark a Todo item as incomplete by ID

**Validation Rules**:
- IDs must be unique
- No duplicate IDs allowed
- Operations on non-existent IDs must return appropriate error status