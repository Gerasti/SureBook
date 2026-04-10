"""TOML configuration management using tomllib."""

import os
import tomllib
from typing import Dict, Optional

from models import Settings, Topic
from file_manager import FileManager


class TomlManager:
    """Manages TOML file reading and writing."""

    def __init__(self, toml_path: str):
        self.toml_path = FileManager.expanduser(toml_path)

    def load_settings(self, defaults: Optional[Dict] = None) -> Settings:
        """Load settings from TOML file.

        Args:
            defaults: Default values to use if keys are missing

        Returns:
            Settings object
        """
        data = {}

        if FileManager.exists(self.toml_path):
            try:
                with open(self.toml_path, "rb") as f:
                    toml_data = tomllib.load(f)
                    data = toml_data.get("settings", {})
            except Exception as e:
                print(f"Warning: Failed to parse TOML: {e}")

        # Apply defaults
        if defaults:
            for key, value in defaults.items():
                if key not in data:
                    data[key] = value

        return Settings.from_dict(data)

    def save_settings(self, settings: Settings) -> None:
        """Save settings to TOML file.

        Preserves [topics] section if it exists.
        """
        # Read existing content to preserve topics
        topics_content = []
        other_sections = []

        if FileManager.exists(self.toml_path):
            content = FileManager.read_text(self.toml_path)
            lines = content.split("\n")

            in_settings = False
            in_topics = False

            for line in lines:
                stripped = line.strip()

                if stripped == "[settings]":
                    in_settings = True
                    in_topics = False
                    continue
                elif stripped == "[topics]" or stripped.startswith('[topics."'):
                    in_settings = False
                    in_topics = True
                    topics_content.append(line)
                    continue
                elif stripped.startswith("[") and not stripped.startswith('[topics."'):
                    in_settings = False
                    in_topics = False
                    other_sections.append(line)
                    continue

                if in_topics:
                    topics_content.append(line)
                elif not in_settings:
                    other_sections.append(line)

        # Write new content
        lines = ["[settings]"]
        settings_dict = settings.to_dict()

        for key, value in settings_dict.items():
            # Expand home directory for paths
            if isinstance(value, str) and value.startswith(os.path.expanduser("~")):
                value = "~" + value[len(os.path.expanduser("~")):]
            lines.append(f'{key} = "{value}"')

        # Add other sections
        if other_sections:
            lines.append("")
            lines.extend(other_sections)

        # Add topics section
        if topics_content:
            if not topics_content[0].strip():
                topics_content = topics_content[1:]
            lines.append("")
            lines.extend(topics_content)

        FileManager.write_text(self.toml_path, "\n".join(lines) + "\n")

    def load_topics(self) -> Dict[str, Topic]:
        """Load all topics from TOML file.

        Returns:
            Dictionary mapping topic key to Topic object
        """
        topics = {}

        if not FileManager.exists(self.toml_path):
            return topics

        try:
            with open(self.toml_path, "rb") as f:
                toml_data = tomllib.load(f)
                topics_data = toml_data.get("topics", {})

                for key, data in topics_data.items():
                    if isinstance(data, dict):
                        topics[key] = Topic.from_dict(key, data)
        except Exception as e:
            print(f"Warning: Failed to parse topics from TOML: {e}")

        return topics

    def save_topic(self, topic: Topic) -> None:
        """Save or update a topic in TOML file.

        Args:
            topic: Topic to save
        """
        # Check if topic already exists
        if self.topic_exists(topic.key):
            # Update existing topic
            self._update_topic(topic)
        else:
            # Append new topic
            self._append_topic(topic)

    def _append_topic(self, topic: Topic) -> None:
        """Append a new topic to TOML file."""
        lines = [f'\n[topics."{topic.key}"]']
        topic_dict = topic.to_dict()

        lines.append(f'title = "{topic_dict["title"]}"')
        lines.append(f'path = "{topic_dict["path"]}"')

        if topic_dict["lists"]:
            list_entries = []
            for entry in topic_dict["lists"]:
                parts = [f'list = "{entry["list"]}"']
                if "link" in entry:
                    parts.append(f'link = "{entry["link"]}"')
                if "link_look" in entry:
                    parts.append(f'link_look = "{entry["link_look"]}"')
                list_entries.append("{" + ", ".join(parts) + "}")
            lines.append(f'lists = [{", ".join(list_entries)}]')
        else:
            lines.append('lists = []')

        FileManager.append_text(self.toml_path, "\n".join(lines) + "\n")

    def _update_topic(self, topic: Topic) -> None:
        """Update an existing topic in TOML file."""
        if not FileManager.exists(self.toml_path):
            return

        content = FileManager.read_text(self.toml_path)
        lines = content.split("\n")

        new_lines = []
        skip = False
        found = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped == f'[topics."{topic.key}"]':
                skip = True
                found = True
                # Insert updated topic
                new_lines.append(line)
                topic_dict = topic.to_dict()
                new_lines.append(f'title = "{topic_dict["title"]}"')
                new_lines.append(f'path = "{topic_dict["path"]}"')

                if topic_dict["lists"]:
                    list_entries = []
                    for entry in topic_dict["lists"]:
                        parts = [f'list = "{entry["list"]}"']
                        if "link" in entry:
                            parts.append(f'link = "{entry["link"]}"')
                        if "link_look" in entry:
                            parts.append(f'link_look = "{entry["link_look"]}"')
                        list_entries.append("{" + ", ".join(parts) + "}")
                    new_lines.append(f'lists = [{", ".join(list_entries)}]')
                else:
                    new_lines.append('lists = []')
                continue

            if skip and stripped.startswith("["):
                skip = False

            if not skip:
                new_lines.append(line)

        if found:
            FileManager.write_text(self.toml_path, "\n".join(new_lines))

    def delete_topic(self, key: str) -> bool:
        """Delete a topic from TOML file.

        Args:
            key: Topic key to delete

        Returns:
            True if topic was deleted, False if not found
        """
        if not FileManager.exists(self.toml_path):
            return False

        content = FileManager.read_text(self.toml_path)
        lines = content.split("\n")

        new_lines = []
        skip = False
        found = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped == f'[topics."{key}"]':
                skip = True
                found = True
                continue

            if skip and stripped.startswith("["):
                skip = False

            if not skip:
                new_lines.append(line)

        if found:
            FileManager.write_text(self.toml_path, "\n".join(new_lines))

        return found

    def topic_exists(self, key: str) -> bool:
        """Check if topic exists in TOML.

        Args:
            key: Topic key

        Returns:
            True if topic exists
        """
        topics = self.load_topics()
        return key in topics

    def update_setting(self, key: str, value: str) -> None:
        """Update a single setting in TOML file.

        Args:
            key: Setting key
            value: Setting value
        """
        settings = self.load_settings()
        settings_dict = settings.to_dict()
        settings_dict[key] = value
        updated_settings = Settings.from_dict(settings_dict)
        self.save_settings(updated_settings)
