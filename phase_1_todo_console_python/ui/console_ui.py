import sys
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text
from managers.todo_manager import TodoManager
from models.task import Task

console = Console()

class ConsoleUI:
    def __init__(self, todo_manager: TodoManager):
        self.todo_manager = todo_manager
    
    # ---------------------------------------------------------
    # MENU
    # ---------------------------------------------------------
    def display_menu(self) -> None:
        console.print(
            Panel.fit(
                "[bold blue]TASK MANAGEMENT SYSTEM[/bold blue]\n"
                "[white]1.[/white] Add Task\n"
                "[white]2.[/white] View All Tasks\n"
                "[white]3.[/white] Edit Task\n"
                "[white]4.[/white] Remove Task\n"
                "[white]5.[/white] Mark Task Completed\n"
                "[white]6.[/white] Mark Task Pending\n"
                "[white]7.[/white] Exit",
                title="📋 Main Menu",
                border_style="blue",
            )
        )
    
    def get_user_choice(self) -> str:
        return Prompt.ask("[bold green]Select an option[/bold green]", choices=[str(i) for i in range(1, 8)])
    
    # ---------------------------------------------------------
    # INPUT HELPERS
    # ---------------------------------------------------------
    def get_task_details(self) -> tuple[str, str]:
        title = Prompt.ask("[yellow]Task Title[/yellow]").strip()
        description = Prompt.ask("[yellow]Additional Details (optional)[/yellow]", default="").strip()
        return title, description
    
    def get_task_id(self) -> Optional[int]:
        try:
            return int(Prompt.ask("[cyan]Enter Task ID[/cyan]"))
        except ValueError:
            console.print("[bold red]❌ Invalid input! Please enter a number.[/bold red]")
            return None

    # ---------------------------------------------------------
    # ACTIONS
    # ---------------------------------------------------------
    def add_task(self) -> None:
        console.print(Panel("[bold blue]➕ Add New Task[/bold blue]", border_style="blue"))
        title, description = self.get_task_details()
        
        if not title:
            console.print("[bold red]❌ Task title cannot be empty.[/bold red]")
            return
        
        task = self.todo_manager.add_task(title, description)
        console.print(f"[bold green]✔ Task Added:[/bold green] [cyan]#{task.id}[/cyan] {task.title}")
    
    def list_tasks(self) -> None:
        tasks = self.todo_manager.list_tasks()
        
        if not tasks:
            console.print("[bold yellow]⚠ No tasks available. Please add a task.[/bold yellow]")
            return
        
        table = Table(title="📋 Task List", show_header=True, header_style="bold blue")
        table.add_column("ID", width=5)
        table.add_column("Title", width=30)
        table.add_column("Status", width=12)
        
        for task in tasks:
            status = "[green]Completed[/green]" if task.completed else "[yellow]Pending[/yellow]"
            table.add_row(str(task.id), task.title, status)

        console.print(table)
    
    def update_task(self) -> None:
        console.print(Panel("[bold blue]✏ Edit Task[/bold blue]", border_style="blue"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        task = self.todo_manager.get_task(task_id)
        if not task:
            console.print(f"[bold red]❌ No task found with ID {task_id}[/bold red]")
            return
        
        console.print(f"[cyan]Current Title:[/cyan] [white]{task.title}[/white]")
        console.print(f"[cyan]Details:[/cyan] [dim]{task.description}[/dim]")
        
        new_title = Prompt.ask("New Title (press Enter to keep current)", default="").strip()
        new_description = Prompt.ask("New Details (press Enter to keep current)", default="").strip()
        
        new_title = new_title or None
        new_description = new_description or None
        
        if self.todo_manager.update_task(task_id, new_title, new_description):
            console.print("[bold green]✔ Task updated successfully.[/bold green]")
        else:
            console.print("[bold red]❌ Failed to update task.[/bold red]")
    
    def delete_task(self) -> None:
        console.print(Panel("[bold red]🗑 Remove Task[/bold red]", border_style="red"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        task = self.todo_manager.get_task(task_id)
        if not task:
            console.print(f"[bold red]❌ No task found with ID {task_id}[/bold red]")
            return
        
        confirm = Confirm.ask(f"Are you sure you want to delete [yellow]{task.title}[/yellow]?", default=False)
        if confirm:
            if self.todo_manager.delete_task(task_id):
                console.print("[bold green]✔ Task removed.[/bold green]")
            else:
                console.print("[bold red]❌ Failed to delete task.[/bold red]")
        else:
            console.print("[cyan]Deletion cancelled.[/cyan]")
    
    def mark_complete(self) -> None:
        console.print(Panel("[bold green]✅ Mark Task Completed[/bold green]", border_style="green"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        if self.todo_manager.mark_complete(task_id):
            console.print("[bold green]✔ Task marked as completed.[/bold green]")
        else:
            console.print(f"[bold red]❌ No task found with ID {task_id}[/bold red]")
    
    def mark_incomplete(self) -> None:
        console.print(Panel("[bold yellow]📋 Mark Task Pending[/bold yellow]", border_style="yellow"))

        task_id = self.get_task_id()
        if task_id is None:
            return
        
        if self.todo_manager.mark_incomplete(task_id):
            console.print("[yellow]○ Task marked as pending.[/yellow]")
        else:
            console.print(f"[bold red]❌ No task found with ID {task_id}[/bold red]")
    
    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------
    def run(self) -> None:
        console.print(Panel("[bold blue]Welcome to the Task Management System[/bold blue]", border_style="blue"))
        
        while True:
            self.display_menu()
            choice = self.get_user_choice()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.list_tasks()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.mark_complete()
            elif choice == '6':
                self.mark_incomplete()
            elif choice == '7':
                console.print("[bold blue]👋 Thank you for using the Task Management System! Goodbye.[/bold blue]")
                sys.exit(0)
