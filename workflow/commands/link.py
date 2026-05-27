"""Link command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import ListRepository
from fileutils import paths_to_list


class LinkCommand(Command):
    """Manage links for topics in list sections."""

    def __init__(self, list_repo: ListRepository):
        self.list_repo = list_repo

    def help(self) -> str:
        """Return help text for link command."""
        return """Link command - manage topic links

Usage:
  link add <t> <s> <url> [display]  Add link to topic
  link del <topic> <section>        Remove link
  link help                         Show this help

Examples:
  link add "Python" backend https://python.org           # Add link
  link add "Python" backend https://python.org "Docs"    # Add with display text
  link del "Python" backend                              # Remove link
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute link command.

        Usage:
            link add <topic> <section> <url> [display]
            link del <topic> <section>
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("link requires subcommand: add, del")

        subcommand = args[0]

        if subcommand == "add":
            return self._add_link(args[1:], flags)
        elif subcommand in ["del", "delete", "rm"]:
            return self._delete_link(args[1:], flags)
        else:
            return self.error(f"Unknown link subcommand: {subcommand}")

    def _add_link(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Add link to topic in section."""
        if len(args) < 3:
            return self.error("link add requires: <topic> <section> <url> [display]")

        topic = args[0]
        section = args[1]
        url = args[2]
        link_look = args[3] if len(args) > 3 else None

        if not self.list_repo.section_exists(section):
            return self.error(f"Section not found: {section}")

        success = self.list_repo.set_link(section, topic, url, link_look)

        if success:
            display = link_look if link_look else topic
            print(f"Set link in [{section}]: {topic} [{display}]({url})")
            return 0
        else:
            return self.error(f"Topic not found in section: {topic}")

    def _delete_link(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Delete link from topic in section."""
        if len(args) < 2:
            return self.error("link del requires: <topic> <section>")

        topic = args[0]
        section = args[1]

        if not self.list_repo.section_exists(section):
            return self.error(f"Section not found: {section}")

        success = self.list_repo.remove_link(section, topic)

        if success:
            print(f"Removed link from [{section}]: {topic}")
            return 0
        else:
            return self.error(f"Topic not found in section: {topic}")
