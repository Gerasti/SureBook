"""Source table command for simple CLI."""

import os
import subprocess
from typing import List, Dict, Any
from .base import Command
from repositories import TopicRepository, ConfigRepository
from file_manager import FileManager
from fileutils import denormalize_topic


class TableCommand(Command):
    """Generate and view source tables."""

    def __init__(self, topic_repo: TopicRepository, config_repo: ConfigRepository):
        self.topic_repo = topic_repo
        self.config_repo = config_repo

    def help(self) -> str:
        """Return help text for table command."""
        return """Table command - manage source table

Usage:
  table [generate]      Generate source table
  table show            View source table
  table help            Show this help

Examples:
  table                 # Generate source table
  table generate        # Same as above
  table show            # View source table
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute table command.

        Usage:
            table generate      - Generate source table
            table show          - View source table
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self._generate([], flags)

        subcommand = args[0]

        if subcommand in ["generate", "gen", "g"]:
            return self._generate(args[1:], flags)
        elif subcommand in ["show", "view", "open"]:
            return self._show(args[1:], flags)
        else:
            return self.error(f"Unknown table subcommand: {subcommand}")

    def _generate(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Generate source table."""
        settings = self.config_repo.get_settings()

        if not settings.source_table_file:
            return self.error("source_table_file not set")

        topics = self.topic_repo.get_all()

        # Sort topics alphabetically if auto_sort is enabled
        if settings.auto_alphabetic_sort:
            topics = sorted(topics, key=lambda t: t.title.lower())

        topic_save = FileManager.expanduser(settings.topic_save) if settings.topic_save else ""

        lines = []
        if settings.last_saved:
            lines.append(f"> last saved: {settings.last_saved}\n")

        lines.append("| № | Topic | Sources (lists + links) | Has file(s) |")
        lines.append("|---|-------|-------------------------|-------------|")

        for i, topic in enumerate(topics, 1):
            sources_parts = []
            for entry in topic.lists:
                if entry.link:
                    display = entry.link_look if entry.link_look else denormalize_topic(topic.title)
                    sources_parts.append(f"{entry.list_name} [{display}]({entry.link})")
                else:
                    sources_parts.append(entry.list_name)

            sources = ", ".join(sources_parts) if sources_parts else ""

            # Check for files
            exts = []
            if topic.path and topic_save and FileManager.is_dir(topic_save):
                stem = os.path.splitext(os.path.basename(topic.path))[0]
                for fname in os.listdir(topic_save):
                    fpath = FileManager.join(topic_save, fname)
                    if FileManager.is_file(fpath) and os.path.splitext(fname)[0] == stem:
                        ext = os.path.splitext(fname)[1].lstrip(".")
                        if ext:
                            exts.append(ext)

            has_files = ", ".join(sorted(exts)) if exts else ""

            lines.append(f"| {i} | {denormalize_topic(topic.title)} | {sources} | {has_files} |")

        action = "renewed" if FileManager.exists(FileManager.expanduser(settings.source_table_file)) else "created"
        source_table_file = FileManager.expanduser(settings.source_table_file)
        FileManager.ensure_dir(os.path.dirname(source_table_file))
        FileManager.write_text(source_table_file, "\n".join(lines) + "\n")

        print(f"Source table {action}: {source_table_file} ({len(topics)} topics)")
        return 0

    def _show(self, args: List[str], flags: Dict[str, Any]) -> int:
        """View source table."""
        settings = self.config_repo.get_settings()

        if not settings.source_table_file:
            return self.error("source_table_file not set")

        source_table_file = FileManager.expanduser(settings.source_table_file)

        if not FileManager.exists(source_table_file):
            return self.error(f"Source table not found: {source_table_file}. Run 'table generate' first")

        viewer = settings.viewers.get("md")
        if not viewer:
            return self.error("No viewer set for md. Use 'config viewer md <cmd>'")

        subprocess.Popen([viewer, source_table_file])
        print(f"Opened: {source_table_file}")
        return 0
