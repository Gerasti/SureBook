"""Post command for simple CLI."""

import os
import subprocess
from typing import List, Dict, Any
from .base import Command
from repositories import ConfigRepository, TopicRepository
from fileutils import normalize_topic
from file_manager import FileManager


class PostCommand(Command):
    """Manage post files."""

    def __init__(self, config_repo: ConfigRepository, topic_repo: TopicRepository = None):
        self.config_repo = config_repo
        self.topic_repo = topic_repo

    def help(self) -> str:
        """Return help text for post command."""
        return """Post command - manage post files

Usage:
  post <name>           Create/open post file with table of contents
  post cat              Show generated content without creating file
  help                  Show this help

Flags:
  format <ext>          Specify format (default: from auto_cast_format)

Examples:
  post "MyArticle"              # Create post with default format
  post "MyArticle" format md    # Create markdown post
  post "MyArticle" -f wikitext  # Create wikitext post
  post cat                      # Preview content without saving

The post file will contain:
  - Table of contents with links to all topics
  - Each topic with its content from .unikey files
"""

    def execute(self, args: List[str], flags: Dict[str, Any]) -> int:
        """Execute post command.

        Usage:
            post <name>       - Create/open post file
            post cat          - Show generated content without creating file
        """
        if args and args[0] == "help" and not flags.get('force'):
            print(self.help())
            return 0

        settings = self.config_repo.get_settings()
        fmt = flags.get("format") or settings.auto_cast_format
        if not fmt:
            return self.error("Format not specified. Use 'post <name> format <ext>'")

        # Handle 'post cat' subcommand
        if args and args[0] == "cat":
            content = self._generate_post_content(settings, fmt)
            print(content, end='')
            return 0

        if not args:
            return self.error("post requires: <name>")

        name = args[0]

        if not settings.post_save:
            return self.error("post_save not set")

        FileManager.ensure_dir(settings.post_save)

        key = normalize_topic(name)
        post_path = FileManager.join(settings.post_save, f"{key}.{fmt}.post")

        # Generate content with table of contents and topics
        content = self._generate_post_content(settings, fmt)

        # Write content to file
        FileManager.write_text(post_path, content)

        if FileManager.exists(post_path):
            print(f"Created: {post_path}")
        else:
            print(f"File exists: {post_path}")

        return 0

    def _generate_post_content(self, settings, fmt: str) -> str:
        """Generate post content with table of contents and all topics."""
        # Get all topics from topic_save directory
        topic_save_dir = FileManager.expanduser(settings.topic_save)
        if not FileManager.exists(topic_save_dir):
            return ""

        # Collect all .unikey files
        topics = []
        for filename in os.listdir(topic_save_dir):
            if filename.endswith('.unikey'):
                topic_key = filename[:-7]  # Remove .unikey extension
                topics.append(topic_key)

        # Sort topics alphabetically
        topics.sort(key=str.casefold)

        # Build unikey content
        unikey_lines = []

        # Check if format needs TOC and links
        no_toc_formats = ['wikitext', 'cyberforum', '4pda']
        needs_toc = fmt not in no_toc_formats

        # Generate each topic section
        for topic in topics:
            # Add topic header (always 'hd' for both formats)
            unikey_lines.append(f"hd {topic}")

            # Add link back to contents only for formats that support it
            if needs_toc:
                unikey_lines.append("lk Содержание Содержание")

            # Read topic content from .unikey file
            topic_path = FileManager.join(topic_save_dir, f"{topic}.unikey")
            if FileManager.exists(topic_path):
                topic_content = FileManager.read_text(topic_path).strip()
                if topic_content:
                    # For formats without links: replace 'hd' with 'ne' and remove 'lk'
                    if fmt in no_toc_formats:
                        topic_content = self._process_no_link_content(topic_content)
                    unikey_lines.append(topic_content)

        unikey_content = "\n".join(unikey_lines) + "\n"

        # Convert through unikey preprocessor
        converted_content = self._convert_unikey(unikey_content, fmt)

        # Prepend table of contents only for formats that support it
        if needs_toc:
            toc = self._generate_toc(topics)
            return toc + "\n\n" + converted_content

        return converted_content

    def _generate_toc(self, topics: list) -> str:
        """Generate table of contents grouped by first letter."""
        from collections import defaultdict

        # Group topics by first letter
        by_letter = defaultdict(list)
        for topic in topics:
            first_letter = topic[0].upper() if topic else '?'
            by_letter[first_letter].append(topic)

        # Generate TOC header and lines
        toc_lines = ["### Содержание <!-- HEAD -->", ""]

        for letter in sorted(by_letter.keys()):
            links = "; ".join([f"[{topic}](#{topic}-)" for topic in by_letter[letter]])
            toc_lines.append(f"{letter}) {links}")
            toc_lines.append("")  # Empty line after each letter

        return "\n".join(toc_lines)

    def _process_no_link_content(self, content: str) -> str:
        """Process topic content for formats without links: replace 'hd' with 'ne' and remove 'lk' lines."""
        lines = []
        for line in content.split('\n'):
            stripped = line.lstrip()

            # Skip 'lk' and '/link' lines
            if stripped.startswith('lk ') or stripped.startswith('/link '):
                continue

            # Replace 'hd' with 'ne' in topic content
            if stripped.startswith('hd '):
                indent = line[:len(line) - len(stripped)]
                lines.append(indent + 'ne ' + stripped[3:])
            elif stripped.startswith('/head '):
                indent = line[:len(line) - len(stripped)]
                lines.append(indent + '/name ' + stripped[6:])
            else:
                lines.append(line)

        return '\n'.join(lines)

    def _convert_unikey(self, unikey_content: str, fmt: str) -> str:
        """Convert unikey content to target format using unikey.py preprocessor."""
        try:
            # Find unikey.py in the same directory as this script
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            unikey_path = os.path.join(script_dir, "unikey.py")

            if not os.path.exists(unikey_path):
                return f"Error: unikey.py not found at {unikey_path}\n"

            # Run unikey preprocessor
            result = subprocess.run(
                ["python3", unikey_path, "-f", fmt],
                input=unikey_content,
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout

        except subprocess.CalledProcessError as e:
            return f"Error converting format: {e.stderr}\n"
        except Exception as e:
            return f"Error: {e}\n"
