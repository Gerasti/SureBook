"""Unsave command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from repositories import TopicRepository
from fileutils import normalize_topic
from file_manager import FileManager


class UnsaveCommand(Command):
    """Remove topics from TOML and delete their files."""

    def __init__(self, topic_repo: TopicRepository):
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for unsave command."""
        return """Unsave command - remove topics from TOML

Usage:
  unsave <topics...>    Remove topics from TOML
  unsave all force      Remove all topics (requires force)
  unsave help           Show this help

Flags:
  force                 Required for 'unsave all'

Examples:
  unsave "Python Tutorial"           # Remove one topic
  unsave "Python" "Django" "Flask"   # Remove multiple topics
  unsave all force                   # Remove all topics
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute unsave command.

        Usage:
            unsave <topics...>  - Remove topics from TOML
            unsave all force    - Remove all topics (requires force)
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("unsave requires topic names or 'all force'")

        # Check for wipe all
        if args[0] == "all":
            if not flags.get("force"):
                return self.error("unsave all requires 'force' flag")
            return self._wipe_all()

        # Remove specific topics
        removed = 0
        for topic_name in args:
            key = normalize_topic(topic_name)
            topic = self.topic_repo.get_by_key(key)

            if not topic:
                print(f"Not found: {topic_name}")
                continue

            # Delete files
            if topic.path and FileManager.exists(topic.path):
                FileManager.remove(topic.path)
                print(f"Deleted file: {topic.path}")

            # Delete topic from TOML
            self.topic_repo.delete(key)
            print(f"Removed from TOML: {topic_name}")
            removed += 1

        if removed > 0:
            print(f"Total removed: {removed}")

        return 0

    def _wipe_all(self) -> int:
        """Remove all topics from TOML."""
        topics = self.topic_repo.get_all()

        if not topics:
            print("No topics to remove")
            return 0

        for topic in topics:
            # Delete files
            if topic.path and FileManager.exists(topic.path):
                FileManager.remove(topic.path)

            # Delete from TOML
            self.topic_repo.delete(topic.key)

        print(f"Wiped all {len(topics)} topics")
        return 0
