"""Rename command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import normalize_topic
from file_manager import FileManager


class RenameCommand(Command):
    """Rename topics or lists."""

    def __init__(self, input_repo: InputRepository, list_repo: ListRepository, topic_repo: TopicRepository):
        self.input_repo = input_repo
        self.list_repo = list_repo
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for rename command."""
        return """Rename command - rename topics and lists

Usage:
  rename <old> <new>    Rename topic everywhere
  rename list <o> <n>   Rename section
  rename help           Show this help

Examples:
  rename "Python Tutorial" "Python Guide"    # Rename topic
  rename list backend server                 # Rename section
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute rename command.

        Usage:
            rename <old> <new>    - Rename topic
            rename list <o> <n>   - Rename section
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if len(args) < 2:
            return self.error("rename requires old and new names")

        if args[0] == "list":
            # rename list <old> <new>
            if len(args) < 3:
                return self.error("rename list requires old and new names")

            old, new = args[1], args[2]
            renamed = self.list_repo.rename_section(old, new)
            if renamed:
                print(f"Renamed list: {old} -> {new}")
            else:
                print(f"List not found: {old}")
            return 0

        # rename <old> <new>
        old, new = args[0], args[1]

        if self.input_repo.rename(old, new):
            print(f"Renamed in input: {old} -> {new}")

        for section in self.list_repo.get_all_sections():
            count = self.list_repo.rename_topic(old, new, section.name)
            if count > 0:
                print(f"Renamed in list [{section.name}]: {old} -> {new}")

        old_key = normalize_topic(old)
        topic = self.topic_repo.get_by_key(old_key)
        if topic:
            # Delete old
            old_path = topic.path
            self.topic_repo.delete(old_key)

            # Create new
            new_key = normalize_topic(new)
            topic.key = new_key
            topic.title = new
            topic.path = topic.path.replace(f"{old_key}.md", f"{new_key}.md")
            self.topic_repo.save(topic)

            # Rename file if exists
            if FileManager.exists(old_path):
                content = FileManager.read_text(old_path)
                FileManager.write_text(topic.path, content)
                FileManager.remove(old_path)

            print(f"Renamed in TOML: {old} -> {new}")

        return 0
