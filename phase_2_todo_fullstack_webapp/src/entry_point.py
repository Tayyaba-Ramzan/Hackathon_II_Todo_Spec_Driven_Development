"""
Entry point script for the todo console application.
This script is used as the entry point in pyproject.toml to avoid import issues.
"""
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.cli.main import main

def main_entry():
    """Main entry point function for the CLI."""
    main()

if __name__ == "__main__":
    main_entry()