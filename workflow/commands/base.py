"""Base command class for simple CLI."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute the command.

        Args:
            args: List of positional arguments
            flags: Dictionary of flags (pure, force, etc.)

        Returns:
            Exit code (0 for success, non-zero for error)
        """
        pass

    def help(self) -> str:
        """Return help text for this command."""
        return "No help available for this command."

    def error(self, msg: str) -> int:
        """Print error and return error code."""
        print(f"Error: {msg}")
        return 1

    def print_items(self, items: List[str], header: str = None, pure: bool = False):
        """Print list of items with optional header."""
        if not pure and header:
            print(header)
        for item in items:
            if pure:
                print(item)
            else:
                print(f"  {item}")
