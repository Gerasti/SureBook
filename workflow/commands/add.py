"""Add command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository


class AddCommand(Command):
    """Add topics to input or list."""

    def __init__(self, input_repo: InputRepository, list_repo: ListRepository):
        self.input_repo = input_repo
        self.list_repo = list_repo

    def help(self) -> str:
        """Return help text for add command."""
        return """Add command - add topics and lists

Usage:
  add <topic>          Add topic to input
  add <topic> to <sec> Add topic to section
  add list <name>      Create new section
  add help             Show this help

Examples:
  add "Python Tutorial"           # Add to input
  add "Django" to backend         # Add to backend section
  add list frontend               # Create frontend section
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute add command.

        Usage:
            add <topic>           - Add topic to input
            add <topic> to <sec>  - Add topic to section
            add list <name>       - Create new section
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("add requires arguments")

        if args[0] == "list":
            # add list <name>
            if len(args) < 2:
                return self.error("add list requires name")

            name = args[1]
            added = self.list_repo.add_section(name)
            if added:
                print(f"Added list: {name}")
            else:
                print(f"List already exists: {name}")
            return 0

        # add <topic> [to <section>]
        topic = args[0]

        if len(args) >= 3 and args[1] == "to":
            section = args[2]
            added = self.list_repo.add_topic_to_section(section, topic)
            if added:
                print(f"Added to list [{section}]: {topic}")
            else:
                print(f"Already exists in [{section}]: {topic}")
        else:
            added = self.input_repo.add(topic)
            if added:
                print(f"Added to input: {topic}")
            else:
                print(f"Already exists in input: {topic}")

        return 0
