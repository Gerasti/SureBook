"""Cleanup command for simple CLI."""

import os
from typing import List, Dict, Any, Set
from .base import Command
from file_manager import FileManager
from toml_manager import TomlManager


class CleanupCommand(Command):
    """Clean up duplicate topics in TOML file and orphaned files."""

    def __init__(self, toml_path: str):
        self.toml_path = toml_path

    def help(self) -> str:
        """Return help text for cleanup command."""
        return """Cleanup command - remove duplicates and orphaned files

Usage:
  cleanup               Remove duplicate topics from TOML
  cleanup force         Remove orphaned files not in current topics
  cleanup help          Show this help

Examples:
  cleanup               # Remove all duplicate topics
  cleanup force         # Remove files not related to current topics
"""

    def _get_topic_keys_from_toml(self) -> Set[str]:
        """Get all topic keys from TOML file."""
        toml_manager = TomlManager(self.toml_path)
        topics = toml_manager.load_topics()
        return set(topics.keys())

    def _get_topic_save_dir(self) -> str:
        """Get topic_save directory from settings."""
        toml_manager = TomlManager(self.toml_path)
        defaults = {
            "topic_save": FileManager.expanduser("~/SureBook/topics"),
        }
        settings = toml_manager.load_settings(defaults)
        return FileManager.expanduser(settings.topic_save)

    def _cleanup_orphaned_files(self) -> int:
        """Remove files that don't belong to current topics."""
        topic_keys = self._get_topic_keys_from_toml()
        topic_save_dir = self._get_topic_save_dir()

        if not FileManager.exists(topic_save_dir):
            print(f"Topic directory not found: {topic_save_dir}")
            return 1

        # Get all files in topic_save directory
        all_files = []
        for filename in os.listdir(topic_save_dir):
            filepath = os.path.join(topic_save_dir, filename)
            if os.path.isfile(filepath):
                all_files.append(filename)

        # Find orphaned files
        orphaned_files = []
        for filename in all_files:
            # Extract base name without extension
            base_name = os.path.splitext(filename)[0]

            # Check if this file belongs to any topic
            if base_name not in topic_keys:
                orphaned_files.append(filename)

        if not orphaned_files:
            print("No orphaned files found")
            return 0

        # Show what will be deleted
        print(f"Found {len(orphaned_files)} orphaned file(s):\n")
        for filename in sorted(orphaned_files):
            filepath = os.path.join(topic_save_dir, filename)
            file_size = os.path.getsize(filepath)
            print(f"  {filename} ({file_size} bytes)")

        # Delete files
        print(f"\nDeleting {len(orphaned_files)} file(s)...")
        deleted_count = 0
        for filename in orphaned_files:
            filepath = os.path.join(topic_save_dir, filename)
            try:
                os.remove(filepath)
                deleted_count += 1
                print(f"  ✓ Deleted: {filename}")
            except Exception as e:
                print(f"  ✗ Failed to delete {filename}: {e}")

        print(f"\nTotal deleted: {deleted_count}/{len(orphaned_files)}")
        return 0

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute cleanup command.

        Usage:
            cleanup             - Remove duplicate topics from TOML
            cleanup force       - Remove orphaned files
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        # Handle cleanup force - remove orphaned files
        if flags.get('force'):
            return self._cleanup_orphaned_files()

        # Default: remove duplicates from TOML
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
