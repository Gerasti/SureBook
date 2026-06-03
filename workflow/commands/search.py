"""Search command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import denormalize_topic


class SearchCommand(Command):
    """Search for topics."""

    def __init__(self, input_repo: InputRepository, list_repo: ListRepository, topic_repo: TopicRepository):
        self.input_repo = input_repo
        self.list_repo = list_repo
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for search command."""
        return """Search command - find topics

Usage:
  search <query>        Search in input and lists
  search saved <query>  Search in saved TOML topics
  search help           Show this help

Flags:
  pure                  Clean output without headers

Examples:
  search python         # Search for "python" in input/lists
  search saved django   # Search for "django" in TOML
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute search command.

        Usage:
            search <query>        - Search in input/lists
            search saved <query>  - Search in TOML
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("search requires query")

        pure = flags.get('pure', False)

        if args[0] == "saved":
            # search saved <query>
            if len(args) < 2:
                return self.error("search saved requires query")

            query = args[1].lower()
            topics = self.topic_repo.get_all()
            found = False

            for t in topics:
                searchable = f"{t.title} {' '.join(e.list_name for e in t.lists)}".lower()
                if query in searchable:
                    found = True
                    if pure:
                        print(denormalize_topic(t.title))
                    else:
                        lists_str = ", ".join(e.list_name for e in t.lists) if t.lists else "—"
                        print(f"{denormalize_topic(t.title)} [{lists_str}]")

            if not found:
                print(f"Not found: {args[1]}")
            return 0

        # search <query>
        query = args[0].lower()
        found = False

        # Search input
        topics = self.input_repo.get_all()
        matches = [t for t in topics if query in t.lower()]
        if matches:
            found = True
            if not pure:
                print(f"\n[input] ({len(matches)}):")
            for t in matches:
                print(f"  {t}" if not pure else t)

        # Search lists
        for section in self.list_repo.get_all_sections():
            matches = [t for t in section.topics if query in t.lower()]
            if matches:
                found = True
                if not pure:
                    print(f"\n[{section.name}] ({len(matches)}):")
                for t in matches:
                    print(f"  {t}" if not pure else t)

        if not found:
            print(f"Not found: {args[0]}")

        return 0
