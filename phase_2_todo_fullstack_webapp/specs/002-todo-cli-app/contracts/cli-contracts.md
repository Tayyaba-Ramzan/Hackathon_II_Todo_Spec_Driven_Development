# API Contracts: In-Memory Todo CLI App

## CLI Command Interface

### Add Todo
- **Command**: `add <title> [description]`
- **Input**: Title (required), Description (optional)
- **Output**: Success message with assigned ID
- **Error Cases**: Invalid input, empty title

### View Todos
- **Command**: `view`
- **Input**: None
- **Output**: List of all todos with ID, title, description, and completion status
- **Error Cases**: No todos exist

### Update Todo
- **Command**: `update <id> [--title NEW_TITLE] [--description NEW_DESCRIPTION]`
- **Input**: Todo ID, new title (optional), new description (optional)
- **Output**: Success message
- **Error Cases**: Todo with ID doesn't exist, invalid ID

### Delete Todo
- **Command**: `delete <id>`
- **Input**: Todo ID
- **Output**: Success message
- **Error Cases**: Todo with ID doesn't exist, invalid ID

### Mark Complete
- **Command**: `complete <id>`
- **Input**: Todo ID
- **Output**: Success message
- **Error Cases**: Todo with ID doesn't exist, invalid ID

### Mark Incomplete
- **Command**: `incomplete <id>`
- **Input**: Todo ID
- **Output**: Success message
- **Error Cases**: Todo with ID doesn't exist, invalid ID

### Exit
- **Command**: `exit` or `quit`
- **Input**: None
- **Output**: Application terminates gracefully
- **Error Cases**: None