"""Cleanup command for simple CLI."""

from typing import List, Dict, Any
from .base import Command
from file_manager import FileManager


class CleanupCommand(Command):
    """Clean up duplicate topics in TOML file."""

    def __init__(self, toml_path: str):
        self.toml_path = toml_path

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute cleanup command.

        Usage:
            cleanup             - Remove duplicate topics from TOML
            cleanup duplicates  - Same as above
        """
        if not FileManager.exists(self.toml_path):
            return self.error(f"TOML file not found: {self.toml_path}")

        content = FileManager.read_text(self.toml_path)
        lines = content.split("\n")

        seen_topics = set()
        new_lines = []
        skip = False
        in_topics_section = False
        duplicates_removed = 0

        for line in lines:
            stripped = line.strip()

            # Check if we're entering topics section
            if stripped == "[topics]" or stripped.startswith('[topics."'):
                in_topics_section = True

            # Check if we're leaving topics section
            if in_topics_section and stripped.startswith("[") and not stripped.startswith('[topics'):
                in_topics_section = False

            # Only process duplicates in topics section
            if in_topics_section and stripped.startswith('[topics."') and stripped.endswith('"]'):
                # Extract topic key
                topic_key = stripped[9:-2]  # Remove [topics." and "]

                if topic_key in seen_topics:
                    # This is a duplicate, skip it
                    skip = True
                    duplicates_removed += 1
                    print(f"Removing duplicate: {topic_key}")
                    continue
                else:
                    # First occurrence, keep it
                    seen_topics.add(topic_key)
                    skip = False
                    new_lines.append(line)
                    continue

            # Check if we're entering a new section (stop skipping)
            if stripped.startswith("[") and not stripped.startswith('[topics."'):
                skip = False

            # Add line if not skipping
            if not skip:
                new_lines.append(line)

        # Write cleaned content
        if duplicates_removed > 0:
            FileManager.write_text(self.toml_path, "\n".join(new_lines))
            print(f"\nRemoved {duplicates_removed} duplicate(s)")
            return 0
        else:
            print("No duplicates found")
            return 0
