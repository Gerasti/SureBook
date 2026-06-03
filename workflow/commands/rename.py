"""Rename command for simple CLI."""

import os
import re
from typing import List, Dict, Any
from .base import Command
from repositories import InputRepository, ListRepository, TopicRepository
from fileutils import normalize_topic, normalize_for_compare, extract_link, strip_link
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
            # Create new topic first
            new_key = normalize_topic(new)
            old_path = topic.path

            # Rename all related files FIRST
            topic_dir = os.path.dirname(old_path)
            new_stem = new_key  # Use new_key as the stem for files

            # Build list of possible old file stems to search for
            old_file_stems = set()
            old_file_stems.add(normalize_topic(old))  # normalized version of input
            old_file_stems.add(old_key)  # key from TOML
            # Add the exact old name if it's different
            if old not in old_file_stems:
                old_file_stems.add(old)

            if FileManager.is_dir(topic_dir):
                # Find all files that match any of the old file stem variations
                for fname in os.listdir(topic_dir):
                    fpath = FileManager.join(topic_dir, fname)
                    if FileManager.is_file(fpath):
                        file_stem = os.path.splitext(fname)[0]
                        # Check if this file matches any variation of old name
                        if file_stem in old_file_stems:
                            ext = os.path.splitext(fname)[1]
                            new_fname = f"{new_stem}{ext}"
                            new_fpath = FileManager.join(topic_dir, new_fname)

                            if fpath != new_fpath:
                                os.rename(fpath, new_fpath)
                                print(f"  Renamed file: {fname} -> {new_fname}")

            # Now update TOML (only if keys are different)
            if old_key != new_key:
                topic.key = new_key
                topic.title = new
                topic.path = topic.path.replace(f"{old_key}.md", f"{new_key}.md")

                # Update lists - rebuild from list_repo after rename
                from models import ListEntry
                topic.lists = []
                for section in self.list_repo.get_all_sections():
                    for t in section.topics:
                        t_clean = strip_link(t)
                        if normalize_for_compare(t_clean) == normalize_for_compare(new):
                            # Extract link if present
                            link = None
                            link_look = None
                            match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', t)
                            if match:
                                link_look = match.group(1)
                                link = match.group(2)

                            topic.lists.append(ListEntry(
                                list_name=section.name,
                                link=link,
                                link_look=link_look
                            ))

                # Save new topic
                self.topic_repo.save(topic)

                # Delete old topic
                self.topic_repo.delete(old_key)

            print(f"Renamed in TOML: {old} -> {new}")

        return 0
