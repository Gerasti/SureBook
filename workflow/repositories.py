"""Repository layer for data access abstraction."""

import os
from typing import List, Set, Dict, Tuple, Optional

from models import Topic, ListEntry, ListSection, Settings
from file_manager import FileManager
from toml_manager import TomlManager
from fileutils import (
    normalize_topic, normalize_for_compare, strip_link, extract_link,
    parse_section_name, uniq_keep_order
)


class ConfigRepository:
    """Repository for configuration management."""

    def __init__(self, toml_path: str):
        self.toml_manager = TomlManager(toml_path)
        self.toml_path = toml_path

    def get_settings(self) -> Settings:
        """Get current settings with defaults."""
        defaults = {
            "input": FileManager.expanduser("~/SureBook/info/def_input.md"),
            "list": FileManager.expanduser("~/SureBook/info/def_lists.md"),
            "topic_save": FileManager.expanduser("~/SureBook/topics"),
            "post_save": FileManager.expanduser("~/SureBook/posting"),
            "source_table_file": FileManager.expanduser("~/SureBook/info/src_table.md"),
            "auto_alphabetic_sort": "false",
            "auto_save": "false",
            "auto_cast": "false",
            "auto_cast_format": "",
            "editor": "nvim",
        }
        settings = self.toml_manager.load_settings(defaults)

        # Expand ~ in paths
        settings.input = FileManager.expanduser(settings.input)
        settings.list = FileManager.expanduser(settings.list)
        settings.topic_save = FileManager.expanduser(settings.topic_save)
        settings.post_save = FileManager.expanduser(settings.post_save)
        settings.source_table_file = FileManager.expanduser(settings.source_table_file)

        return settings

    def save_settings(self, settings: Settings) -> None:
        """Save settings."""
        self.toml_manager.save_settings(settings)

    def update_setting(self, key: str, value: str) -> None:
        """Update a single setting."""
        self.toml_manager.update_setting(key, value)


class TopicRepository:
    """Repository for topic management."""

    def __init__(self, toml_path: str):
        self.toml_manager = TomlManager(toml_path)

    def get_all(self) -> List[Topic]:
        """Get all topics."""
        topics_dict = self.toml_manager.load_topics()
        return list(topics_dict.values())

    def get_by_key(self, key: str) -> Optional[Topic]:
        """Get topic by key."""
        topics = self.toml_manager.load_topics()
        return topics.get(key)

    def get_by_title(self, title: str) -> Optional[Topic]:
        """Get topic by title."""
        key = normalize_topic(title)
        return self.get_by_key(key)

    def exists(self, key: str) -> bool:
        """Check if topic exists."""
        return self.toml_manager.topic_exists(key)

    def get_existing_keys(self) -> Set[str]:
        """Get set of all existing topic keys."""
        topics = self.toml_manager.load_topics()
        return set(topics.keys())

    def save(self, topic: Topic) -> None:
        """Save a topic."""
        self.toml_manager.save_topic(topic)

    def delete(self, key: str) -> bool:
        """Delete a topic.

        Returns:
            True if deleted, False if not found
        """
        return self.toml_manager.delete_topic(key)

    def delete_by_title(self, title: str) -> bool:
        """Delete topic by title."""
        key = normalize_topic(title)
        return self.delete(key)


class InputRepository:
    """Repository for input file management."""

    def __init__(self, input_path: str):
        self.input_path = FileManager.expanduser(input_path)

    def get_all(self) -> List[str]:
        """Get all topics from input file."""
        return FileManager.read_non_empty_lines(self.input_path)

    def add(self, topic: str) -> bool:
        """Add topic to input file.

        Returns:
            True if added, False if already exists
        """
        existing = self.get_all()
        existing_norm = {normalize_for_compare(t) for t in existing}

        if normalize_for_compare(topic) in existing_norm:
            return False

        FileManager.append_lines(self.input_path, [topic])
        return True

    def add_many(self, topics: List[str]) -> int:
        """Add multiple topics.

        Returns:
            Number of topics added
        """
        existing = self.get_all()
        existing_norm = {normalize_for_compare(t) for t in existing}

        new_topics = [t for t in topics if normalize_for_compare(t) not in existing_norm]

        if new_topics:
            FileManager.append_lines(self.input_path, new_topics)

        return len(new_topics)

    def remove(self, topic: str) -> bool:
        """Remove topic from input file.

        Returns:
            True if removed, False if not found
        """
        topics = self.get_all()
        topic_norm = normalize_for_compare(topic)

        filtered = [t for t in topics if normalize_for_compare(t) != topic_norm]

        if len(filtered) == len(topics):
            return False

        FileManager.write_lines(self.input_path, filtered)
        return True

    def remove_many(self, topics_to_remove: List[str]) -> int:
        """Remove multiple topics.

        Returns:
            Number of topics removed
        """
        topics = self.get_all()
        remove_norm = {normalize_for_compare(t) for t in topics_to_remove}

        filtered = [t for t in topics if normalize_for_compare(t) not in remove_norm]
        removed_count = len(topics) - len(filtered)

        if removed_count > 0:
            FileManager.write_lines(self.input_path, filtered)

        return removed_count

    def sort_alphabetically(self) -> None:
        """Sort topics alphabetically."""
        topics = self.get_all()
        sorted_topics = sorted(topics, key=str.casefold)
        FileManager.write_lines(self.input_path, sorted_topics)

    def rename(self, old_name: str, new_name: str) -> bool:
        """Rename a topic.

        Returns:
            True if renamed, False if not found
        """
        topics = self.get_all()
        found = False

        new_topics = []
        for t in topics:
            if t == old_name:
                new_topics.append(new_name)
                found = True
            else:
                new_topics.append(t)

        if found:
            FileManager.write_lines(self.input_path, new_topics)

        return found


class ListRepository:
    """Repository for list file management."""

    def __init__(self, list_path: str):
        self.list_path = FileManager.expanduser(list_path)

    def get_all_sections(self) -> List[ListSection]:
        """Get all sections with their topics."""
        sections = []
        lines = FileManager.read_lines(self.list_path)

        current_section = None

        for line in lines:
            section_name = parse_section_name(line)

            if section_name is not None:
                if current_section:
                    sections.append(current_section)
                current_section = ListSection(name=section_name, topics=[])
            elif line.strip() and current_section:
                current_section.topics.append(line.strip())

        if current_section:
            sections.append(current_section)

        return sections

    def get_section(self, section_name: str) -> Optional[ListSection]:
        """Get a specific section."""
        sections = self.get_all_sections()
        for section in sections:
            if section.name == section_name:
                return section
        return None

    def get_section_names(self) -> List[str]:
        """Get list of all section names."""
        sections = self.get_all_sections()
        return [s.name for s in sections]

    def get_all_topics(self) -> List[str]:
        """Get all topics from all sections."""
        topics = []
        for section in self.get_all_sections():
            topics.extend(section.topics)
        return uniq_keep_order(topics)

    def section_exists(self, section_name: str) -> bool:
        """Check if section exists."""
        return section_name in self.get_section_names()

    def add_section(self, section_name: str) -> bool:
        """Add a new section.

        Returns:
            True if added, False if already exists
        """
        if self.section_exists(section_name):
            return False

        FileManager.append_text(self.list_path, f"\n## {section_name} list:\n")
        return True

    def delete_section(self, section_name: str) -> bool:
        """Delete a section.

        Returns:
            True if deleted, False if not found
        """
        lines = FileManager.read_lines(self.list_path)
        header = f"## {section_name} list:"

        new_lines = []
        skip = False
        found = False

        for line in lines:
            if line.strip() == header:
                skip = True
                found = True
                continue

            if skip and line.strip().startswith("##"):
                skip = False

            if not skip:
                new_lines.append(line)

        if found:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return found

    def add_topic_to_section(self, section_name: str, topic: str) -> bool:
        """Add topic to section.

        Returns:
            True if added, False if already exists or section not found
        """
        section = self.get_section(section_name)
        if not section:
            # Create section if it doesn't exist
            self.add_section(section_name)
            FileManager.append_lines(self.list_path, [topic, ""])
            return True

        # Check if topic already exists
        topic_norm = normalize_for_compare(topic)
        for existing in section.topics:
            if normalize_for_compare(existing) == topic_norm:
                return False

        # Add topic after section header
        lines = FileManager.read_lines(self.list_path)
        header = f"## {section_name} list:"
        new_lines = []

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == header:
                new_lines.append(topic + "\n")
                new_lines.append("\n")

        FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)
        return True

    def remove_topic_from_section(self, section_name: str, topic: str) -> bool:
        """Remove topic from section.

        Returns:
            True if removed, False if not found
        """
        lines = FileManager.read_lines(self.list_path)
        header = f"## {section_name} list:"

        new_lines = []
        in_section = False
        found = False
        topic_norm = normalize_for_compare(topic)

        for line in lines:
            stripped = line.strip()

            if stripped == header:
                in_section = True
                new_lines.append(line)
                continue

            if in_section and stripped.startswith("##"):
                in_section = False

            if in_section and normalize_for_compare(stripped) == topic_norm:
                # Remove empty line before if exists
                if new_lines and new_lines[-1].strip() == "":
                    new_lines.pop()
                found = True
                continue

            new_lines.append(line)

        if found:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return found

    def rename_section(self, old_name: str, new_name: str) -> bool:
        """Rename a section.

        Returns:
            True if renamed, False if not found
        """
        old_header = f"## {old_name} list:"
        new_header = f"## {new_name} list:"

        lines = FileManager.read_lines(self.list_path)
        found = False

        new_lines = []
        for line in lines:
            if line.strip() == old_header:
                new_lines.append(new_header + "\n")
                found = True
            else:
                new_lines.append(line)

        if found:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return found

    def rename_topic(self, old_name: str, new_name: str, section_name: Optional[str] = None) -> int:
        """Rename a topic in all sections or specific section.

        Returns:
            Number of occurrences renamed
        """
        lines = FileManager.read_lines(self.list_path)
        new_lines = []
        count = 0
        current_section = None
        in_target = section_name is None

        for line in lines:
            section = parse_section_name(line)
            if section is not None:
                current_section = section
                in_target = section_name is None or current_section == section_name

            stripped = line.strip()
            if in_target and stripped == old_name:
                new_lines.append(new_name + "\n")
                count += 1
            else:
                new_lines.append(line)

        if count > 0:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return count

    def sort_alphabetically(self) -> None:
        """Sort topics in all sections alphabetically."""
        sections = self.get_all_sections()
        lines = []

        for section in sections:
            lines.append(f"## {section.name} list:\n")
            sorted_topics = sorted(section.topics, key=str.casefold)
            for topic in sorted_topics:
                lines.append(f"{topic}\n\n")

        FileManager.write_lines(self.list_path, lines, ensure_newline=False)

    def set_link(self, section_name: str, topic: str, url: str, link_look: Optional[str] = None) -> bool:
        """Set link for a topic in section.

        Returns:
            True if link was set, False if topic not found
        """
        display = link_look if link_look else topic
        md_link = f"{topic} [{display}]({url})"

        lines = FileManager.read_lines(self.list_path)
        new_lines = []
        found = False
        current_section = None

        for line in lines:
            section = parse_section_name(line)
            if section is not None:
                current_section = section

            stripped = line.strip()
            if current_section == section_name and strip_link(stripped) == topic:
                new_lines.append(md_link + "\n")
                found = True
            else:
                new_lines.append(line)

        if found:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return found

    def remove_link(self, section_name: str, topic: str) -> bool:
        """Remove link from a topic in section.

        Returns:
            True if link was removed, False if topic not found
        """
        lines = FileManager.read_lines(self.list_path)
        new_lines = []
        found = False
        current_section = None

        for line in lines:
            section = parse_section_name(line)
            if section is not None:
                current_section = section

            stripped = line.strip()
            if current_section == section_name and stripped.startswith(f"{topic} ["):
                new_lines.append(topic + "\n")
                found = True
            else:
                new_lines.append(line)

        if found:
            FileManager.write_lines(self.list_path, new_lines, ensure_newline=False)

        return found
