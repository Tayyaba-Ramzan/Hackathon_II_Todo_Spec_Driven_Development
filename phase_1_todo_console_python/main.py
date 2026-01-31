from managers.todo_manager import TodoManager
from ui.console_ui import ConsoleUI
from colorama import init, Fore, Style

def main():
    # Initialize color support
    init(autoreset=True)

    print(Fore.MAGENTA + Style.BRIGHT + "=========================================")
    print(Fore.YELLOW + Style.BRIGHT + "        📝 Personal Task Manager")
    print(Fore.MAGENTA + Style.BRIGHT + "=========================================")
    print(Fore.CYAN + "Plan smart. Stay organized. Get things done.\n")

    task_manager = TodoManager()
    ui = ConsoleUI(task_manager)
    ui.run()

if __name__ == "__main__":
    main()
