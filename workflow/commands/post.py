"""Post command for simple CLI."""

import os
from typing import List, Dict, Any
from .base import Command
from repositories import ConfigRepository
from fileutils import normalize_topic
from file_manager import FileManager


class PostCommand(Command):
    """Manage post files."""

    def __init__(self, config_repo: ConfigRepository):
        self.config_repo = config_repo

    def help(self) -> str:
        """Return help text for post command."""
        return """Post command - manage post files

Usage:
  post <name>           Create/open post file
  help                  Show this help

Flags:
  format <ext>          Specify format (default: from auto_cast_format)

Examples:
  post "MyArticle"              # Create post with default format
  post "MyArticle" format md    # Create markdown post
  post "MyArticle" -f wikitext  # Create wikitext post
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute post command.

        Usage:
            post <name>       - Create/open post file
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        if not args:
            return self.error("post requires: <name>")

        name = args[0]
        settings = self.config_repo.get_settings()

        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'post <name> format <ext>'")

        if not settings.post_save:
            return self.error("post_save not set")

        FileManager.ensure_dir(settings.post_save)

        key = normalize_topic(name)
        post_path = FileManager.join(settings.post_save, f"{key}.{fmt}.post")

        # Create empty file if it doesn't exist
        if not FileManager.exists(post_path):
            FileManager.write_text(post_path, "")
            print(f"Created: {post_path}")
        else:
            print(f"File exists: {post_path}")

        return 0
