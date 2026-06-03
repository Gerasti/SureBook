"""Uniformat command for simple CLI."""

import os
from typing import List, Dict, Any
from .base import Command
from file_manager import FileManager
from toml_manager import TomlManager


class UniformatCommand(Command):
    """Format .unikey files by removing leading whitespace from each line."""

    def __init__(self, toml_path: str):
        self.toml_path = toml_path

    def help(self) -> str:
        """Return help text for uniformat command."""
        return """Uniformat command - remove leading whitespace from .unikey files

Usage:
  uniformat                 Format all .unikey files in topic_save
  uniformat <topic>         Format specific topic's .unikey file
  uniformat help            Show this help

Examples:
  uniformat                 # Format all .unikey files
  uniformat "Python"        # Format Python.unikey only
"""

    def _get_topic_save_dir(self) -> str:
        """Get topic_save directory from settings."""
        toml_manager = TomlManager(self.toml_path)
        defaults = {
            "topic_save": FileManager.expanduser("~/SureBook/topics"),
        }
        settings = toml_manager.load_settings(defaults)
        return FileManager.expanduser(settings.topic_save)

    def _format_unikey_file(self, filepath: str) -> bool:
        """Format a single .unikey file by removing leading whitespace.

        Returns:
            True if file was modified, False otherwise
        """
        if not FileManager.exists(filepath):
            return False

        content = FileManager.read_text(filepath)
        lines = content.split('\n')

        # Remove leading whitespace from each line
        formatted_lines = [line.lstrip() for line in lines]
        formatted_content = '\n'.join(formatted_lines)

        # Check if content changed
        if content != formatted_content:
            FileManager.write_text(filepath, formatted_content)
            return True

        return False

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute uniformat command.

        Usage:
            uniformat               - Format all .unikey files
            uniformat <topic>       - Format specific topic
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        topic_save_dir = self._get_topic_save_dir()

        if not FileManager.exists(topic_save_dir):
            return self.error(f"Topic directory not found: {topic_save_dir}")

        # If specific topic is given
        if args:
            topic_name = args[0]
            # Convert spaces to underscores for filename
            filename = topic_name.replace(' ', '_')
            filepath = os.path.join(topic_save_dir, f"{filename}.unikey")

            if not FileManager.exists(filepath):
                return self.error(f"File not found: {filepath}")

            if self._format_unikey_file(filepath):
                print(f"Formatted: {filename}.unikey")
            else:
                print(f"No changes: {filename}.unikey")

            return 0

        # Format all .unikey files
        unikey_files = []
        for filename in os.listdir(topic_save_dir):
            if filename.endswith('.unikey'):
                filepath = os.path.join(topic_save_dir, filename)
                if os.path.isfile(filepath):
                    unikey_files.append((filename, filepath))

        if not unikey_files:
            print("No .unikey files found")
            return 0

        formatted_count = 0
        unchanged_count = 0

        for filename, filepath in sorted(unikey_files):
            if self._format_unikey_file(filepath):
                print(f"  ✓ Formatted: {filename}")
                formatted_count += 1
            else:
                if not flags.get('pure'):
                    print(f"  - No changes: {filename}")
                unchanged_count += 1

        print(f"\nTotal: {formatted_count} formatted, {unchanged_count} unchanged")
        return 0
