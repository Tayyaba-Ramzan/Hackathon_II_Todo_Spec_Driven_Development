"""
Command-line interface for the todo application.
"""
import sys
from typing import List
from src.services.todo_service import TodoService
from src.lib.storage import InMemoryStorage


class TodoCLI:
    """
    Command-line interface for the todo application.
    """
    
    def __init__(self):
        """Initialize the CLI with a service instance."""
        self.storage = InMemoryStorage()
        self.service = TodoService(self.storage)
    
    def display_menu(self):
        """Display the main menu options."""
        print("\n--- Todo CLI App ---")
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Complete")
        print("6. Mark Incomplete")
        print("7. Exit")
        print("--------------------")
    
    def get_user_choice(self) -> str:
        """Get the user's menu choice."""
        try:
            choice = input("Enter your choice (1-7): ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)
    
    def handle_add_todo(self):
        """Handle adding a new todo."""
        try:
            title = input("Enter title: ").strip()
            if not title:
                print("Error: Title cannot be empty")
                return
            
            description = input("Enter description (optional): ").strip()
            
            task_id = self.service.add_task(title, description)
            print(f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def handle_view_todos(self):
        """Handle viewing all todos."""
        todos = self.service.get_all_tasks()
        
        if not todos:
            print("No tasks found")
            return
        
        print("\nYour Todos:")
        for todo in todos:
            status = "X" if todo.completed else "O"
            print(f"[{status}] ID: {todo.id} | Title: {todo.title} | Description: {todo.description}")
    
    def handle_update_todo(self):
        """Handle updating a todo."""
        try:
            task_id = int(input("Enter task ID to update: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        # Check if task exists
        todos = self.service.get_all_tasks()
        if not any(todo.id == task_id for todo in todos):
            print(f"Error: Task with ID {task_id} does not exist")
            return
        
        title_input = input("Enter new title (leave blank to keep current): ").strip()
        description_input = input("Enter new description (leave blank to keep current): ").strip()
        
        # Prepare new values (None means don't update that field)
        new_title = title_input if title_input else None
        new_description = description_input if description_input else None
        
        # At least one field should be updated
        if new_title is None and new_description is None:
            print("Error: Please provide at least one field to update (title or description)")
            return
        
        success = self.service.update_task(task_id, new_title, new_description)
        if success:
            print(f"Task {task_id} updated successfully")
        else:
            print(f"Error: Failed to update task with ID {task_id}")
    
    def handle_delete_todo(self):
        """Handle deleting a todo."""
        try:
            task_id = int(input("Enter task ID to delete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        success = self.service.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully")
        else:
            print(f"Error: Task with ID {task_id} does not exist")
    
    def handle_mark_complete(self):
        """Handle marking a todo as complete."""
        try:
            task_id = int(input("Enter task ID to mark complete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        success = self.service.mark_task_complete(task_id)
        if success:
            print(f"Task {task_id} marked as complete")
        else:
            print(f"Error: Task with ID {task_id} does not exist")
    
    def handle_mark_incomplete(self):
        """Handle marking a todo as incomplete."""
        try:
            task_id = int(input("Enter task ID to mark incomplete: "))
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return
        
        success = self.service.mark_task_incomplete(task_id)
        if success:
            print(f"Task {task_id} marked as incomplete")
        else:
            print(f"Error: Task with ID {task_id} does not exist")
    
    def run(self):
        """Run the CLI application."""
        print("Welcome to the Todo CLI App!")
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == "1":
                self.handle_add_todo()
            elif choice == "2":
                self.handle_view_todos()
            elif choice == "3":
                self.handle_update_todo()
            elif choice == "4":
                self.handle_delete_todo()
            elif choice == "5":
                self.handle_mark_complete()
            elif choice == "6":
                self.handle_mark_incomplete()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
            
            # Pause to let user see the result before showing the menu again
            input("\nPress Enter to continue...")


def main():
    """Main entry point for the application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()